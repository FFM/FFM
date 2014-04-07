# #*** <License> ************************************************************#
# This module is part of the program FFM.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# #*** </License> ***********************************************************#

import os

from multiprocessing   import Pool, Manager
from rsclib.autosuper  import autosuper
from rsclib.execute    import Log
from rsclib.timeout    import Timeout, Timeout_Error
from rsclib.HTML_Parse import Retries_Exceeded
from rsclib.IP_Address import IP4_Address
from olsr.parser       import get_olsr_container
from spider.parser     import Guess, site_template
from itertools         import islice
from logging           import INFO
from gzip              import GzipFile

def get_node_info \
    (result_dict, ip, timeout = 180, ip_port = {}, debug = False) :
    w = Worker \
        (result_dict, ip, timeout = timeout, ip_port = ip_port, debug = debug)
    try :
        return w.get_node_info ()
    except Exception, err :
        self.log.error ("Error in IP %s:" % ip)
        w.log.log_exception ()
# end def get_node_info

class Worker (Log, Timeout) :

    def __init__ \
        ( self
        , result_dict
        , ip
        , timeout = 180
        , ip_port = {}
        , debug = False
        , **kw
        ) :
        self.__super.__init__ (** kw)
        self.ip          = ip
        self.result_dict = result_dict
        self.timeout     = timeout
        self.ip_port     = ip_port
        if not debug :
            self.log.setLevel (INFO)
        self.log.debug ("Started for IP: %s" % self.ip)
    # end def __init__

    def get_node_info (self) :
        try :
            if self.ip in self.result_dict :
                return
            self.arm_alarm (timeout = self.timeout)
            try :
                url  = ''
                site = site_template % self.__dict__
                self.log.debug ("%s: before guess" % self.ip)
                port = None
                if self.ip in self.ip_port :
                    port = self.ip_port [self.ip]
                g    = Guess (site = site, ip = self.ip, url = '', port = port)
                self.log.debug ("%s: after  guess" % self.ip)
            except ValueError, err :
                self.disable_alarm ()
                self.log.error ("Error in IP %s:" % self.ip)
                self.log_exception ()
                self.result_dict [self.ip] = ('ValueError', err)
                return
            except Timeout_Error, err :
                self.disable_alarm ()
                self.log.debug ("Timeout")
                self.result_dict [self.ip] = ('Timeout_Error', err)
                return
            except Retries_Exceeded, err :
                self.disable_alarm ()
                self.log.debug ("Retries exceeded")
                self.result_dict [self.ip] = ('Retries_Exceeded', err)
                return
            except Exception, err :
                self.disable_alarm ()
                self.log.error ("Error in IP %s:" % self.ip)
                self.log_exception ()
                self.result_dict [self.ip] = ('Exception', err)
                return
            self.disable_alarm ()
            result = []
#            for iface_ip in g.ips.iterkeys () :
#                iface = iface_ip.iface
#                r = [iface.name]
#                if iface.is_wlan :
#                    r.extend \
#                        (( True
#                        ,  iface.wlan_info.ssid
#                        ,  iface.wlan_info.mode
#                        ,  iface.wlan_info.channel
#                        ,  iface.wlan_info.bssid
#                        ))
#                else :
#                    r.append (False)
#                result.append (r)
            self.result_dict [self.ip] = g
        except Exception, err :
            self.log.error ("Error in IP %s:" % self.ip)
            self.log_exception ()
            self.result_dict [self.ip] = ("ERROR", err)
    # end def get_node_info

# end class Worker

class Spider (Log) :

    def __init__ \
        ( self
        , olsr_file
        , processes =    20
        , N         =     0
        , timeout   =   180
        , ip_port   =    {}
        , debug     = False
        , ** kw
        ) :
        self.__super.__init__ (**kw)
        olsr = get_olsr_container (olsr_file)
        self.olsr_nodes = {}
        for t in olsr.topo.forward.iterkeys () :
            self.olsr_nodes [t] = True
        for t in olsr.topo.reverse.iterkeys () :
            self.olsr_nodes [t] = True
        # limit to N elements
        if N :
            self.olsr_nodes = dict \
                ((k, v) for k, v in islice (self.olsr_nodes.iteritems (), N))
        self.pool        = Pool (processes = processes)
        self.mgr         = Manager ()
        self.result_dict = self.mgr.dict ()
        self.timeout     = timeout
        self.ip_port     = ip_port
        self.debug       = debug
        olsr_nodes       = None
        if not debug :
            self.log.setLevel (INFO)
        self.log.debug ("Starting ...")
    # end def __init__

    def process (self) :
        for node in self.olsr_nodes :
            self.pool.apply_async \
                ( get_node_info
                , ( self.result_dict
                  , str (node)
                  , self.timeout
                  , self.ip_port
                  , self.debug
                  )
                )
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
        ( "-D", "--debug"
        , dest    = "debug"
        , help    = "Turn on debug logging"
        , action  = "store_true"
        , default = False
        )
    cmd.add_option \
        ( "-d", "--dump"
        , dest    = "dump"
        , help    = "Destination file of pickle dump, default: %default"
        , default = "Funkfeuer-spider-pickle.dump"
        )
    cmd.add_option \
        ( "-i", "--ip-port"
        , dest    = "ip_port"
        , action  = "append"
        , help    = "IP-Addres:Port combination with non-standard port"
        , default = []
        )
    cmd.add_option \
        ( "-n", "--limit-devices"
        , dest    = "limit_devices"
        , help    = "Limit spidering to given number of devices"
        , type    = "int"
        , default = 0
        )
    cmd.add_option \
        ( "-p", "--processes"
        , dest    = "processes"
        , help    = "Use given number of processes, default: %default"
        , type    = "int"
        , default = 20
        )
    cmd.add_option \
        ( "-o", "--olsr-file"
        , dest    = "olsr_file"
        , help    = "File or Backfire-URL containing OLSR information, "
                    "default: %default"
        , default = "olsr/txtinfo.txt"
        )
    cmd.add_option \
        ( "-t", "--timeout"
        , dest    = "timeout"
        , help    = "Timout in seconds for subprocesses, default: %default"
        , type    = "int"
        , default = 180
        )
    cmd.add_option \
        ( "-v", "--verbose"
        , dest    = "verbose"
        , help    = "Show verbose results"
        , action  = "count"
        )
    (opt, args) = cmd.parse_args ()
    if len (args) :
        cmd.print_help ()
        sys.exit (23)
    sp = Spider \
        ( opt.olsr_file
        , opt.processes
        , opt.limit_devices
        , opt.timeout
        , dict (x.split (':', 1) for x in opt.ip_port)
        , opt.debug
        )
    try :
        sp.process ()
        if opt.dump.endswith ('.gz') :
            f = GzipFile (opt.dump, "wb", 9)
        else :
            f = open (opt.dump, "wb")
        pickle.dump (sp.result_dict, f)
        f.close ()
        if opt.verbose :
            for k, v in sorted \
                ( sp.result_dict.iteritems ()
                , key = lambda z : IP4_Address (z [0])
                ) :
                print k, v
    except Exception, err :
        sp.log_exception ()
