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

from   rsclib.autosuper   import autosuper
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
