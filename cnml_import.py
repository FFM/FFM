#!/usr/bin/python

import urllib2
import sys, os
import xml.etree.ElementTree  as ElementTree

from   rsclib.ETree           import ETree
from   _GTW                   import GTW
from   _TFL                   import TFL
from   _FFM                   import FFM

import _TFL.CAO
import model

# 'http://guifi.net/pt-pt/guifi/cnml/2441/detail'

def fix_mac (mac) :
    """ Fix typos, seems guifi.net doesn't check syntax of mac address
    """
    if mac is None :
        return mac
    return mac.replace ('!', '1')
# end def fix_mac

class Convert (object) :
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
        ffm        = self.scope.FFM
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
        name = element.get ('title')
        node = ffm.Node (name = name)
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
        dev = ffm.Net_Device (left = t, name = name, raw = True)
        ffm.Node_has_Net_Device (node, dev)
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
                pass # FIXME
            else :
                raise ValueError, "Unknown node type in interface %s" % n.tag
    # end def insert_links

    def insert_wired_interface (self, device, element) :
        mac  = fix_mac (element.get ('mac'))
        ffm  = self.scope.FFM
        name = element.get ('id')
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
        self.insert_links (nif, element)
        return nif
    # end def insert_wired_interface

    def insert_wireless_interface (self, device, radio, element, antenna) :
        ffm  = self.scope.FFM
        mac  = fix_mac (element.get ('mac'))
        ssid = radio.get   ('ssid')
        # an interface may have more than one IP address and occur
        # multiple times in the XML
        name = "Wireless%s" % element.get ('id')
        mode = element.get ('mode')
        wif  = ffm.Wireless_Interface.instance \
            ( left        = device
            , name        = name
            , mac_address = mac
            )
        prot = radio.get ('protocol')
        if wif :
            assert (wif.raw_attr ('protocol') == prot)
            assert (wif.ssid                  == ssid)
            assert (wif.mac_address           == mac)
        else :
            wif  = ffm.Wireless_Interface \
                ( left        = device
                , name        = name
                , protocol    = prot
                , ssid        = ssid
                , mac_address = mac
                , raw         = True
                )
            ffm.Wireless_Interface_uses_Antenna (wif, antenna)
        if mode :
            self.modes [mode] (wif)
        self.insert_links (wif, element)
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
        ant  = ffm.Antenna \
            ( left        = antt
            , name        = "%s_%s" % (device.name, id)
            , azimuth     = element.get ('antenna_azimuth')
            #, orientation = element.get ('antenna_angle') FIXME: polarisation?
            , inclination = incl
            , raw         = True
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
    ( handler       = _main
    , args          =
        ( "xml_file:S?XML file to convert"
        ,
        )
    , opts          =
        ( "verbose:B"
        , "create:B"
        ) + model.opts
    , min_args      = 1
    , defaults      = model.command.defaults
    )

if __name__ == "__main__" :
    _Command ()

