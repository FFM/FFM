#!/usr/bin/python
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

# Note: You need at least rsclib-0.21.9310 from rsclib.sourceforge.net
# Note: for testing we used 'http://guifi.net/pt-pt/guifi/cnml/2441/detail'

# Note: Testing with detail_guifiworld_20111130 yields the following problems:
# - ssids longer than 32 (Wifi standards maximum)
# - Node titles are not unique -- we now use the concatenation of the node id
#   and the title from the XML as the name in our model

import urllib2
import sys, os
import xml.etree.ElementTree  as ElementTree

from   string                 import maketrans
from   rsclib.ETree           import ETree
from   rsclib.IP_Address      import IP4_Address
from   rsclib.iter_recipes    import grouper
from   _GTW                   import GTW
from   _TFL                   import TFL
from   _FFM                   import FFM

import _TFL.CAO
import model

# common typos in mac addresses. 'L' -> '7' is just a guess we're so 7334.
_mac_translate = maketrans ('!OLGPR', '10769B')

def fix_mac (mac) :
    """ Fix typos, seems guifi.net doesn't check syntax of mac address
    >>> fix_mac ('!O:LG:PR:00:00:00')
    '10:76:9B:00:00:00'
    >>> fix_mac ('')
    ''
    >>> fix_mac (None)
    ''
    """
    if not mac :
        return ''
    if len (mac) == 12 :
        mac = ':'.join (''.join (k) for k in grouper (2, mac))
    mac = mac.translate (_mac_translate)
    if mac == '00:00:00:00:00:00' :
        return ''
    return mac
# end def fix_mac

class Convert (object) :

    # this is only for parsing: don't know what legacy is and
    # WiMAX is surely not 802.11n, will have to model this separately if
    # needed.
    protocol_translate = {'legacy' : '802.11b', 'WiMAX' : '802.11n'}

    def __init__ (self, args, scope) :
        if len (args) > 0 :
            fn = args [0]
            if fn.startswith ('http') :
                f = urllib2.urlopen (fn)
            else :
                f = open (fn)
        else :
            f = sys.stdin

        self.et    = ETree (ElementTree.parse (f))
        self.stati = {}
        self.attrs = {}
        self.scope = scope
        self.links = {} # list of linked interfaces by link id
        self.ffm   = self.scope.FFM
        PAP        = self.scope.PAP
        self.owner = PAP.Person (first_name = "guifi", last_name = "net")
        self.modes = dict \
            ( client = 'Client'
            , ap     = 'AP'
            , ad_hoc = 'Ad_Hoc'
            )
        self.modes [None] = None

        #print self.et.pretty (with_text = 1)
        #print self.et.pretty ()

        self.networks = []
        # Umm: our test data uses lots of addresses in the 178.18.8.0/22
        # range which according to whois belongs to some russion entity.
        # We add this for now.
        # Then there is one address from 178.26.0.0/30 from a range of
        # some german cable provider which we simply ignore.
        for n in ('10.0.0.0/8', '172.16.0.0/12', '178.18.8.0/22') :
            n = self.ffm.IP4_Network (n, owner = self.owner)
            self.networks.append (n)

        self.et.walk (self.insert)
        #self.et.walk (self.record_attributes)
    # end def __init__

    def record_status (self, parent, child) :
        """ Callback routine for walk to record existing status or
            link_status fields.
        """
        s = child.get ('status')
        if not s :
            s = child.get ('link_status')
        if s :
            self.stati [s] = 1
    # end def record_status

    def record_attributes (self, parent, child) :
        """ Callback routine for walk to record attributes (with tag).
        """
        for n in child.attrib :
            self.attrs ['.'.join ((child.tag, n))] = 1
    # end def record_attributes

    def insert_node (self, element) :
        """ Insert a node.
        """
        name = '-'.join ((element.get ('title'), element.get ('id')))
        pos  = dict (lat = element.get ('lat'), lon = element.get ('lon'))
        node = self.ffm.Node \
            (name = name, position = pos, manager = self.owner, raw = True)
        for n in element :
            if n.tag == 'device' :
                self.insert_device (node, n)
            else :
                raise ValueError, "Unknown tag in node: %s" % n.tag
    # end insert_node

    def insert_device (self, node, element) :
        """ Insert a device (aka Net_Device)
            Note: guifi.net seems to use the 'name' attribute as the
            device_type (names repeat for devices while the title
            seems to be stable). For now use the name as the name
            of the Net_Device_Type.
        """
        devname = element.get ('name')
        name    = element.get ('title')
        if not devname :
            t = self.ffm.Net_Device_Type.instance (name = "Generic", raw = True)
        else :
            t = self.ffm.Net_Device_Type.instance_or_new \
                (name = devname, raw = True)
        dev = self.ffm.Net_Device \
            (left = t, node = node, name = name, raw = True)
        for nif in element :
            if nif.tag == 'radio' :
                self.insert_radio (dev, nif)
            elif nif.tag == 'interface' :
                self.insert_wired_interface (dev, nif)
            elif nif.tag == 'service' :
                pass # FIXME
            else :
                raise ValueError, "Unknown tag in device: %s" % nif.tag
    # end def insert_device

    def insert_links (self, interface, element) :
        """ Links between interfaces.
        """
        for n in element :
            if n.tag == 'link' :
                # linked_interface_id is bogus in guifi cnml, seems to
                # contain the node id, not the id of the other linked
                # interface
                #r_id  = n.get ('linked_interface_id')
                name  = n.get ('id')
                if name in self.links :
                    assert (len (self.links [name]) == 1)
                    r_id = self.links [name][0]
                    self.links [name].append (element.get ('id'))
                    left  = interface
                    right = self.ffm.Net_Interface.query (name = r_id).one ()
                    self.ffm.Net_Link (left, right)
                else :
                    self.links [name] = [element.get ('id')]
            else :
                raise ValueError, "Unknown node type in interface %s" % n.tag
    # end def insert_links

    def insert_ip_network (self, interface, ip, mask) :
        net = IP4_Address (ip, mask)
        adr = IP4_Address (ip)
        assert (adr in net)
        netadr = self.ffm.IP4_Network.instance (adr)
        if netadr and not netadr.is_free :
            ni = self.ffm.Net_Interface_in_IP4_Network.instance \
                (interface, netadr, mask_len = net.mask)
            assert (ni)
        else :
            n = [x for x in self.networks if net in x.net_address]
            if len (n) < 1 :
                print >> sys.stderr, 'Warning: ignoring address %s' % net
                return
            assert len (n) == 1
            n = n [0]
            try :
                network = n.reserve (net, self.owner)
            except FFM.Error.Address_Already_Used :
                network = self.ffm.IP4_Network.instance (net)
            netadr  = n.reserve (adr, self.owner)
            try :
               self.ffm.Net_Interface_in_IP4_Network \
                   (interface, netadr, mask_len = net.mask)
            except Exception as exc :
                print >> sys.stderr, "Warning: broken IP triggers: %s" % exc
    # end def insert_ip_network

    def insert_wired_interface (self, device, element) :
        mac  = fix_mac (element.get ('mac'))
        name = element.get ('id')
        wif  = self.ffm._Wireless_Interface_.instance \
            ( left        = device
            , name        = name
            , mac_address = mac
            , raw         = True
            )
        if wif :
            # CNML seems to have interfaces that are child of a radio
            # and are repeated on the device-level. Fortunately they seem
            # to always be in the right order (radio parent first).
            # Since there is no good way to distinguish wired from
            # wirelesse interfaces we're using the ones that have a
            # radio as parent for the wireless interfaces.
            assert (wif.mac_address == mac)
            return
        nif  = self.ffm.Wired_Interface.instance \
            ( left        = device
            , name        = name
            , mac_address = mac
            , raw         = True
            )
        if nif :
            assert (nif.mac_address == mac)
        else :
            nif  = self.ffm.Wired_Interface \
                ( left        = device
                , name        = name
                , mac_address = mac
                , raw         = True
                )
            assert (nif.mac_address == mac)
        self.insert_links (nif, element)
        ipv4 = element.get ('ipv4')
        mask = element.get ('mask')
        if ipv4 and mask :
            self.insert_ip_network (nif, ipv4, mask)
        return nif
    # end def insert_wired_interface

    def insert_wireless_interface \
            (self, device, radio, element, antenna, master) :
        mac  = fix_mac (element.get ('mac'))
        ssid = radio.get ('ssid')
        if ssid and len (ssid) > 32 :
            print >> sys.stderr, 'Warning ssid "%s" too long, shortened' % ssid
            ssid = ssid [:32]
        # an interface may have more than one IP address and occur
        # multiple times in the XML
        name  = element.get ('id')
        mode  = element.get ('mode')
        prot  = radio.get ('protocol')
        if prot :
            prot = self.protocol_translate.get (prot, prot)
        std   = self.ffm.Wireless_Standard.instance (prot, raw = True)
        param = dict \
            ( left        = device
            , name        = name
            , essid       = ssid
            , mac_address = mac
            , mode        = self.modes [mode]
            , raw         = True
            )
        wif = self.ffm.Wireless_Interface.instance (** param)
        if master and wif is None :
            wif = self.ffm.Virtual_Wireless_Interface.instance \
                (hardware = master, ** param)
        if wif :
            assert (wif.essid                 == ssid)
            assert (wif.mac_address           == mac)
        else :
            if master :
                wif = self.ffm.Virtual_Wireless_Interface \
                    (hardware = master, ** param)
            else :
                wif = self.ffm.Wireless_Interface (standard = std, ** param)
                self.ffm.Wireless_Interface_uses_Antenna.instance_or_new \
                    (wif, antenna, raw = True)
            assert (wif.mac_address == mac)
        self.insert_links (wif, element)
        ipv4 = element.get ('ipv4')
        mask = element.get ('mask')
        if ipv4 and mask :
            self.insert_ip_network (wif, ipv4, mask)
        return wif
    # end def insert_wireless_interface

    def insert_radio (self, device, element) :
        """ Insert a radio.
            guifi.net lumps all antenna and antenna_type parameters
            into the radio. No reuse of antenna types and antenna (!)
            we create an antenna_type name from the antenna
            parameters, create an antenna and create a network
            interface.
        """
        id   = element.get ('id')
        gn   = element.get ('antenna_gain') or '0'
        p    = dict \
            ( name        = gn
            , gain        = gn
            , raw         = True
            )
        antt = self.ffm.Antenna_Type.instance (** p)
        if not antt :
            antt = self.ffm.Antenna_Type (** p)
            band = self.ffm.Antenna_Band \
                ( antt
                , band = dict (lower = "1 Hz", upper = "1 THz")
                , raw = True
                )
        angle = element.get ('antenna_angle')
        elev  = None
        if angle :
            elev = str (90 - (int (angle) % 360))
        ant  = self.ffm.Antenna.instance_or_new \
            ( left        = antt
            , name        = '.'.join ((id, element.get ('device_id')))
            , azimuth     = element.get ('antenna_azimuth') or '0'
            #, orientation = element.get ('antenna_angle') FIXME: polarisation?
            , elevation   = elev
            , raw         = True
            )
        # FIXME: First check if there are multiple (wireless)
        # interfaces. If yes, we want one wireless interface with
        # several virtual interfaces
        wif = None
        for n in element :
            if n.tag == 'interface' :
                w = self.insert_wireless_interface \
                    (device, element, n, ant, wif)
                if not wif :
                    wif = w
            else :
                raise ValueError, "Unknown node type in radio: %s" % n.tag
    # end def insert_radio

    def insert (self, parent, child) :
        """ Insert given node into the database """
        if child.tag in ('network', 'zone') :
            return
        if child.tag == 'node' :
            self.insert_node (child)
    # end def insert
# end def Convert

def _main (cmd) :
    scope = model.scope (cmd)
    if cmd.Break :
        TFL.Environment.py_shell ()
    c = Convert (cmd.argv, scope)
    for k in sorted (c.attrs.iterkeys ()) :
        print k
    scope.commit ()
    scope.ems.compact ()
    scope.destroy ()
    model.command._handle_load_auth_mig \
        (cmd, mig_auth_file = model.command.default_mig_auth_file + ".cnml")
# end def _main

_Command = TFL.CAO.Cmd \
    ( handler         = _main
    , args            =
        ( "xml_file:S=http://guifi.net/pt-pt/guifi/cnml/2441/detail?XML file to convert"
        ,
        )
    , opts            =
        ( "verbose:B"
        , "create:B"
        ) + model.opts
    , min_args        = 1
    , defaults        = model.command.defaults
    )

if __name__ == "__main__" :
    _Command ()
### __END__ cnml_import
