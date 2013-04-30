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

from   rsclib.HTML_Parse  import tag, Page_Tree
from   rsclib.autosuper   import autosuper
from   spider.common      import Interface, Inet4, Inet6, unroutable
from   spider.common      import WLAN_Config
from   olsr.common        import Topo_Entry, HNA_Entry

class Version_Mixin (autosuper) :
    version      = "Unknown"
    luci_version = bf_version = None

    def try_get_version (self, div) :
        if div.get ('class') == 'footer' :
            for p in div.findall (".//%s" % tag ("p")) :
                if  (   p.get ('class') == 'luci'
                    and len (p)
                    and p [0].tag == tag ("a")
                    ) :
                    a = p [0]
                    if a.text.startswith ("Powered by LuCI") :
                        self.luci_version = a.text
        if div.get ('class') == 'header_right' :
            self.bf_version = div.text
        if div.get ('class') == 'hostinfo' :
            assert self.bf_version is None
            self.bf_version = div.text.split ('|') [0].strip ()
    # end def try_get_version

    def set_version (self, root) :
        lv = self.luci_version
        if lv is None :
            p = root [-1][-1]
            if p.tag == tag ('p') and p.get ('class') == 'luci' :
                lv = self.luci_version = p.text
        if (lv and lv.startswith ('Powered by LuCI')) :
            lv = lv.split ('(', 1) [-1].split (')', 1) [0]
            self.luci_version = lv
        if self.bf_version and self.luci_version :
            self.version = "%s / Luci %s" % (self.bf_version, self.luci_version)
    # end def set_version

# end class Version_Mixin

class Interfaces (Page_Tree, Version_Mixin) :
    url          = 'cgi-bin/luci/freifunk/olsr/interfaces'
    retries      = 2
    wlan_info    = None
    timeout      = 10
    html_charset = 'utf-8' # force utf-8 encoding

    def parse (self) :
        root = self.tree.getroot ()
        self.if_by_name = {}
        self.ips        = {}
        for div in root.findall (".//%s" % tag ("div")) :
            self.try_get_version (div)
            if div.get ('id') == 'maincontent' and not self.if_by_name :
                tbl = div.find (".//%s" % tag ("table"))
                for n, tr in enumerate (tbl) :
                    if tr [0].tag == tag ('th') :
                        assert tr [0].text in ('Interface', 'Schnittstelle') \
                            , tr [0].text
                        continue
                    name, status, mtu, wlan, ip, mask, bcast = \
                        (x.text for x in tr)
                    if name in self.if_by_name :
                        iface = self.if_by_name [name]
                    else :
                        iface = Interface (n, name, mtu)
                        iface.is_wlan = wlan == 'Yes'
                    if status == 'DOWN' :
                        continue
                    if ':' in ip :
                        i6 = Inet6 (ip, mask, bcast, iface = name)
                        iface.append_inet6 (i6)
                    else :
                        i4 = Inet4 (ip, mask, bcast, iface = name)
                        iface.append_inet4 (i4)
                        if not unroutable (i4.ip) :
                            self.if_by_name [name] = iface
                            self.ips [i4] = True
        self.set_version (root)
        if not self.if_by_name :
            raise ValueError, "No interface config found"
        bfw = Backfire_WLAN_Config (site = self.site)
        for d in bfw.wlans :
            if d.name in self.if_by_name :
                iface = self.if_by_name [d.name]
                iface.wlan_info = d
    # end def parse

# end class Interfaces

class Backfire_WLAN_Config (Page_Tree) :
    url          = 'cgi-bin/luci/freifunk/status'
    retries      = 2
    timeout      = 10
    html_charset = 'utf-8' # force utf-8 encoding

    def parse (self) :
        wlo = ('Wireless Overview', 'Drahtlosübersicht'.decode ('latin1'))
        root = self.tree.getroot ()
        self.wlans = []
        for div in root.findall (".//%s" % tag ("div")) :
            if div.get ('class') != 'cbi-map' :
                continue
            if not len (div) or div [0].tag != tag ('h2') :
                continue
            if div [0].text not in wlo :
                continue
            for tr in div.findall (".//%s" % tag ("tr")) :
                cls = tr.get ('class') or ''
                cls = cls.split ()
                if 'cbi-section-table-row' not in cls :
                    continue
                d = WLAN_Config ()
                self.wlans.append (d)
                for td in tr :
                    k = td.get ('id')
                    if k :
                        k = k.split ('-') [-1]
                    else :
                        k = 'name'
                    v = td.text
                    setattr (d, k, v)
            break
    # end def parse
# end class Backfire_WLAN_Config

class MID_Parser (Page_Tree) :

    url = 'cgi-bin/luci/freifunk/olsr/mid/'

    def __init__ (self, site, content) :
        self.content = content
        self.__super.__init__ (site = site)
    # end def __init__

    def parse (self) :
        root = self.tree.getroot ()
        for fs in root.findall (".//%s" % tag ("fieldset")) :
            if fs.get ('class') == 'cbi-section' :
                tbl = fs.find (".//%s" % tag ("table"))
                assert tbl.get ('class') == 'cbi-section-table'
                for tr in tbl :
                    if tr [0].tag == tag ('th') :
                        assert tr [0].text == 'OLSR node'
                        continue
                    assert tr [0][0].tag == tag ('a')
                    self.content.add (tr [0][0].text, * tr [1].text.split (';'))
    # end def parse

# end class MID_Parser

class HNA_Parser (Page_Tree) :

    url = 'cgi-bin/luci/freifunk/olsr/hna/'

    def __init__ (self, site, content) :
        self.content = content
        self.__super.__init__ (site = site)
    # end def __init__

    def parse (self) :
        root = self.tree.getroot ()
        for fs in root.findall (".//%s" % tag ("fieldset")) :
            if fs.get ('class') == 'cbi-section' :
                tbl = fs.find (".//%s" % tag ("table"))
                assert tbl.get ('class') == 'cbi-section-table'
                for tr in tbl :
                    if tr [0].tag == tag ('th') :
                        assert tr [0].text == 'Announced network'
                        continue
                    assert tr [1][0].tag == tag ('a')
                    self.content.add (HNA_Entry (tr [0].text, tr [1][0].text))
    # end def parse

# end class HNA_Parser

class Topo_Parser (Page_Tree) :

    url = 'cgi-bin/luci/freifunk/olsr/topology/'

    def __init__ (self, site, content) :
        self.content = content
        self.__super.__init__ (site = site)
    # end def __init__

    def parse (self) :
        root = self.tree.getroot ()
        for fs in root.findall (".//%s" % tag ("fieldset")) :
            if fs.get ('class') == 'cbi-section' :
                tbl = fs.find (".//%s" % tag ("table"))
                assert tbl.get ('class') == 'cbi-section-table'
                for tr in tbl :
                    if tr [0].tag == tag ('th') :
                        assert tr [0].text == 'OLSR node'
                        continue
                    assert tr [0][0].tag == tag ('a')
                    assert tr [1][0].tag == tag ('a')
                    p = [tr [0][0].text, tr [1][0].text]
                    for v in tr [2:] :
                        v = v.text
                        if v == 'INFINITE' : v = 'inf'
                        v = float (v)
                        p.append (v)
                    self.content.add (Topo_Entry (* p))
    # end def parse

# end class Topo_Parser

class Backfire (autosuper) :

    parsers = dict (hna = HNA_Parser, mid = MID_Parser, topo = Topo_Parser)

    def __init__ (self, site, request) :
        self.site    = site
        self.request = request
        if 'interfaces' in self.request or 'ips' in self.request :
            bfi = Interfaces (site = self.site)
            self.request ['ips']        = bfi.ips
            self.request ['interfaces'] = bfi.if_by_name
            self.request ['version']    = bfi.version
        for k, v in self.parsers.iteritems () :
            if k in self.request :
                v (site = self.site, content = self.request [k])
    # end def __init__

# end class Backfire
