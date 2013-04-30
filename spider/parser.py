#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
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
from   rsclib.HTML_Parse  import tag, Page_Tree
from   rsclib.stateparser import Parser
from   rsclib.autosuper   import autosuper
from   rsclib.IP_Address  import IP4_Address
from   spider.freifunk    import Freifunk
from   spider.olsr        import OLSR
from   spider.backfire    import Backfire

# for pickle
from   spider.common      import Interface, Net_Link, Inet4, Inet6, WLAN_Config
from   spider.freifunk    import Interface_Config, WLAN_Config_Freifunk

class Guess (Page_Tree) :
    site    = 'http://%(ip)s'
    url     = ''
    delay   = 0
    retries = 2
    timeout = 10

    status_url = 'cgi-bin-status.html'
    status_ok  = 0

    backend_table = dict \
        ( Backfire = Backfire
        , Freifunk = Freifunk
        , OLSR     = OLSR
        )

    def __init__ (self, site, url, port = 0) :
        if port :
            site = "%s:%s" % (site, port)
        self.__super.__init__ (site = site, url = url)
    # end def __init__

    def parse (self) :
        #print self.tree_as_string ()
        root = self.tree.getroot ()
        self.backend = None
        self.version = "Unknown"
        title = root.find (".//%s" % tag ("title"))
        t     = 'olsr.org httpinfo plugin'
        if title is not None and title.text and title.text.strip () == t :
            self.backend = 'OLSR'
            self.params  = dict (site = self.url)
        if not self.backend :
            for meta in root.findall (".//%s" % tag ("meta")) :
                if meta.get ('http-equiv') == 'refresh' :
                    c = meta.get ('content')
                    if c and c.endswith ('cgi-bin/luci') :
                        self.backend = 'Backfire'
                        self.params  = dict (site = self.site)
                        break
            else : # Freifunk
                for sm in root.findall (".//%s" % tag ("small")) :
                    if sm.text.startswith ('v1.') :
                        self.version = sm.text
                        break
                #print "Version: %s" % self.version
                for a in root.findall (".//%s" % tag ("a")) :
                    if a.get ('class') == 'plugin' :
                        # Allow 'Status klassisch' to override status
                        # even if found first
                        if a.text == 'Status klassisch' :
                            self.status_url = a.get ('href')
                            self.status_ok = 1
                        elif a.text == 'Status' and not self.status_ok :
                            self.status_url = a.get ('href')
                self.backend = "Freifunk"
                self.params  = dict (site = self.site, url = self.status_url)

        self.status = self.backend_table [self.backend] (** self.params)
        if self.version == "Unknown" :
            try :
                self.version = self.status.version
            except AttributeError :
                pass
        self.type = self.status.__class__.__name__
    # end def parse

    def verbose_repr (self) :
        r = [str (self)]
        for v in self.if_by_name.itervalues () :
            r.append (str (v))
        for v in self.ips.iterkeys () :
            r.append (str (v))
        return '\n'.join (r)
    # end def verbose_repr

    def __getattr__ (self, name) :
        if 'status' not in self.__dict__ :
            raise AttributeError ("my 'status' attribute vanished")
        r = getattr (self.status, name)
        setattr (self, name, r)
        return r
    # end def __getattr__

    def __str__ (self) :
        return "%s Version: %s" % (self.type, self.version)
    # end def __str__

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
        site = Guess.site % locals ()
        url  = ''
        # For testing we download the index page and cgi-bin-status.html
        # page into a directory named with the ip address
        if opt.local :
            site = 'file://' + os.path.abspath (ip)
            url  = 'index.html'
        ff = Guess (site = site, url = url, port = port)
        print ff.verbose_repr ()
        ipdict [str (ip)] = ff
    if opt.output_pickle :
        f = open (opt.output_pickle, 'wb')
        pickle.dump (ipdict, f)
        f.close ()
# end def main

if __name__ == '__main__' :
    import spider.parser
    spider.parser.main ()
