#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

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
        self.modes        = dict \
            ( client      = self.ffm.Client_Mode
            , ap          = self.ffm.AP_Mode
            , ad_hoc      = self.ffm.Ad_Hoc_Mode
            )
        self.networks     = {}

        self.parser       = SQL_Parser (verbose = False, fix_double_encode = 1)
        self.parser.parse (f)
        self.contents     = self.parser.contents
        self.tables       = self.parser.tables
        self.dupes_by_id  = {}
        self.person_by_id = {}
        self.nicknames    = {}
        self.phone_ids    = {}
    # end def __init__

    def create (self) :
        self.create_persons ()
        self.create_nodes   ()
    # end def create

    def create_nodes (self) :
        for n in self.contents ['location'] :
            person_id = self.person_dupes.get (n.person_id, n.person_id)
            if person_id not in self.person_by_id :
                print "WARN: Location %s owner %s missing" % (n.id, person_id)
                continue
            person = self.person_by_id [person_id]
            node = self.ffm.Node \
                ( name        = n.name
                , show_in_map = not n.hidden
                , manager     = person
                , raw         = True
                )
            if n.gps_lon :
                print n.gps_lon
            if n.gps_lat :
                print n.gps_lat
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
            if m.id in self.person_dupes :
                print "INFO: Duplicate person: %s" % m.id
                self.dupes_by_id [m.id] = m
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
            if m_id not in self.person_by_id :
                continue
            d = self.dupes_by_id [d_id]
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
