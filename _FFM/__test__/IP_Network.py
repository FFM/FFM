# -*- coding: iso-8859-15 -*-
# Copyright (C) 2013 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package FFM.__test__.
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
#
#++
# Name
#    FFM.__test__.IP_Network
#
# Purpose
#    Test IP_Network
#
# Revision Dates
#    26-Jan-2013 (CT) Creation
#     4-Mar-2013 (CT) Add tests for `allocate`
#     5-Mar-2013 (CT) Add tests for `reserve`
#     5-Mar-2013 (CT) Add `electric`
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _FFM.__test__.model      import *
from   datetime                 import datetime

_test_code = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...

    >>> FFM = scope.FFM
    >>> PAP = scope.PAP
    >>> Adr = FFM.IP4_Network.net_address.P_Type

    >>> ff  = PAP.Association ("Funkfeuer", short_name = "0xFF", raw = True)
    >>> mg  = PAP.Person ("Glueck", "Martin", raw = True)
    >>> ak  = PAP.Person ("Kaplan", "Aaron", raw = True)
    >>> rs  = PAP.Person ("Schlatterbeck", "Ralf", raw = True)
    >>> ct  = PAP.Person ("Tanzer", "Christian", raw = True)
    >>> lt  = PAP.Person ("Tanzer", "Laurens", raw = True)
    >>> osc = PAP.Company ("Open Source Consulting", raw = True)

    >>> show_networks (scope) ### nothing allocated yet

    >>> ff_pool  = FFM.IP4_Network (('10.0.0.0/8', ), owner = ff, raw = True)
    >>> show_networks (scope) ### 10.0.0.0/8
    10.0.0.0/8         Funkfeuer                : electric = F, children = F

    >>> show_network_count (scope)
    FFM.IP4_Network count: 1

    >>> osc_pool = ff_pool.allocate (16, osc)
    >>> show_networks (scope) ### 10.0.0.0/16
    10.0.0.0/8         Funkfeuer                : electric = F, children = T
    10.0.0.0/16        Open Source Consulting   : electric = F, children = F
    10.0.0.0/9         Funkfeuer                : electric = T, children = T
    10.0.0.0/10        Funkfeuer                : electric = T, children = T
    10.0.0.0/11        Funkfeuer                : electric = T, children = T
    10.0.0.0/12        Funkfeuer                : electric = T, children = T
    10.0.0.0/13        Funkfeuer                : electric = T, children = T
    10.0.0.0/14        Funkfeuer                : electric = T, children = T
    10.0.0.0/15        Funkfeuer                : electric = T, children = T
    10.128.0.0/9       Funkfeuer                : electric = T, children = F
    10.64.0.0/10       Funkfeuer                : electric = T, children = F
    10.32.0.0/11       Funkfeuer                : electric = T, children = F
    10.16.0.0/12       Funkfeuer                : electric = T, children = F
    10.8.0.0/13        Funkfeuer                : electric = T, children = F
    10.4.0.0/14        Funkfeuer                : electric = T, children = F
    10.2.0.0/15        Funkfeuer                : electric = T, children = F
    10.1.0.0/16        Funkfeuer                : electric = T, children = F

    >>> show_network_count (scope)
    FFM.IP4_Network count: 17

    >>> rs_pool = osc_pool.allocate (28, rs)
    >>> show_networks (scope, pool = osc_pool) ### 10.0.0.0/28
    10.0.0.0/16        Open Source Consulting   : electric = F, children = T
    10.0.0.0/28        Schlatterbeck Ralf       : electric = F, children = F
    10.0.0.0/17        Open Source Consulting   : electric = T, children = T
    10.0.0.0/18        Open Source Consulting   : electric = T, children = T
    10.0.0.0/19        Open Source Consulting   : electric = T, children = T
    10.0.0.0/20        Open Source Consulting   : electric = T, children = T
    10.0.0.0/21        Open Source Consulting   : electric = T, children = T
    10.0.0.0/22        Open Source Consulting   : electric = T, children = T
    10.0.0.0/23        Open Source Consulting   : electric = T, children = T
    10.0.0.0/24        Open Source Consulting   : electric = T, children = T
    10.0.0.0/25        Open Source Consulting   : electric = T, children = T
    10.0.0.0/26        Open Source Consulting   : electric = T, children = T
    10.0.0.0/27        Open Source Consulting   : electric = T, children = T
    10.0.128.0/17      Open Source Consulting   : electric = T, children = F
    10.0.64.0/18       Open Source Consulting   : electric = T, children = F
    10.0.32.0/19       Open Source Consulting   : electric = T, children = F
    10.0.16.0/20       Open Source Consulting   : electric = T, children = F
    10.0.8.0/21        Open Source Consulting   : electric = T, children = F
    10.0.4.0/22        Open Source Consulting   : electric = T, children = F
    10.0.2.0/23        Open Source Consulting   : electric = T, children = F
    10.0.1.0/24        Open Source Consulting   : electric = T, children = F
    10.0.0.128/25      Open Source Consulting   : electric = T, children = F
    10.0.0.64/26       Open Source Consulting   : electric = T, children = F
    10.0.0.32/27       Open Source Consulting   : electric = T, children = F
    10.0.0.16/28       Open Source Consulting   : electric = T, children = F

    >>> ct_addr = osc_pool.reserve (Adr ('10.0.0.1/32', raw = True), owner = ct)
    Traceback (most recent call last):
      ...
    Address_Already_Used: Address ("10.0.0.1", ) already in use by 'Schlatterbeck Ralf'

    >>> show_networks (scope, pool = rs_pool) ### 10.0.0.0/28
    10.0.0.0/28        Schlatterbeck Ralf       : electric = F, children = F

    >>> show_network_count (scope)
    FFM.IP4_Network count: 41

    >>> ct_pool = rs_pool.allocate (30, ct)
    >>> show_networks (scope, pool = rs_pool) ### 10.0.0.0/30
    10.0.0.0/28        Schlatterbeck Ralf       : electric = F, children = T
    10.0.0.0/30        Tanzer Christian         : electric = F, children = F
    10.0.0.0/29        Schlatterbeck Ralf       : electric = T, children = T
    10.0.0.8/29        Schlatterbeck Ralf       : electric = T, children = F
    10.0.0.4/30        Schlatterbeck Ralf       : electric = T, children = F

    >>> ak_pool = rs_pool.allocate (28, ak)
    Traceback (most recent call last):
      ...
    No_Free_Address_Range: Address range [("10.0.0.0/28", )] of this IP4_Network doesn't contain a free subrange for mask length 28

    >>> ak_pool = rs_pool.allocate (30, ak)
    >>> show_networks (scope, pool = rs_pool) ### 10.0.0.4/30
    10.0.0.0/28        Schlatterbeck Ralf       : electric = F, children = T
    10.0.0.0/30        Tanzer Christian         : electric = F, children = F
    10.0.0.4/30        Kaplan Aaron             : electric = F, children = F
    10.0.0.0/29        Schlatterbeck Ralf       : electric = T, children = T
    10.0.0.8/29        Schlatterbeck Ralf       : electric = T, children = F

    >>> show_network_count (scope)
    FFM.IP4_Network count: 45

    >>> mg_pool = rs_pool.allocate (29, mg)
    >>> show_networks (scope, pool = rs_pool) ### 10.0.0.8/29
    10.0.0.0/28        Schlatterbeck Ralf       : electric = F, children = T
    10.0.0.8/29        Glueck Martin            : electric = F, children = F
    10.0.0.0/30        Tanzer Christian         : electric = F, children = F
    10.0.0.4/30        Kaplan Aaron             : electric = F, children = F
    10.0.0.0/29        Schlatterbeck Ralf       : electric = T, children = T

    >>> xx_pool = rs_pool.allocate (30, mg)
    Traceback (most recent call last):
      ...
    No_Free_Address_Range: Address range [("10.0.0.0/28", )] of this IP4_Network doesn't contain a free subrange for mask length 30

    >>> yy_pool = mg_pool.allocate (29, mg)
    Traceback (most recent call last):
      ...
    No_Free_Address_Range: Address range [("10.0.0.8/29", )] of this IP4_Network doesn't contain a free subrange for mask length 29

    >>> show_network_count (scope)
    FFM.IP4_Network count: 45

    >>> mg_addr = ct_pool.reserve (Adr ('10.0.0.1/32', raw = True), owner = mg)
    >>> show_networks (scope, pool = rs_pool) ### 10.0.0.1/32
    10.0.0.0/28        Schlatterbeck Ralf       : electric = F, children = T
    10.0.0.0/30        Tanzer Christian         : electric = F, children = T
    10.0.0.8/29        Glueck Martin            : electric = F, children = F
    10.0.0.4/30        Kaplan Aaron             : electric = F, children = F
    10.0.0.1           Glueck Martin            : electric = F, children = F
    10.0.0.0/29        Schlatterbeck Ralf       : electric = T, children = T
    10.0.0.0/31        Tanzer Christian         : electric = T, children = T
    10.0.0.2/31        Tanzer Christian         : electric = T, children = F
    10.0.0.0           Tanzer Christian         : electric = T, children = F

    >>> lt_addr = ct_pool.reserve (Adr ('10.0.0.2/32', raw = True), owner = lt)
    >>> show_networks (scope, pool = rs_pool) ### 10.0.0.2/32
    10.0.0.0/28        Schlatterbeck Ralf       : electric = F, children = T
    10.0.0.0/30        Tanzer Christian         : electric = F, children = T
    10.0.0.8/29        Glueck Martin            : electric = F, children = F
    10.0.0.4/30        Kaplan Aaron             : electric = F, children = F
    10.0.0.1           Glueck Martin            : electric = F, children = F
    10.0.0.2           Tanzer Laurens           : electric = F, children = F
    10.0.0.0/29        Schlatterbeck Ralf       : electric = T, children = T
    10.0.0.0/31        Tanzer Christian         : electric = T, children = T
    10.0.0.2/31        Tanzer Christian         : electric = T, children = T
    10.0.0.0           Tanzer Christian         : electric = T, children = F
    10.0.0.3           Tanzer Christian         : electric = T, children = F

    >>> rs_addr = ct_pool.reserve (Adr ('10.0.0.0/32', raw = True), owner = rs)
    >>> ct_addr = ct_pool.reserve (Adr ('10.0.0.3/32', raw = True), owner = ct)
    >>> show_networks (scope, pool = rs_pool) ### 10.0.0.3/32
    10.0.0.0/28        Schlatterbeck Ralf       : electric = F, children = T
    10.0.0.0/30        Tanzer Christian         : electric = F, children = T
    10.0.0.8/29        Glueck Martin            : electric = F, children = F
    10.0.0.4/30        Kaplan Aaron             : electric = F, children = F
    10.0.0.0           Schlatterbeck Ralf       : electric = F, children = F
    10.0.0.1           Glueck Martin            : electric = F, children = F
    10.0.0.2           Tanzer Laurens           : electric = F, children = F
    10.0.0.3           Tanzer Christian         : electric = F, children = F
    10.0.0.0/29        Schlatterbeck Ralf       : electric = T, children = T
    10.0.0.0/31        Tanzer Christian         : electric = T, children = T
    10.0.0.2/31        Tanzer Christian         : electric = T, children = T

    >>> mg_pool_2 = mg_pool.allocate (30, mg)
    >>> show_networks (scope, pool = rs_pool) ### 10.0.0.8/30
    10.0.0.0/28        Schlatterbeck Ralf       : electric = F, children = T
    10.0.0.8/29        Glueck Martin            : electric = F, children = T
    10.0.0.0/30        Tanzer Christian         : electric = F, children = T
    10.0.0.4/30        Kaplan Aaron             : electric = F, children = F
    10.0.0.8/30        Glueck Martin            : electric = F, children = F
    10.0.0.0           Schlatterbeck Ralf       : electric = F, children = F
    10.0.0.1           Glueck Martin            : electric = F, children = F
    10.0.0.2           Tanzer Laurens           : electric = F, children = F
    10.0.0.3           Tanzer Christian         : electric = F, children = F
    10.0.0.0/29        Schlatterbeck Ralf       : electric = T, children = T
    10.0.0.0/31        Tanzer Christian         : electric = T, children = T
    10.0.0.2/31        Tanzer Christian         : electric = T, children = T
    10.0.0.12/30       Glueck Martin            : electric = T, children = F

    >>> ct_addr = ff_pool.reserve (Adr ('10.42.137.1/32', raw = True), owner = ct)
    >>> show_networks (scope) ### 10.42.137.1/32
    10.0.0.0/8         Funkfeuer                : electric = F, children = T
    10.0.0.0/16        Open Source Consulting   : electric = F, children = T
    10.0.0.0/28        Schlatterbeck Ralf       : electric = F, children = T
    10.0.0.8/29        Glueck Martin            : electric = F, children = T
    10.0.0.0/30        Tanzer Christian         : electric = F, children = T
    10.0.0.4/30        Kaplan Aaron             : electric = F, children = F
    10.0.0.8/30        Glueck Martin            : electric = F, children = F
    10.0.0.0           Schlatterbeck Ralf       : electric = F, children = F
    10.0.0.1           Glueck Martin            : electric = F, children = F
    10.0.0.2           Tanzer Laurens           : electric = F, children = F
    10.0.0.3           Tanzer Christian         : electric = F, children = F
    10.42.137.1        Tanzer Christian         : electric = F, children = F
    10.0.0.0/9         Funkfeuer                : electric = T, children = T
    10.0.0.0/10        Funkfeuer                : electric = T, children = T
    10.0.0.0/11        Funkfeuer                : electric = T, children = T
    10.32.0.0/11       Funkfeuer                : electric = T, children = T
    10.0.0.0/12        Funkfeuer                : electric = T, children = T
    10.32.0.0/12       Funkfeuer                : electric = T, children = T
    10.0.0.0/13        Funkfeuer                : electric = T, children = T
    10.40.0.0/13       Funkfeuer                : electric = T, children = T
    10.0.0.0/14        Funkfeuer                : electric = T, children = T
    10.40.0.0/14       Funkfeuer                : electric = T, children = T
    10.0.0.0/15        Funkfeuer                : electric = T, children = T
    10.42.0.0/15       Funkfeuer                : electric = T, children = T
    10.42.0.0/16       Funkfeuer                : electric = T, children = T
    10.0.0.0/17        Open Source Consulting   : electric = T, children = T
    10.42.128.0/17     Funkfeuer                : electric = T, children = T
    10.0.0.0/18        Open Source Consulting   : electric = T, children = T
    10.42.128.0/18     Funkfeuer                : electric = T, children = T
    10.0.0.0/19        Open Source Consulting   : electric = T, children = T
    10.42.128.0/19     Funkfeuer                : electric = T, children = T
    10.0.0.0/20        Open Source Consulting   : electric = T, children = T
    10.42.128.0/20     Funkfeuer                : electric = T, children = T
    10.0.0.0/21        Open Source Consulting   : electric = T, children = T
    10.42.136.0/21     Funkfeuer                : electric = T, children = T
    10.0.0.0/22        Open Source Consulting   : electric = T, children = T
    10.42.136.0/22     Funkfeuer                : electric = T, children = T
    10.0.0.0/23        Open Source Consulting   : electric = T, children = T
    10.42.136.0/23     Funkfeuer                : electric = T, children = T
    10.0.0.0/24        Open Source Consulting   : electric = T, children = T
    10.42.137.0/24     Funkfeuer                : electric = T, children = T
    10.0.0.0/25        Open Source Consulting   : electric = T, children = T
    10.42.137.0/25     Funkfeuer                : electric = T, children = T
    10.0.0.0/26        Open Source Consulting   : electric = T, children = T
    10.42.137.0/26     Funkfeuer                : electric = T, children = T
    10.0.0.0/27        Open Source Consulting   : electric = T, children = T
    10.42.137.0/27     Funkfeuer                : electric = T, children = T
    10.42.137.0/28     Funkfeuer                : electric = T, children = T
    10.0.0.0/29        Schlatterbeck Ralf       : electric = T, children = T
    10.42.137.0/29     Funkfeuer                : electric = T, children = T
    10.42.137.0/30     Funkfeuer                : electric = T, children = T
    10.0.0.0/31        Tanzer Christian         : electric = T, children = T
    10.0.0.2/31        Tanzer Christian         : electric = T, children = T
    10.42.137.0/31     Funkfeuer                : electric = T, children = T
    10.128.0.0/9       Funkfeuer                : electric = T, children = F
    10.64.0.0/10       Funkfeuer                : electric = T, children = F
    10.16.0.0/12       Funkfeuer                : electric = T, children = F
    10.48.0.0/12       Funkfeuer                : electric = T, children = F
    10.8.0.0/13        Funkfeuer                : electric = T, children = F
    10.32.0.0/13       Funkfeuer                : electric = T, children = F
    10.4.0.0/14        Funkfeuer                : electric = T, children = F
    10.44.0.0/14       Funkfeuer                : electric = T, children = F
    10.2.0.0/15        Funkfeuer                : electric = T, children = F
    10.40.0.0/15       Funkfeuer                : electric = T, children = F
    10.1.0.0/16        Funkfeuer                : electric = T, children = F
    10.43.0.0/16       Funkfeuer                : electric = T, children = F
    10.0.128.0/17      Open Source Consulting   : electric = T, children = F
    10.42.0.0/17       Funkfeuer                : electric = T, children = F
    10.0.64.0/18       Open Source Consulting   : electric = T, children = F
    10.42.192.0/18     Funkfeuer                : electric = T, children = F
    10.0.32.0/19       Open Source Consulting   : electric = T, children = F
    10.42.160.0/19     Funkfeuer                : electric = T, children = F
    10.0.16.0/20       Open Source Consulting   : electric = T, children = F
    10.42.144.0/20     Funkfeuer                : electric = T, children = F
    10.0.8.0/21        Open Source Consulting   : electric = T, children = F
    10.42.128.0/21     Funkfeuer                : electric = T, children = F
    10.0.4.0/22        Open Source Consulting   : electric = T, children = F
    10.42.140.0/22     Funkfeuer                : electric = T, children = F
    10.0.2.0/23        Open Source Consulting   : electric = T, children = F
    10.42.138.0/23     Funkfeuer                : electric = T, children = F
    10.0.1.0/24        Open Source Consulting   : electric = T, children = F
    10.42.136.0/24     Funkfeuer                : electric = T, children = F
    10.0.0.128/25      Open Source Consulting   : electric = T, children = F
    10.42.137.128/25   Funkfeuer                : electric = T, children = F
    10.0.0.64/26       Open Source Consulting   : electric = T, children = F
    10.42.137.64/26    Funkfeuer                : electric = T, children = F
    10.0.0.32/27       Open Source Consulting   : electric = T, children = F
    10.42.137.32/27    Funkfeuer                : electric = T, children = F
    10.0.0.16/28       Open Source Consulting   : electric = T, children = F
    10.42.137.16/28    Funkfeuer                : electric = T, children = F
    10.42.137.8/29     Funkfeuer                : electric = T, children = F
    10.0.0.12/30       Glueck Martin            : electric = T, children = F
    10.42.137.4/30     Funkfeuer                : electric = T, children = F
    10.42.137.2/31     Funkfeuer                : electric = T, children = F
    10.42.137.0        Funkfeuer                : electric = T, children = F

    >>> show_network_count (scope)
    FFM.IP4_Network count: 95

"""

def show_networks (scope, * qargs, ** qkw) :
    ETM = scope.FFM.IP4_Network
    sk = TFL.Sorted_By \
        ( "electric", "-has_children"
        , * tuple
            ( ".".join (("net_address", c))
            for c in ETM.net_address.P_Type.sort_key_address.criteria
            )
        )
    pool = qkw.pop ("pool", None)
    if pool is not None :
        qargs += (Q.net_address.IN (pool.net_address), )
    for nw in ETM.query (* qargs, sort_key = sk, ** qkw) :
        print \
            ( "%-18s %-25s: electric = %1.1s, children = %1.1s"
            % (nw.FO.net_address, nw.FO.owner, nw.electric, nw.has_children)
            )
# end def show_networks

def show_network_count (scope) :
    ETM = scope.FFM.IP4_Network
    print ("%s count: %s" % (ETM.type_name, ETM.count))
# end def show_network_count

__test__ = Scaffold.create_test_dict \
  ( dict
      ( main       = _test_code
      )
  )

### __END__ FFM.__test__.IP_Network
