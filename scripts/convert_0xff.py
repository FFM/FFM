#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

import sys, os
import re

from   datetime               import datetime, tzinfo, timedelta
from   rsclib.IP4_Address     import IP4_Address
from   _GTW                   import GTW
from   _TFL                   import TFL
from   _FFM                   import FFM
from   _GTW._OMP._PAP         import PAP
from   olsr.parser            import OLSR_Parser

import _TFL.CAO
import model

class TZ (tzinfo) :
    def __init__ (self, offset = 0) :
        self.offset = int (offset, 10)
    # end def __init__

    def utcoffset (self, dt = None) :
        return timedelta (hours = self.offset)
    # end def utcoffset

    def __str__ (self) :
        return "TZ (%s)" % self.offset
    # end def __str__
    __repr__ = __str__

# end class TZ

sql_bool = {'t' : True, 'f' : False}

def sql_boolean (b) :
    """ Parse boolean from sql dump and return as python bool.
    >>> sql_boolean ('\\N')
    >>> sql_boolean ('f')
    False
    >>> sql_boolean ('t')
    True
    """
    if b == '\\N' :
        return None
    return sql_bool [b]
# end def sql_boolean

def sql_double (f) :
    if f == '\\N' :
        return None
    return float (f)
# end def sql_double

def sql_integer (i) :
    if i == '\\N' :
        return None
    return int (i)
# end def sql_integer
sql_bigint = sql_smallint = sql_integer

def sql_character (s) :
    """ Get string from sql dump and convert to unicode.
    >>> sql_str ('\xc3\x96ffnungswinkel')
    u'\\xd6ffnungswinkel'
    """
    if s == '\\N' :
        return None
    return s.decode ('utf-8')
# end def sql_character

def sql_timestamp_without_zone (ts) :
    """ convert sql timestamp with time zone.
    >>> sql_timestamp_without_zone ("2012-05-24 17:05:16.609")
    datetime.datetime(2012, 5, 24, 17, 5, 16, 609000)
    >>> sql_timestamp_without_zone ("2012-05-24 17:43:33")
    datetime.datetime(2012, 5, 24, 17, 43, 33)
    """
    if ts == '\\N' :
        return None
    format = '%Y-%m-%d %H:%M:%S.%f'
    if len (ts) == 19 :
        format = '%Y-%m-%d %H:%M:%S'
    return datetime.strptime (ts, format)
# end def sql_timestamp_without_zone

def sql_timestamp_with_zone (ts) :
    """ convert sql timestamp with time zone.
    >>> sql_timestamp_with_zone ("2011-01-17 20:12:09.04032+01")
    datetime.datetime(2011, 1, 17, 20, 12, 9, 40320, tzinfo=TZ (1))
    """
    if ts == '\\N' :
        return None
    d  = sql_timestamp_without_zone (ts [:-3])
    tz = TZ (ts [-3:])
    return d.replace (tzinfo = tz)
# end def sql_timestamp_with_zone

def make_naive (dt) :
    """Make a naive datetime object."""
    if dt is None :
        return dt
    offs = dt.utcoffset ()
    if offs is None :
        return dt
    x = dt.replace (tzinfo = None)
    return x - offs
# end make_naive

class adict (dict) :

    def __init__ (self, *args, **kw) :
        self.done = False
        dict.__init__ (self, *args, **kw)
    # end def __init__

    def __getattr__ (self, key) :
        if key in self :
            return self [key]
        raise AttributeError, key
    # end def __getattr__

    def set_done (self, done = True) :
        self.done = done
    # end def set_done

# end class adict

class Convert (object) :

    re_copy  = re.compile (r'^COPY\s+(\S+)\s\(([^)]+)\) FROM stdin;$')
    re_table = re.compile (r'^CREATE TABLE (\S+) \(')

    def __init__ (self, cmd, scope) :
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
        for k in self.olsr_mid.itervalues () :
            for mid in k :
                assert mid not in self.rev_mid
                self.rev_mid [mid] = True
        self.scope        = scope
        self.ffm          = self.scope.FFM
        self.pap          = self.scope.GTW.OMP.PAP
        self.tables       = {}
        self.contents     = {}
        self.mentor       = {}
        self.modes        = dict \
            ( client      = self.ffm.Client_Mode
            , ap          = self.ffm.AP_Mode
            , ad_hoc      = self.ffm.Ad_Hoc_Mode
            )
        self.networks     = {}
        self.node_by_id   = {}
        self.ip_by_ip     = {}
        self.dev_by_id    = {}
        self.email_ids    = {}
        self.phone_ids    = {}
        self.person_by_id = {}
        self.dupes_by_id  = {}
        self.ip_by_dev    = {}
        self.dev_by_node  = {}
        self.iter         = enumerate (f)
        try :
            for self.lineno, line in self.iter :
                m = self.re_copy.match (line)
                if m :
                    table  = m.group (1)
                    fields = [x.strip ('"') for x in m.group (2).split (', ')]
                    self.parse_fields (table, fields)
                m = self.re_table.match (line)
                if m :
                    table  = m.group (1)
                    self.parse_table (table)
        except :
            print "Error in line %s" % (self.lineno + 1)
            raise
    # end def __init__

    def dump (self) :
        for tbl, ct in self.contents.iteritems () :
            print "Table: %s" % tbl
            for line in ct :
                print
                for k, v in line.iteritems () :
                    print "  %s: %s" % (k, repr (v))
    # end dump

    def parse_fields (self, table, fields) :
        contents = self.contents [table] = []
        tbl      = self.tables [table]
        for self.lineno, line in self.iter :
            line = line.rstrip ('\n')
            if line == '\\.' :
                return
            datafields = line.split ('\t')
            contents.append \
                (adict ((a, tbl [a] (b)) for a, b in zip (fields, datafields)))
    # end def parse_fields

    def parse_table (self, table) :
        tbl = self.tables [table] = {}
        for self.lineno, line in self.iter :
            line = line.strip ()
            if line == ');' :
                return
            try :
                name, type, rest = line.split (None, 2)
            except ValueError :
                name, type = line.split (None, 1)
                if type.endswith (',') :
                    type = type [:-1]
                rest = ''
            if name.startswith ('"') :
                name = name [1:-1]
            method = getattr (self, 'type_' + type, self.type_default)
            tbl [name] = method (type, rest)
    # end def parse_table

    def type_default (self, type, rest) :
        return globals () ['sql_' + type]
    # end def type_default

    def type_character (self, type, rest) :
        assert (rest.startswith ('varying'))
        return self.type_default (type, rest)
    # end def type_character

    def type_double (self, type, rest) :
        assert (rest.startswith ('precision'))
        return self.type_default (type, rest)
    # end def type_double

    def type_timestamp (self, type, rest) :
        if rest.startswith ('with time zone') :
            return sql_timestamp_with_zone
        elif rest.startswith ('without time zone') :
            return sql_timestamp_without_zone
        else :
            raise ValueError, "Invalid timestamp spec: %s" % rest
    # end def type_timestamp

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
            node = self.ffm.Node (name = n.name, position = gps, map_p = n.map)
            self.set_last_change (node, n.changed, n.created)
            assert (node)
            id = self.person_dupes.get (n.id_members, n.id_members)
            person = self.person_by_id.get (id)
            if person :
                self.ffm.Subject_owns_Node (person, node)
            else :
                print "WARN: Node %s: member %s not found" \
                    % (n.id, n.id_members)
            self.node_by_id [n.id] = node
            if n.id_tech_c and n.id_tech_c != n.id_members :
                print "Tech contact found: %s" % n.id_tech_c
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
                        ))

    number_types = \
        { '720' : 'Ortsunabhängig'.decode ('latin1')
        , '780' : 'Kovergenter Dienst'.decode ('latin1')
        }

    area_codes = dict.fromkeys \
        (('2243', '2245', '2168', '2230', '2572', '2287', '2165', '2256'))

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
    phone_special = dict.fromkeys \
        (('650', '660', '664', '676', '680', '681', '688', '699', '720', '780'))

    def parse_phone (self, m, orig_number, type) :
        number = orig_number.replace (' ', '')
        number = number.replace ('/', '')
        number = number.replace ('-', '')
        number = number.replace ('(0)', '')
        if number.startswith ('00') :
            cc   = number [2:4]
            if cc == '41' and number [4:6] == '76' :
                return dict \
                    ( country_code = cc
                    , area_code    = '76'
                    , number       = number [6:]
                    , desc         = 'Mobil'
                    )
            if cc == '43' :
                rest = number [4:]
            elif number [2:5] in self.phone_special :
                cc   = '43'
                rest = number [2:]
            else :
                raise ValueError, "Number: %s" % orig_number
        elif number.startswith ('0') :
            cc   = '43'
            rest = number [1:]
        elif number.startswith ('+430') and number [4:7] in self.phone_special :
            cc   = '43'
            rest = number [4:]
        elif number.startswith ('+43') :
            cc   = '43'
            rest = number [3:]
        elif number.startswith ('+31650') :
            cc   = '43'
            area = '650' # mobile number for netherlands, really
            n    = number [6:]
            type = 'Mobil'
            return dict \
                (country_code = cc, area_code = area, number = n, desc = type)
        elif len (number) == 7 and m.town.lower ().startswith ('wien') :
            cc   = '43'
            rest = '1' + number
            if type != 'Fax' :
                type = 'Festnetz'
        elif number.startswith ('650') and type == 'Mobil' :
            cc   = '43'
            rest = number
        elif number.startswith ('43') and number [2:5] in self.phone_special :
            cc   = '43'
            rest = number [2:]
        elif '@' in number :
            print "WARN: Email in phone field? %s" % orig_number
            return
        else :
            raise ValueError, "Number: %s" % orig_number

        if rest.startswith ('1') :
            area = '1'
            number = rest [1:]
        elif rest [0:3] in self.phone_special :
            area   = rest [0:3]
            type   = self.number_types.get (area, 'Mobil')
            number = rest [3:]
        elif rest [0:4] in self.area_codes :
            area   = rest [0:4]
            if type != 'Fax' :
                type = 'Festnetz'
            number = rest [4:]
        else :
            raise ValueError, "Unknown area code: %s" % orig_number
        return dict \
            (country_code = cc, area_code = area, number = number, desc = type)
    # end def parse_phone

    def try_insert_phone (self, person, m, x, c) :
        if x :
            if x in self.phone_bogus :
                return
            p = self.parse_phone (m, x, c)
            if not p :
                return
            t = self.pap.Phone.instance (** p)
            k = "+%(country_code)s/%(area_code)s/%(number)s" % p
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
                t = self.pap.Phone (** p)
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
            for a, c in self.phone_types.iteritems () :
                x = getattr (m, a)
                self.try_insert_phone (person, m, x, c)
            if m.mentor_id and m.mentor_id != m.id :
                self.mentor [m.id] = m.mentor_id
            if m.nickname :
                self.ffm.Nickname (person, m.nickname)
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
                self.ffm.Nickname (person, d.nickname)
    # end def create_persons

    def create_device (self, d) :
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
        net = str (IP4_Address (ip.ip.encode ('ascii'), ip.cidr))
        network = self.networks [net]
        self.ffm.Net_Interface_in_IP4_Network \
            (iface, network, dict (address = ip.ip), raw = True)
    # end def create_interface

    def create_ips_and_devices (self) :
        for ip in self.contents ['ips'] :
            assert not ip.id_nodes
            assert not ip.id_members or ip.id_members == 1
            assert not ip.id_members or not ip.id_devices
            if not ip.id_devices :
                # FIXME: Do we need a "free-pool"?
                continue
            print ip.ip, type (ip.ip), ip.cidr
            # Ignore IPs that belong to some device
            if ip.ip in self.rev_mid :
                continue
            d = self.dev_by_id [ip.id_devices]
            dev = self.create_device (d)
            self.create_interface (dev, d.name, ip)
            # main IP/Interface of a device, add others
            if ip.ip in self.olsr_mid :
                for s_ip_ip in self.olsr_mid [ip.ip] :
                    s_ip = self.ip_by_ip [s_ip_ip]
                    ip_dev = self.dev_by_id [s_ip.id_devices]
                    self.create_interface (dev, ip_dev.name, s_ip)
    # end def create_ips_and_devices

    def build_device_structure (self) :
        for ip in self.contents ['ips'] :
            self.ip_by_ip [ip.ip] = ip
            if ip.id_devices :
                if ip.id_devices not in self.ip_by_dev :
                    self.ip_by_dev [ip.id_devices] = []
                self.ip_by_dev [ip.id_devices].append (ip)
            net = str (IP4_Address (ip.ip.encode ('ascii'), ip.cidr))
            network = self.ffm.IP4_Network.instance_or_new \
                (dict (address = net))
            self.networks [net] = network
        for n in self.networks :
            print n
        for k in self.ffm.IP4_Network.query () :
            print k
        for d in self.contents ['devices'] :
            if d.id_nodes not in self.dev_by_node :
                self.dev_by_node [d.id_nodes] = []
            self.dev_by_node [d.id_nodes].append (d)
            self.dev_by_id [d.id] = d
        # consistency check of olsr data against redeemer db
        # check nodes from topology
        for ip in self.olsr_nodes :
            if ip not in self.ip_by_ip :
                print "WARN: ip %s from olsr topo not in ips" % ip
                del self.olsr_nodes [ip]
        # check mid table
        midkey = []
        midtbl = {}
        for ip, aliases in self.olsr_mid.iteritems () :
            if ip not in self.ip_by_ip :
                print "WARN: key ip %s from olsr mid not in ips" % ip
                midkey.append (ip)
            for a in aliases :
                if a not in self.ip_by_ip :
                    print "WARN: ip %s from olsr mid not in ips" % a
                    if ip not in midtbl :
                        midtbl [ip] = []
                    midtbl [ip].append (a)
        assert not midkey
        for k, v in midtbl.iteritems () :
            x = dict.fromkeys (self.olsr_mid [k])
            for ip in v :
                del x [ip]
            self.olsr_mid [k] = x.keys ()
    # end def build_device_structure

    def debug_output (self) :
        for k in sorted \
            ( self.olsr_nodes.iterkeys ()
            , key = lambda x : tuple (int (z) for z in x.split ('.'))
            ) :
            print k
        for node in self.contents ['nodes'] :
            print "Node: %s" % node.name.encode ('latin1')
            for d in self.dev_by_node.get (node.id, []) :
                print "    Device: %s" % d.name
                ips = self.ip_by_dev.get (d.id, [])
                ips.sort ()
                for ip in ips :
                    x = ''
                    if ip.ip.decode ('ascii') in self.olsr_nodes :
                        x = ' USED'
                    print "        IP: %s/%s%s" % (ip.ip, ip.cidr, x)
                l = len (ips)
                if not l :
                    print "    No IPs!!"
                for ip in ips :
                    if ip.ip in self.olsr_mid :
                        ips1 = [x.ip for x in ips]
                        ips2 = []
                        ips2.extend (self.olsr_mid [ip.ip])
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
        self.debug_output           ()
        self.create_persons         ()
        self.create_nodes           ()
        #self.create_ips_and_devices ()
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
