#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

import sys, os
import re

from   UserDict               import UserDict
from   datetime               import datetime, tzinfo, timedelta
from   rsclib.IP4_Address     import IP4_Address
from   _GTW                   import GTW
from   _TFL                   import TFL
from   _FFM                   import FFM
from   _GTW._OMP._PAP         import PAP


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

class adict (UserDict) :
    def __getattr__ (self, key) :
        if key in self :
            return self [key]
        raise AttributeError, key
    # end def __getattr__
# end class adict

class Convert (object) :

    re_copy  = re.compile (r'^COPY\s+(\S+)\s\(([^)]+)\) FROM stdin;$')
    re_table = re.compile (r'^CREATE TABLE (\S+) \(')

    def __init__ (self, args, scope) :
        if len (args) > 0 :
            f  = open (args [0])
        else :
            f = sys.stdin

        self.scope        = scope
        self.ffm          = self.scope.FFM
        self.pap          = self.scope.GTW.OMP.PAP
        self.tables       = {}
        self.contents     = {}
        self.modes        = dict \
            ( client      = self.ffm.Client_Mode
            , ap          = self.ffm.AP_Mode
            , ad_hoc      = self.ffm.Ad_Hoc_Mode
            )
        self.node_by_id   = {}
        self.person_by_id = {}
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
            #gps ['raw'] = True
            #node = self.ffm.Node (name = n.name, position = gps, raw = True)
            node = self.ffm.Node (name = n.name, position = gps)
            assert (node)
            if n.id_members not in self.person_by_id :
                print "Node %s: id member %s not found" % (n.id, n.id_members)
            self.node_by_id [n.id] = node
    # end def create_nodes

    def create_devices (self) :
        for d in self.contents ['devices'] :
            node = self.node_by_id [d.id_nodes]
            name = ''.join ((node.name, d.name))
            if d.hardware :
                devtype = self.ffm.Net_Device_Type.instance_or_new \
                    (name = d.hardware, raw = True)
            else :
                devtype = self.ffm.Net_Device_Type.instance (name = 'Generic')
            dev = self.ffm.Net_Device (left = devtype, name = name, raw = True)
            self.ffm.Node_has_Net_Device (node, dev)
    # end def create_devices

    # first id is the one to remove, the second one is the correct one
    # FIXME: we may need to merge some attributes from one entry to the other
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
                        ))

    def create_persons (self) :
        for m in self.contents ['members'] :
            if m.id in self.person_dupes :
                print "skipping: %s" % m.id
                continue
            if not m.firstname and not m.lastname :
                print "no name:", m.id
                continue
            if not m.lastname :
                print "no lastname: %s" % m.id
                continue
            person = self.pap.Person \
                ( first_name = m.firstname
                , last_name  = m.lastname
                , raw        = True
                )
            self.person_by_id [m.id] = person
            street  = ' '.join (x for x in (m.street, m.housenumber) if x)
            if street or m.town or m.zip :
                if not m.town :
                    print "no city: %s" % m.id
                    m ['town'] = 'Wien'
                if not m.zip :
                    if m.id == 653 :
                        m ['zip'] = 'USA'
                    elif m.id == 787 :
                        m ['zip'] = '2351'
                    else :
                        print "no zip: %s" % m.id
                elif m.zip.startswith ('I-') :
                    m ['zip'] = m.zip [2:]
                    country = 'Italy'.decode ('latin1')
                address = self.pap.Address.instance_or_new \
                    ( street     = street
                    , zip        = m.zip
                    , city       = m.town
                    , country    = 'Austria'.decode ('latin1')
                    )
            # FIXME: we should import these.
            if m.mentor_id and m.mentor_id != m.id :
                #print "mentor: %s" % m.mentor_id
                pass
    # end def create_persons

    def create (self) :
        self.create_persons ()
        self.create_nodes   ()
        self.create_devices ()
    # end def create

# end def Convert


def _main (cmd) :
    scope = model.scope (cmd)
    if cmd.Break :
        TFL.Environment.py_shell ()
    c = Convert (cmd.argv, scope)
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
