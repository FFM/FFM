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
        self.scope = scope
        self.dev_by_name   = {}
        # store Net_Device under radio name
        self.netdev_by_radio_name = {}

        #print self.et.pretty (with_text = 1)
        #print self.et.pretty ()

        self.et.walk (self.insert)
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

    def insert (self, parent, child) :
        """ Insert given node into the database """
        if child.tag in ('network', 'zone') :
            return
        ffm = self.scope.FFM
        if child.tag == 'device' :
            # Note: guifi.net seems to use the 'name' attribute as the
            # device_type (names repeat for devices while the title
            # seems to be stable). For now use the name as the model_no
            # of the Net_Device_Type
            model_no = child.get ('name')
            name     = child.get ('title')
            if not model_no :
                print "Warning: ignoring device without type: %s" % name
                return
            t = ffm.Net_Device_Type.instance_or_new (model_no = model_no)
            d = ffm.Net_Device (left = t, name = name)
            self.dev_by_name [name] = d
        if child.tag == 'radio' :
            # guifi.net lumps all antenna and antenna_type parameters
            # into the radio. No reuse of antenna types and antenna (!)
            # we create an antenna_type model_no from the antenna
            # parameters.
            assert (parent.tag == 'device')
            dev = self.dev_by_name.get (parent.get ('title'))
            if not dev :
                # FIXME
                return
            self.netdev_by_radio_name [child.get ('name')] = dev
        if child.tag == 'interface' :
            mac  = child.get ('mac')
            if not mac :
                print "Warning: interface without mac"
                return
            if parent.tag == 'radio' :
                dev  = self.netdev_by_radio_name.get (parent.get ('name'))
                ssid = child.get ('ssid')
                if not dev :
                    # FIXME
                    return
                if not ssid :
                    print "Warning: wireless interface without ssid"
                    return
                wif  = ffm.Wireless_Interface \
                    ( left        = dev
                    # FIXME:Fails , protocol    = child.get ('protocol')
                    , ssid        = ssid
                    , mac_address = mac
                    )
                gn   = parent.get ('antenna_gain') or '0'
                antt = ffm.Antenna_Type.instance_or_new \
                    ( model_no    = gn
                    , gain        = gn
                    )
                ant  = ffm.Antenna \
                    ( left        = antt
                    , azimuth     = child.get ('antenna_azimuth')
                    , orientation = child.get ('antenna_angle')
                    , inclination = child.get ('antenna_elevation')
                    )
            else :
                assert (parent.tag == 'device')
                dev  = self.dev_by_name.get (parent.get ('title'))
                if not dev :
                    # FIXME
                    return
                try :
                    nif  = ffm.Net_Interface \
                        ( left        = dev
                        , mac_address = child.get ('mac')
                        )
                # FIXME: This is a duplicate entry, catch right
                # exception. We seem to have duplicate macs in the
                # network
                except Exception, cause :
                    print "Warning: %s", cause
    # end def insert
# end def Convert


def _main (cmd) :
    scope = model.scope (cmd)
    if cmd.Break :
        TFL.Environment.py_shell ()
    c = Convert (cmd.argv, scope)
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
    )

if __name__ == "__main__" :
    _Command ()

