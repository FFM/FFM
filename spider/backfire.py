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
from   spider.common      import Interface, Inet4, Inet6, is_rfc1918
from   spider.common      import WLAN_Config

class Backfire (Page_Tree) :
    url          = 'cgi-bin/luci/freifunk/olsr/interfaces'
    retries      = 2
    wlan_info    = None
    timeout      = 10
    html_charset = 'utf-8' # force utf-8 encoding

    def parse (self) :
        root = self.tree.getroot ()
        self.if_by_name = {}
        self.ips        = {}
        self.version    = "Unknown"
        self.luci_version = self.bf_version = None
        for div in root.findall (".//%s" % tag ("div")) :
            if div.get ('class') == 'footer' :
                for p in div.findall (".//%s" % tag ("p")) :
                    if  (   p.get ('class') == 'luci'
                        and len (p)
                        and p [0].tag == tag ("a")
                        ) :
                        a = p [0]
                        if a.text.startswith ("Powered by LuCI") :
                            t = a.text.split ('(', 1) [-1].rstrip (')')
                            self.luci_version = t
            if div.get ('class') == 'header_right' :
                self.bf_version = div.text
            if div.get ('class') == 'hostinfo' :
                assert self.bf_version is None
                self.bf_version = div.text.split ('|') [0].strip ()
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
                        if not is_rfc1918 (i4.ip) :
                            self.if_by_name [name] = iface
                            self.ips [i4] = True
        if self.luci_version is None :
            p = root [-1][-1]
            if p.tag == tag ('p') and p.get ('class') == 'luci' :
                self.luci_version = p.text
        if  (   self.luci_version
            and self.luci_version.startswith ('Powered by LuCI Trunk (')
            ) :
            self.luci_version = self.luci_version.split ('(', 1) [-1]
            self.luci_version = self.luci_version.split (')', 1) [0]
        if not self.if_by_name :
            raise ValueError, "No interface config found"
        if self.bf_version and self.luci_version :
            self.version = "%s / Luci %s" % (self.bf_version, self.luci_version)
#        else :
#            print "bf: %s luci: %s" % (self.bf_version, self.luci_version)
        bfw = Backfire_WLAN_Config (site = self.site)
        for d in bfw.wlans :
            if d.name in self.if_by_name :
                iface = self.if_by_name [d.name]
                iface.wlan_info = d
    # end def parse

# end class Backfire

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
