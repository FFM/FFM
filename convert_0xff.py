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
from   olsr.parser            import OLSR_Parser

import _TFL.CAO
import model

class Convert (object) :

    def __init__ (self, cmd, scope, debug = False) :
        self.debug = debug
        if len (cmd.argv) > 0 :
            f  = open (cmd.argv [0])
        else :
            f = sys.stdin
        olsr_parser       = OLSR_Parser ()
        olsr_parser.parse (open (cmd.olsr_file))
        self.olsr_nodes   = {}
        for t in olsr_parser.topo.forward.iterkeys () :
            self.olsr_nodes [t]   = True
        for t in olsr_parser.topo.reverse.iterkeys () :
            self.olsr_nodes [t]   = True
        self.olsr_mid     = olsr_parser.mid.by_ip
        self.olsr_hna     = olsr_parser.hna
        self.rev_mid      = {}
        for k, v in self.olsr_mid.iteritems () :
            assert k in self.olsr_nodes
            for mid in v :
                assert mid not in self.rev_mid
                self.rev_mid [mid] = True
        self.scope        = scope
        self.ffm          = self.scope.FFM
        self.pap          = self.scope.GTW.OMP.PAP
        self.mentor       = {}
        self.modes        = dict \
            ( client      = self.ffm.Client_Mode
            , ap          = self.ffm.AP_Mode
            , ad_hoc      = self.ffm.Ad_Hoc_Mode
            )
        self.networks     = {}
        self.rsrvd_nets   = {}
        self.net_dupes    = {}
        self.node_by_id   = {}
        self.ip_by_ip     = {}
        self.dev_by_id    = {}
        self.email_ids    = {}
        self.phone_ids    = {}
        self.person_by_id = {}
        self.dupes_by_id  = {}
        self.ip_by_dev    = {}
        self.dev_by_node  = {}

        self.parser       = SQL_Parser (verbose = False)
        self.parser.parse (f)
        self.contents     = self.parser.contents
        self.tables       = self.parser.tables
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
                print "INFO: Tech contact found: %s" % n.id_tech_c
            else :
                manager = person
                person  = None
            # node with missing manager has devices, use 0xff admin as owner
            if not manager and n.id in self.dev_by_node :
                manager = self.person_by_id.get (1)
                print "WARN: Node %s: member %s not found, using 1" \
                    % (n.id, n.id_members)
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
                print "ERR:  Node %s: member %s not found" \
                    % (n.id, n.id_members)
    # end def create_nodes

    # first id is the one to remove, the second one is the correct one
    # FIXME: we may need to merge some attributes from one entry to the other
    # FIXME: We want to set the creation date to minimum of both records
    # FIXME: We want to set the last modified to the maximum of both records
    # FIXME: Check used resources of dupe
    # FIXME: 189/281 is unclear if same person (only identifyable
    #        attribute is email which differs)
    person_dupes = dict (( (373, 551)
                         , (338, 109)
                         , (189, 281)
                         , (285, 284)
                         , (299, 297)
                         , (300, 462)
                         , (542, 586)
                         , (251, 344)
                         , (188, 614)
                         , (177, 421)
                         , (432, 433) # merge addresses ??
                         , ( 26, 480) # same person? merge adrs + email?
                         , ( 90, 499) # same person? merge adrs + email?
                         , (505, 507)
                         , (410, 547)
                         , (712, 680)
                         , (230, 729) # merge phone number?
                         , (375, 743)
                         , (755, 175) # use newer phone number?
                         , (219, 759) # same person?
                         , (453, 454)
                         , (803, 804)
                         , (295, 556) # same person? same gmx address!
                         , (697, 814)
                         , (476, 854) # merge web?
                         , (312, 307)
                         , (351, 355)
                         , (401, 309)
                         , (871, 870)
                         , (580, 898)
                         , (894, 896)
                         , (910, 766)
                        ))

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
            if x in self.phone_bogus :
                return
            try :
                p = Phone (x, m.town, c)
            except ValueError, err :
                if str (err).startswith ('WARN') :
                    print err
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
                print "WARN: %s/%s %s/%s: Duplicate phone: %s" \
                    % (eid, prs.pid, m.id, person.pid, x)
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
            print "WARN: %s/%s %s/%s: Duplicate email: %s" \
                % (eid, prs.pid, m.id, person.pid, mail)
        else :
            desc = None
            if second :
                desc = "von 2. Account"
                print "INFO: Second email for %s/%s: %s" \
                    % (m.id, person.pid, mail)
            self.email_ids [mail.lower ()] = m.id
            email = self.pap.Email (address = mail, desc = desc)
            self.pap.Person_has_Email (person, email)
    # end def try_insert_email

    def try_insert_url (self, m, person) :
        hp = m.homepage
        if not hp.startswith ('http') :
            hp = 'http://' + hp
        url = self.pap.Url.instance_or_new (hp, desc = 'Homepage', raw = True)
        self.pap.Person_has_Url (person, url)
    # end def try_insert_url

    def try_insert_im (self, m, person) :
        print "INFO: Instant messenger nickname: %s" % m.instant_messenger_nick
        im = self.pap.IM_Handle (address = m.instant_messenger_nick)
        self.pap.Person_has_IM_Handle (person, im)
    # end def try_insert_im

    phone_types = dict \
        ( telephone   = 'Festnetz'
        , mobilephone = 'Mobil'
        , fax         = 'Fax'
        )

    def create_persons (self) :
        for m in sorted (self.contents ['members'], key = lambda x : x.id) :
            if m.id == 309 and m.street.startswith ("'") :
                m.street = m.street [1:]
            if m.id in self.person_dupes :
                print "INFO: skipping person (duplicate): %s" % m.id
                self.dupes_by_id [m.id] = m
                continue
            if not m.firstname and not m.lastname :
                print "WARN: skipping person, no name:", m.id
                continue
            if not m.lastname :
                print "WARN: skipping person, no lastname: %s" % m.id
                continue
            person = self.pap.Person \
                ( first_name = m.firstname
                , last_name  = m.lastname
                , raw        = True
                )
            self.set_last_change (person, m.changed, m.created)
            self.person_by_id [m.id] = person
            street  = ' '.join (x for x in (m.street, m.housenumber) if x)
            if street or m.town or m.zip :
                country = 'Austria'.decode ('latin1')
                if not m.town :
                    print 'INFO: no city (setting to "Wien"): %s/%s' \
                        % (m.id, person.pid)
                    m ['town'] = 'Wien'
                if not m.zip :
                    if m.id == 653 :
                        m ['zip'] = 'USA'
                    elif m.id == 787 :
                        m ['zip'] = '2351'
                    else :
                        print "INFO: no zip: %s/%s" % (m.id, person.pid)
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
            if m.email :
                self.try_insert_email (person, m)
            if m.fax and '@' in m.fax :
                self.try_insert_email (person, m, attr = 'fax')
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
            d = self.dupes_by_id [dupe]
            person = self.person_by_id [id]
            if d.email :
                self.try_insert_email (person, d, second = True)
            for a, c in self.phone_types.iteritems () :
                x = getattr (d, a)
                self.try_insert_phone (person, d, x, c)
            if d.mentor_id and d.mentor_id != d.id :
                assert (False)
            if d.nickname :
                nick = self.pap.Nickname (d.nickname, raw = True)
                self.pap.Person_has_Nickname (person, nick)
            if d.homepage :
                self.try_insert_url (d, person)
            if d.instant_messenger_nick :
                self.try_insert_im (d, person)
    # end def create_persons

    def create_device (self, d) :
        if self.debug :
            print 'dev:', d.id, d.name
        node = self.node_by_id [d.id_nodes]
        if d.hardware :
            # FIXME: We want correct info from nodes directly
            # looks like most firmware can give us this info
            devtype = self.ffm.Net_Device_Type.instance_or_new \
                (name = d.hardware, raw = True)
        else :
            devtype = self.ffm.Net_Device_Type.instance (name = 'Generic')
        dev = self.ffm.Net_Device \
            (left = devtype, node = node, name = d.name, raw = True)
        self.set_last_change (dev, d.changed, d.created)
        # no member info in DB:
        assert not d.id_members
        return dev
    # end def create_device

    def create_interface (self, dev, name, ip) :
        # FIXME: Need info on wireless vs wired Net_Interface
        iface = self.ffm.Wired_Interface (left = dev, name = name, raw = True)
        net = IP4_Address (ip.ip, ip.cidr)
        net = self.net_dupes.get (net, net)
        network = self.ffm.IP4_Network.instance \
            (dict (address = str (net)), raw = True)
        ip4 = IP4_Address (ip.ip)
        self.ffm.Net_Interface_in_IP4_Network \
            (iface, network, dict (address = ip4))
    # end def create_interface

    def create_interfaces_for_dev (self, dev, d, ip) :
        if len (self.ip_by_dev [d.id]) > 1 :
            for n, dev_ip in enumerate (self.ip_by_dev [d.id]) :
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
                print "ERR:  key %s from mid has no device" % ip4
            for a in aliases :
                ip = self.ip_by_ip [a]
                if not ip.id_devices :
                    print "ERR:  %s from mid %s has no device" % (a, ip4)
                    continue
                d  = self.dev_by_id [ip.id_devices]
                if d.id_nodes not in nodes :
                    nodes [d.id_nodes] = ({}, {})
                nodes [d.id_nodes] [0] [ip.id_devices] = d
                nodes [d.id_nodes] [1] [ip.id] = ip
            if len (nodes) > 1 :
                print "WARN: mid %s expands to %s nodes" % (ip4, len (nodes))
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
                        print "HNA: %s" % ip4

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
                print "WARN: ip %s from olsr topo not in ips" % ip4
                del self.olsr_nodes [ip4]
        # check mid table
        midkey = []
        midtbl = {}
        for ip4, aliases in self.olsr_mid.iteritems () :
            if ip4 not in self.ip_by_ip :
                print "WARN: key ip %s from olsr mid not in ips" % ip4
                midkey.append (ip4)
            for a in aliases :
                if a not in self.ip_by_ip :
                    print "WARN: ip %s from olsr mid not in ips" % a
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
            print k
        for node in self.contents ['nodes'] :
            print "Node: %s (%s)" % (node.name.encode ('latin1'), node.id)
            for d in self.dev_by_node.get (node.id, []) :
                print "    Device: %s" % d.name
                ips = self.ip_by_dev.get (d.id, [])
                ips.sort ()
                for ip in ips :
                    x = ''
                    if IP4_Address (ip.ip) in self.olsr_nodes :
                        x = ' USED'
                    print "        IP: %s/%s%s" % (ip.ip, ip.cidr, x)
                l = len (ips)
                if not l :
                    print "    No IPs!!"
                for ip in ips :
                    adr = IP4_Address (ip.ip)
                    if adr in self.olsr_mid :
                        ips1 = [x.ip for x in ips]
                        ips2 = []
                        ips2.extend (str (x) for x in self.olsr_mid [adr])
                        ips2.append (ip.ip)
                        ips2.sort ()
                        if ips1 != ips2 :
                            print "        Ooops: %s/%s" % (ips1, ips2)
                        break
                else :
                    if l > 1 :
                        print "        Not found in olsr_mid!"
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
        ) + model.opts
    , min_args        = 1
    , defaults        = model.command.defaults
    )

if __name__ == "__main__" :
    _Command ()
### __END__ cnml_import
