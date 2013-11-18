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
from   spider.common      import Interface, Inet4, Inet6, unroutable
from   spider.common      import WLAN_Config
from   spider.luci        import Version_Mixin

class Status (Page_Tree, Version_Mixin) :
    url          = 'cgi-bin/luci/freifunk/status/status'
    retries      = 2
    timeout      = 10
    html_charset = 'utf-8' # force utf-8 encoding

    wl_names = dict \
        ( ssid    = 'ssid'
        , _bsiid  = 'bssid'
        , channel = 'channel'
        , mode    = 'mode'
        )

    def parse (self) :
        root  = self.tree.getroot ()
        self.wlans  = []
        self.routes = {}
        for div in root.findall (".//%s" % tag ("div")) :
            id = div.get ('id')
            if id == 'cbi-wireless' :
                wlan_div = div
            elif id == 'cbi-routes' :
                route_div = div
            self.try_get_version (div)
        for d in self.tbl_iter (wlan_div) :
            for k, newkey in self.wl_names.iteritems () :
                if k in d :
                    d [newkey] = d [k]
            wl = WLAN_Config (** d)
            self.wlans.append (wl)
        for d in self.tbl_iter (route_div) :
            iface = d.get ('iface')
            gw    = d.get ('gateway')
            if iface and gw :
                self.routes [iface] = gw
        self.set_version (root)
    # end def parse

    def tbl_iter (self, div) :
        tbl = div.find (".//%s" % tag ("table"))
        assert tbl.get ('class') == 'cbi-section-table'
        d = {}
        for tr in tbl :
            if 'cbi-section-table-row' not in tr.get ('class').split () :
                continue
            for input in tr.findall (".//%s" % tag ('input')) :
                name = input.get ('id').split ('.') [-1]
                val  = input.get ('value')
                d [name] = val
            if not d :
                continue
            yield d
    # end def tbl_iter

# end class Status

class Table_Iter (Page_Tree) :

    def table_iter (self) :
        root  = self.tree.getroot ()
        for div in root.findall (".//%s" % tag ("div")) :
            if div.get ('id') == 'maincontent' :
                break
        tbl = div.find (".//%s" % tag ("table"))
        if tbl is None :
            return
        for tr in tbl :
            if tr [0].tag == tag ('th') :
                continue
            yield (self.tree.get_text (x) for x in tr)
    # end def table_iter

# end class Table_Iter

class OLSR_Connections (Table_Iter) :
    url          = 'cgi-bin/luci/freifunk/olsr/'
    retries      = 2
    timeout      = 10
    html_charset = 'utf-8' # force utf-8 encoding

    def parse (self) :
        self.neighbors = {}
        for l in self.table_iter () :
            neighbor, ip, lq, nlq, etx = l
            lq, nlq, etx = (float (x) for x in (lq, nlq, etx))
            self.neighbors [neighbor] = [ip, lq, nlq, etx]
    # end def parse

# end class OLSR_Connections

class OLSR_Routes (Table_Iter) :
    url          = 'cgi-bin/luci/freifunk/olsr/routes'
    retries      = 2
    timeout      = 10
    html_charset = 'utf-8' # force utf-8 encoding

    def parse (self) :
        self.iface_by_gw = {}
        for l in self.table_iter () :
            announced, gw, iface, metric, etx = l
            if gw in self.iface_by_gw :
                assert iface == self.iface_by_gw [gw]
            else :
                self.iface_by_gw [gw] = iface
    # end def parse

# end class OLSR_Routes

class OpenWRT (autosuper) :

    def __init__ (self, site, request) :
        self.site    = site
        self.request = request
        if 'interfaces' in self.request or 'ips' in self.request :
            st    = Status           (site = site)
            conn  = OLSR_Connections (site = site)
            route = OLSR_Routes      (site = site)
            self.version = st.version
            assert len (st.wlans) <= 1
            interfaces   = {}
            ips          = {}
            count = 0
            for gw, ifname in route.iface_by_gw.iteritems () :
                ip, lq, nlq, etx  = conn.neighbors [gw]
                i4 = Inet4 (ip, None, None, iface = ifname)
                ips [i4] = 1
                is_wlan = True
                if lq == nlq == etx == 1.0 :
                    is_wlan = False
                if ifname in interfaces :
                    iface = interfaces [ifname]
                    if not iface.is_wlan and is_wlan :
                        iface.is_wlan   = True
                        iface.wlan_info = st.wlans [0]
                else :
                    iface = Interface (count, ifname, None)
                    iface.is_wlan = is_wlan
                    if is_wlan :
                        iface.wlan_info = st.wlans [0]
                    count += 1
                    interfaces [ifname] = iface
                if i4 not in iface.inet4 :
                    iface.append_inet4 (i4)
            wl_if = None
            for iface in interfaces.itervalues () :
                if iface.is_wlan :
                    if wl_if :
                        m = "Duplicate wlan: %s/%s" % (iface.name, wl_if.name)
                        raise ValueError (m)
                    wl_if = iface
            # check own ip
            n  = 'unknown'
            i4 = Inet4 (self.request ['ip'], None, None, iface = n)
            if i4 not in ips :
                assert n not in interfaces
                iface = interfaces [n] = Interface (count, n, None)
                iface.append_inet4 (i4)
                iface.is_wlan = False
                if not wl_if and st.wlans :
                    iface.is_wlan   = True
                    iface.wlan_info = st.wlans [0]
                ips [i4] = True

            self.request ['ips']        = ips
            self.request ['interfaces'] = interfaces
            self.request ['version']    = st.version
    # end def __init__

# end class OpenWRT
