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
import csv
import uuid

from   datetime               import datetime, date, tzinfo, timedelta
from   rsclib.IP_Address      import IP4_Address
from   rsclib.Phone           import Phone
from   rsclib.sqlparser       import make_naive, SQL_Parser
from   _GTW                   import GTW
from   _TFL                   import TFL
from   _FFM                   import FFM
from   _GTW._OMP._PAP         import PAP
from   _MOM.import_MOM        import Q

import _TFL.CAO
import model

class Convert (object) :

        #  54 : 655 # nick == email vorn?
    person_dupes = \
        {  71 :  72
        , 140 : 460
        , 179 : 124
        , 267 : 322
        , 273 : 272 # probably same unnamed person, almost same nick
        , 276 : 272 # yet another dupe with almost same nick
        , 307 : 306
        , 314 : 311
        , 372 : 380 # same phone *and* password (!) different name (!)
        , 424 : 418
        , 440 : 838
        , 617 : 623
        , 669 : 1001 # same person?
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
        , 973 : 544
        }

    person_ignore = dict.fromkeys \
        ((  11
         ,  15
         ,  41
         ,  42
         ,  62
         ,  63
         ,  64
         ,  66
         ,  70
         ,  93
         , 100
         , 106
         , 108
         , 112
         , 118
         , 123
         , 132
         , 136
         , 142
         , 172
         , 174
         , 177
         , 199
         , 209
         , 242
         , 244
         , 245
         , 254
         , 263
         , 266
         , 270
         , 287
         , 313
         , 320
         , 324
         , 338
         , 937
         # Lastname missing:
         ,  34
         ,  69
         , 107
         , 166
         , 168
         , 200
         , 251
         , 260
         , 323
         # Bogus, only initials etc, ignore if no node:
         , 102
         , 103
         , 185
         , 233
         , 299
         , 455
         , 530
         , 845
         , 872
         , 919
         , 955
        ))

    def __init__ (self, cmd, scope, debug = False) :
        self.anonymize = cmd.anonymize
        self.verbose   = cmd.verbose
        self.pers_exception = {}
        try :
            pf = open ('pers.csv', 'r')
            cr = csv.reader (pf, delimiter = ';')
            for line in cr :
                self.pers_exception [int (line [0])] = (line [1], line [2])
        except IOError :
            print "WARN: Can't read additional person data"

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
        self.dev_by_id    = {}
        self.ffm_node     = {}
        self.member_by_id = {}
        self.net_by_id    = {}
        self.nicknames    = {}
        self.nifin_by_id  = {}
        self.ntype_by_id  = {}
        self.node_by_id   = {}
        self.person_by_id = {}
        self.phone_ids    = {}
    # end def __init__

    def create (self) :
        if self.anonymize :
            self.fake_persons ()
        else :
            self.create_persons ()
        self.create_nettypes ()
        self.scope.commit ()
        self.create_nodes   ()
        self.scope.commit ()
        self.create_networks ()
        self.scope.commit ()
        self.create_devices ()
        self.scope.commit ()
        self.create_interfaces ()
        self.scope.commit ()
        self.create_dns_aliases ()
        self.scope.commit ()
    # end def create

    def create_devices (self) :
        # ignore snmp_ip and snmp_lastseen (only used by three nodes)
        dt = self.ffm.Net_Device_Type.instance (name = 'Generic', raw = True)
        for d in sorted (self.contents ['node'], key = lambda x : x.id) :
            if self.verbose :
                print "INFO: Dev: %s Node: %s" % (d.id, d.location_id)
            node = None
            n = self.node_by_id.get (d.location_id)
            if n :
                if d.person_id and d.person_id != n.person_id :
                    print \
                        ( "WARN: Device (node) %s, (loc) %s: "
                          "person mismatch d:%s n:%s"
                        % (d.id, n.id, d.person_id, n.person_id)
                        )
                node = self.ffm_node.get (d.location_id)
                if not node :
                    print "WARN: Node (location) %s for dev (node) %s missing" \
                        % (d.location_id, d.id)
                    continue
            else :
                mgr  = self.person_by_id.get (d.person_id) or self.graz_admin
                node = self.ffm.Node \
                    ( name        = d.name
                    , desc        = 'Auto-created node (id: %s)' % d.location_id
                    , show_in_map = True
                    , manager     = mgr
                    , raw         = True
                    )
                print "WARN: Manufacturing Node (loc: %s) for dev (node) %s" \
                    % (d.location_id, d.id)
            dev = self.ffm.Net_Device \
                ( left = dt
                , node = node
                , name = d.name
                , desc = d.comment
                , raw  = True
                )
            self.set_creation (dev, d.time)
            self.dev_by_id [d.id] = dev
            if len (self.scope.uncommitted_changes) > 10 :
                self.scope.commit ()
    # end def create_devices

    def create_dns_aliases (self) :
        for dal in self.contents ['dnsalias'] :
            if dal.ip_id not in self.nifin_by_id :
                print 'WARN: ignoring dns_alias %s "%s" IP not found %s' \
                    % (dal.id, dal.name, dal.ip_id)
                return
            self.ffm.IP4_DNS_Alias \
                (left = self.nifin_by_id [dal.ip_id], name = dal.name)
            if len (self.scope.uncommitted_changes) > 10 :
                self.scope.commit ()
    # end def create_dns_aliases

    def create_interfaces (self) :
        for iface in self.contents ['ip'] :
            if iface.node_id not in self.dev_by_id :
                print "WARN: Ignoring IP %s %s: no device (node) %s" \
                    % (iface.id, iface.ip, iface.node_id)
                continue
            dev = self.dev_by_id [iface.node_id]
            net = self.net_by_id [iface.net_id]
            ip  = IP4_Address (iface.ip)
            if ip not in net.net_address :
                parent = self.ffm.IP4_Network.query \
                    ( Q.net_address.CONTAINS (ip)
                    , ~ Q.electric
                    , sort_key = TFL.Sorted_By ("-net_address.mask_len")
                    ).first ()
                print "WARN: IP %s %s not in net %s %s found %s" \
                    % ( iface.id
                      , iface.ip
                      , iface.net_id
                      , net.net_address
                      , parent.net_address
                      )
                net = parent
            nw  = net.reserve (ip, owner = dev.node.owner)
            nif = self.ffm.Wired_Interface (left = dev, name = iface.name)
            nii = self.ffm.Net_Interface_in_IP4_Network \
                (nif, nw, mask_len = 32, name = iface.name)
            self.nifin_by_id [iface.id] = nii
            if len (self.scope.uncommitted_changes) > 10 :
                self.scope.commit ()
    # end def create_interfaces

    def create_nettypes (self) :
        """ Network ranges for reservation
        """
        by_mask = {}
        # first group by netmask
        for nw in self.contents ['nettype'] :
            if not nw.comment :
                print 'WARN: Ignoring nettype %s "%s"' % (nw.id, nw.name)
                continue
            for net_ip in nw.comment.split (',') :
                ip = IP4_Address (net_ip)
                if ip.mask not in by_mask :
                    by_mask [ip.mask] = []
                by_mask [ip.mask].append ((ip, nw.name, nw.id))
        typ = self.ffm.IP4_Network
        for mask in sorted (by_mask) :
            for ip, name, id in by_mask [mask] :
                if id not in self.ntype_by_id :
                    self.ntype_by_id [id] = []
                r = typ.query \
                    ( Q.net_address.CONTAINS (ip)
                    , ~ Q.electric
                    , sort_key = TFL.Sorted_By ("-net_address.mask_len")
                    ).first ()
                reserver = r.reserve if r else typ
                network  = reserver (ip, owner = self.graz_admin)
                self.ntype_by_id [id].append (network)
                if name :
                    network.set_raw (desc = name)
    # end def create_nettypes

    def create_networks (self) :
        for net in self.contents ['net'] :
            parents = self.ntype_by_id.get (net.nettype_id, [])
            node    = self.ffm_node.get (net.location_id)
            ip      = IP4_Address (net.netip, net.netmask)
            if node :
                owner = node.owner
            else :
                print "WARN: Network %s %s Location %s missing" \
                    % (net.id, net.netip, net.location_id)
                owner = self.graz_admin
            parent = None
            for p in parents :
                if ip in p.net_address :
                    parent = p
                    break
            else :
                parent = None
                for ps in self.ntype_by_id.itervalues () :
                    for p in ps :
                        if ip in p.net_address :
                            parent = p
                            print "Got parent in ntype_by_id: %s" % parent
                            break
                else :
                    parent = self.ffm.IP4_Network.query \
                        ( Q.net_address.CONTAINS (ip)
                        , ~ Q.electric
                        , sort_key = TFL.Sorted_By ("-net_address.mask_len")
                        ).first ()
                    if parent :
                        print "Got parent by network query: %s" % parent
            if parent :
                reserver = parent.reserve
            else :
                print "WARN: No parent: new network: %s" % ip
                reserver = self.ffm.IP4_Network
            network = reserver (ip, owner = owner)
            self.net_by_id [net.id] = network
            if node :
                pool = self.ffm.IP4_Pool (left = network, node = node)
            if net.comment :
                network.set_raw (desc = net.comment)
            if len (self.scope.uncommitted_changes) > 10 :
                self.scope.commit ()
    # end def create_networks

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
            if person_id != 0 and person_id not in self.person_by_id :
                # should not happen now
                print "WARN: Location %s owner %s missing" % (n.id, person_id)
                continue
            if person_id == 0 :
                person = self.graz_admin
            else :
                person = self.person_by_id [person_id]
            lat = lon = None
            if n.pixel_x is not None and n.pixel_y is not None :
                lon = "%f" % (x_lon + (n.pixel_x - x_start) / dx_lon)
                lat = "%f" % (y_lat + (n.pixel_y - y_start) / dy_lat)

            node = self.ffm.Node \
                ( name        = n.name
                , desc        = n.comment.strip () or None
                , show_in_map = not n.hidden
                , manager     = person
                , position    = dict (lat = lat, lon = lon)
                , raw         = True
                )
            self.ffm_node [n.id] = node
            self.set_creation (node, n.time)
            if n.street :
                s = ' '.join (x for x in (n.street, n.streetnr) if x)
                adr = self.pap.Address.instance_or_new \
                    ( street = s
                    , zip    = '8010'
                    , city   = 'Graz'
                    , country = 'Austria'
                    )
                node.set (address = adr)
            if n.gallery_link :
                MOM = self.scope.MOM
                abs = 'http://gallery.funkfeuer.at/v/Graz/Knoten/%s/'
                if n.gallery_link.startswith ('http') :
                    abs = "%s"
                url = MOM.Document \
                    (node, url = abs % n.gallery_link, type = 'Gallery')
            if len (self.scope.uncommitted_changes) > 10 :
                self.scope.commit ()
    # end def create_nodes

    def fake_persons (self) :
        self.graz_admin = self.pap.Person \
            ( first_name = 'Graz'
            , last_name  = 'Admin'
            , raw        = True
            )
        mail  = 'admin@graz.funkfeuer.at'
        email = self.pap.Email (address = mail)
        self.pap.Person_has_Email (self.graz_admin, email)
        auth = self.scope.Auth.Account.create_new_account_x \
            ( mail
            , enabled   = True
            , suspended = True
            , password  = uuid.uuid4 ().hex
            )
        self.pap.Person_has_Account (self.graz_admin, auth)
        for m in sorted (self.contents ['person'], key = lambda x : x.id) :
            self.person_by_id [m.id] = self.graz_admin
    # end def fake_persons

    def create_persons (self) :
        for m in sorted (self.contents ['person'], key = lambda x : x.id) :
            #print "%s: %r %r" % (m.id, m.firstname, m.lastname)
            if m.id in self.person_ignore :
                print "INFO: Ignoring anonymous without location: %s" % m.id
                continue
            if m.id in self.pers_exception :
                pe = self.pers_exception [m.id]
                fn, ln = (x.decode ('utf-8') for x in pe)
            else :
                fn = m.firstname.strip ()
                ln = m.lastname.strip ()
            self.member_by_id [m.id] = m
            if m.id in self.person_dupes :
                print "INFO: Duplicate person: %s" % m.id
                continue
            if not fn or not ln :
                print >> sys.stderr, "WARN: name missing: %s (%r/%r)" \
                    % (m.id, m.firstname, m.lastname)
                if not fn and not ln :
                    if m.nick :
                        fn = m.nick
                    else :
                        fn = m.email.split ('@') [0]
                fn = fn or '?'
                ln = ln or '?'
            print "Person: %s %r/%r" % (m.id, fn, ln)
            person = self.pap.Person \
                ( first_name = fn
                , last_name  = ln
                , raw        = True
                )
            self.person_by_id [m.id] = person
            if m.nick :
                self.try_insert_nick (m.nick, m.id, person)
            if m.email :
                mail  = m.email.replace ('[at]', '@')
                email = self.pap.Email (address = mail)
                self.pap.Person_has_Email (person, email)
                if m.email == 'admin@graz.funkfeuer.at' :
                    self.graz_admin = person
                auth = self.scope.Auth.Account.create_new_account_x \
                    ( mail
                    , enabled   = True
                    , suspended = True
                    , password  = uuid.uuid4 ().hex
                    )
                self.pap.Person_has_Account (person, auth)
            if m.tel :
                self.try_insert_phone (m.tel, m.id, person)
            if len (self.scope.uncommitted_changes) > 10 :
                self.scope.commit ()
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
            if len (self.scope.uncommitted_changes) > 10 :
                self.scope.commit ()
    # end def create_persons

    def set_creation (self, obj, create_time) :
        if not create_time :
            return
        if not isinstance (create_time, datetime) :
            create_time = datetime (* create_time.timetuple () [:3])
        create_time = make_naive (create_time)
        self.scope.ems.convert_creation_change (obj.pid, c_time = create_time)
    # end def set_creation

    def try_insert_phone (self, tel, id, person) :
        if tel.startswith ('+430659') :
            tel = '+43650' + tel [6:]
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
        , "anonymize:B"
        , "create:B"
        ) + model.opts
    , min_args        = 1
    , defaults        = model.command.defaults
    )

if __name__ == "__main__" :
    _Command ()
### __END__ cnml_import
