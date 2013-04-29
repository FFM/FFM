#!/usr/bin/python
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

import re

from   rsclib.HTML_Parse  import Page_Tree, tag
from   rsclib.autosuper   import autosuper
from   rsclib.stateparser import Parser
from   rsclib.IP_Address  import IP4_Address

class Topo_Entry (autosuper) :
    """ Model an OLSR topology entry. """

    def __init__ (self, dst_ip, last_hop, lq, nlq, cost) :
        self.dst_ip   = IP4_Address (dst_ip)
        self.last_hop = IP4_Address (last_hop)
        self.lq       = lq
        self.nlq      = nlq
        self.cost     = cost
    # end def __init__

    def __str__ (self) :
        return "Topo_Entry (%(dst_ip)s, %(last_hop)s)" % self.__dict__
    # end def __str__
    __repr__ = __str__

# end class Topo_Entry

class Topology (autosuper) :

    def __init__ (self) :
        self.forward = {}
        self.reverse = {}
    # end def __init__

    def add (self, entry) :
        if entry.dst_ip not in self.forward :
            self.forward [entry.dst_ip] = []
        self.forward [entry.dst_ip].append (entry)
        if entry.last_hop not in self.reverse :
            self.reverse [entry.last_hop] = []
        self.reverse [entry.last_hop].append (entry)
    # end def add

# end class Topology

class MID (autosuper) :
    """ Model OLSR MID table. """

    def __init__ (self) :
        self.by_ip = {}
    # end def __init__

    def add (self, ip, *aliases) :
        ip = IP4_Address (ip)
        aliases = [IP4_Address (a) for a in aliases]
        assert ip not in self.by_ip or self.by_ip [ip] == aliases
        self.by_ip [ip] = aliases
    # end def __init__

    def __str__ (self) :
        return '\n'.join \
            ("MID %s -> %s" % (k, ';'.join (str (i) for i in v))
             for k, v in self.by_ip.iteritems ()
            )
    # end def __str__
    __repr__ = __str__

# end class MID

class HNA_Entry (autosuper) :

    def __init__ (self, dest, gw) :
        self.dest = IP4_Address (dest)
        self.gw   = IP4_Address (gw)
    # end def __init__

    def __str__ (self) :
        return "HNA_Entry (%(dest)s, %(gw)s)" % self.__dict__
    # end def __str__
    __repr__ = __str__

# end class HNA_Entry

class HNA (autosuper) :

    def __init__ (self) :
        self.by_dest = {}
    # end def __init__

    def add (self, entry) :
        self.by_dest [entry.dest] = entry
    # end def add

# end class HNA

class OLSR_Parser (Parser) :
    re_mid_head  = re.compile (r"IP address\s+Aliases")
    re_topo_head = re.compile \
        (r"Dest. IP\s+Last hop\s+IP\s+LQ\s+NLQ\s+Cost")
    re_hna_head  = re.compile (r"Destination\s+Gateway")
    ip           = r"([0-9.]+)"
    gw           = r"(%(ip)s/([0-9]+))" % locals ()
    n            = r"((?:[0-9.]+)|INFINITE)"
    re_topo_line = re.compile (r"^" + r"\s+".join ([ip] * 2 + [n] * 3) + r"$")
    re_mid_line  = re.compile (r"^%s\s+(%s\s*(;\s*%s)*)$" % (n, n, n))
    re_hna_line  = re.compile (r"^%(gw)s\s+%(ip)s$" % locals ())
    matrix = \
        [ ["init",      "Table: MID",      "mid_tbl",   "push"]
        , ["init",      "Table: Topology", "topo_tbl",  "push"]
        , ["init",      "Table: HNA",      "hna_tbl",   "push"]
        , ["init",      None,              "init",      None]
        , ["mid_tbl",   re_mid_head,       "mid_line",  None]
        , ["topo_tbl",  re_topo_head,      "topo_line", None]
        , ["hna_tbl",   re_hna_head,       "hna_line",  None]
        , ["hna_line",  re_hna_line,       "hna_line",  "hna_line"]
        , ["hna_line",  None,              "init",      "pop"]
        , ["mid_line",  re_mid_line,       "mid_line",  "mid_line"]
        , ["mid_line",  None,              "init",      "pop"]
        , ["topo_line", re_topo_line,      "topo_line", "topo_line"]
        , ["topo_line", None,              "init",      "pop"]
        ]

    def __init__ (self, *args, **kw) :
        self.hna  = HNA      ()
        self.mid  = MID      ()
        self.topo = Topology ()
        self.__super.__init__ (*args, **kw)
    # end def __init__

    def hna_line (self, state, new_state, match) :
        self.hna.add (HNA_Entry (match.group (1), match.group (4)))
    # end def hna_line

    def mid_line (self, state, new_state, match) :
        aliases = (x.strip () for x in match.group (2).split (';'))
        m = self.mid.add (match.group (1), *aliases)
    # end def mid_line

    def topo_line (self, state, new_state, match) :
        g = match.groups ()
        p = []
        for n, v in enumerate (g) :
            if n > 1 :
                if v == 'INFINITE' : v = 'inf'
                v = float (v)
            p.append (v)
        self.topo.add (Topo_Entry (* p))
    # end def topo_line

# end class OLSR_Parser

class Backfire_MID_Parser (Page_Tree) :

    url = 'cgi-bin/luci/freifunk/olsr/mid/'

    def __init__ (self, site, mid) :
        self.mid = mid
        self.__super.__init__ (site = site)
    # end def __init__

    def parse (self) :
        root = self.tree.getroot ()
        for fs in root.findall (".//%s" % tag ("fieldset")) :
            if fs.get ('class') == 'cbi-section' :
                tbl = fs.find (".//%s" % tag ("table"))
                assert tbl.get ('class') == 'cbi-section-table'
                for tr in tbl :
                    if tr [0].tag == tag ('th') :
                        assert tr [0].text == 'OLSR node'
                        continue
                    assert tr [0][0].tag == tag ('a')
                    self.mid.add (tr [0][0].text, * tr [1].text.split (';'))
    # end def parse

# end class Backfire_MID_Parser

class Backfire_HNA_Parser (Page_Tree) :

    url = 'cgi-bin/luci/freifunk/olsr/hna/'

    def __init__ (self, site, hna) :
        self.hna = hna
        self.__super.__init__ (site = site)
    # end def __init__

    def parse (self) :
        root = self.tree.getroot ()
        for fs in root.findall (".//%s" % tag ("fieldset")) :
            if fs.get ('class') == 'cbi-section' :
                tbl = fs.find (".//%s" % tag ("table"))
                assert tbl.get ('class') == 'cbi-section-table'
                for tr in tbl :
                    if tr [0].tag == tag ('th') :
                        assert tr [0].text == 'Announced network'
                        continue
                    assert tr [1][0].tag == tag ('a')
                    self.hna.add (HNA_Entry (tr [0].text, tr [1][0].text))
    # end def parse

# end class Backfire_HNA_Parser

class Backfire_Topo_Parser (Page_Tree) :

    url = 'cgi-bin/luci/freifunk/olsr/topology/'

    def __init__ (self, site, topo) :
        self.topo = topo
        self.__super.__init__ (site = site)
    # end def __init__

    def parse (self) :
        root = self.tree.getroot ()
        for fs in root.findall (".//%s" % tag ("fieldset")) :
            if fs.get ('class') == 'cbi-section' :
                tbl = fs.find (".//%s" % tag ("table"))
                assert tbl.get ('class') == 'cbi-section-table'
                for tr in tbl :
                    if tr [0].tag == tag ('th') :
                        assert tr [0].text == 'OLSR node'
                        continue
                    assert tr [0][0].tag == tag ('a')
                    assert tr [1][0].tag == tag ('a')
                    p = [tr [0][0].text, tr [1][0].text]
                    for v in tr [2:] :
                        v = v.text
                        if v == 'INFINITE' : v = 'inf'
                        v = float (v)
                        p.append (v)
                    self.topo.add (Topo_Entry (* p))
    # end def parse

# end class Backfire_Topo_Parser

class Backfire_OLSR_Parser (autosuper) :

    def __init__ (self, site) :
        self.hna  = HNA      ()
        self.mid  = MID      ()
        self.topo = Topology ()
        self.__super.__init__ (site = site)
        p = Backfire_MID_Parser (site, self.mid)
        p = Backfire_HNA_Parser (site, self.hna)
        p = Backfire_Topo_Parser (site, self.topo)
    # end def __init__

# end class Backfire_OLSR_Parser

def get_olsr_container (file_or_url) :
    if file_or_url.startswith ('http://') :
        olsr = Backfire_OLSR_Parser (site = file_or_url)
    else :
        f = open (file_or_url)
        olsr = OLSR_Parser (verbose = 0)
        olsr.parse (f)
    return olsr
# end def get_olsr_container

if __name__ == "__main__" :
    import sys
    import os
    if len (sys.argv) != 2 :
        bn = os.path.basename (sys.argv [0])
        print >> sys.stderr, "Usage: %(bn)s <file-or-url>" % locals ()
        sys.exit (23)
    olsr = get_olsr_container (sys.argv [1])
    for t in olsr.topo.forward.itervalues () :
        print t
    print olsr.mid
    for h in olsr.hna.by_dest.itervalues () :
        print h
