import os

from multiprocessing  import Pool, Manager
from rsclib.autosuper import autosuper
from rsclib.execute   import Log
from rsclib.timeout   import Timeout, Timeout_Error
from olsr.parser      import OLSR_Parser
from spider.parser    import Guess
from itertools        import islice

def get_node_info (result_dict, ip) :
    w = Worker (result_dict, ip)
    try :
        return w.get_node_info ()
    except Exception, err :
        w.log.log_exception ()
# end def get_node_info

class Worker (Log, Timeout) :

    def __init__ (self, result_dict, ip, **kw) :
        self.__super.__init__ (** kw)
        self.ip          = ip
        self.result_dict = result_dict
    # end def __init__

    def get_node_info (self) :
        try :
            if self.ip in self.result_dict :
                return
            self.arm_alarm (timeout = 60)
            try :
                url  = ''
                site = Guess.site % self.__dict__
                #site = 'file:///' + os.path.abspath ('spider/%s' % self.ip)
                #url  = 'index.html'
                self.log.debug ("%s: before guess" % self.ip)
                g    = Guess (site = site, url = 'index.html')
                self.log.debug ("%s: after  guess" % self.ip)
            except ValueError, err :
                self.result_dict [self.ip] = ('ValueError', err)
                return
            except Timeout_Error, err :
                self.disable_alarm ()
                self.result_dict [self.ip] = ('TimeoutError', err)
                return
            except :
                self.log_exception ()
                return
            self.disable_alarm ()
            result = []
            for iface_ip in g.ips.iterkeys () :
                iface = iface_ip.iface
                r = [iface.name]
                if iface.is_wlan :
                    r.extend \
                        (( True
                        ,  iface.wlan_info.ssid
                        ,  iface.wlan_info.mode
                        ,  iface.wlan_info.channel
                        ,  iface.wlan_info.bssid
                        ))
                else :
                    r.append (False)
                result.append (r)
            self.result_dict [self.ip] = result
        except Exception, err :
            self.log.error (err)
            self.result_dict [self.ip] = ("ERROR", err)
    # end def get_node_info

# end class Worker

class Spider (Log) :

    def __init__ (self, olsr_file, processes = 20, N = 0, **kw) :
        self.__super.__init__ (**kw)
        olsr_parser = OLSR_Parser ()
        olsr_parser.parse (open (olsr_file))
        self.olsr_nodes = {}
        for t in olsr_parser.topo.forward.iterkeys () :
            self.olsr_nodes [t] = True
        for t in olsr_parser.topo.reverse.iterkeys () :
            self.olsr_nodes [t] = True
        # limit to N elements
        if N :
            self.olsr_nodes = dict \
                ((k, v) for k, v in islice (self.olsr_nodes.iteritems (), N))
        self.pool  = Pool (processes = processes)
        self.mgr   = Manager ()
        self.result_dict = self.mgr.dict ()
        olsr_nodes = None
    # end def __init__

    def process (self) :
        for node in self.olsr_nodes :
            self.pool.apply_async \
                (get_node_info, (self.result_dict, str (node)))
        self.pool.close ()
        self.pool.join  ()
        # broken dict proxy interface, make local dict with full interface
        self.result_dict = dict (self.result_dict)
    # end def process

# end def Spider

if __name__ == '__main__' :
    import pickle
    import sys
    from optparse import OptionParser

    cmd = OptionParser ()
    cmd.add_option \
        ( "-d", "--dump"
        , dest    = "dump"
        , help    = "Destination file of pickle dump"
        , default = "Funkfeuer-spider-pickle.dump"
        )
    cmd.add_option \
        ( "-n", "--limit-nodes"
        , dest    = "limit_nodes"
        , help    = "Limit spidering to given number of nodes"
        , type    = "int"
        , default = 0
        )
    cmd.add_option \
        ( "-p", "--processes"
        , dest    = "processes"
        , help    = "Use given number of processes"
        , type    = "int"
        , default = 20
        )
    cmd.add_option \
        ( "-o", "--olsr-file"
        , dest    = "olsr_file"
        , help    = "File containing OLSR information"
        , default = "olsr/txtinfo.txt"
        )
    (opt, args) = cmd.parse_args ()
    if len (args) :
        cmd.print_help ()
        sys.exit (23)
    sp = Spider (opt.olsr_file, opt.processes, opt.limit_nodes)
    try :
        sp.process ()
        f = open (opt.dump, "wb")
        pickle.dump (sp.result_dict, f)
        f.close ()
        for k, v in sorted \
            (sp.result_dict.iteritems (), key = lambda z : (z [1][0], z [0])) :
            print k, v
    except Exception, err :
        sp.log_exception ()
