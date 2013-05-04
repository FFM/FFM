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

from   rsclib.autosuper   import autosuper
from   rsclib.IP_Address  import IP4_Address

class Parse_Error (ValueError) :
    pass

rfc1918_networks = \
    [IP4_Address (x)
     for x in ('10.0.0.0/8', '172.16.0.0/12', '192.168.0.0/16')
    ]
localnet  = IP4_Address ('127.0.0.0/8')
linklocal = IP4_Address ('169.254.0.0/16')

def is_rfc1918 (ip) :
    for n in rfc1918_networks :
        if ip in n :
            return True
    return False
# end def is_rfc1918

def is_local (ip) :
    return ip in localnet
# end def is_local

def is_link_local (ip) :
    return ip in linklocal
# end def is_link_local

def unroutable (ip) :
    ip  = IP4_Address (ip)
    return is_rfc1918 (ip) or is_local (ip) or is_link_local (ip)
# end def unroutable

class Compare_Mixin (autosuper) :

    def __ne__ (self, other) :
        return not self == other
    # end def __ne__

# end class Compare_Mixin

class Net_Link (autosuper) :
    """Physical layer link interface
    """

    def __init__ (self, linktype, mac, bcast) :
        self.linktype = linktype
        self.mac      = mac
        self.bcast    = bcast
    # end def __init__

    def __str__ (self) :
        return "Net_Link (%(linktype)s, %(mac)s, %(bcast)s)" % self.__dict__
    # end def __str__
    __repr__ = __str__

# end class Net_Link

class Inet (Compare_Mixin) :
    """IP Network address
    """

    def __init__ (self, ip, netmask, scope = None, iface = None, bcast = None) :
        self.ip      = ip
        self.netmask = netmask
        self.scope   = scope
        self.iface   = iface
        self.bcast   = bcast
    # end def __init__

    def __str__ (self) :
        return self.__class__.__name__ \
            + " (%(ip)s/%(netmask)s, %(bcast)s, %(scope)s)" % self.__dict__
    # end def __str__
    __repr__ = __str__

    def __hash__ (self) :
        return hash (self.ip)
    # end def __hash__

    def __eq__ (self, other) :
        return self.ip == other.ip
    # end def __eq__

# end class Inet

class Inet4 (Inet) :

    def __init__ (self, ip, mask, bcast, scope = None, iface = None, ** kw) :
        self.__super.__init__ (ip, mask, scope, iface, bcast = bcast)
    # end def __init__

# end class Inet4

class Inet6 (Inet) :

    def __init__ (self, ip, mask, bcast, scope = None, iface = None, ** kw) :
        self.__super.__init__ (ip, mask, scope, iface, bcast = bcast)
    # end def __init__

# end class Inet6

class Interface (Compare_Mixin) :
    """Network interface
    """

    def __init__ (self, number, name, mtu = None, qdisc = None, qlen = None) :
        self.number    = number
        self.name      = name
        self.mtu       = mtu
        self.qdisc     = qdisc
        self.qlen      = qlen
        self.link      = None
        self.inet4     = []
        self.inet6     = []
        self.is_wlan   = None
        self.wlan_info = None
    # end def __init__

    def append_inet4 (self, inet) :
        self.inet4.append (inet)
        if not inet.iface.startswith (self.name) :
            raise Parse_Error \
                ( "Wrong interface name in inet4 address: %s %s"
                % (inet.iface, self.name)
                )
        inet.iface = self
    # end def append_inet4

    def append_inet6 (self, inet) :
        self.inet6.append (inet)
        if inet.iface is not None and not inet.iface.startswith (self.name) :
            raise Parse_Error \
                ( "Wrong interface name in inet6 address: %s %s"
                % (inet.iface, self.name)
                )
        inet.iface = self
    # end def append_inet6

    def __eq__ (self, other) :
        return \
            (   self.name      == other.name
            and self.inet4     == other.inet4
            and self.inet6     == other.inet6
            and self.is_wlan   == other.is_wlan
            and self.wlan_info == other.wlan_info
            )
    # end def __eq__

    def __str__ (self) :
        r = []
        r.append \
            ( "Interface (%(name)s, %(number)s, is_wlan=%(is_wlan)s)"
            % self.__dict__
            )
        if self.link :
            r.append (str (self.link))
        for i in self.inet4 :
            r.append (str (i))
        for i in self.inet6 :
            r.append (str (i))
        if self.wlan_info :
            r.append (str (self.wlan_info))
        return "\n    ".join (r)
    # end def __str__
    __repr__ = __str__

    def __getattr__ (self, name) :
        if name == 'names' :
            self.names = [self.name]
            return self.names
        raise AttributeError, name
    # end def __getattr__

# end class Interface

class WLAN_Config (Compare_Mixin) :

    modes = \
        { 'ad-hoc' : 'Ad-Hoc'
        , 'adhoc'  : 'Ad-Hoc'
        , 'ad hoc' : 'Ad-Hoc'
        }

    frq = \
        { '2.412' :  '1'
        , '2.417' :  '2'
        , '2.422' :  '3'
        , '2.427' :  '4'
        , '2.432' :  '5'
        , '2.437' :  '6'
        , '2.442' :  '7'
        , '2.447' :  '8'
        , '2.452' :  '9'
        , '2.457' : '10'
        , '2.462' : '11'
        , '2.467' : '12'
        , '2.472' : '13'
        , '2.484' : '14'
        }

    def __init__ (self, ** kw) :
        self.set (** kw)
        self.__super.__init__ (** kw)
    # end def __init__

    def set (self, ** kw) :
        self.name     = kw.get ('name')
        self.ssid     = kw.get ('ssid')
        self.mode     = kw.get ('mode')
        if self.mode :
            self.mode = self.mode.lower ()
            self.mode = self.modes.get (self.mode, self.mode)
        self.channel  = kw.get ('channel')
        self.bssid    = kw.get ('bssid')
        if not self.channel and 'frequency' in kw :
            self.channel = self.frq [kw ['frequency']]
    # end def set

    def __eq__ (self, other) :
        return \
            (   self.ssid    == other.ssid
            and self.mode    == other.mode
            and self.channel == other.channel
            and self.bssid   == other.bssid
            )
    # end def __eq__

    def __str__ (self) :
        x = [self.__class__.__name__, "\n        ( "]
        z = []
        for k in 'ssid', 'mode', 'channel', 'bssid' :
            z.append ("%s=%%(%s)s" % (k, k))
        x.append ('\n        , '.join (z))
        x.append ('\n        )')
        return ''.join (x) % self.__dict__
    # end def __str__
    __repr__ = __str__

# end class WLAN_Config
