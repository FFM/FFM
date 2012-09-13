#!/usr/bin/python

import re

from   rsclib.HTML_Parse  import Page_Tree
from   rsclib.autosuper   import autosuper
from   rsclib.stateparser import Parser

class Topology (autosuper) :
    """ Model an OLSR topology entry. """

    def __init__ (self, dst_ip, last_hop, lq, nlq, cost) :
        self.dst_ip   = dst_ip
        self.last_hop = last_hop
        self.lq       = lq
        self.nlq      = nlq
        self.cost     = cost
    # end def __init__

    def __str__ (self) :
        return "Topology (%(dst_ip)s, %(last_hop)s)" % self.__dict__
    # end def __str__
    __repr__ = __str__

# end class Topology

class MID (autosuper) :
    """ Model an OLSR MID entry. """

    def __init__ (self, ip, *aliases) :
        self.ip      = ip
        self.aliases = aliases
    # end def __init__

    def __str__ (self) :
        return "MID (%(ip)s, * %(aliases)s)" % self.__dict__
    # end def __str__
    __repr__ = __str__

# end class MID

class OLSR_Parser (Parser) :
    re_mid_head  = re.compile (r"IP address\s+Aliases")
    re_topo_head = re.compile \
        (r"Dest. IP\s+Last hop\s+IP\s+LQ\s+NLQ\s+Cost")
    n            = r"([0-9.]+)"
    re_topo_line = re.compile (r"^" + r"\s+".join ([n] * 5) + r"$")
    re_mid_line  = re.compile (r"^%s\s+(%s\s*(;\s*%s)*)$" % (n, n, n))
    matrix = \
        [ ["init",      "Table: MID",      "mid_tbl",   "push"]
        , ["init",      "Table: Topology", "topo_tbl",  "push"]
        , ["init",      None,              "init",      None]
        , ["mid_tbl",   re_mid_head,       "mid_line",  None]
        , ["topo_tbl",  re_topo_head,      "topo_line", None]
        , ["mid_line",  re_mid_line,       "mid_line",  "mid_line"]
        , ["mid_line",  None,              "init",      "pop"]
        , ["topo_line", re_topo_line,      "topo_line", "topo_line"]
        , ["topo_line", None,              "init",      "pop"]
        ]

    def __init__ (self, *args, **kw) :
        self.mids  = []
        self.topo = []
        self.__super.__init__ (*args, **kw)
    # end def __init__

    def mid_line (self, state, new_state, match) :
        aliases = (x.strip () for x in match.group (2).split (';'))
        m = MID (match.group (1), *aliases)
        self.mids.append (m)
    # end def mid_line

    def topo_line (self, state, new_state, match) :
        t = Topology \
            ( match.group (1)
            , match.group (2)
            , float (match.group (3))
            , float (match.group (4))
            , float (match.group (5))
            )
        self.topo.append (t)
    # end def topo_line

# end class OLSR_Parser

if __name__ == "__main__" :
    import sys
    f = open (sys.argv [1])
    parser = OLSR_Parser ()
    parser.parse (f)
    for t in parser.topo :
        print t
    for m in parser.mids :
        print m
