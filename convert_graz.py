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

import sys, os
import re

from   datetime               import datetime, tzinfo, timedelta
from   rsclib.IP_Address      import IP4_Address
from   rsclib.Phone           import Phone
from   rsclib.sqlparser       import make_naive, SQL_Parser
from   _GTW                   import GTW
from   _TFL                   import TFL
from   _FFM                   import FFM
from   _GTW._OMP._PAP         import PAP

import _TFL.CAO
import model

class Convert (object) :

    person_dupes = \
        { 179 : 124
        , 267 : 322
        , 307 : 306
        , 372 : 380 # same phone *and* password (!) different name (!)
        , 424 : 418
        , 617 : 623
        , 686 : 687
        , 708 : 707
        , 709 : 707
        , 718 : 860
        , 729 : 728
        , 741 : 740
        , 755 : 754
        , 776 : 301
        , 799 : 807
        , 820 : 359
        , 821 : 359
        , 831 : 836
        , 852 : 851
        , 892 : 706
        , 903 : 904
        }

    def __init__ (self, cmd, scope, debug = False) :
        self.debug = debug
        if len (cmd.argv) > 0 :
            f  = open (cmd.argv [0])
        else :
            f = sys.stdin
        self.scope        = scope
        self.ffm          = self.scope.FFM
        self.pap          = self.scope.GTW.OMP.PAP
        self.networks     = {}

        self.parser       = SQL_Parser (verbose = False, fix_double_encode = 1)
        self.parser.parse (f)
        self.contents     = self.parser.contents
        self.tables       = self.parser.tables
        self.member_by_id = {}
        self.person_by_id = {}
        self.nicknames    = {}
        self.node_by_id   = {}
        self.phone_ids    = {}
    # end def __init__

    def create (self) :
        self.create_persons ()
        self.create_nodes   ()
        self.create_devices ()
    # end def create

    def create_devices (self) :
        # ignore snmp_ip and snmp_lastseen (only used by three nodes)
        # FIXME: Use smokeping?
        # FIXME: hastinc?
        for d in self.contents ['node'] :
            if d.location_id not in self.node_by_id :
                print "WARN: Ignoring device (node) %s with location_id %s" \
                    % (d.id, d.location_id)
                continue
            n = self.node_by_id [d.location_id]
            if d.person_id and d.person_id != n.person_id :
                print "person %s: d:%s n:%s" % (d.id, d.person_id, n.person_id)
    # end def create_devices

    def create_nodes (self) :
        x_start = 4080
        y_start = 4806
        x_lon   = 15.43844103813
        y_lat   = 47.07177327969
        dx_lon  = 50675.5176
        dy_lat  = 75505.521
        for n in sorted (self.contents ['location'], key = lambda x : x.id) :
            self.node_by_id [n.id] = n
            person_id = self.person_dupes.get (n.person_id, n.person_id)
            if person_id not in self.person_by_id :
                print "WARN: Location %s owner %s missing" % (n.id, person_id)
                continue
            person = self.person_by_id [person_id]


            lat = lon = None
            if n.pixel_x is not None and n.pixel_y is not None :
                lon = "%f" % (x_lon + (n.pixel_x - x_start) / dx_lon)
                lat = "%f" % (y_lat + (n.pixel_y - y_start) / dy_lat)

            node = self.ffm.Node \
                ( name        = n.name
                , show_in_map = not n.hidden
                , manager     = person
                , position    = dict (lat = lat, lon = lon)
                , raw         = True
                )
            if n.street :
                s = ' '.join (x for x in (n.street, n.streetnr) if x)
                adr = self.pap.Address.instance_or_new \
                    ( street = s
                    , zip    = '8010'
                    , city   = 'Graz'
                    , country = 'Austria'
                    )
                self.pap.Node_has_Address (node, adr)
            if n.gallery_link :
                abs = 'http://gallery.funkfeuer.at/v/Graz/Knoten/%s/'
                if n.gallery_link.startswith ('http') :
                    abs = "%s"
                url = self.pap.Url.instance_or_new \
                    (abs % n.gallery_link, desc = 'Gallery')
                self.pap.Node_has_Url (node, url)
            #print "%4d %s %s %r %s %s %s %r" % \
            #    (n.id, n.hastinc, n.time, n.street, n.streetnr, n.gps_lon, n.gps_lat, n.comment)
    # end def create_nodes

    def create_persons (self) :
        for m in sorted (self.contents ['person'], key = lambda x : x.id) :
            #print "%s: %r %r" % (m.id, m.firstname, m.lastname)
            self.member_by_id [m.id] = m
            if m.id in self.person_dupes :
                print "INFO: Duplicate person: %s" % m.id
                continue
            if not m.firstname or not m.lastname :
                print >> sys.stderr, "WARN: name missing: %s (%s/%s)" \
                    % (m.id, m.firstname, m.lastname)
                continue
            person = self.pap.Person \
                ( first_name = m.firstname.strip ()
                , last_name  = m.lastname.strip ()
                , raw        = True
                )
            self.person_by_id [m.id] = person
            if m.nick :
                self.try_insert_nick (m.nick, m.id, person)
            if m.email :
                email = self.pap.Email (address = m.email)
                self.pap.Person_has_Email (person, email)
            if m.tel :
                self.try_insert_phone (m.tel, m.id, person)
        # get data from dupes
        for d_id, m_id in self.person_dupes.iteritems () :
            # older version of db or dupe removed:
            if d_id not in self.member_by_id or m_id not in self.person_by_id :
                continue
            d = self.member_by_id [d_id]
            m = self.member_by_id [m_id]
            person = self.person_by_id [m_id]
            if d.email :
                email = self.pap.Email (address = d.email)
                self.pap.Person_has_Email (person, email)
            if d.nick :
                self.try_insert_nick (d.nick, m_id, person)
            if d.tel :
                self.try_insert_phone (d.tel, m_id, person)
    # end def create_persons

    def set_creation (self, obj, create_time) :
        create_time = make_naive (create_time)
        self.scope.ems.convert_creation_change (obj.pid, c_time = create_time)
    # end def set_creation

    def try_insert_phone (self, tel, id, person) :
        p = Phone (tel, city = "Graz")
        if p :
            k = str (p)
            t = self.pap.Phone.instance (*p)
            if t :
                eid = self.phone_ids [k]
                prs = self.person_by_id [eid]
                if eid != id :
                    print "WARN: %s/%s %s/%s: Duplicate Phone: %s" \
                        % (eid, prs.pid, id, person.pid, tel)
            else :
                self.phone_ids [k] = id
                phone = self.pap.Phone (*p)
                self.pap.Person_has_Phone (person, phone)
    # end def try_insert_phone

    def try_insert_nick (self, nick, id, person) :
        lnick = nick.lower ()
        if lnick in self.nicknames :
            eid = self.nicknames [lnick]
            prs = self.person_by_id [eid]
            if eid != id :
                print "WARN: %s/%s %s/%s Duplicate Nickname: %s" \
                    % (eid, prs.pid, id, person.pid, nick)
        else :
            n = self.pap.Nickname (nick, raw = True)
            self.pap.Person_has_Nickname (person, n)
            self.nicknames [lnick] = id
    # end def try_insert_nick

# end def Convert


def _main (cmd) :
    scope = model.scope (cmd)
    if cmd.Break :
        TFL.Environment.py_shell ()
    c = Convert (cmd, scope)
    #c.dump ()
    c.create ()
    scope.commit ()
    scope.ems.compact ()
    scope.destroy ()
# end def _main

_Command = TFL.CAO.Cmd \
    ( handler         = _main
    , args            =
        ( "file:S?PG database dumpfile to convert"
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
