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

from   rsclib.HTML_Parse  import tag, Page_Tree
from   rsclib.autosuper   import autosuper
from   spider.common      import Interface, Inet4, unroutable

class Routes (Page_Tree) :
    retries      = 2
    timeout      = 10
    url          = '/cgi-bin/index.cgi?post_routes=1'

    def parse (self) :
        root  = self.tree.getroot ()
        self.ip_dev = {}
        for pre in root.findall (".//%s" % tag ("pre")) :
            state = 0
            for a in pre :
                if a.tag != tag ('a') :
                    continue
                if state == 0 and a.tail and 'scope link' in a.tail :
                    state = 1
                    found = False
                    for w in a.tail.strip ().split () :
                        if found :
                            devname = w
                            break
                        if w == 'dev' :
                            found = True
                    continue
                if state == 1 :
                    if devname :
                        self.ip_dev [a.text.strip ()] = devname
                    devname = None
                    state = 0
        for sm in root.findall (".//%s" % tag ("small")) :
            if sm.text :
                s = sm.text.strip ()
                if s.startswith ('0xffolsr') :
                    self.version = s
                    break
    # end def parse

# end class Routes

class Details (Page_Tree) :
    retries      = 2
    timeout      = 10
    url          = '/cgi-bin/index.cgi?post_olsr=1'

    def parse (self) :
        root  = self.tree.getroot ()
        self.ip_dev = {}
        self.gw_ip  = {}
        self.metric = {}
        for pre in root.findall (".//%s" % tag ("pre")) :
            state = 0
            assert 'Table: Links' in pre.text
            for a in pre :
                if a.tag != tag ('a') :
                    continue
                if state == 0 :
                    state = 1
                    ip = a.text
                elif state == 1 :
                    state = 0
                    if 'Table:' in a.tail :
                        state = 2
                    assert ip
                    self.gw_ip [a.text] = ip
                    # LQ, NLQ, Cost, 0th parameter varies with version
                    pars = a.tail.strip ().split () [1:4]
                    pars = ((x, 'nan')[x == 'INFINITE'] for x in pars)
                    self.metric [ip] = [float (x) for x in pars]
                elif state == 2 :
                    if 'Table: Routes' in a.tail :
                        state = 3
                elif state == 3 :
                    state = 4
                    dst = a.text
                    if dst in self.gw_ip :
                        ip = self.gw_ip [dst]
                    else :
                        ip = None
                elif state == 4 :
                    state = 3
                    if ip :
                        assert dst
                        self.ip_dev [ip] = a.tail.strip ().split () [-1]
    # end def parse

# end class Details

class Router_OS (autosuper) :

    url = '/cgi-bin/index.cgi?post_routes=1'

    def __init__ (self, site, request, url = url) :
        self.site    = site
        self.request = request
        rtparm = 1
        if url.endswith ('cgi') :
            rtparm = 2
        if 'interfaces' in self.request or 'ips' in self.request :
            rt = Routes  (site = site, url = url + '?post_routes=%s' % rtparm)
            dt = Details (site = site, url = url + '?post_olsr=1')
            self.version = rt.version
            interfaces   = {}
            ips          = {}
            base         = 0
            for count, (ip, ifname) in enumerate (rt.ip_dev.iteritems ()) :
                i4 = Inet4 (ip, None, None, iface = ifname)
                # ignore interfaces with unroutable IPs
                if unroutable (i4.ip) :
                    #print "Unroutable: %s" % i4
                    continue
                ips [i4] = 1
                iface = Interface (count, ifname, None)
                iface.is_wlan = False
                interfaces [ifname] = iface
                iface.append_inet4 (i4)
                base = count
            base += 1
            for count, (ip, ifname) in enumerate (dt.ip_dev.iteritems ()) :
                i4 = Inet4 (ip, None, None, iface = ifname)
                is_wlan = sum (x == 1.0 for x in dt.metric [ip]) != 3
                #print "ip", ip, dt.metric [ip]
                if unroutable (i4.ip) :
                    continue
                if i4 in ips :
                    if ifname not in interfaces :
                        iface = Interface (base + count, ifname, None)
                        interfaces [ifname] = iface
                        iface.append_inet4 (i4)
                    else :
                        iface = interfaces [ifname]
                        if i4 not in iface.inet4 :
                            #print "Oops:", ifname, i4, iface.inet4 [0]
                            del iface.inet4 [0]
                            iface.append_inet4 (i4)
                    iface.is_wlan = is_wlan
                    continue
                ips [i4] = 1
                iface = Interface (base + count, ifname, None)
                iface.is_wlan = is_wlan
                interfaces [ifname] = iface
                iface.append_inet4 (i4)

            # check own ip
            n  = 'unknown'
            i4 = Inet4 (self.request ['ip'], None, None, iface = n)
            assert i4 in ips

            self.request ['ips']        = ips
            self.request ['interfaces'] = interfaces
            self.request ['version']    = rt.version
    # end def __init__

# end class Router_OS
