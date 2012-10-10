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
        { 708 : 707
        , 709 : 707
        , 718 : 860
        , 729 : 728
        , 741 : 740
        , 776 : 301
        , 820 : 359
        , 821 : 359
        , 831 : 836
        , 852 : 851
        , 892 : 706
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
        self.person_by_id = {}
        self.phone_ids    = {}
    # end def __init__

    def set_last_change (self, obj, change_time, create_time) :
        change_time = make_naive (change_time)
        create_time = make_naive (create_time)
        self.scope.ems.convert_creation_change \
            (obj.pid, c_time = create_time, time = change_time or create_time)
        #print obj, obj.creation_date, obj.last_changed
    # end def set_last_change

    def create_nodes (self) :
        for n in self.contents ['nodes'] :
            pass
    # end def create_nodes

    def create_persons (self) :
        for m in sorted (self.contents ['person'], key = lambda x : x.id) :
            #print "%s: %r %r" % (m.id, m.firstname, m.lastname)
            if m.id in self.person_dupes :
                print "INFO: Duplicate person: %s" % m.id
                continue
            if not m.firstname or not m.lastname :
                print >> sys.stderr, "WARN: name missing: %s (%s/%s)" \
                    % (m.id, m.firstname, m.lastname)
                continue
            person = self.pap.Person \
                ( first_name = m.firstname
                , last_name  = m.lastname
                , raw        = True
                )
            self.person_by_id [m.id] = person
            if m.nick :
                self.ffm.Nickname (person, m.nick)
            if m.email :
                email = self.pap.Email (address = m.email)
                self.pap.Person_has_Email (person, email)
            if m.tel :
                p = Phone (m.tel, city = "Graz")
                if p :
                    k = str (p)
                    t = self.pap.Phone.instance (*p)
                    if t :
                        eid = self.phone_ids [k]
                        prs = self.person_by_id [eid]
                        print "WARN: %s/%s %s/%s: Duplicate Phone: %s" \
                            % (eid, prs.pid, m.id, person.pid, m.tel)
                    else :
                        self.phone_ids [k] = m.id
                        phone = self.pap.Phone (*p)
                        self.pap.Person_has_Phone (person, phone)
    # end def create_persons

    def create (self) :
        self.create_persons         ()
        #self.create_nodes           ()
    # end def create

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
