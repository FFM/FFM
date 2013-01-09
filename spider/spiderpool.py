import os

from multiprocessing  import Pool, Manager
from rsclib.autosuper import autosuper
from olsr.parser      import OLSR_Parser
from spider.parser    import Guess

def get_node_info (result_dict, ip) :
    try :
        if ip in result_dict :
            return
        try :
            url  = ''
            site = Guess.site % locals ()
            #site = 'file:///' + os.path.abspath ('spider/%s' % ip)
            #url  = 'index.html'
            g    = Guess (site = site, url = 'index.html')
        except ValueError, err :
            result_dict [ip] = ('ValueError', err)
            return
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
        result_dict [ip] = result
    except Exception, err :
        result_dict [ip] = ("ERROR", err)
# end def get_node_info

class Spider (autosuper) :

    def __init__ (self, olsr_file) :
        olsr_parser = OLSR_Parser ()
        olsr_parser.parse (open (olsr_file))
        self.olsr_nodes = {}
        for t in olsr_parser.topo.forward.iterkeys () :
            self.olsr_nodes [t] = True
        for t in olsr_parser.topo.reverse.iterkeys () :
            self.olsr_nodes [t] = True
        self.pool  = Pool (processes = 5)
        self.mgr   = Manager ()
        self.result_dict = self.mgr.dict ()
        olsr_nodes = None
    # end def __init__

    def process (self) :
        #for n, node in enumerate \
        #    (('193.238.158.241', '78.41.113.91', '193.238.159.20')) :
        for n, node in enumerate (self.olsr_nodes) :
            if n > 4 :
                break
            self.pool.apply_async \
                (get_node_info, (self.result_dict, str (node)))
        self.pool.close ()
        self.pool.join  ()
        # broken dict proxy interface, make local dict with full interface
        self.result_dict = dict (self.result_dict)
    # end def process

# end def Spider

if __name__ == '__main__' :
    olsr_file = 'olsr/txtinfo.txt'
    sp = Spider (olsr_file)
    sp.process ()
    for k, v in sorted \
        (sp.result_dict.iteritems (), key = lambda z : (z [1][0], z [0])) :
        print k, v
