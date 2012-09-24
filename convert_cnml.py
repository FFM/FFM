#!/usr/bin/python

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

def id_mangle (name) :
    return '-'.join (('x', name))
# end def id_mangle

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
        ffm        = self.scope.FFM
        PAP        = self.scope.PAP
        self.owner = PAP.Person (first_name = "guifi", last_name = "net")
        self.modes = dict \
            ( client = ffm.Client_Mode
            , ap     = ffm.AP_Mode
            , ad_hoc = ffm.Ad_Hoc_Mode
            )

        #print self.et.pretty (with_text = 1)
        #print self.et.pretty ()


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
        ffm  = self.scope.FFM
        name = '-'.join ((element.get ('title'), element.get ('id')))
        pos  = dict (lat = element.get ('lat'), lon = element.get ('lon'))
        node = ffm.Node (name = name, position = pos, manager = self.owner)
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
        ffm     = self.scope.FFM
        if not devname :
            t = ffm.Net_Device_Type.instance (name = "Generic", raw = True)
        else :
            t = ffm.Net_Device_Type.instance_or_new (name = devname, raw = True)
        dev = ffm.Net_Device (left = t, node = node, name = name, raw = True)
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
        ffm  = self.scope.FFM
        for n in element :
            if n.tag == 'link' :
                # linked_interface_id is bogus in guifi cnml, seems to
                # contain the node id, not the id of the other linked
                # interface
                #r_id  = n.get ('linked_interface_id')
                name  = n.get ('id')
                if name in self.links :
                    assert (len (self.links [name]) == 1)
                    r_id = id_mangle (self.links [name][0])
                    self.links [name].append (element.get ('id'))
                    left  = interface
                    right = ffm.Net_Interface.query (name = r_id).one ()
                    if isinstance (left, ffm.Wireless_Interface) :
                        ffm.Wireless_Link (left, right)
                    else :
                        ffm.Wired_Link    (left, right)
                else :
                    self.links [name] = [element.get ('id')]
            else :
                raise ValueError, "Unknown node type in interface %s" % n.tag
    # end def insert_links

    def insert_ip_network (self, interface, ip, mask) :
        ffm = self.scope.FFM
        net = IP4_Address (ip, mask)
        adr = IP4_Address (ip)
        assert (adr in net)
        network = ffm.IP4_Network.instance_or_new \
            (dict (address = str (net)), raw = True)
        ffm.Net_Interface_in_IP4_Network.instance_or_new \
            (interface, network, dict (address = adr))
    # end def insert_ip_network

    def insert_wired_interface (self, device, element) :
        mac  = fix_mac (element.get ('mac'))
        ffm  = self.scope.FFM
        name = id_mangle (element.get ('id'))
        wif  = ffm.Wireless_Interface.instance \
            ( left        = device
            , name        = name
            , mac_address = mac
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
        nif  = ffm.Wired_Interface.instance \
            ( left        = device
            , name        = name
            , mac_address = mac
            )
        if nif :
            assert (nif.mac_address == mac)
        else :
            nif  = ffm.Wired_Interface \
                ( left        = device
                , name        = name
                , mac_address = mac
                )
            assert (nif.mac_address == mac)
        self.insert_links (nif, element)
        ipv4 = element.get ('ipv4')
        mask = element.get ('mask')
        if ipv4 and mask :
            self.insert_ip_network (nif, ipv4, mask)
        return nif
    # end def insert_wired_interface

    def insert_wireless_interface (self, device, radio, element, antenna) :
        ffm  = self.scope.FFM
        mac  = fix_mac (element.get ('mac'))
        ssid = radio.get ('ssid')
        if ssid and len (ssid) > 32 :
            print >> sys.stderr, 'Warning ssid "%s" too long, shortened' % ssid
            ssid = ssid [:32]
        # an interface may have more than one IP address and occur
        # multiple times in the XML
        name = id_mangle (element.get ('id'))
        mode = element.get ('mode')
        wif  = ffm.Wireless_Interface.instance \
            ( left        = device
            , name        = name
            , mac_address = mac
            )
        prot = radio.get ('protocol')
        if prot :
            prot = self.protocol_translate.get (prot, prot)
        if wif :
            assert (wif.essid                 == ssid)
            assert (wif.mac_address           == mac)
        else :
            std  = ffm.Wireless_Standard.instance (prot)
            wif  = ffm.Wireless_Interface \
                ( left        = device
                , name        = name
                , standard    = std
                , essid       = ssid
                , mac_address = mac
                , raw         = True
                )
            assert (wif.mac_address == mac)
            ffm.Wireless_Interface_uses_Antenna (wif, antenna)
        if mode :
            self.modes [mode] (wif)
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
        ffm  = self.scope.FFM
        gn   = element.get ('antenna_gain') or '0'
        antt = ffm.Antenna_Type.instance_or_new \
            ( name        = gn
            , gain        = gn
            , raw         = True
            )
        angle = element.get ('antenna_angle')
        incl  = None
        if angle :
            incl = str (90 - (int (angle) % 360))
        ant  = ffm.Antenna.instance_or_new \
            ( left        = antt
            , name        = id
            , azimuth     = element.get ('antenna_azimuth') or '0'
            #, orientation = element.get ('antenna_angle') FIXME: polarisation?
            , inclination = incl
            )
        for n in element :
            if n.tag == 'interface' :
                self.insert_wireless_interface (device, element, n, ant)
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
