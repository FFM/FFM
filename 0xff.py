#!/usr/bin/python

import sys, os
import re

from   datetime               import datetime, tzinfo, timedelta
from   rsclib.IP4_Address     import IP4_Address
from   _GTW                   import GTW
from   _TFL                   import TFL
from   _FFM                   import FFM

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

def sql_float (f) :
    if f == '\\N' :
        return None
    return float (f)
# end def sql_float

def sql_int (i) :
    if i == '\\N' :
        return None
    return int (i)
# end def sql_int

def sql_str (s) :
    """ Get string from sql dump and convert to unicode.
    >>> sql_str ('\xc3\x96ffnungswinkel')
    u'\\xd6ffnungswinkel'
    """
    if s == '\\N' :
        return None
    return s.decode ('utf-8')
# end def sql_str

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

class Convert (object) :

    re_copy  = re.compile (r'^COPY\s+(\S+)\s\(([^)]+)\) FROM stdin;$')
    re_table = re.compile (r'^CREATE TABLE (\S+) \(')

    def __init__ (self, args, scope) :
        if len (args) > 0 :
            f  = open (args [0])
        else :
            f = sys.stdin

        self.scope    = scope
        self.ffm      = self.scope.FFM
        self.tables   = {}
        self.contents = {}
        self.modes    = dict \
            ( client  = self.ffm.Client_Mode
            , ap      = self.ffm.AP_Mode
            , ad_hoc  = self.ffm.Ad_Hoc_Mode
            )
        self.iter     = enumerate (f)
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
        for tbl, ct in self.contents.iteritems () :
            print "Table: %s" % tbl
            for line in ct :
                print
                for k, v in line.iteritems () :
                    print "  %s: %s" % (k, repr (v))
    # end def __init__

    def parse_fields (self, table, fields) :
        contents = self.contents [table] = []
        tbl      = self.tables [table]
        for self.lineno, line in self.iter :
            line = line.rstrip ('\n')
            if line == '\\.' :
                return
            datafields = line.split ('\t')
            contents.append \
                (dict ((a, tbl [a] (b)) for a, b in zip (fields, datafields)))
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
            method = getattr (self, 'type_' + type)
            tbl [name] = method (rest)
    # end def parse_table

    def type_bigint (self, rest) :
        return sql_int
    # end def type_bigint

    def type_boolean (self, rest) :
        return sql_boolean
    # end def type_bigint

    def type_character (self, rest) :
        assert (rest.startswith ('varying'))
        return sql_str
    # end def type_character

    def type_double (self, rest) :
        assert (rest.startswith ('precision'))
        return sql_float
    # end def type_double

    def type_integer (self, rest) :
        return sql_int
    # end def type_integer

    def type_smallint (self, rest) :
        return sql_int
    # end def type_smallint

    def type_timestamp (self, rest) :
        if rest.startswith ('with time zone') :
            return sql_timestamp_with_zone
        elif rest.startswith ('without time zone') :
            return sql_timestamp_without_zone
        else :
            raise ValueError, "Invalid timestamp spec: %s" % rest
    # end def type_timestamp

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
