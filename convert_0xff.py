#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
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
import uuid
import pickle

from   datetime               import datetime, tzinfo, timedelta
from   rsclib.IP_Address      import IP4_Address
from   rsclib.Phone           import Phone
from   rsclib.sqlparser       import make_naive, SQL_Parser
from   _GTW                   import GTW
from   _TFL                   import TFL
from   _TFL                   import pyk
from   _FFM                   import FFM
from   _GTW._OMP._PAP         import PAP
from   _GTW._OMP._Auth        import Auth
from   olsr.parser            import get_olsr_container
from   spider.parser          import Guess
from   spider.common          import unroutable, Interface, Inet4

import _TFL.CAO
import model

class Convert (object) :

    def __init__ (self, cmd, scope, debug = False) :
        self.debug   = debug
        self.verbose = cmd.verbose
        if len (cmd.argv) > 0 :
            f  = open (cmd.argv [0])
        else :
            f = sys.stdin
        olsr = get_olsr_container (cmd.olsr_file)
        self.olsr_nodes   = {}
        for t in olsr.topo.forward.iterkeys () :
            self.olsr_nodes [t]   = True
        for t in olsr.topo.reverse.iterkeys () :
            self.olsr_nodes [t]   = True
        self.olsr_mid     = olsr.mid.by_ip
        self.olsr_hna     = olsr.hna
        self.rev_mid      = {}
        for k, v in self.olsr_mid.iteritems () :
            if k not in self.olsr_nodes :
                pyk.fprint ("WARN: MIB %s: not in OLSR Topology" % k)
            #assert k in self.olsr_nodes
            for mid in v :
                assert mid not in self.rev_mid
                self.rev_mid [mid] = True
        self.spider_info  = pickle.load (open (cmd.spider_dump, 'rb'))
        self.spider_devs  = {}
        self.spider_iface = {}
        for ip, dev in self.spider_info.iteritems () :
            if self.verbose :
                pyk.fprint ("IP:", ip)
            # ignore spider errors
            if not isinstance (dev, Guess) :
                continue
            for iface in dev.interfaces.itervalues () :
                for ip4 in iface.inet4 :
                    i4 = ip4.ip
                    # ignore rfc1918, link local, localnet
                    if unroutable (i4) :
                        continue
                    if  (   i4 in self.spider_devs
                        and self.spider_devs [i4] != dev
                        ) :
                        pyk.fprint ("WARN: Device %s/%s not equal:" % (ip, i4))
                        pyk.fprint ("=" * 60)
                        pyk.fprint (dev.verbose_repr ())
                        pyk.fprint ("-" * 60)
                        pyk.fprint (self.spider_devs [i4].verbose_repr ())
                        pyk.fprint ("=" * 60)
                    elif (   i4 in self.spider_iface
                         and self.spider_iface [i4] != iface
                         ) :
                        assert dev == self.spider_devs [i4]
                        spif = self.spider_iface [i4]
                        pyk.fprint \
                            ( "WARN: Interfaces %s/%s of dev-ip %s share ip %s"
                            % (iface.name, spif.name, ip, i4)
                            )
                        spif.names.append (iface.name)
                        if iface.is_wlan :
                            spif.is_wlan = iface.is_wlan
                            spif.wlan_info = getattr (iface, 'wlan_info', None)
                        if self.verbose :
                            pyk.fprint ("=" * 60)
                            pyk.fprint (iface)
                            pyk.fprint (spif)
                            pyk.fprint ("-" * 60)
                            pyk.fprint (dev.verbose_repr ())
                            pyk.fprint ("=" * 60)
                        iface = spif
                    self.spider_devs  [i4] = dev
                    self.spider_iface [i4] = iface
                    iface.device = dev
            if ip not in self.spider_devs :
                pyk.fprint ("WARN: ip %s not in dev" % ip)
                if self.verbose :
                    pyk.fprint ("=" * 60)
                    pyk.fprint (dev.verbose_repr ())
                    pyk.fprint ("=" * 60)
                name = 'unknown'
                assert name not in dev.interfaces
                iface = Interface (4711, name)
                dev.interfaces [name] = iface
                iface.append_inet4 (Inet4 (ip, None, None, iface = name))

        self.scope        = scope
        self.ffm          = self.scope.FFM
        self.pap          = self.scope.GTW.OMP.PAP
        self.mentor       = {}
        self.networks     = {}
        self.rsrvd_nets   = {}
        self.net_dupes    = {}
        self.node_by_id   = {}
        self.ip_by_ip     = {}
        self.dev_by_id    = {}
        self.email_ids    = {}
        self.phone_ids    = {}
        self.person_by_id = {}
        self.member_by_id = {}
        self.ip_by_dev    = {}
        self.dev_by_node  = {}

        self.parser       = SQL_Parser \
            (verbose = False, fix_double_encode = True)
        self.parser.parse (f)
        self.contents     = self.parser.contents
        self.tables       = self.parser.tables
    # end def __init__

    def set_last_change (self, obj, change_time, create_time) :
        change_time = make_naive (change_time)
        create_time = make_naive (create_time)
        self.scope.ems.convert_creation_change \
            (obj.pid, c_time = create_time, time = change_time or create_time)
        #pyk.fprint (obj, obj.creation_date, obj.last_changed)
    # end def set_last_change

    def create_nodes (self) :
        for n in self.contents ['nodes'] :
            gps = None
            if n.gps_lat_deg is None :
                assert n.gps_lat_min is None
                assert n.gps_lat_sec is None
                assert n.gps_lon_deg is None
                assert n.gps_lon_min is None
                assert n.gps_lon_sec is None
            elif n.gps_lat_min is None :
                assert n.gps_lat_sec is None
                assert n.gps_lon_min is None
                assert n.gps_lon_sec is None
                lat = "%f" % n.gps_lat_deg
                lon = "%f" % n.gps_lon_deg
                gps = dict (lat = lat, lon = lon)
            else :
                assert n.gps_lat_deg == int (n.gps_lat_deg)
                assert n.gps_lat_min == int (n.gps_lat_min)
                assert n.gps_lon_deg == int (n.gps_lon_deg)
                assert n.gps_lon_min == int (n.gps_lon_min)
                lat = "%d d %d m" % (int (n.gps_lat_deg), int (n.gps_lat_min))
                lon = "%d d %d m" % (int (n.gps_lon_deg), int (n.gps_lon_min))
                if n.gps_lat_sec is not None :
                    lat = lat + " %f s" % n.gps_lat_sec
                if n.gps_lon_sec is not None :
                    lon = lon + " %f s" % n.gps_lon_sec
                gps = dict (lat = lat, lon = lon)
            id = self.person_dupes.get (n.id_members, n.id_members)
            person = self.person_by_id.get (id)
            if n.id_tech_c and n.id_tech_c != n.id_members :
                manager = self.person_by_id.get (n.id_tech_c)
                assert (manager)
                pyk.fprint ("INFO: Tech contact found: %s" % n.id_tech_c)
            else :
                manager = person
                person  = None
            # node with missing manager has devices, use 0xff admin as owner
            if not manager and n.id in self.dev_by_node :
                manager = self.person_by_id.get (1)
                pyk.fprint \
                    ( "WARN: Node %s: member %s not found, using 1"
                    % (n.id, n.id_members)
                    )
            if manager :
                node = self.ffm.Node \
                    ( name        = n.name
                    , position    = gps
                    , show_in_map = n.map
                    , manager     = manager
                    , owner       = person
                    , raw         = True
                    )
                self.set_last_change (node, n.changed, n.created)
                assert (node)
                self.node_by_id [n.id] = node
            else :
                pyk.fprint \
                    ( "ERR:  Node %s: member %s not found"
                    % (n.id, n.id_members)
                    )
    # end def create_nodes

    # first id is the one to remove, the second one is the correct one
    person_dupes = dict (( (373, 551) # checked, real dupe
                         , (338, 109) # checked, real dupe
                         , (189, 281) # checked, 189 contains almost no data
                                      # and 189 has no nodes
                         , (285, 284) # checked, real dupe
                         , (299, 297) # checked, real dupe
                         , (300, 462) # checked, real dupe
                         , (542, 586) # checked, real dupe
                         , (251, 344) # checked, real dupe
                         , (188, 614) # checked, real dupe
                         , (177, 421) # checked, real dupe
                         , (432, 433) # checked, real dupe, merge addresses
                         , ( 26, 480) # probably: almost same nick, merge adrs
                         , ( 90, 499) # FIXME: same person? merge adrs?
                                      #  90 has node 1110
                                      # 499 has node 1105 and 812
                                      # two accounts, one for HTL, one private?
                                      # maybe create company?
                                      # make company owner of 1110 and
                                      # 499 tech-c of all nodes?
                         , (505, 507) # checked, real dupe
                         , (410, 547) # checked, real dupe
                         , (712, 680) # checked, real dupe
                         , (230, 729) # checked, real dupe
                         , (375, 743) # checked, real dupe
                         , (755, 175) # checked, real dupe
                         , (219, 759) # Probably same (nick similar), merge adr
                         , (453, 454) # checked, real dupe
                         , (803, 804) # checked, real dupe
                         , (295, 556) # same gmx address, merge adr
                         , (697, 814) # checked, real dupe
                         , (476, 854) # checked, real dupe
                         , (312, 307) # checked, real dupe
                         , (351, 355) # checked, real dupe
                         , (401, 309) # checked, real dupe
                         , (871, 870) # checked, real dupe
                         , (580, 898) # checked, real dupe
                         , (894, 896) # checked, real dupe
                         , (910, 766) # checked, real dupe
                         , (926, 927) # checked, real dupe
                         , (938, 939) # checked, real dupe
                         , (584, 939) # not entirely sure but all
                                      # lowercase in both records
                                      # indicates same person
                         , (  0,   1) # ignore Funkfeuer Parkplatz
                        ))
    rev_person_dupes = dict ((v, k) for k, v in person_dupes.iteritems ())

    merge_adr = dict.fromkeys ((432, 26, 759, 295))

    phone_bogus   = dict.fromkeys \
        (( '01111111'
        ,  '1234567'
        ,  '0048334961656'
        ,  '001123456789'
        ,  '+972 1234567'
        ,  '003468110524227'
        ,  '1234'
        ,  '0'
        ,  '-'
        ,  '+49 1 35738755'
        ,  '974 5517 9729'
        ,  '0525001340'
        ,  '59780'
        ,  '1013'
        ))

    def try_insert_phone (self, person, m, x, c) :
        if x :
            p = None
            if x in self.phone_bogus :
                return
            try :
                p = Phone (x, m.town, c)
            except ValueError, err :
                if str (err).startswith ('WARN') :
                    pyk.fprint (err)
                    return
            if not p :
                return
            t = self.pap.Phone.instance (* p)
            k = str (p)
            if t :
                eid = self.phone_ids [k]
                prs = self.person_by_id [eid]
                if  (  prs.pid == person.pid
                    or self.pap.Person_has_Phone.instance (person, t)
                    ) :
                    return # don't insert twice
                pyk.fprint \
                    ( "WARN: %s/%s %s/%s: Duplicate phone: %s"
                    % (eid, prs.pid, m.id, person.pid, x)
                    )
            else :
                t = self.pap.Phone (* p)
                self.phone_ids [k] = m.id
            self.pap.Person_has_Phone (person, t)
    # end def try_insert_phone

    def try_insert_email (self, person, m, attr = 'email', second = False) :
        mail  = getattr (m, attr)
        email = self.pap.Email.instance (address = mail)
        if email :
            if mail.lower () in (e.address for e in person.emails) :
                return
            eid = self.email_ids [mail.lower ()]
            prs = self.person_by_id [eid]
            pyk.fprint \
                ( "WARN: %s/%s %s/%s: Duplicate email: %s"
                % (eid, prs.pid, m.id, person.pid, mail)
                )
        else :
            desc = None
            if second :
                desc = "von 2. Account"
                pyk.fprint \
                    ( "INFO: Second email for %s/%s: %s"
                    % (m.id, person.pid, mail)
                    )
            self.email_ids [mail.lower ()] = m.id
            email = self.pap.Email (address = mail, desc = desc)
            self.pap.Person_has_Email (person, email)
            auth  = self.scope.Auth.Account.create_new_account_x \
                ( mail
                , enabled   = True
                , suspended = True
                , password  = uuid.uuid4 ().hex
                )
            self.pap.Person_has_Account (person, auth)
    # end def try_insert_email

    def try_insert_url (self, m, person) :
        hp = m.homepage
        if not hp.startswith ('http') :
            hp = 'http://' + hp
        url = self.pap.Url.instance (hp, raw = True)
        assert url is None or url.value == hp.lower ()
        if url :
            return
        url = self.pap.Url (hp, desc = 'Homepage', raw = True)
        self.pap.Person_has_Url (person, url)
    # end def try_insert_url

    def try_insert_im (self, m, person) :
        pyk.fprint \
            ("INFO: Instant messenger nickname: %s" % m.instant_messenger_nick)
        im = self.pap.IM_Handle (address = m.instant_messenger_nick)
        self.pap.Person_has_IM_Handle (person, im)
    # end def try_insert_im

    phone_types = dict \
        ( telephone   = 'Festnetz'
        , mobilephone = 'Mobil'
        , fax         = 'Fax'
        )

    def try_insert_address (self, m, person) :
        street  = ' '.join (x for x in (m.street, m.housenumber) if x)
        if street or m.town or m.zip :
            country = 'Austria'.decode ('latin1')
            if not m.town :
                pyk.fprint \
                    ( 'INFO: no city (setting to "Wien"): %s/%s'
                    % (m.id, person.pid)
                    )
                m ['town'] = 'Wien'
            if not m.zip :
                if m.id == 653 :
                    m ['zip'] = 'USA'
                elif m.id == 787 :
                    m ['zip'] = '2351'
                elif m.id == 836 :
                    m ['zip'] = '1160'
                else :
                    pyk.fprint ("INFO: no zip: %s/%s" % (m.id, person.pid))
            elif m.zip.startswith ('I-') :
                m ['zip'] = m.zip [2:]
                country = 'Italy'.decode ('latin1')
            address = self.pap.Address.instance_or_new \
                ( street     = street
                , zip        = m.zip
                , city       = m.town
                , country    = country
                )
            self.pap.Person_has_Address (person, address)
    # end def try_insert_address

    def create_persons (self) :
        for m in sorted (self.contents ['members'], key = lambda x : x.id) :
            self.member_by_id [m.id] = m
            if m.id == 309 and m.street.startswith ("'") :
                m.street = m.street [1:]
            if m.id in self.person_dupes :
                pyk.fprint \
                    ( "INFO: skipping person %s (duplicate of %s)"
                    % (m.id, self.person_dupes [m.id])
                    )
                continue
            if not m.firstname and not m.lastname :
                pyk.fprint ("WARN: skipping person, no name:", m.id)
                continue
            if not m.lastname :
                pyk.fprint ("WARN: skipping person, no lastname: %s" % m.id)
                continue
            if self.verbose :
                pyk.fprint \
                    ("Creating person:", repr (m.lastname), repr (m.firstname))
            person = self.pap.Person \
                ( first_name = m.firstname
                , last_name  = m.lastname
                , raw        = True
                )
            if m.id not in self.rev_person_dupes :
                self.set_last_change (person, m.changed, m.created)
            self.person_by_id [m.id] = person
            self.try_insert_address (m, person)
            if m.email :
                self.try_insert_email (person, m)
            if m.fax and '@' in m.fax :
                self.try_insert_email (person, m, attr = 'fax')
                pyk.fprint \
                    ("INFO: Using email %s in fax field as email" % m.fax)
            if m.instant_messenger_nick :
                self.try_insert_im (m, person)
            for a, c in self.phone_types.iteritems () :
                x = getattr (m, a)
                self.try_insert_phone (person, m, x, c)
            if m.mentor_id and m.mentor_id != m.id :
                self.mentor [m.id] = m.mentor_id
            if m.nickname :
                nick = self.pap.Nickname (m.nickname, raw = True)
                self.pap.Person_has_Nickname (person, nick)
            if m.homepage :
                self.try_insert_url (m, person)
        for mentor_id, person_id in self.mentor.iteritems () :
            mentor = self.person_by_id [mentor_id]
            person = self.person_by_id [person_id]
            self.ffm.Person_mentors_Person (mentor, person)
        # Retrieve info from dupe account
        for dupe, id in self.person_dupes.iteritems () :
            # older version of db or dupe removed:
            if id not in self.person_by_id :
                continue
            d = self.member_by_id [dupe]
            m = self.member_by_id [id]
            person = self.person_by_id [id]
            changed = max \
                (d for d in (m.changed, d.changed, m.created, d.created) if d)
            created = min (m.created, d.created)
            self.set_last_change (person, changed, created)
            if d.email :
                self.try_insert_email (person, d, second = True)
            for a, c in self.phone_types.iteritems () :
                x = getattr (d, a)
                self.try_insert_phone (person, d, x, c)
            if  (   d.mentor_id is not None
                and d.mentor_id != d.id
                and d.mentor_id != id
                ) :
                assert (False)
            if d.nickname :
                nick = self.pap.Nickname (d.nickname, raw = True)
                self.pap.Person_has_Nickname (person, nick)
            if d.homepage :
                self.try_insert_url (d, person)
            if d.instant_messenger_nick :
                self.try_insert_im (d, person)
            if dupe in self.merge_adr :
                self.try_insert_address (d, person)
    # end def create_persons

    def create_device (self, d) :
        if self.debug :
            pyk.fprint ('dev:', d.id, d.name)
        node = self.node_by_id [d.id_nodes]
        # FIXME: We want correct info from nodes directly
        # looks like most firmware can give us this info
        devtype = self.ffm.Net_Device_Type.instance (name = 'Generic')
        comments = dict \
            ( hardware = 'Hardware'
            , antenna  = 'Antenne'
            , comment  = 'Kommentar'
            )
        desc = '\n'.join \
            (': '.join ((v, d [k])) for k, v in comments.iteritems () if d [k])
        dev = self.ffm.Net_Device \
            ( left = devtype
            , node = node
            , name = d.name
            , desc = desc
            , raw  = True
            )
        self.set_last_change (dev, d.changed, d.created)
        # no member info in DB:
        assert not d.id_members
        return dev
    # end def create_device

    def create_interface (self, dev, name, ip) :
        Adr = self.ffm.IP4_Network.net_address.P_Type
        # FIXME: Need info on wireless vs wired Net_Interface
        iface = self.ffm.Wired_Interface (left = dev, name = name, raw = True)
        net = IP4_Address (ip.ip, ip.cidr)
        net = self.net_dupes.get (net, net)
        network = self.ffm.IP4_Network.instance \
            (dict (address = str (net)), raw = True)
        manager = dev.node.manager
        netadr  = network.reserve (Adr (ip.ip, raw = True), manager)
        self.ffm.Net_Interface_in_IP4_Network \
            (iface, netadr, mask_len = 32)
    # end def create_interface

    def create_interfaces_for_dev (self, dev, d, ip) :
        ips = self.ip_by_dev [d.id]
        l = len (ips)
        if l > 1 :
            pyk.fprint \
                ( "WARN: dev %s.%s has %d ips: %s" \
                % (dev.node.name, d.name, l, ', '.join (i.ip for i in ips))
                )
            for n, dev_ip in enumerate (ips) :
                name = "%s-%d" % (d.name, n)
                self.create_interface (dev, name, dev_ip)
                dev_ip.set_done ()
        else :
            self.create_interface (dev, d.name, ip)
            ip.set_done ()
        assert ip.done
    # end def create_interfaces_for_dev

    def create_ips_and_devices (self) :
        # compound devices from mid table
        for ip4, aliases in self.olsr_mid.iteritems () :
            nodes = {}
            ip    = self.ip_by_ip [ip4]
            if ip.id_devices :
                d = self.dev_by_id [ip.id_devices]
                nodes [d.id_nodes] = ({ ip.id_devices : d }, { ip.id : ip })
            else :
                pyk.fprint ("ERR:  key %s from mid has no device" % ip4)
            for a in aliases :
                ip = self.ip_by_ip [a]
                if not ip.id_devices :
                    pyk.fprint ("ERR:  %s from mid %s has no device" % (a, ip4))
                    continue
                d  = self.dev_by_id [ip.id_devices]
                if d.id_nodes not in nodes :
                    nodes [d.id_nodes] = ({}, {})
                nodes [d.id_nodes] [0] [ip.id_devices] = d
                nodes [d.id_nodes] [1] [ip.id] = ip
            if len (nodes) > 1 :
                pyk.fprint \
                    ("WARN: mid %s expands to %s nodes" % (ip4, len (nodes)))
            # all devices from same node (!), get dev with shortest name
            for n, (devs, ips) in nodes.iteritems () :
                nd = None
                for d in devs.itervalues () :
                    assert not d.done
                    if nd is None or len (nd.name) > len (d.name) :
                        nd = d
                    # get remaining ips not active in olsr
                    for ip in self.ip_by_dev [d.id] :
                        ips [ip.id] = ip
                    d.set_done ()
                dev = self.create_device (nd)
                for ip in ips.itervalues () :
                    if ip.done :
                        continue
                    d   = devs [ip.id_devices]
                    self.create_interfaces_for_dev (dev, d, ip)

        # devices and reserved nets from hna table
        for ip4 in self.olsr_hna.by_dest.iterkeys () :
            for n in self.networks.iterkeys () :
                if ip4 in n :
                    break
            else :
                # only subnets of one of our networks
                continue
            if ip4.mask == 32 :
                if ip4 not in self.olsr_nodes :
                    ip = self.ip_by_ip [ip4]
                    if ip.done :
                        continue
                    if ip.id_devices :
                        d = self.dev_by_id [ip.id_devices]
                        dev = self.create_device (d)
                        self.create_interface (dev, d.name, ip)
                        ip.set_done ()
                        for i in self.ip_by_dev [d.id] :
                            if not i.done :
                                break
                        else :
                            d.set_done ()
                    else :
                        # FIXME: Reserve network in database
                        self.rsrvd_nets [ip4] = True
            else :
                # FIXME: Reserve network in database
                self.rsrvd_nets [ip4] = True
                for i in ip4 :
                    assert i not in self.olsr_nodes
                for i in ip4 :
                    assert i not in self.rev_mid
        if self.debug :
            for ip4 in self.olsr_hna.by_dest :
                for nw in self.networks.iterkeys () :
                    if ip4 in nw :
                        pyk.fprint ("HNA: %s" % ip4)

        # remaining ips
        for ip in self.contents ['ips'] :
            if ip.done :
                continue
            ip4 = IP4_Address (ip.ip)
            assert not ip.id_nodes
            assert not ip.id_members or ip.id_members == 1
            if not ip.id_devices :
                # FIXME: Do we need a "free-pool"?
                continue
            # Ignore IPs that belong to some device
            if ip4 in self.rev_mid :
                assert (0) # already covered above, should be marked done
                continue
            d = self.dev_by_id [ip.id_devices]
            dev = self.create_device (d)
            self.create_interfaces_for_dev (dev, d, ip)
    # end def create_ips_and_devices

    def build_device_structure (self) :
        for ip in self.contents ['ips'] :
            self.ip_by_ip [IP4_Address (ip.ip)] = ip
            if ip.id_devices :
                if ip.id_devices not in self.ip_by_dev :
                    self.ip_by_dev [ip.id_devices] = []
                self.ip_by_dev [ip.id_devices].append (ip)
            net = IP4_Address (ip.ip, ip.cidr)
            self.networks [net] = True
        self.net_dupes = {}
        for net in self.networks.iterkeys () :
            for net2 in self.networks.iterkeys () :
                if net != net2 :
                    if net in net2 :
                        self.net_dupes [net]  = net2
                    if net2 in net :
                        self.net_dupes [net2] = net
        for net in self.net_dupes :
            del self.networks [net]
        for net in self.networks :
            network = self.ffm.IP4_Network.instance_or_new \
                (dict (address = str (net)), raw = True)
        for d in self.contents ['devices'] :
            if d.id_nodes not in self.dev_by_node :
                self.dev_by_node [d.id_nodes] = []
            self.dev_by_node [d.id_nodes].append (d)
            self.dev_by_id [d.id] = d
        # consistency check of olsr data against redeemer db
        # check nodes from topology
        for ip4 in self.olsr_nodes :
            if ip4 not in self.ip_by_ip :
                pyk.fprint ("WARN: ip %s from olsr topo not in ips" % ip4)
                del self.olsr_nodes [ip4]
        # check mid table
        midkey = []
        midtbl = {}
        for ip4, aliases in self.olsr_mid.iteritems () :
            if ip4 not in self.ip_by_ip :
                pyk.fprint ("WARN: key ip %s from olsr mid not in ips" % ip4)
                midkey.append (ip4)
            for a in aliases :
                if a not in self.ip_by_ip :
                    pyk.fprint ("WARN: ip %s from olsr mid not in ips" % a)
                    if ip4 not in midtbl :
                        midtbl [ip4] = []
                    midtbl [ip4].append (a)
        assert not midkey
        for k, v in midtbl.iteritems () :
            x = dict.fromkeys (self.olsr_mid [k])
            for ip4 in v :
                del x [ip4]
            self.olsr_mid [k] = x.keys ()
    # end def build_device_structure

    def debug_output (self) :
        for k in sorted (self.olsr_nodes.iterkeys ()) :
            pyk.fprint (k)
        for node in self.contents ['nodes'] :
            pyk.fprint ("Node: %s (%s)" % (node.name.encode ('latin1'), node.id))
            for d in self.dev_by_node.get (node.id, []) :
                pyk.fprint ("    Device: %s" % d.name)
                ips = self.ip_by_dev.get (d.id, [])
                ips.sort ()
                for ip in ips :
                    x = ''
                    if IP4_Address (ip.ip) in self.olsr_nodes :
                        x = ' USED'
                    pyk.fprint ("        IP: %s/%s%s" % (ip.ip, ip.cidr, x))
                l = len (ips)
                if not l :
                    pyk.fprint ("    No IPs!!")
                for ip in ips :
                    adr = IP4_Address (ip.ip)
                    if adr in self.olsr_mid :
                        ips1 = [x.ip for x in ips]
                        ips2 = []
                        ips2.extend (str (x) for x in self.olsr_mid [adr])
                        ips2.append (ip.ip)
                        ips2.sort ()
                        if ips1 != ips2 :
                            pyk.fprint ("        Ooops: %s/%s" % (ips1, ips2))
                        break
                else :
                    if l > 1 :
                        pyk.fprint ("        Not found in olsr_mid!")
    # end def debug_output

    def create (self) :
        self.build_device_structure ()
        if self.debug :
            self.debug_output       ()
        self.create_persons         ()
        self.create_nodes           ()
        self.create_ips_and_devices ()
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
        , "olsr_file:S=olsr/txtinfo.txt?OLSR dump-file to convert"
        , "spider_dump:S=Funkfeuer.dump?Spider pickle dump"
        ) + model.opts
    , min_args        = 1
    , defaults        = model.command.defaults
    )

if __name__ == "__main__" :
    _Command ()
### __END__ cnml_import
