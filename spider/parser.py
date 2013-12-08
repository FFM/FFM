#!/usr/bin/python
# -*- coding: utf-8 -*-
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
import re
from   csv                  import DictWriter
from   rsclib.HTML_Parse    import tag, Page_Tree
from   rsclib.stateparser   import Parser
from   rsclib.autosuper     import autosuper
from   rsclib.IP_Address    import IP4_Address
from   spider.freifunk      import Freifunk
from   spider.olsr_httpinfo import OLSR
from   spider.backfire      import Backfire
from   spider.openwrt       import OpenWRT

# for pickle
from   spider.common      import Interface, Net_Link, Inet4, Inet6, WLAN_Config
from   spider.common      import Compare_Mixin
from   spider.freifunk    import Interface_Config, WLAN_Config_Freifunk

site_template = 'http://%(ip)s'

class First_Guess (Page_Tree) :
    url     = ''
    delay   = 0
    retries = 2
    timeout = 10

    status_url = 'cgi-bin-status.html'
    status_ok  = 0

    def __init__ (self, rqinfo, site, url, port = 0) :
        self.rqinfo = rqinfo
        if port :
            site = "%s:%s" % (site, port)
        self.params = dict (request = self.rqinfo, site = site)
        self.__super.__init__ (site = site, url = url)
    # end def __init__

    def parse (self) :
        self.backend = None
        root  = self.tree.getroot ()
        #print self.tree_as_string (root)
        title = root.find (".//%s" % tag ("title"))
        t     = 'olsr.org httpinfo plugin'
        if title is not None and title.text and title.text.strip () == t :
            self.backend = 'OLSR'
            self.params.update (site = self.url)
        if not self.backend :
            for meta in root.findall (".//%s" % tag ("meta")) :
                if meta.get ('http-equiv') == 'refresh' :
                    c = meta.get ('content')
                    if c and c.endswith ('cgi-bin/luci') :
                        self.backend = 'Luci'
                        break
                    elif c and c.endswith ('URL=/cgi-bin-index.html') :
                        # e.g. Fonera
                        self.backend = 'Freifunk'
                        break
            else : # Freifunk
                for big in root.findall (".//%s" % tag ("big")) :
                    if big.get ('class') == 'plugin' :
                        self.backend = "Freifunk"
                        break
                else :
                    raise ValueError ("Unknown Web Frontend")
                # Best effort to find status url
                for a in root.findall (".//%s" % tag ("a")) :
                    if a.get ('class') == 'plugin' :
                        # Allow 'Status klassisch' to override status
                        # even if found first
                        if a.text == 'Status klassisch' :
                            self.status_url = a.get ('href')
                            self.status_ok = 1
                        elif a.text == 'Status' and not self.status_ok :
                            self.status_url = a.get ('href')
                self.params.update (url = self.status_url)

    # end def parse

# end class First_Guess

class Luci_Guess (Page_Tree) :
    delay        = 0
    retries      = 2
    timeout      = 10
    url          = 'cgi-bin/luci'
    html_charset = 'utf-8' # force utf-8 encoding

    def __init__ (self, rqinfo, site, url = None) :
        self.rqinfo = rqinfo
        self.params = dict (request = self.rqinfo, site = site)
        self.__super.__init__ (site = site, url = url)
    # end def __init__

    def parse (self) :
        self.backend = 'Backfire'
        root  = self.tree.getroot ()
        #print self.tree_as_string (root)
        for h in root.findall (".//%s" % tag ('div')) :
            if h.get ('id') == 'header' :
                for p in h :
                    if p.tag not in (tag ('p'), tag ('h1')) :
                        break
                else :
                    self.backend = 'OpenWRT'
                break
    # end def parse

# end class Luci_Guess

class Guess (Compare_Mixin) :

    backend_table = dict \
        ( Backfire = Backfire
        , Freifunk = Freifunk
        , OLSR     = OLSR
        , OpenWRT  = OpenWRT
        )

    def __init__ (self, site, ip, url = None, port = 0) :
        self.version = "Unknown"
        self.rqinfo  = dict.fromkeys (('ips', 'interfaces'))
        self.rqinfo ['ip'] = ip
        g = First_Guess (self.rqinfo, site, url, port)
        self.params  = g.params
        self.backend = g.backend
        if self.backend == 'Luci' :
            g2  = Luci_Guess (self.rqinfo, self.params ['site'])
            self.params  = g2.params
            self.backend = g2.backend
        self.status  = self.backend_table [self.backend] (** self.params)
        try :
            self.version = self.rqinfo ['version']
        except KeyError :
            pass
        self.type = self.status.__class__.__name__
    # end def __init__

    def as_json (self) :
        d = dict (type = self.type, version = self.version)
        iface = d ['interfaces'] = []
        for i in self.interfaces.itervalues () :
            iface.append (i.as_dict) 
        ips = d ['ips'] = []
        for i in self.ips.iterkeys () :
            ips.append (str (i))
        return json.dumps (d)
    # end def as_json

    def verbose_repr (self) :
        r = [str (self)]
        for v in self.interfaces.itervalues () :
            r.append (str (v))
        for v in self.ips.iterkeys () :
            r.append (str (v))
        return '\n'.join (r)
    # end def verbose_repr

    def __eq__ (self, other) :
        if not hasattr (other, 'interfaces') :
            return False
        return self.ips == other.ips and self.interfaces == other.interfaces
    # end def __eq__

    def __hash__ (self) :
        return hash \
            (( tuple (self.ips.iterkeys ())
             , tuple (self.interfaces.itervalues ())
            ))
    # end def __hash__

    def __getattr__ (self, name) :
        if 'rqinfo' not in self.__dict__ :
            raise AttributeError ("my 'rqinfo' attribute vanished: %s" % name)
        try :
            r = self.rqinfo [name]
        except KeyError, cause :
            raise AttributeError (cause)
        setattr (self, name, r)
        return r
    # end def __getattr__

    def __repr__ (self) :
        return "%s Version: %s" % (self.type, self.version)
    # end def __repr__
    __str__ = __repr__

# end class Guess

def main () :
    import sys
    import pickle
    from optparse import OptionParser

    cmd = OptionParser ()
    cmd.add_option \
        ( "-d", "--debug"
        , dest    = "debug"
        , action  = "store_true"
        , help    = "Debug merging of pickle dumps"
        )
    cmd.add_option \
        ( "-l", "--local"
        , dest    = "local"
        , action  = "store_true"
        , help    = "Use local download for testing with file:// url"
        )
    cmd.add_option \
        ( "-o", "--output-pickle"
        , dest    = "output_pickle"
        , help    = "Optional pickle output file"
        )
    cmd.add_option \
        ( "-p", "--port"
        , dest    = "port"
        , help    = "Optional port number to fetch from"
        , type    = "int"
        , default = 0
        )
    cmd.add_option \
        ( "-r", "--read-pickle"
        , dest    = "read_pickle"
        , help    = "Read old pickle files, merge and preserve information"
        , action  = "append"
        , default = []
        )
    cmd.add_option \
        ( "-V", "--version-statistics"
        , dest    = "version_statistics"
        , help    = "Output version information by spidered IP"
        )
    cmd.add_option \
        ( "-I", "--interface-info"
        , dest    = "interface_info"
        , help    = "Output interface information by spidered IP"
        )
    cmd.add_option \
        ( "-v", "--verbose"
        , dest    = "verbose"
        , action  = "count"
        , help    = "Show verbose results"
        )
    (opt, args) = cmd.parse_args ()
    if len (args) < 1 and not opt.read_pickle :
        cmd.print_help ()
        sys.exit (23)
    ipdict = {}
    for fn in opt.read_pickle :
        if opt.debug :
            print "Processing pickle dump %s" % fn
        keys = dict.fromkeys (ipdict.iterkeys ())
        f    = open (fn, 'r')
        obj  = pickle.load (f)
        for k, v in obj.iteritems () :
            # Fixup of object
            if isinstance (v, Guess) and not hasattr (v, 'rqinfo') :
                v.rqinfo                = {}
                v.rqinfo ['ips']        = v.status.ips
                v.rqinfo ['interfaces'] = v.status.if_by_name
                v.status                = None
            if k in ipdict :
                keys [k] = True
                ov       = ipdict [k]
                istuple  = isinstance (v, tuple)
                if isinstance (ov, tuple) :
                    overwrite = False
                    if not istuple :
                        overwrite = True
                    elif ov [0] == 'Timeout_Error' :
                        overwrite = True
                    elif v [0] == 'ValueError' :
                        overwrite = True
                    if overwrite :
                        #print opt.debug, istuple, v, ov [0]
                        if (opt.debug and (not istuple or v [0] != ov [0])) :
                            print "%s: overwriting %s with %s" % (k, ov, v)
                        ipdict [k] = v
                    elif istuple and ov [0] != v [0] and opt.debug :
                        print "%s: Not overwriting %s with %s" % (k, ov, v)
                else :
                    assert isinstance (ov, Guess)
                    if istuple :
                        if opt.debug :
                            print "%s: Not overwriting %s with %s" % (k, ov, v)
                    else :
                        assert isinstance (v, Guess)
                        ipdict [k] = v
            else :
                if opt.debug :
                    print "%s: new: %s" % (k, v)
                ipdict [k] = v
        if opt.debug :
            for k, v in keys.iteritems () :
                if not v :
                    print "%s: not existing in dump %s" % (k, fn)

    for ip in args :
        port = opt.port
        try :
            ip, port = ip.split (':', 1)
        except ValueError :
            pass
        site = site_template % locals ()
        url  = ''
        # For testing we download the index page and cgi-bin-status.html
        # page into a directory named with the ip address
        if opt.local :
            site = 'file://' + os.path.abspath (ip)
            url  = 'index.html'
        ff = Guess (site = site, ip = ip, url = url, port = port)
        print ff.verbose_repr ()
        ipdict [str (ip)] = ff
    if opt.output_pickle :
        f = open (opt.output_pickle, 'wb')
        pickle.dump (ipdict, f)
        f.close ()
    key = lambda x : IP4_Address (x [0])
    if opt.version_statistics :
        fields = ['address', 'type', 'version']
        if opt.version_statistics == '-' :
            f  = sys.stdout
        else :
            f  = open (opt.version_statistics, 'w')
        dw     = DictWriter (f, fields, delimiter = ';')
        dw.writerow (dict ((k, k) for k in fields))
        for ip, guess in sorted (ipdict.iteritems (), key = key) :
            if isinstance (guess, Guess) :
                dw.writerow \
                    ( dict
                        ( address = str (ip)
                        , version = guess.version
                        , type    = guess.type
                        )
                    )
        f.close ()
    if opt.interface_info :
        fields = \
            [ 'address', 'interface', 'wlan'
            , 'ssid', 'mode', 'channel', 'bssid'
            , 'ip4', 'ip6', 'signal', 'noise'
            ]
        if opt.interface_info == '-' :
            f  = sys.stdout
        else :
            f  = open (opt.interface_info, 'w')
        dw     = DictWriter (f, fields, delimiter = ';')
        dw.writerow (dict ((k, k) for k in fields))
        for ip, guess in sorted (ipdict.iteritems (), key = key) :
            if isinstance (guess, Guess) :
                for iface in guess.interfaces.itervalues () :
                    wi = iface.wlan_info
                    d  = dict \
                        ( address   = str (ip)
                        , interface = iface.name
                        , wlan      = bool (wi)
                        , ip4       = ' '.join (str (i.ip) for i in iface.inet4)
                        , ip6       = ' '.join (str (i.ip) for i in iface.inet6)
                        )
                    if wi :
                        d.update \
                            ( channel = wi.channel
                            , bssid   = wi.bssid
                            , ssid    = wi.ssid
                            , mode    = wi.mode
                            , signal  = wi.signal
                            , noise   = wi.noise
                            )
                    dw.writerow (d)
        f.close ()
    if opt.verbose :
        for ip, guess in sorted (ipdict.iteritems (), key = key) :
            if opt.verbose > 1 :
                print "%-15s" % ip
                print '=' * 15
                if isinstance (guess, Guess) :
                    print guess.verbose_repr ()
                else :
                    print "Exception:", guess
            else :
                print "%-15s: %s" % (ip, guess)
# end def main

if __name__ == '__main__' :
    import spider.parser
    spider.parser.main ()
