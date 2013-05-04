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

import re
from   rsclib.HTML_Parse  import tag, Page_Tree
from   rsclib.autosuper   import autosuper
from   rsclib.stateparser import Parser
from   spider.common      import unroutable, Net_Link
from   spider.common      import Inet4, Inet6, Interface, WLAN_Config

pt_mac    = r'((?:[0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2})'

class Interface_Config (Parser) :
    re_assign = re.compile (r'^([a-zA-Z0-9_]+)\s*=\s*([a-zA-Z0-9 ]*)$')
    re_brhead = re.compile (r'^bridge name.*$')
    re_bridge = re.compile (r'^(\S+)\s*(\S+)\s*(\S+)\s*(\S+)$')
    re_ifonly = re.compile (r'^\s+(\S+)$')
    re_if     = re.compile \
        (r'^(\d+):\s*(\S+):\s*mtu\s*(\d+)\s*qdisc\s*(\S+)(?:qlen\s*(\d+))?')
    pt_mac    = pt_mac
    re_link   = re.compile \
        (r'^\s*link/(\S+)(?:\s*(\S+)\s*brd\s*(\S+))?$' % locals ())
    pt_ip     = r'((?:\d{1,3}[.]){3}\d{1,3})'
    re_inet   = re.compile \
        ( r'^\s*inet\s+%(pt_ip)s/(\d+)\s+'
          r'(?:brd\s+%(pt_ip)s\s+)?scope\s+(\S+)\s+(\S+)$'
        % locals ()
        )
    pt_ip6    = r'([0-9a-fA-F:]+)'
    re_inet6  = re.compile \
        ( r'^\s*inet6\s+%(pt_ip6)s/(\d+)\s+scope\s+(\S+)$' % locals ())
    matrix = \
        [ ["init",   re_assign, "init",   "assign"]
        , ["init",   re_brhead, "bridge", None]
        , ["init",   re_if,     "iface",  "iface"]
        , ["init",   None,      "init",   None]
        , ["bridge", re_bridge, "bridge", "bridge"]
        , ["bridge", re_ifonly, "bridge", None]
        , ["bridge", '',        "init",   None]
        , ["iface",  re_link,   "iface",  "link"]
        , ["iface",  re_inet,   "iface",  "inet"]
        , ["iface",  re_inet6,  "iface",  "inet6"]
        , ["iface",  None,      "init",   "pop"]
        ]

    def __init__ (self, **kw) :
        self.assignments = {}
        self.bridges     = []
        self.interfaces  = []
        self.if_by_name  = {}
        self.__super.__init__ (**kw)
    # end def __init__

    def assign (self, state, new_state, match) :
        self.assignments [match.group (1)] = match.group (2)
    # end def assign

    def bridge (self, state, new_state, match) :
        self.bridges.append (match.groups ())
    # end def bridge

    def iface (self, state, new_state, match) :
        self.interface = Interface (* match.groups ())
        self.interfaces.append (self.interface)
        self.if_by_name [self.interface.name] = self.interface
        self.push (state, new_state, match)
    # end def iface

    def link (self, state, new_state, match) :
        self.interface.link = Net_Link (* match.groups ())
    # end def link

    def inet (self, state, new_state, match) :
        self.interface.append_inet4 (Inet4 (* match.groups ()))
    # end def inet

    def inet6 (self, state, new_state, match) :
        self.interface.append_inet6 (Inet6 (* match.groups ()))
    # end def inet6

    def __str__ (self) :
        r = []
        for k, v in self.assignments.iteritems () :
            r.append ("%(k)s = %(v)s" % locals ())
        for b in self.bridges :
            r.append ("Bridge: %s" % str (b))
        for i in self.interfaces :
            r.append (str (i))
        return '\n'.join (r)
    # end def __str__
    __repr__ = __str__

# end class Interface_Config

class WLAN_Config_Freifunk (WLAN_Config, Parser) :
    r_ifname  = r'^(?:([a-zA-Z0-9]+).*)?'
    r_nick    = r'(?:\s*Nickname:\s*"[^"]*")?'
    re_ssid   = re.compile (r'%sE?SSID:\s*"([^"]+)"%s' % (r_ifname, r_nick))
    r_mode    = r'Mode:\s*(.*)'
    r_frq     = r'Frequency:\s*([0-9.]+)\s*GHz'
    re_mode   = re.compile (r'%s\s+(?:rssi|RSSI).*Channel:\s+(\d+)' % r_mode)
    re_mode2  = re.compile \
        (r'%s\s+%s\s+Cell:\s*([0-9a-fA-F:]+)' % (r_mode, r_frq))
    re_bssid  = re.compile (r'BSSID:\s+%(pt_mac)s' % globals ())
    re_ssid_e = re.compile \
        (r'\s+'.join ((re_ssid.pattern, re_mode.pattern, re_bssid.pattern)))
    re_ssid_x = re.compile \
        (r'\s+'.join ((re_ssid.pattern, re_mode2.pattern)))
    matrix = \
        [ ["init",   re_ssid_x, "init",   "p_ssid2"]
        , ["init",   re_ssid_e, "init",   "p_ssid"]
        , ["init",   re_ssid,   "init",   "p_ssid"]
        , ["init",   re_mode,   "init",   "p_mode"]
        , ["init",   re_bssid,  "init",   "p_bssid"]
        , ["init",   None,      "init",   None]
        ]

    def __init__ (self, **kw) :
        self.ssid    = None
        self.mode    = None
        self.channel = None
        self.bssid   = None
        self.__super.__init__ (** kw)
    # end def __init__

    def p_bssid (self, state, new_state, match) :
        self.set (bssid = match.group (1))
    # end def p_bssid

    def p_mode (self, state, new_state, match) :
        self.set (mode = match.group (1).strip (), channel = match.group (2))
    # end def p_mode

    def p_ssid (self, state, new_state, match) :
        self.set (name = match.group (1), ssid = match.group (2))
        if len (match.groups ()) > 2 :
            self.set \
                ( mode    = match.group (3)
                , channel = match.group (4)
                , bssid   = match.group (5)
                )
    # end def p_ssid

    def p_ssid2 (self, state, new_state, match) :
        self.set \
            ( name      = match.group (1)
            , ssid      = match.group (2)
            , mode      = match.group (3)
            , frequency = match.group (4)
            , bssid     = match.group (5)
            )
    # end def p_ssid2

# end class WLAN_Config_Freifunk

class Status (Page_Tree) :
    url       = 'cgi-bin-status.html'
    retries   = 2
    wlan_info = None
    timeout   = 10
    version   = 'Unknown'

    def _check_interface (self, iface, is_wlan = False) :
        found = False
        for ip4 in iface.inet4 :
            if unroutable (ip4.ip) :
                continue
            found = True
            self.ips [ip4] = True
        if found :
            self.if_by_name [iface.name] = iface
            iface.is_wlan = is_wlan
    # end def _check_interface

    def parse (self) :
        #print self.tree_as_string ()
        root = self.tree.getroot ()
        for pre in root.findall (".//%s" % tag ("pre")) :
            if pre.get ('id') == 'ifconfig' :
                self.ifconfig = Interface_Config ()
                self.ifconfig.parse (pre.text.split ('\n'))
                #print pre.text
                self.if_by_name = {}
                self.ips        = {}
                for k, v in self.ifconfig.assignments.iteritems () :
                    v = v.strip ()
                    if not v :
                        continue
                    if k == 'lan_ifname' :
                        is_wlan = False
                    elif k == 'wan_ifname' :
                        is_wlan = False
                    elif k.startswith ('wl') and k.endswith ('_ifname') :
                        is_wlan = True
                    elif k == 'wifi_ifname' :
                        is_wlan = True
                    else :
                        continue
                    # unused interface name:
                    if v not in self.ifconfig.if_by_name :
                        continue
                    iface = self.ifconfig.if_by_name [v]
                    self._check_interface (iface, is_wlan)
                for iface in self.ifconfig.interfaces :
                    if iface.name not in self.if_by_name :
                        self._check_interface (iface)
                break
        else :
            raise ValueError, "No interface config found"
        for td in root.findall (".//%s" % tag ("td")) :
            if (not td.text or 'SSID:' not in td.text) :
                continue
            self.wlan_info = WLAN_Config_Freifunk ()
            self.wlan_info.parse (td.text.split ('\n'))
            break
        wl_count = 0
        if self.wlan_info :
            for iface in self.if_by_name.itervalues () :
                if iface.is_wlan :
                    iface.wlan_info = self.wlan_info
                    wl_count += 1
        if not wl_count and getattr (self.wlan_info, 'name', None) :
            iface = self.if_by_name [self.wlan_info.name]
            iface.is_wlan = True
            iface.wlan_info = self.wlan_info
            wl_count += 1

        assert wl_count <= 1
        for sm in root.findall (".//%s" % tag ("small")) :
            if sm.text :
                s = sm.text.strip ()
                if s.startswith ('v1.') or s.startswith ('1.') :
                    self.version = sm.text
                    break
        if self.version == 'Unknown' :
            for td in root.findall (".//%s" % tag ("td")) :
                if td.text :
                    s = td.text.strip ()
                    if s.startswith ('v1.') or s.startswith ('Fonera-1') :
                        self.version = td.text.strip ()
                        break
    # end def parse

# end class Status

class Freifunk (autosuper) :

    def __init__ (self, site, request, url = None) :
        self.site    = site
        self.request = request
        if 'interfaces' in self.request or 'ips' in self.request :
            st = Status (site = self.site, url = url)
            self.request ['ips']        = st.ips
            self.request ['interfaces'] = st.if_by_name
            self.request ['version']    = st.version
    # end def __init__

# end class Freifunk

