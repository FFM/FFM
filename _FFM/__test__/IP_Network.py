# -*- coding: utf-8 -*-
# Copyright (C) 2013-2014 Mag. Christian Tanzer All rights reserved
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
#     7-Mar-2013 (RS) Test for previously failing `CONTAINS` query
#    19-Mar-2013 (CT) Add test case `test_AQ`
#    22-Mar-2013 (CT) Add test for `Query_Restriction`
#    28-Mar-2013 (CT) Add `AQ.Attrs_Transitive...ui_name`, `.pool.pool.pool...`
#    11-Apr-2013 (CT) Adapt to changes in `MOM.Attr.Querier`
#    28-Apr-2013 (CT) Adapt to addition of `IP_Network.desc`
#     7-Aug-2013 (CT) Adapt to major surgery of GTW.OMP.NET.Attr_Type
#    13-Aug-2013 (CT) Add `test_order`, adapt other tests to change in order
#    22-Aug-2013 (CT) Add tests for I4N and I6N calls with wrong `raw` value
#     7-Oct-2013 (CT) Add tests for `belongs_to_node`
#     8-Apr-2014 (RS) Test failing allocation in sub-pool
#    14-Apr-2014 (CT) Rename `belongs_to_node` to `my_node`
#    25-Apr-2014 (RS) Add `_test_partial`
#    13-Jun-2014 (RS) Fixes for new `PAP` objects, renaming of
#                     `IP_Network.cool_down`, `Node` no longer derived
#                     from `Subject`, addition of `Node.desc`, `ui_name`
#                     for `desc`
#    14-Jun-2014 (RS) Add `node` to `IP_Network`
#    20-Jun-2014 (RS) `IP_Pool` and derivatives, `node` moved to `IP_Pool`
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _FFM.__test__.model      import *
from   datetime                 import datetime

import _GTW._RST._TOP._MOM.Query_Restriction

from _FFM.__test__.fixtures import net_fixtures, create as std_fixtures

_test_alloc = """
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

    >>> ETM = scope.FFM.IP4_Network
    >>> show_networks (scope, ETM) ### nothing allocated yet

    >>> ff_pool  = FFM.IP4_Network ('10.0.0.0/8', owner = ff, raw = True)
    >>> show_networks (scope, ETM) ### 10.0.0.0/8
    10.0.0.0/8         Funkfeuer                : electric = F, children = F

    >>> show_network_count (scope, ETM)
    FFM.IP4_Network count: 1

    >>> osc_pool = ff_pool.allocate (16, osc)
    >>> show_networks (scope, ETM) ### 10.0.0.0/16
    10.0.0.0/8         Funkfeuer                : electric = F, children = T
    10.0.0.0/16        Open Source Consulting   : electric = F, children = F
    10.0.0.0/9         Funkfeuer                : electric = T, children = T
    10.0.0.0/10        Funkfeuer                : electric = T, children = T
    10.0.0.0/11        Funkfeuer                : electric = T, children = T
    10.0.0.0/12        Funkfeuer                : electric = T, children = T
    10.0.0.0/13        Funkfeuer                : electric = T, children = T
    10.0.0.0/14        Funkfeuer                : electric = T, children = T
    10.0.0.0/15        Funkfeuer                : electric = T, children = T
    10.1.0.0/16        Funkfeuer                : electric = T, children = F
    10.2.0.0/15        Funkfeuer                : electric = T, children = F
    10.4.0.0/14        Funkfeuer                : electric = T, children = F
    10.8.0.0/13        Funkfeuer                : electric = T, children = F
    10.16.0.0/12       Funkfeuer                : electric = T, children = F
    10.32.0.0/11       Funkfeuer                : electric = T, children = F
    10.64.0.0/10       Funkfeuer                : electric = T, children = F
    10.128.0.0/9       Funkfeuer                : electric = T, children = F

    >>> show_network_count (scope, ETM)
    FFM.IP4_Network count: 17

    >>> rs_pool = osc_pool.allocate (28, rs)
    >>> show_networks (scope, ETM, pool = osc_pool) ### 10.0.0.0/28
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
    10.0.0.16/28       Open Source Consulting   : electric = T, children = F
    10.0.0.32/27       Open Source Consulting   : electric = T, children = F
    10.0.0.64/26       Open Source Consulting   : electric = T, children = F
    10.0.0.128/25      Open Source Consulting   : electric = T, children = F
    10.0.1.0/24        Open Source Consulting   : electric = T, children = F
    10.0.2.0/23        Open Source Consulting   : electric = T, children = F
    10.0.4.0/22        Open Source Consulting   : electric = T, children = F
    10.0.8.0/21        Open Source Consulting   : electric = T, children = F
    10.0.16.0/20       Open Source Consulting   : electric = T, children = F
    10.0.32.0/19       Open Source Consulting   : electric = T, children = F
    10.0.64.0/18       Open Source Consulting   : electric = T, children = F
    10.0.128.0/17      Open Source Consulting   : electric = T, children = F

    >>> ct_addr = osc_pool.reserve ('10.0.0.1/32', owner = ct)
    Traceback (most recent call last):
      ...
    Address_Already_Used: Address 10.0.0.1 already in use by 'Schlatterbeck Ralf'

    >>> show_networks (scope, ETM, pool = rs_pool) ### 10.0.0.0/28
    10.0.0.0/28        Schlatterbeck Ralf       : electric = F, children = F

    >>> show_network_count (scope, ETM)
    FFM.IP4_Network count: 41

    >>> ct_pool = rs_pool.allocate (30, ct)
    >>> show_networks (scope, ETM, pool = rs_pool) ### 10.0.0.0/30 ct
    10.0.0.0/28        Schlatterbeck Ralf       : electric = F, children = T
    10.0.0.0/30        Tanzer Christian         : electric = F, children = F
    10.0.0.0/29        Schlatterbeck Ralf       : electric = T, children = T
    10.0.0.4/30        Schlatterbeck Ralf       : electric = T, children = F
    10.0.0.8/29        Schlatterbeck Ralf       : electric = T, children = F

    >>> ak_pool = rs_pool.allocate (28, ak)
    Traceback (most recent call last):
      ...
    No_Free_Address_Range: Address range [10.0.0.0/28] of this IP4_Network doesn't contain a free subrange for mask length 28

    >>> show_networks (scope, ETM, pool = rs_pool) ### 10.0.0.0/30 ct after alloc error
    10.0.0.0/28        Schlatterbeck Ralf       : electric = F, children = T
    10.0.0.0/30        Tanzer Christian         : electric = F, children = F
    10.0.0.0/29        Schlatterbeck Ralf       : electric = T, children = T
    10.0.0.4/30        Schlatterbeck Ralf       : electric = T, children = F
    10.0.0.8/29        Schlatterbeck Ralf       : electric = T, children = F

    >>> for a, m in ETM.query (Q.net_address.IN (rs_pool.net_address), sort_key = TFL.Sorted_By ("-net_address.mask_len", "net_address")).attrs ("net_address", "net_address.mask_len") :
    ...     print (a, m)
    10.0.0.0/30 30
    10.0.0.4/30 30
    10.0.0.0/29 29
    10.0.0.8/29 29
    10.0.0.0/28 28

    >>> ak_pool = rs_pool.allocate (30, ak)
    >>> show_networks (scope, ETM, pool = rs_pool) ### 10.0.0.4/30 ct+ak
    10.0.0.0/28        Schlatterbeck Ralf       : electric = F, children = T
    10.0.0.0/30        Tanzer Christian         : electric = F, children = F
    10.0.0.4/30        Kaplan Aaron             : electric = F, children = F
    10.0.0.0/29        Schlatterbeck Ralf       : electric = T, children = T
    10.0.0.8/29        Schlatterbeck Ralf       : electric = T, children = F

    >>> show_network_count (scope, ETM)
    FFM.IP4_Network count: 45

    >>> mg_pool = rs_pool.allocate (29, mg)
    >>> show_networks (scope, ETM, pool = rs_pool) ### 10.0.0.8/29
    10.0.0.0/28        Schlatterbeck Ralf       : electric = F, children = T
    10.0.0.0/30        Tanzer Christian         : electric = F, children = F
    10.0.0.4/30        Kaplan Aaron             : electric = F, children = F
    10.0.0.8/29        Glueck Martin            : electric = F, children = F
    10.0.0.0/29        Schlatterbeck Ralf       : electric = T, children = T

    >>> xx_pool = rs_pool.allocate (30, mg)
    Traceback (most recent call last):
      ...
    No_Free_Address_Range: Address range [10.0.0.0/28] of this IP4_Network doesn't contain a free subrange for mask length 30

    >>> yy_pool = mg_pool.allocate (29, mg)
    Traceback (most recent call last):
      ...
    No_Free_Address_Range: Address range [10.0.0.8/29] of this IP4_Network doesn't contain a free subrange for mask length 29

    >>> show_network_count (scope, ETM)
    FFM.IP4_Network count: 45

    >>> mg_addr = ct_pool.reserve ('10.0.0.1/32', owner = mg)
    >>> show_networks (scope, ETM, pool = rs_pool) ### 10.0.0.1/32
    10.0.0.0/28        Schlatterbeck Ralf       : electric = F, children = T
    10.0.0.0/30        Tanzer Christian         : electric = F, children = T
    10.0.0.1           Glueck Martin            : electric = F, children = F
    10.0.0.4/30        Kaplan Aaron             : electric = F, children = F
    10.0.0.8/29        Glueck Martin            : electric = F, children = F
    10.0.0.0/29        Schlatterbeck Ralf       : electric = T, children = T
    10.0.0.0/31        Tanzer Christian         : electric = T, children = T
    10.0.0.0           Tanzer Christian         : electric = T, children = F
    10.0.0.2/31        Tanzer Christian         : electric = T, children = F

    >>> lt_addr = ct_pool.reserve ('10.0.0.2/32', owner = lt)
    >>> show_networks (scope, ETM, pool = rs_pool) ### 10.0.0.2/32
    10.0.0.0/28        Schlatterbeck Ralf       : electric = F, children = T
    10.0.0.0/30        Tanzer Christian         : electric = F, children = T
    10.0.0.1           Glueck Martin            : electric = F, children = F
    10.0.0.2           Tanzer Laurens           : electric = F, children = F
    10.0.0.4/30        Kaplan Aaron             : electric = F, children = F
    10.0.0.8/29        Glueck Martin            : electric = F, children = F
    10.0.0.0/29        Schlatterbeck Ralf       : electric = T, children = T
    10.0.0.0/31        Tanzer Christian         : electric = T, children = T
    10.0.0.2/31        Tanzer Christian         : electric = T, children = T
    10.0.0.0           Tanzer Christian         : electric = T, children = F
    10.0.0.3           Tanzer Christian         : electric = T, children = F

    >>> rs_addr = ct_pool.reserve ('10.0.0.0/32', owner = rs)
    >>> ct_addr = ct_pool.reserve (Adr ('10.0.0.3/32'), owner = ct)
    >>> show_networks (scope, ETM, pool = rs_pool) ### 10.0.0.3/32
    10.0.0.0/28        Schlatterbeck Ralf       : electric = F, children = T
    10.0.0.0/30        Tanzer Christian         : electric = F, children = T
    10.0.0.0           Schlatterbeck Ralf       : electric = F, children = F
    10.0.0.1           Glueck Martin            : electric = F, children = F
    10.0.0.2           Tanzer Laurens           : electric = F, children = F
    10.0.0.3           Tanzer Christian         : electric = F, children = F
    10.0.0.4/30        Kaplan Aaron             : electric = F, children = F
    10.0.0.8/29        Glueck Martin            : electric = F, children = F
    10.0.0.0/29        Schlatterbeck Ralf       : electric = T, children = T
    10.0.0.0/31        Tanzer Christian         : electric = T, children = T
    10.0.0.2/31        Tanzer Christian         : electric = T, children = T

    >>> mg_pool_2 = mg_pool.allocate (30, mg)
    >>> show_networks (scope, ETM, pool = rs_pool) ### 10.0.0.8/30
    10.0.0.0/28        Schlatterbeck Ralf       : electric = F, children = T
    10.0.0.0/30        Tanzer Christian         : electric = F, children = T
    10.0.0.8/29        Glueck Martin            : electric = F, children = T
    10.0.0.0           Schlatterbeck Ralf       : electric = F, children = F
    10.0.0.1           Glueck Martin            : electric = F, children = F
    10.0.0.2           Tanzer Laurens           : electric = F, children = F
    10.0.0.3           Tanzer Christian         : electric = F, children = F
    10.0.0.4/30        Kaplan Aaron             : electric = F, children = F
    10.0.0.8/30        Glueck Martin            : electric = F, children = F
    10.0.0.0/29        Schlatterbeck Ralf       : electric = T, children = T
    10.0.0.0/31        Tanzer Christian         : electric = T, children = T
    10.0.0.2/31        Tanzer Christian         : electric = T, children = T
    10.0.0.12/30       Glueck Martin            : electric = T, children = F

    >>> ct_addr = ff_pool.reserve (Adr ('10.42.137.1/32'), owner = ct)
    >>> show_networks (scope, ETM) ### 10.42.137.1/32
    10.0.0.0/8         Funkfeuer                : electric = F, children = T
    10.0.0.0/16        Open Source Consulting   : electric = F, children = T
    10.0.0.0/28        Schlatterbeck Ralf       : electric = F, children = T
    10.0.0.0/30        Tanzer Christian         : electric = F, children = T
    10.0.0.8/29        Glueck Martin            : electric = F, children = T
    10.0.0.0           Schlatterbeck Ralf       : electric = F, children = F
    10.0.0.1           Glueck Martin            : electric = F, children = F
    10.0.0.2           Tanzer Laurens           : electric = F, children = F
    10.0.0.3           Tanzer Christian         : electric = F, children = F
    10.0.0.4/30        Kaplan Aaron             : electric = F, children = F
    10.0.0.8/30        Glueck Martin            : electric = F, children = F
    10.42.137.1        Tanzer Christian         : electric = F, children = F
    10.0.0.0/9         Funkfeuer                : electric = T, children = T
    10.0.0.0/10        Funkfeuer                : electric = T, children = T
    10.0.0.0/11        Funkfeuer                : electric = T, children = T
    10.0.0.0/12        Funkfeuer                : electric = T, children = T
    10.0.0.0/13        Funkfeuer                : electric = T, children = T
    10.0.0.0/14        Funkfeuer                : electric = T, children = T
    10.0.0.0/15        Funkfeuer                : electric = T, children = T
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
    10.0.0.0/29        Schlatterbeck Ralf       : electric = T, children = T
    10.0.0.0/31        Tanzer Christian         : electric = T, children = T
    10.0.0.2/31        Tanzer Christian         : electric = T, children = T
    10.32.0.0/11       Funkfeuer                : electric = T, children = T
    10.32.0.0/12       Funkfeuer                : electric = T, children = T
    10.40.0.0/13       Funkfeuer                : electric = T, children = T
    10.40.0.0/14       Funkfeuer                : electric = T, children = T
    10.42.0.0/15       Funkfeuer                : electric = T, children = T
    10.42.0.0/16       Funkfeuer                : electric = T, children = T
    10.42.128.0/17     Funkfeuer                : electric = T, children = T
    10.42.128.0/18     Funkfeuer                : electric = T, children = T
    10.42.128.0/19     Funkfeuer                : electric = T, children = T
    10.42.128.0/20     Funkfeuer                : electric = T, children = T
    10.42.136.0/21     Funkfeuer                : electric = T, children = T
    10.42.136.0/22     Funkfeuer                : electric = T, children = T
    10.42.136.0/23     Funkfeuer                : electric = T, children = T
    10.42.137.0/24     Funkfeuer                : electric = T, children = T
    10.42.137.0/25     Funkfeuer                : electric = T, children = T
    10.42.137.0/26     Funkfeuer                : electric = T, children = T
    10.42.137.0/27     Funkfeuer                : electric = T, children = T
    10.42.137.0/28     Funkfeuer                : electric = T, children = T
    10.42.137.0/29     Funkfeuer                : electric = T, children = T
    10.42.137.0/30     Funkfeuer                : electric = T, children = T
    10.42.137.0/31     Funkfeuer                : electric = T, children = T
    10.0.0.12/30       Glueck Martin            : electric = T, children = F
    10.0.0.16/28       Open Source Consulting   : electric = T, children = F
    10.0.0.32/27       Open Source Consulting   : electric = T, children = F
    10.0.0.64/26       Open Source Consulting   : electric = T, children = F
    10.0.0.128/25      Open Source Consulting   : electric = T, children = F
    10.0.1.0/24        Open Source Consulting   : electric = T, children = F
    10.0.2.0/23        Open Source Consulting   : electric = T, children = F
    10.0.4.0/22        Open Source Consulting   : electric = T, children = F
    10.0.8.0/21        Open Source Consulting   : electric = T, children = F
    10.0.16.0/20       Open Source Consulting   : electric = T, children = F
    10.0.32.0/19       Open Source Consulting   : electric = T, children = F
    10.0.64.0/18       Open Source Consulting   : electric = T, children = F
    10.0.128.0/17      Open Source Consulting   : electric = T, children = F
    10.1.0.0/16        Funkfeuer                : electric = T, children = F
    10.2.0.0/15        Funkfeuer                : electric = T, children = F
    10.4.0.0/14        Funkfeuer                : electric = T, children = F
    10.8.0.0/13        Funkfeuer                : electric = T, children = F
    10.16.0.0/12       Funkfeuer                : electric = T, children = F
    10.32.0.0/13       Funkfeuer                : electric = T, children = F
    10.40.0.0/15       Funkfeuer                : electric = T, children = F
    10.42.0.0/17       Funkfeuer                : electric = T, children = F
    10.42.128.0/21     Funkfeuer                : electric = T, children = F
    10.42.136.0/24     Funkfeuer                : electric = T, children = F
    10.42.137.0        Funkfeuer                : electric = T, children = F
    10.42.137.2/31     Funkfeuer                : electric = T, children = F
    10.42.137.4/30     Funkfeuer                : electric = T, children = F
    10.42.137.8/29     Funkfeuer                : electric = T, children = F
    10.42.137.16/28    Funkfeuer                : electric = T, children = F
    10.42.137.32/27    Funkfeuer                : electric = T, children = F
    10.42.137.64/26    Funkfeuer                : electric = T, children = F
    10.42.137.128/25   Funkfeuer                : electric = T, children = F
    10.42.138.0/23     Funkfeuer                : electric = T, children = F
    10.42.140.0/22     Funkfeuer                : electric = T, children = F
    10.42.144.0/20     Funkfeuer                : electric = T, children = F
    10.42.160.0/19     Funkfeuer                : electric = T, children = F
    10.42.192.0/18     Funkfeuer                : electric = T, children = F
    10.43.0.0/16       Funkfeuer                : electric = T, children = F
    10.44.0.0/14       Funkfeuer                : electric = T, children = F
    10.48.0.0/12       Funkfeuer                : electric = T, children = F
    10.64.0.0/10       Funkfeuer                : electric = T, children = F
    10.128.0.0/9       Funkfeuer                : electric = T, children = F

    >>> show_network_count (scope, ETM)
    FFM.IP4_Network count: 95

    >>> ETM = FFM.IP4_Network
    >>> q   = ETM.query
    >>> n   = '10.42.137.0/28'
    >>> q (Q.net_address.IN (n)).count ()
    9

    >>> s = TFL.Sorted_By ("-net_address.mask_len")
    >>> q (Q.net_address.CONTAINS (n), sort_key = s).first ()
    FFM.IP4_Network ("10.42.137.0/28")

    >>> ETM = FFM.IP4_Network
    >>> xpool  = FFM.IP4_Network ('192.168.0.0/16', owner = ff, raw = True)
    >>> mgpool = xpool.allocate (17, mg)
    >>> ctpool = xpool.allocate (17, ct)
    >>> rspool = xpool.allocate (32, rs)
    Traceback (most recent call last):
      ...
    No_Free_Address_Range: Address range [192.168.0.0/16] of this IP4_Network doesn't contain a free subrange for mask length 32
    >>> ffpool = mgpool.allocate (22, ff)

"""

_test_partial = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...

    >>> FFM = scope.FFM
    >>> PAP = scope.PAP

    Clear the cache, how can we avoid to cache across tests??
    #>>> FFM.Net_Interface_in_IP4_Network.child_np_map = {}
    #>>> FFM.Net_Interface_in_IP4_Network.child_np_map
    #{}

    >>> ff = PAP.Association ("Funkfeuer", short_name = "0xFF", raw = True)
    >>> rs = PAP.Person ("Schlatterbeck", "Ralf", raw = True)
    >>> fp = FFM.IP4_Network ('10.0.0.0/8', owner = ff, raw = True)
    >>> a4 = fp.reserve ('10.0.0.1/32', owner = ff)
    >>> dt = FFM.Net_Device_Type.instance_or_new (name = 'G', raw = True)
    >>> n1 = FFM.Node (name = "nogps", manager = rs, raw = True)
    >>> dv = FFM.Net_Device (left = dt, node = n1, name = 'dev', raw = True)
    >>> wl = FFM.Wireless_Interface (left = dv, name = 'wl', raw = True)
    >>> scope.commit ()

    >>> il2 = FFM.Net_Interface_in_IP4_Network (wl, a4, mask_len = 24)

"""

_test_AQ = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...

    >>> FFM = scope.FFM
    >>> PAP = scope.PAP
    >>> AQ = FFM.IP4_Network.E_Type.AQ
    >>> AQ
    <Attr.Type.Querier.E_Type for FFM.IP4_Network>
    >>> for aq in AQ.Attrs :
    ...     print (aq)
    <net_address.AQ [Attr.Type.Querier Ckd]>
    <desc.AQ [Attr.Type.Querier String]>
    <owner.AQ [Attr.Type.Querier Id_Entity]>
    <creation.AQ [Attr.Type.Querier Rev_Ref]>
    <last_change.AQ [Attr.Type.Querier Rev_Ref]>
    <last_cid.AQ [Attr.Type.Querier Ckd]>
    <pid.AQ [Attr.Type.Querier Ckd]>
    <type_name.AQ [Attr.Type.Querier String]>
    <expiration_date.AQ [Attr.Type.Querier Ckd]>
    <has_children.AQ [Attr.Type.Querier Boolean]>
    <is_free.AQ [Attr.Type.Querier Boolean]>
    <parent.AQ [Attr.Type.Querier Id_Entity]>
    <ip_pool.AQ [Attr.Type.Querier Rev_Ref]>
    <net_interface.AQ [Attr.Type.Querier Rev_Ref]>
    <documents.AQ [Attr.Type.Querier Rev_Ref]>
    <wired_interface.AQ [Attr.Type.Querier Rev_Ref]>
    <wireless_interface.AQ [Attr.Type.Querier Rev_Ref]>
    <virtual_wireless_interface.AQ [Attr.Type.Querier Rev_Ref]>

    >>> for aq in AQ.Attrs_Transitive :
    ...     print (aq, aq.E_Type.type_name if aq.E_Type else "-"*5)
    <net_address.AQ [Attr.Type.Querier Ckd]> -----
    <desc.AQ [Attr.Type.Querier String]> -----
    <owner.AQ [Attr.Type.Querier Id_Entity]> PAP.Subject
    <creation.AQ [Attr.Type.Querier Rev_Ref]> MOM.MD_Change
    <creation.c_time.AQ [Attr.Type.Querier Ckd]> -----
    <creation.c_user.AQ [Attr.Type.Querier Id_Entity]> MOM.Id_Entity
    <creation.kind.AQ [Attr.Type.Querier String]> -----
    <creation.time.AQ [Attr.Type.Querier Ckd]> -----
    <creation.user.AQ [Attr.Type.Querier Id_Entity]> MOM.Id_Entity
    <last_change.AQ [Attr.Type.Querier Rev_Ref]> MOM.MD_Change
    <last_change.c_time.AQ [Attr.Type.Querier Ckd]> -----
    <last_change.c_user.AQ [Attr.Type.Querier Id_Entity]> MOM.Id_Entity
    <last_change.kind.AQ [Attr.Type.Querier String]> -----
    <last_change.time.AQ [Attr.Type.Querier Ckd]> -----
    <last_change.user.AQ [Attr.Type.Querier Id_Entity]> MOM.Id_Entity
    <last_cid.AQ [Attr.Type.Querier Ckd]> -----
    <pid.AQ [Attr.Type.Querier Ckd]> -----
    <type_name.AQ [Attr.Type.Querier String]> -----
    <expiration_date.AQ [Attr.Type.Querier Ckd]> -----
    <has_children.AQ [Attr.Type.Querier Boolean]> -----
    <is_free.AQ [Attr.Type.Querier Boolean]> -----
    <parent.AQ [Attr.Type.Querier Id_Entity]> FFM.IP4_Network
    <parent.net_address.AQ [Attr.Type.Querier Ckd]> -----
    <parent.desc.AQ [Attr.Type.Querier String]> -----
    <parent.owner.AQ [Attr.Type.Querier Id_Entity]> PAP.Subject
    <parent.expiration_date.AQ [Attr.Type.Querier Ckd]> -----
    <parent.has_children.AQ [Attr.Type.Querier Boolean]> -----
    <parent.is_free.AQ [Attr.Type.Querier Boolean]> -----
    <parent.parent.AQ [Attr.Type.Querier Id_Entity]> FFM.IP4_Network
    <ip_pool.AQ [Attr.Type.Querier Rev_Ref]> FFM.IP_Pool
    <ip_pool.netmask_interval.AQ [Attr.Type.Querier Composite]> MOM.Int_Interval_C
    <ip_pool.netmask_interval.lower.AQ [Attr.Type.Querier Ckd]> -----
    <ip_pool.netmask_interval.upper.AQ [Attr.Type.Querier Ckd]> -----
    <ip_pool.netmask_interval.center.AQ [Attr.Type.Querier Ckd]> -----
    <ip_pool.netmask_interval.length.AQ [Attr.Type.Querier Ckd]> -----
    <ip_pool.node.AQ [Attr.Type.Querier Id_Entity]> FFM.Node
    <ip_pool.node.name.AQ [Attr.Type.Querier String]> -----
    <ip_pool.node.manager.AQ [Attr.Type.Querier Id_Entity]> PAP.Person
    <ip_pool.node.manager.last_name.AQ [Attr.Type.Querier String_FL]> -----
    <ip_pool.node.manager.first_name.AQ [Attr.Type.Querier String_FL]> -----
    <ip_pool.node.manager.middle_name.AQ [Attr.Type.Querier String]> -----
    <ip_pool.node.manager.title.AQ [Attr.Type.Querier String]> -----
    <ip_pool.node.manager.lifetime.AQ [Attr.Type.Querier Composite]> MOM.Date_Interval
    <ip_pool.node.manager.lifetime.start.AQ [Attr.Type.Querier Date]> -----
    <ip_pool.node.manager.lifetime.finish.AQ [Attr.Type.Querier Date]> -----
    <ip_pool.node.manager.lifetime.alive.AQ [Attr.Type.Querier Boolean]> -----
    <ip_pool.node.manager.sex.AQ [Attr.Type.Querier Ckd]> -----
    <ip_pool.node.address.AQ [Attr.Type.Querier Id_Entity]> PAP.Address
    <ip_pool.node.address.street.AQ [Attr.Type.Querier String]> -----
    <ip_pool.node.address.zip.AQ [Attr.Type.Querier String]> -----
    <ip_pool.node.address.city.AQ [Attr.Type.Querier String]> -----
    <ip_pool.node.address.country.AQ [Attr.Type.Querier String]> -----
    <ip_pool.node.address.desc.AQ [Attr.Type.Querier String]> -----
    <ip_pool.node.address.region.AQ [Attr.Type.Querier String]> -----
    <ip_pool.node.desc.AQ [Attr.Type.Querier String]> -----
    <ip_pool.node.owner.AQ [Attr.Type.Querier Id_Entity]> PAP.Subject
    <ip_pool.node.position.AQ [Attr.Type.Querier Composite]> MOM.Position
    <ip_pool.node.position.lat.AQ [Attr.Type.Querier Raw]> -----
    <ip_pool.node.position.lon.AQ [Attr.Type.Querier Raw]> -----
    <ip_pool.node.position.height.AQ [Attr.Type.Querier Ckd]> -----
    <ip_pool.node.show_in_map.AQ [Attr.Type.Querier Boolean]> -----
    <net_interface.AQ [Attr.Type.Querier Rev_Ref]> FFM.Net_Interface
    <documents.AQ [Attr.Type.Querier Rev_Ref]> MOM.Document
    <documents.url.AQ [Attr.Type.Querier String]> -----
    <documents.type.AQ [Attr.Type.Querier String]> -----
    <documents.desc.AQ [Attr.Type.Querier String]> -----
    <wired_interface.AQ [Attr.Type.Querier Rev_Ref]> FFM.Wired_Interface
    <wired_interface.left.AQ [Attr.Type.Querier Id_Entity]> FFM.Net_Device
    <wired_interface.left.left.AQ [Attr.Type.Querier Id_Entity]> FFM.Net_Device_Type
    <wired_interface.left.left.name.AQ [Attr.Type.Querier String]> -----
    <wired_interface.left.left.model_no.AQ [Attr.Type.Querier String]> -----
    <wired_interface.left.left.revision.AQ [Attr.Type.Querier String]> -----
    <wired_interface.left.left.desc.AQ [Attr.Type.Querier String]> -----
    <wired_interface.left.node.AQ [Attr.Type.Querier Id_Entity]> FFM.Node
    <wired_interface.left.node.name.AQ [Attr.Type.Querier String]> -----
    <wired_interface.left.node.manager.AQ [Attr.Type.Querier Id_Entity]> PAP.Person
    <wired_interface.left.node.manager.last_name.AQ [Attr.Type.Querier String_FL]> -----
    <wired_interface.left.node.manager.first_name.AQ [Attr.Type.Querier String_FL]> -----
    <wired_interface.left.node.manager.middle_name.AQ [Attr.Type.Querier String]> -----
    <wired_interface.left.node.manager.title.AQ [Attr.Type.Querier String]> -----
    <wired_interface.left.node.manager.lifetime.AQ [Attr.Type.Querier Composite]> MOM.Date_Interval
    <wired_interface.left.node.manager.lifetime.start.AQ [Attr.Type.Querier Date]> -----
    <wired_interface.left.node.manager.lifetime.finish.AQ [Attr.Type.Querier Date]> -----
    <wired_interface.left.node.manager.lifetime.alive.AQ [Attr.Type.Querier Boolean]> -----
    <wired_interface.left.node.manager.sex.AQ [Attr.Type.Querier Ckd]> -----
    <wired_interface.left.node.address.AQ [Attr.Type.Querier Id_Entity]> PAP.Address
    <wired_interface.left.node.address.street.AQ [Attr.Type.Querier String]> -----
    <wired_interface.left.node.address.zip.AQ [Attr.Type.Querier String]> -----
    <wired_interface.left.node.address.city.AQ [Attr.Type.Querier String]> -----
    <wired_interface.left.node.address.country.AQ [Attr.Type.Querier String]> -----
    <wired_interface.left.node.address.desc.AQ [Attr.Type.Querier String]> -----
    <wired_interface.left.node.address.region.AQ [Attr.Type.Querier String]> -----
    <wired_interface.left.node.desc.AQ [Attr.Type.Querier String]> -----
    <wired_interface.left.node.owner.AQ [Attr.Type.Querier Id_Entity]> PAP.Subject
    <wired_interface.left.node.position.AQ [Attr.Type.Querier Composite]> MOM.Position
    <wired_interface.left.node.position.lat.AQ [Attr.Type.Querier Raw]> -----
    <wired_interface.left.node.position.lon.AQ [Attr.Type.Querier Raw]> -----
    <wired_interface.left.node.position.height.AQ [Attr.Type.Querier Ckd]> -----
    <wired_interface.left.node.show_in_map.AQ [Attr.Type.Querier Boolean]> -----
    <wired_interface.left.name.AQ [Attr.Type.Querier String]> -----
    <wired_interface.left.desc.AQ [Attr.Type.Querier String]> -----
    <wired_interface.left.my_node.AQ [Attr.Type.Querier Id_Entity]> FFM.Node
    <wired_interface.left.my_node.name.AQ [Attr.Type.Querier String]> -----
    <wired_interface.left.my_node.manager.AQ [Attr.Type.Querier Id_Entity]> PAP.Person
    <wired_interface.left.my_node.manager.last_name.AQ [Attr.Type.Querier String_FL]> -----
    <wired_interface.left.my_node.manager.first_name.AQ [Attr.Type.Querier String_FL]> -----
    <wired_interface.left.my_node.manager.middle_name.AQ [Attr.Type.Querier String]> -----
    <wired_interface.left.my_node.manager.title.AQ [Attr.Type.Querier String]> -----
    <wired_interface.left.my_node.manager.lifetime.AQ [Attr.Type.Querier Composite]> MOM.Date_Interval
    <wired_interface.left.my_node.manager.lifetime.start.AQ [Attr.Type.Querier Date]> -----
    <wired_interface.left.my_node.manager.lifetime.finish.AQ [Attr.Type.Querier Date]> -----
    <wired_interface.left.my_node.manager.lifetime.alive.AQ [Attr.Type.Querier Boolean]> -----
    <wired_interface.left.my_node.manager.sex.AQ [Attr.Type.Querier Ckd]> -----
    <wired_interface.left.my_node.address.AQ [Attr.Type.Querier Id_Entity]> PAP.Address
    <wired_interface.left.my_node.address.street.AQ [Attr.Type.Querier String]> -----
    <wired_interface.left.my_node.address.zip.AQ [Attr.Type.Querier String]> -----
    <wired_interface.left.my_node.address.city.AQ [Attr.Type.Querier String]> -----
    <wired_interface.left.my_node.address.country.AQ [Attr.Type.Querier String]> -----
    <wired_interface.left.my_node.address.desc.AQ [Attr.Type.Querier String]> -----
    <wired_interface.left.my_node.address.region.AQ [Attr.Type.Querier String]> -----
    <wired_interface.left.my_node.desc.AQ [Attr.Type.Querier String]> -----
    <wired_interface.left.my_node.owner.AQ [Attr.Type.Querier Id_Entity]> PAP.Subject
    <wired_interface.left.my_node.position.AQ [Attr.Type.Querier Composite]> MOM.Position
    <wired_interface.left.my_node.position.lat.AQ [Attr.Type.Querier Raw]> -----
    <wired_interface.left.my_node.position.lon.AQ [Attr.Type.Querier Raw]> -----
    <wired_interface.left.my_node.position.height.AQ [Attr.Type.Querier Ckd]> -----
    <wired_interface.left.my_node.show_in_map.AQ [Attr.Type.Querier Boolean]> -----
    <wired_interface.mac_address.AQ [Attr.Type.Querier String]> -----
    <wired_interface.name.AQ [Attr.Type.Querier String]> -----
    <wired_interface.is_active.AQ [Attr.Type.Querier Boolean]> -----
    <wired_interface.desc.AQ [Attr.Type.Querier String]> -----
    <wired_interface.my_node.AQ [Attr.Type.Querier Id_Entity]> FFM.Node
    <wired_interface.my_node.name.AQ [Attr.Type.Querier String]> -----
    <wired_interface.my_node.manager.AQ [Attr.Type.Querier Id_Entity]> PAP.Person
    <wired_interface.my_node.manager.last_name.AQ [Attr.Type.Querier String_FL]> -----
    <wired_interface.my_node.manager.first_name.AQ [Attr.Type.Querier String_FL]> -----
    <wired_interface.my_node.manager.middle_name.AQ [Attr.Type.Querier String]> -----
    <wired_interface.my_node.manager.title.AQ [Attr.Type.Querier String]> -----
    <wired_interface.my_node.manager.lifetime.AQ [Attr.Type.Querier Composite]> MOM.Date_Interval
    <wired_interface.my_node.manager.lifetime.start.AQ [Attr.Type.Querier Date]> -----
    <wired_interface.my_node.manager.lifetime.finish.AQ [Attr.Type.Querier Date]> -----
    <wired_interface.my_node.manager.lifetime.alive.AQ [Attr.Type.Querier Boolean]> -----
    <wired_interface.my_node.manager.sex.AQ [Attr.Type.Querier Ckd]> -----
    <wired_interface.my_node.address.AQ [Attr.Type.Querier Id_Entity]> PAP.Address
    <wired_interface.my_node.address.street.AQ [Attr.Type.Querier String]> -----
    <wired_interface.my_node.address.zip.AQ [Attr.Type.Querier String]> -----
    <wired_interface.my_node.address.city.AQ [Attr.Type.Querier String]> -----
    <wired_interface.my_node.address.country.AQ [Attr.Type.Querier String]> -----
    <wired_interface.my_node.address.desc.AQ [Attr.Type.Querier String]> -----
    <wired_interface.my_node.address.region.AQ [Attr.Type.Querier String]> -----
    <wired_interface.my_node.desc.AQ [Attr.Type.Querier String]> -----
    <wired_interface.my_node.owner.AQ [Attr.Type.Querier Id_Entity]> PAP.Subject
    <wired_interface.my_node.position.AQ [Attr.Type.Querier Composite]> MOM.Position
    <wired_interface.my_node.position.lat.AQ [Attr.Type.Querier Raw]> -----
    <wired_interface.my_node.position.lon.AQ [Attr.Type.Querier Raw]> -----
    <wired_interface.my_node.position.height.AQ [Attr.Type.Querier Ckd]> -----
    <wired_interface.my_node.show_in_map.AQ [Attr.Type.Querier Boolean]> -----
    <wired_interface.my_net_device.AQ [Attr.Type.Querier Id_Entity]> FFM.Net_Device
    <wired_interface.my_net_device.left.AQ [Attr.Type.Querier Id_Entity]> FFM.Net_Device_Type
    <wired_interface.my_net_device.left.name.AQ [Attr.Type.Querier String]> -----
    <wired_interface.my_net_device.left.model_no.AQ [Attr.Type.Querier String]> -----
    <wired_interface.my_net_device.left.revision.AQ [Attr.Type.Querier String]> -----
    <wired_interface.my_net_device.left.desc.AQ [Attr.Type.Querier String]> -----
    <wired_interface.my_net_device.node.AQ [Attr.Type.Querier Id_Entity]> FFM.Node
    <wired_interface.my_net_device.node.name.AQ [Attr.Type.Querier String]> -----
    <wired_interface.my_net_device.node.manager.AQ [Attr.Type.Querier Id_Entity]> PAP.Person
    <wired_interface.my_net_device.node.manager.last_name.AQ [Attr.Type.Querier String_FL]> -----
    <wired_interface.my_net_device.node.manager.first_name.AQ [Attr.Type.Querier String_FL]> -----
    <wired_interface.my_net_device.node.manager.middle_name.AQ [Attr.Type.Querier String]> -----
    <wired_interface.my_net_device.node.manager.title.AQ [Attr.Type.Querier String]> -----
    <wired_interface.my_net_device.node.manager.lifetime.AQ [Attr.Type.Querier Composite]> MOM.Date_Interval
    <wired_interface.my_net_device.node.manager.lifetime.start.AQ [Attr.Type.Querier Date]> -----
    <wired_interface.my_net_device.node.manager.lifetime.finish.AQ [Attr.Type.Querier Date]> -----
    <wired_interface.my_net_device.node.manager.lifetime.alive.AQ [Attr.Type.Querier Boolean]> -----
    <wired_interface.my_net_device.node.manager.sex.AQ [Attr.Type.Querier Ckd]> -----
    <wired_interface.my_net_device.node.address.AQ [Attr.Type.Querier Id_Entity]> PAP.Address
    <wired_interface.my_net_device.node.address.street.AQ [Attr.Type.Querier String]> -----
    <wired_interface.my_net_device.node.address.zip.AQ [Attr.Type.Querier String]> -----
    <wired_interface.my_net_device.node.address.city.AQ [Attr.Type.Querier String]> -----
    <wired_interface.my_net_device.node.address.country.AQ [Attr.Type.Querier String]> -----
    <wired_interface.my_net_device.node.address.desc.AQ [Attr.Type.Querier String]> -----
    <wired_interface.my_net_device.node.address.region.AQ [Attr.Type.Querier String]> -----
    <wired_interface.my_net_device.node.desc.AQ [Attr.Type.Querier String]> -----
    <wired_interface.my_net_device.node.owner.AQ [Attr.Type.Querier Id_Entity]> PAP.Subject
    <wired_interface.my_net_device.node.position.AQ [Attr.Type.Querier Composite]> MOM.Position
    <wired_interface.my_net_device.node.position.lat.AQ [Attr.Type.Querier Raw]> -----
    <wired_interface.my_net_device.node.position.lon.AQ [Attr.Type.Querier Raw]> -----
    <wired_interface.my_net_device.node.position.height.AQ [Attr.Type.Querier Ckd]> -----
    <wired_interface.my_net_device.node.show_in_map.AQ [Attr.Type.Querier Boolean]> -----
    <wired_interface.my_net_device.name.AQ [Attr.Type.Querier String]> -----
    <wired_interface.my_net_device.desc.AQ [Attr.Type.Querier String]> -----
    <wired_interface.my_net_device.my_node.AQ [Attr.Type.Querier Id_Entity]> FFM.Node
    <wired_interface.my_net_device.my_node.name.AQ [Attr.Type.Querier String]> -----
    <wired_interface.my_net_device.my_node.manager.AQ [Attr.Type.Querier Id_Entity]> PAP.Person
    <wired_interface.my_net_device.my_node.manager.last_name.AQ [Attr.Type.Querier String_FL]> -----
    <wired_interface.my_net_device.my_node.manager.first_name.AQ [Attr.Type.Querier String_FL]> -----
    <wired_interface.my_net_device.my_node.manager.middle_name.AQ [Attr.Type.Querier String]> -----
    <wired_interface.my_net_device.my_node.manager.title.AQ [Attr.Type.Querier String]> -----
    <wired_interface.my_net_device.my_node.manager.lifetime.AQ [Attr.Type.Querier Composite]> MOM.Date_Interval
    <wired_interface.my_net_device.my_node.manager.lifetime.start.AQ [Attr.Type.Querier Date]> -----
    <wired_interface.my_net_device.my_node.manager.lifetime.finish.AQ [Attr.Type.Querier Date]> -----
    <wired_interface.my_net_device.my_node.manager.lifetime.alive.AQ [Attr.Type.Querier Boolean]> -----
    <wired_interface.my_net_device.my_node.manager.sex.AQ [Attr.Type.Querier Ckd]> -----
    <wired_interface.my_net_device.my_node.address.AQ [Attr.Type.Querier Id_Entity]> PAP.Address
    <wired_interface.my_net_device.my_node.address.street.AQ [Attr.Type.Querier String]> -----
    <wired_interface.my_net_device.my_node.address.zip.AQ [Attr.Type.Querier String]> -----
    <wired_interface.my_net_device.my_node.address.city.AQ [Attr.Type.Querier String]> -----
    <wired_interface.my_net_device.my_node.address.country.AQ [Attr.Type.Querier String]> -----
    <wired_interface.my_net_device.my_node.address.desc.AQ [Attr.Type.Querier String]> -----
    <wired_interface.my_net_device.my_node.address.region.AQ [Attr.Type.Querier String]> -----
    <wired_interface.my_net_device.my_node.desc.AQ [Attr.Type.Querier String]> -----
    <wired_interface.my_net_device.my_node.owner.AQ [Attr.Type.Querier Id_Entity]> PAP.Subject
    <wired_interface.my_net_device.my_node.position.AQ [Attr.Type.Querier Composite]> MOM.Position
    <wired_interface.my_net_device.my_node.position.lat.AQ [Attr.Type.Querier Raw]> -----
    <wired_interface.my_net_device.my_node.position.lon.AQ [Attr.Type.Querier Raw]> -----
    <wired_interface.my_net_device.my_node.position.height.AQ [Attr.Type.Querier Ckd]> -----
    <wired_interface.my_net_device.my_node.show_in_map.AQ [Attr.Type.Querier Boolean]> -----
    <wireless_interface.AQ [Attr.Type.Querier Rev_Ref]> FFM.Wireless_Interface
    <wireless_interface.left.AQ [Attr.Type.Querier Id_Entity]> FFM.Net_Device
    <wireless_interface.left.left.AQ [Attr.Type.Querier Id_Entity]> FFM.Net_Device_Type
    <wireless_interface.left.left.name.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.left.left.model_no.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.left.left.revision.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.left.left.desc.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.left.node.AQ [Attr.Type.Querier Id_Entity]> FFM.Node
    <wireless_interface.left.node.name.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.left.node.manager.AQ [Attr.Type.Querier Id_Entity]> PAP.Person
    <wireless_interface.left.node.manager.last_name.AQ [Attr.Type.Querier String_FL]> -----
    <wireless_interface.left.node.manager.first_name.AQ [Attr.Type.Querier String_FL]> -----
    <wireless_interface.left.node.manager.middle_name.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.left.node.manager.title.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.left.node.manager.lifetime.AQ [Attr.Type.Querier Composite]> MOM.Date_Interval
    <wireless_interface.left.node.manager.lifetime.start.AQ [Attr.Type.Querier Date]> -----
    <wireless_interface.left.node.manager.lifetime.finish.AQ [Attr.Type.Querier Date]> -----
    <wireless_interface.left.node.manager.lifetime.alive.AQ [Attr.Type.Querier Boolean]> -----
    <wireless_interface.left.node.manager.sex.AQ [Attr.Type.Querier Ckd]> -----
    <wireless_interface.left.node.address.AQ [Attr.Type.Querier Id_Entity]> PAP.Address
    <wireless_interface.left.node.address.street.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.left.node.address.zip.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.left.node.address.city.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.left.node.address.country.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.left.node.address.desc.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.left.node.address.region.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.left.node.desc.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.left.node.owner.AQ [Attr.Type.Querier Id_Entity]> PAP.Subject
    <wireless_interface.left.node.position.AQ [Attr.Type.Querier Composite]> MOM.Position
    <wireless_interface.left.node.position.lat.AQ [Attr.Type.Querier Raw]> -----
    <wireless_interface.left.node.position.lon.AQ [Attr.Type.Querier Raw]> -----
    <wireless_interface.left.node.position.height.AQ [Attr.Type.Querier Ckd]> -----
    <wireless_interface.left.node.show_in_map.AQ [Attr.Type.Querier Boolean]> -----
    <wireless_interface.left.name.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.left.desc.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.left.my_node.AQ [Attr.Type.Querier Id_Entity]> FFM.Node
    <wireless_interface.left.my_node.name.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.left.my_node.manager.AQ [Attr.Type.Querier Id_Entity]> PAP.Person
    <wireless_interface.left.my_node.manager.last_name.AQ [Attr.Type.Querier String_FL]> -----
    <wireless_interface.left.my_node.manager.first_name.AQ [Attr.Type.Querier String_FL]> -----
    <wireless_interface.left.my_node.manager.middle_name.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.left.my_node.manager.title.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.left.my_node.manager.lifetime.AQ [Attr.Type.Querier Composite]> MOM.Date_Interval
    <wireless_interface.left.my_node.manager.lifetime.start.AQ [Attr.Type.Querier Date]> -----
    <wireless_interface.left.my_node.manager.lifetime.finish.AQ [Attr.Type.Querier Date]> -----
    <wireless_interface.left.my_node.manager.lifetime.alive.AQ [Attr.Type.Querier Boolean]> -----
    <wireless_interface.left.my_node.manager.sex.AQ [Attr.Type.Querier Ckd]> -----
    <wireless_interface.left.my_node.address.AQ [Attr.Type.Querier Id_Entity]> PAP.Address
    <wireless_interface.left.my_node.address.street.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.left.my_node.address.zip.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.left.my_node.address.city.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.left.my_node.address.country.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.left.my_node.address.desc.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.left.my_node.address.region.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.left.my_node.desc.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.left.my_node.owner.AQ [Attr.Type.Querier Id_Entity]> PAP.Subject
    <wireless_interface.left.my_node.position.AQ [Attr.Type.Querier Composite]> MOM.Position
    <wireless_interface.left.my_node.position.lat.AQ [Attr.Type.Querier Raw]> -----
    <wireless_interface.left.my_node.position.lon.AQ [Attr.Type.Querier Raw]> -----
    <wireless_interface.left.my_node.position.height.AQ [Attr.Type.Querier Ckd]> -----
    <wireless_interface.left.my_node.show_in_map.AQ [Attr.Type.Querier Boolean]> -----
    <wireless_interface.mac_address.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.name.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.is_active.AQ [Attr.Type.Querier Boolean]> -----
    <wireless_interface.desc.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.mode.AQ [Attr.Type.Querier Ckd]> -----
    <wireless_interface.essid.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.bssid.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.standard.AQ [Attr.Type.Querier Id_Entity]> FFM.Wireless_Standard
    <wireless_interface.standard.name.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.standard.bandwidth.AQ [Attr.Type.Querier Raw]> -----
    <wireless_interface.txpower.AQ [Attr.Type.Querier Raw]> -----
    <wireless_interface.my_node.AQ [Attr.Type.Querier Id_Entity]> FFM.Node
    <wireless_interface.my_node.name.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.my_node.manager.AQ [Attr.Type.Querier Id_Entity]> PAP.Person
    <wireless_interface.my_node.manager.last_name.AQ [Attr.Type.Querier String_FL]> -----
    <wireless_interface.my_node.manager.first_name.AQ [Attr.Type.Querier String_FL]> -----
    <wireless_interface.my_node.manager.middle_name.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.my_node.manager.title.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.my_node.manager.lifetime.AQ [Attr.Type.Querier Composite]> MOM.Date_Interval
    <wireless_interface.my_node.manager.lifetime.start.AQ [Attr.Type.Querier Date]> -----
    <wireless_interface.my_node.manager.lifetime.finish.AQ [Attr.Type.Querier Date]> -----
    <wireless_interface.my_node.manager.lifetime.alive.AQ [Attr.Type.Querier Boolean]> -----
    <wireless_interface.my_node.manager.sex.AQ [Attr.Type.Querier Ckd]> -----
    <wireless_interface.my_node.address.AQ [Attr.Type.Querier Id_Entity]> PAP.Address
    <wireless_interface.my_node.address.street.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.my_node.address.zip.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.my_node.address.city.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.my_node.address.country.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.my_node.address.desc.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.my_node.address.region.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.my_node.desc.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.my_node.owner.AQ [Attr.Type.Querier Id_Entity]> PAP.Subject
    <wireless_interface.my_node.position.AQ [Attr.Type.Querier Composite]> MOM.Position
    <wireless_interface.my_node.position.lat.AQ [Attr.Type.Querier Raw]> -----
    <wireless_interface.my_node.position.lon.AQ [Attr.Type.Querier Raw]> -----
    <wireless_interface.my_node.position.height.AQ [Attr.Type.Querier Ckd]> -----
    <wireless_interface.my_node.show_in_map.AQ [Attr.Type.Querier Boolean]> -----
    <wireless_interface.my_net_device.AQ [Attr.Type.Querier Id_Entity]> FFM.Net_Device
    <wireless_interface.my_net_device.left.AQ [Attr.Type.Querier Id_Entity]> FFM.Net_Device_Type
    <wireless_interface.my_net_device.left.name.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.my_net_device.left.model_no.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.my_net_device.left.revision.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.my_net_device.left.desc.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.my_net_device.node.AQ [Attr.Type.Querier Id_Entity]> FFM.Node
    <wireless_interface.my_net_device.node.name.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.my_net_device.node.manager.AQ [Attr.Type.Querier Id_Entity]> PAP.Person
    <wireless_interface.my_net_device.node.manager.last_name.AQ [Attr.Type.Querier String_FL]> -----
    <wireless_interface.my_net_device.node.manager.first_name.AQ [Attr.Type.Querier String_FL]> -----
    <wireless_interface.my_net_device.node.manager.middle_name.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.my_net_device.node.manager.title.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.my_net_device.node.manager.lifetime.AQ [Attr.Type.Querier Composite]> MOM.Date_Interval
    <wireless_interface.my_net_device.node.manager.lifetime.start.AQ [Attr.Type.Querier Date]> -----
    <wireless_interface.my_net_device.node.manager.lifetime.finish.AQ [Attr.Type.Querier Date]> -----
    <wireless_interface.my_net_device.node.manager.lifetime.alive.AQ [Attr.Type.Querier Boolean]> -----
    <wireless_interface.my_net_device.node.manager.sex.AQ [Attr.Type.Querier Ckd]> -----
    <wireless_interface.my_net_device.node.address.AQ [Attr.Type.Querier Id_Entity]> PAP.Address
    <wireless_interface.my_net_device.node.address.street.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.my_net_device.node.address.zip.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.my_net_device.node.address.city.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.my_net_device.node.address.country.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.my_net_device.node.address.desc.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.my_net_device.node.address.region.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.my_net_device.node.desc.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.my_net_device.node.owner.AQ [Attr.Type.Querier Id_Entity]> PAP.Subject
    <wireless_interface.my_net_device.node.position.AQ [Attr.Type.Querier Composite]> MOM.Position
    <wireless_interface.my_net_device.node.position.lat.AQ [Attr.Type.Querier Raw]> -----
    <wireless_interface.my_net_device.node.position.lon.AQ [Attr.Type.Querier Raw]> -----
    <wireless_interface.my_net_device.node.position.height.AQ [Attr.Type.Querier Ckd]> -----
    <wireless_interface.my_net_device.node.show_in_map.AQ [Attr.Type.Querier Boolean]> -----
    <wireless_interface.my_net_device.name.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.my_net_device.desc.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.my_net_device.my_node.AQ [Attr.Type.Querier Id_Entity]> FFM.Node
    <wireless_interface.my_net_device.my_node.name.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.my_net_device.my_node.manager.AQ [Attr.Type.Querier Id_Entity]> PAP.Person
    <wireless_interface.my_net_device.my_node.manager.last_name.AQ [Attr.Type.Querier String_FL]> -----
    <wireless_interface.my_net_device.my_node.manager.first_name.AQ [Attr.Type.Querier String_FL]> -----
    <wireless_interface.my_net_device.my_node.manager.middle_name.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.my_net_device.my_node.manager.title.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.my_net_device.my_node.manager.lifetime.AQ [Attr.Type.Querier Composite]> MOM.Date_Interval
    <wireless_interface.my_net_device.my_node.manager.lifetime.start.AQ [Attr.Type.Querier Date]> -----
    <wireless_interface.my_net_device.my_node.manager.lifetime.finish.AQ [Attr.Type.Querier Date]> -----
    <wireless_interface.my_net_device.my_node.manager.lifetime.alive.AQ [Attr.Type.Querier Boolean]> -----
    <wireless_interface.my_net_device.my_node.manager.sex.AQ [Attr.Type.Querier Ckd]> -----
    <wireless_interface.my_net_device.my_node.address.AQ [Attr.Type.Querier Id_Entity]> PAP.Address
    <wireless_interface.my_net_device.my_node.address.street.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.my_net_device.my_node.address.zip.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.my_net_device.my_node.address.city.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.my_net_device.my_node.address.country.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.my_net_device.my_node.address.desc.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.my_net_device.my_node.address.region.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.my_net_device.my_node.desc.AQ [Attr.Type.Querier String]> -----
    <wireless_interface.my_net_device.my_node.owner.AQ [Attr.Type.Querier Id_Entity]> PAP.Subject
    <wireless_interface.my_net_device.my_node.position.AQ [Attr.Type.Querier Composite]> MOM.Position
    <wireless_interface.my_net_device.my_node.position.lat.AQ [Attr.Type.Querier Raw]> -----
    <wireless_interface.my_net_device.my_node.position.lon.AQ [Attr.Type.Querier Raw]> -----
    <wireless_interface.my_net_device.my_node.position.height.AQ [Attr.Type.Querier Ckd]> -----
    <wireless_interface.my_net_device.my_node.show_in_map.AQ [Attr.Type.Querier Boolean]> -----
    <virtual_wireless_interface.AQ [Attr.Type.Querier Rev_Ref]> FFM.Virtual_Wireless_Interface
    <virtual_wireless_interface.left.AQ [Attr.Type.Querier Id_Entity]> FFM.Net_Device
    <virtual_wireless_interface.left.left.AQ [Attr.Type.Querier Id_Entity]> FFM.Net_Device_Type
    <virtual_wireless_interface.left.left.name.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.left.left.model_no.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.left.left.revision.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.left.left.desc.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.left.node.AQ [Attr.Type.Querier Id_Entity]> FFM.Node
    <virtual_wireless_interface.left.node.name.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.left.node.manager.AQ [Attr.Type.Querier Id_Entity]> PAP.Person
    <virtual_wireless_interface.left.node.manager.last_name.AQ [Attr.Type.Querier String_FL]> -----
    <virtual_wireless_interface.left.node.manager.first_name.AQ [Attr.Type.Querier String_FL]> -----
    <virtual_wireless_interface.left.node.manager.middle_name.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.left.node.manager.title.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.left.node.manager.lifetime.AQ [Attr.Type.Querier Composite]> MOM.Date_Interval
    <virtual_wireless_interface.left.node.manager.lifetime.start.AQ [Attr.Type.Querier Date]> -----
    <virtual_wireless_interface.left.node.manager.lifetime.finish.AQ [Attr.Type.Querier Date]> -----
    <virtual_wireless_interface.left.node.manager.lifetime.alive.AQ [Attr.Type.Querier Boolean]> -----
    <virtual_wireless_interface.left.node.manager.sex.AQ [Attr.Type.Querier Ckd]> -----
    <virtual_wireless_interface.left.node.address.AQ [Attr.Type.Querier Id_Entity]> PAP.Address
    <virtual_wireless_interface.left.node.address.street.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.left.node.address.zip.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.left.node.address.city.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.left.node.address.country.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.left.node.address.desc.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.left.node.address.region.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.left.node.desc.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.left.node.owner.AQ [Attr.Type.Querier Id_Entity]> PAP.Subject
    <virtual_wireless_interface.left.node.position.AQ [Attr.Type.Querier Composite]> MOM.Position
    <virtual_wireless_interface.left.node.position.lat.AQ [Attr.Type.Querier Raw]> -----
    <virtual_wireless_interface.left.node.position.lon.AQ [Attr.Type.Querier Raw]> -----
    <virtual_wireless_interface.left.node.position.height.AQ [Attr.Type.Querier Ckd]> -----
    <virtual_wireless_interface.left.node.show_in_map.AQ [Attr.Type.Querier Boolean]> -----
    <virtual_wireless_interface.left.name.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.left.desc.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.left.my_node.AQ [Attr.Type.Querier Id_Entity]> FFM.Node
    <virtual_wireless_interface.left.my_node.name.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.left.my_node.manager.AQ [Attr.Type.Querier Id_Entity]> PAP.Person
    <virtual_wireless_interface.left.my_node.manager.last_name.AQ [Attr.Type.Querier String_FL]> -----
    <virtual_wireless_interface.left.my_node.manager.first_name.AQ [Attr.Type.Querier String_FL]> -----
    <virtual_wireless_interface.left.my_node.manager.middle_name.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.left.my_node.manager.title.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.left.my_node.manager.lifetime.AQ [Attr.Type.Querier Composite]> MOM.Date_Interval
    <virtual_wireless_interface.left.my_node.manager.lifetime.start.AQ [Attr.Type.Querier Date]> -----
    <virtual_wireless_interface.left.my_node.manager.lifetime.finish.AQ [Attr.Type.Querier Date]> -----
    <virtual_wireless_interface.left.my_node.manager.lifetime.alive.AQ [Attr.Type.Querier Boolean]> -----
    <virtual_wireless_interface.left.my_node.manager.sex.AQ [Attr.Type.Querier Ckd]> -----
    <virtual_wireless_interface.left.my_node.address.AQ [Attr.Type.Querier Id_Entity]> PAP.Address
    <virtual_wireless_interface.left.my_node.address.street.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.left.my_node.address.zip.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.left.my_node.address.city.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.left.my_node.address.country.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.left.my_node.address.desc.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.left.my_node.address.region.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.left.my_node.desc.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.left.my_node.owner.AQ [Attr.Type.Querier Id_Entity]> PAP.Subject
    <virtual_wireless_interface.left.my_node.position.AQ [Attr.Type.Querier Composite]> MOM.Position
    <virtual_wireless_interface.left.my_node.position.lat.AQ [Attr.Type.Querier Raw]> -----
    <virtual_wireless_interface.left.my_node.position.lon.AQ [Attr.Type.Querier Raw]> -----
    <virtual_wireless_interface.left.my_node.position.height.AQ [Attr.Type.Querier Ckd]> -----
    <virtual_wireless_interface.left.my_node.show_in_map.AQ [Attr.Type.Querier Boolean]> -----
    <virtual_wireless_interface.hardware.AQ [Attr.Type.Querier Id_Entity]> FFM.Wireless_Interface
    <virtual_wireless_interface.hardware.left.AQ [Attr.Type.Querier Id_Entity]> FFM.Net_Device
    <virtual_wireless_interface.hardware.left.left.AQ [Attr.Type.Querier Id_Entity]> FFM.Net_Device_Type
    <virtual_wireless_interface.hardware.left.left.name.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.left.left.model_no.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.left.left.revision.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.left.left.desc.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.left.node.AQ [Attr.Type.Querier Id_Entity]> FFM.Node
    <virtual_wireless_interface.hardware.left.node.name.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.left.node.manager.AQ [Attr.Type.Querier Id_Entity]> PAP.Person
    <virtual_wireless_interface.hardware.left.node.manager.last_name.AQ [Attr.Type.Querier String_FL]> -----
    <virtual_wireless_interface.hardware.left.node.manager.first_name.AQ [Attr.Type.Querier String_FL]> -----
    <virtual_wireless_interface.hardware.left.node.manager.middle_name.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.left.node.manager.title.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.left.node.manager.lifetime.AQ [Attr.Type.Querier Composite]> MOM.Date_Interval
    <virtual_wireless_interface.hardware.left.node.manager.lifetime.start.AQ [Attr.Type.Querier Date]> -----
    <virtual_wireless_interface.hardware.left.node.manager.lifetime.finish.AQ [Attr.Type.Querier Date]> -----
    <virtual_wireless_interface.hardware.left.node.manager.lifetime.alive.AQ [Attr.Type.Querier Boolean]> -----
    <virtual_wireless_interface.hardware.left.node.manager.sex.AQ [Attr.Type.Querier Ckd]> -----
    <virtual_wireless_interface.hardware.left.node.address.AQ [Attr.Type.Querier Id_Entity]> PAP.Address
    <virtual_wireless_interface.hardware.left.node.address.street.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.left.node.address.zip.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.left.node.address.city.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.left.node.address.country.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.left.node.address.desc.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.left.node.address.region.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.left.node.desc.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.left.node.owner.AQ [Attr.Type.Querier Id_Entity]> PAP.Subject
    <virtual_wireless_interface.hardware.left.node.position.AQ [Attr.Type.Querier Composite]> MOM.Position
    <virtual_wireless_interface.hardware.left.node.position.lat.AQ [Attr.Type.Querier Raw]> -----
    <virtual_wireless_interface.hardware.left.node.position.lon.AQ [Attr.Type.Querier Raw]> -----
    <virtual_wireless_interface.hardware.left.node.position.height.AQ [Attr.Type.Querier Ckd]> -----
    <virtual_wireless_interface.hardware.left.node.show_in_map.AQ [Attr.Type.Querier Boolean]> -----
    <virtual_wireless_interface.hardware.left.name.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.left.desc.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.left.my_node.AQ [Attr.Type.Querier Id_Entity]> FFM.Node
    <virtual_wireless_interface.hardware.left.my_node.name.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.left.my_node.manager.AQ [Attr.Type.Querier Id_Entity]> PAP.Person
    <virtual_wireless_interface.hardware.left.my_node.manager.last_name.AQ [Attr.Type.Querier String_FL]> -----
    <virtual_wireless_interface.hardware.left.my_node.manager.first_name.AQ [Attr.Type.Querier String_FL]> -----
    <virtual_wireless_interface.hardware.left.my_node.manager.middle_name.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.left.my_node.manager.title.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.left.my_node.manager.lifetime.AQ [Attr.Type.Querier Composite]> MOM.Date_Interval
    <virtual_wireless_interface.hardware.left.my_node.manager.lifetime.start.AQ [Attr.Type.Querier Date]> -----
    <virtual_wireless_interface.hardware.left.my_node.manager.lifetime.finish.AQ [Attr.Type.Querier Date]> -----
    <virtual_wireless_interface.hardware.left.my_node.manager.lifetime.alive.AQ [Attr.Type.Querier Boolean]> -----
    <virtual_wireless_interface.hardware.left.my_node.manager.sex.AQ [Attr.Type.Querier Ckd]> -----
    <virtual_wireless_interface.hardware.left.my_node.address.AQ [Attr.Type.Querier Id_Entity]> PAP.Address
    <virtual_wireless_interface.hardware.left.my_node.address.street.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.left.my_node.address.zip.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.left.my_node.address.city.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.left.my_node.address.country.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.left.my_node.address.desc.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.left.my_node.address.region.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.left.my_node.desc.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.left.my_node.owner.AQ [Attr.Type.Querier Id_Entity]> PAP.Subject
    <virtual_wireless_interface.hardware.left.my_node.position.AQ [Attr.Type.Querier Composite]> MOM.Position
    <virtual_wireless_interface.hardware.left.my_node.position.lat.AQ [Attr.Type.Querier Raw]> -----
    <virtual_wireless_interface.hardware.left.my_node.position.lon.AQ [Attr.Type.Querier Raw]> -----
    <virtual_wireless_interface.hardware.left.my_node.position.height.AQ [Attr.Type.Querier Ckd]> -----
    <virtual_wireless_interface.hardware.left.my_node.show_in_map.AQ [Attr.Type.Querier Boolean]> -----
    <virtual_wireless_interface.hardware.mac_address.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.name.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.is_active.AQ [Attr.Type.Querier Boolean]> -----
    <virtual_wireless_interface.hardware.desc.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.mode.AQ [Attr.Type.Querier Ckd]> -----
    <virtual_wireless_interface.hardware.essid.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.bssid.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.standard.AQ [Attr.Type.Querier Id_Entity]> FFM.Wireless_Standard
    <virtual_wireless_interface.hardware.standard.name.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.standard.bandwidth.AQ [Attr.Type.Querier Raw]> -----
    <virtual_wireless_interface.hardware.txpower.AQ [Attr.Type.Querier Raw]> -----
    <virtual_wireless_interface.hardware.my_node.AQ [Attr.Type.Querier Id_Entity]> FFM.Node
    <virtual_wireless_interface.hardware.my_node.name.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.my_node.manager.AQ [Attr.Type.Querier Id_Entity]> PAP.Person
    <virtual_wireless_interface.hardware.my_node.manager.last_name.AQ [Attr.Type.Querier String_FL]> -----
    <virtual_wireless_interface.hardware.my_node.manager.first_name.AQ [Attr.Type.Querier String_FL]> -----
    <virtual_wireless_interface.hardware.my_node.manager.middle_name.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.my_node.manager.title.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.my_node.manager.lifetime.AQ [Attr.Type.Querier Composite]> MOM.Date_Interval
    <virtual_wireless_interface.hardware.my_node.manager.lifetime.start.AQ [Attr.Type.Querier Date]> -----
    <virtual_wireless_interface.hardware.my_node.manager.lifetime.finish.AQ [Attr.Type.Querier Date]> -----
    <virtual_wireless_interface.hardware.my_node.manager.lifetime.alive.AQ [Attr.Type.Querier Boolean]> -----
    <virtual_wireless_interface.hardware.my_node.manager.sex.AQ [Attr.Type.Querier Ckd]> -----
    <virtual_wireless_interface.hardware.my_node.address.AQ [Attr.Type.Querier Id_Entity]> PAP.Address
    <virtual_wireless_interface.hardware.my_node.address.street.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.my_node.address.zip.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.my_node.address.city.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.my_node.address.country.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.my_node.address.desc.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.my_node.address.region.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.my_node.desc.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.my_node.owner.AQ [Attr.Type.Querier Id_Entity]> PAP.Subject
    <virtual_wireless_interface.hardware.my_node.position.AQ [Attr.Type.Querier Composite]> MOM.Position
    <virtual_wireless_interface.hardware.my_node.position.lat.AQ [Attr.Type.Querier Raw]> -----
    <virtual_wireless_interface.hardware.my_node.position.lon.AQ [Attr.Type.Querier Raw]> -----
    <virtual_wireless_interface.hardware.my_node.position.height.AQ [Attr.Type.Querier Ckd]> -----
    <virtual_wireless_interface.hardware.my_node.show_in_map.AQ [Attr.Type.Querier Boolean]> -----
    <virtual_wireless_interface.hardware.my_net_device.AQ [Attr.Type.Querier Id_Entity]> FFM.Net_Device
    <virtual_wireless_interface.hardware.my_net_device.left.AQ [Attr.Type.Querier Id_Entity]> FFM.Net_Device_Type
    <virtual_wireless_interface.hardware.my_net_device.left.name.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.my_net_device.left.model_no.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.my_net_device.left.revision.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.my_net_device.left.desc.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.my_net_device.node.AQ [Attr.Type.Querier Id_Entity]> FFM.Node
    <virtual_wireless_interface.hardware.my_net_device.node.name.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.my_net_device.node.manager.AQ [Attr.Type.Querier Id_Entity]> PAP.Person
    <virtual_wireless_interface.hardware.my_net_device.node.manager.last_name.AQ [Attr.Type.Querier String_FL]> -----
    <virtual_wireless_interface.hardware.my_net_device.node.manager.first_name.AQ [Attr.Type.Querier String_FL]> -----
    <virtual_wireless_interface.hardware.my_net_device.node.manager.middle_name.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.my_net_device.node.manager.title.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.my_net_device.node.manager.lifetime.AQ [Attr.Type.Querier Composite]> MOM.Date_Interval
    <virtual_wireless_interface.hardware.my_net_device.node.manager.lifetime.start.AQ [Attr.Type.Querier Date]> -----
    <virtual_wireless_interface.hardware.my_net_device.node.manager.lifetime.finish.AQ [Attr.Type.Querier Date]> -----
    <virtual_wireless_interface.hardware.my_net_device.node.manager.lifetime.alive.AQ [Attr.Type.Querier Boolean]> -----
    <virtual_wireless_interface.hardware.my_net_device.node.manager.sex.AQ [Attr.Type.Querier Ckd]> -----
    <virtual_wireless_interface.hardware.my_net_device.node.address.AQ [Attr.Type.Querier Id_Entity]> PAP.Address
    <virtual_wireless_interface.hardware.my_net_device.node.address.street.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.my_net_device.node.address.zip.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.my_net_device.node.address.city.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.my_net_device.node.address.country.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.my_net_device.node.address.desc.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.my_net_device.node.address.region.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.my_net_device.node.desc.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.my_net_device.node.owner.AQ [Attr.Type.Querier Id_Entity]> PAP.Subject
    <virtual_wireless_interface.hardware.my_net_device.node.position.AQ [Attr.Type.Querier Composite]> MOM.Position
    <virtual_wireless_interface.hardware.my_net_device.node.position.lat.AQ [Attr.Type.Querier Raw]> -----
    <virtual_wireless_interface.hardware.my_net_device.node.position.lon.AQ [Attr.Type.Querier Raw]> -----
    <virtual_wireless_interface.hardware.my_net_device.node.position.height.AQ [Attr.Type.Querier Ckd]> -----
    <virtual_wireless_interface.hardware.my_net_device.node.show_in_map.AQ [Attr.Type.Querier Boolean]> -----
    <virtual_wireless_interface.hardware.my_net_device.name.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.my_net_device.desc.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.my_net_device.my_node.AQ [Attr.Type.Querier Id_Entity]> FFM.Node
    <virtual_wireless_interface.hardware.my_net_device.my_node.name.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.my_net_device.my_node.manager.AQ [Attr.Type.Querier Id_Entity]> PAP.Person
    <virtual_wireless_interface.hardware.my_net_device.my_node.manager.last_name.AQ [Attr.Type.Querier String_FL]> -----
    <virtual_wireless_interface.hardware.my_net_device.my_node.manager.first_name.AQ [Attr.Type.Querier String_FL]> -----
    <virtual_wireless_interface.hardware.my_net_device.my_node.manager.middle_name.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.my_net_device.my_node.manager.title.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.my_net_device.my_node.manager.lifetime.AQ [Attr.Type.Querier Composite]> MOM.Date_Interval
    <virtual_wireless_interface.hardware.my_net_device.my_node.manager.lifetime.start.AQ [Attr.Type.Querier Date]> -----
    <virtual_wireless_interface.hardware.my_net_device.my_node.manager.lifetime.finish.AQ [Attr.Type.Querier Date]> -----
    <virtual_wireless_interface.hardware.my_net_device.my_node.manager.lifetime.alive.AQ [Attr.Type.Querier Boolean]> -----
    <virtual_wireless_interface.hardware.my_net_device.my_node.manager.sex.AQ [Attr.Type.Querier Ckd]> -----
    <virtual_wireless_interface.hardware.my_net_device.my_node.address.AQ [Attr.Type.Querier Id_Entity]> PAP.Address
    <virtual_wireless_interface.hardware.my_net_device.my_node.address.street.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.my_net_device.my_node.address.zip.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.my_net_device.my_node.address.city.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.my_net_device.my_node.address.country.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.my_net_device.my_node.address.desc.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.my_net_device.my_node.address.region.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.my_net_device.my_node.desc.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.hardware.my_net_device.my_node.owner.AQ [Attr.Type.Querier Id_Entity]> PAP.Subject
    <virtual_wireless_interface.hardware.my_net_device.my_node.position.AQ [Attr.Type.Querier Composite]> MOM.Position
    <virtual_wireless_interface.hardware.my_net_device.my_node.position.lat.AQ [Attr.Type.Querier Raw]> -----
    <virtual_wireless_interface.hardware.my_net_device.my_node.position.lon.AQ [Attr.Type.Querier Raw]> -----
    <virtual_wireless_interface.hardware.my_net_device.my_node.position.height.AQ [Attr.Type.Querier Ckd]> -----
    <virtual_wireless_interface.hardware.my_net_device.my_node.show_in_map.AQ [Attr.Type.Querier Boolean]> -----
    <virtual_wireless_interface.mac_address.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.name.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.is_active.AQ [Attr.Type.Querier Boolean]> -----
    <virtual_wireless_interface.desc.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.mode.AQ [Attr.Type.Querier Ckd]> -----
    <virtual_wireless_interface.essid.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.bssid.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.my_node.AQ [Attr.Type.Querier Id_Entity]> FFM.Node
    <virtual_wireless_interface.my_node.name.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.my_node.manager.AQ [Attr.Type.Querier Id_Entity]> PAP.Person
    <virtual_wireless_interface.my_node.manager.last_name.AQ [Attr.Type.Querier String_FL]> -----
    <virtual_wireless_interface.my_node.manager.first_name.AQ [Attr.Type.Querier String_FL]> -----
    <virtual_wireless_interface.my_node.manager.middle_name.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.my_node.manager.title.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.my_node.manager.lifetime.AQ [Attr.Type.Querier Composite]> MOM.Date_Interval
    <virtual_wireless_interface.my_node.manager.lifetime.start.AQ [Attr.Type.Querier Date]> -----
    <virtual_wireless_interface.my_node.manager.lifetime.finish.AQ [Attr.Type.Querier Date]> -----
    <virtual_wireless_interface.my_node.manager.lifetime.alive.AQ [Attr.Type.Querier Boolean]> -----
    <virtual_wireless_interface.my_node.manager.sex.AQ [Attr.Type.Querier Ckd]> -----
    <virtual_wireless_interface.my_node.address.AQ [Attr.Type.Querier Id_Entity]> PAP.Address
    <virtual_wireless_interface.my_node.address.street.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.my_node.address.zip.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.my_node.address.city.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.my_node.address.country.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.my_node.address.desc.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.my_node.address.region.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.my_node.desc.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.my_node.owner.AQ [Attr.Type.Querier Id_Entity]> PAP.Subject
    <virtual_wireless_interface.my_node.position.AQ [Attr.Type.Querier Composite]> MOM.Position
    <virtual_wireless_interface.my_node.position.lat.AQ [Attr.Type.Querier Raw]> -----
    <virtual_wireless_interface.my_node.position.lon.AQ [Attr.Type.Querier Raw]> -----
    <virtual_wireless_interface.my_node.position.height.AQ [Attr.Type.Querier Ckd]> -----
    <virtual_wireless_interface.my_node.show_in_map.AQ [Attr.Type.Querier Boolean]> -----
    <virtual_wireless_interface.my_net_device.AQ [Attr.Type.Querier Id_Entity]> FFM.Net_Device
    <virtual_wireless_interface.my_net_device.left.AQ [Attr.Type.Querier Id_Entity]> FFM.Net_Device_Type
    <virtual_wireless_interface.my_net_device.left.name.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.my_net_device.left.model_no.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.my_net_device.left.revision.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.my_net_device.left.desc.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.my_net_device.node.AQ [Attr.Type.Querier Id_Entity]> FFM.Node
    <virtual_wireless_interface.my_net_device.node.name.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.my_net_device.node.manager.AQ [Attr.Type.Querier Id_Entity]> PAP.Person
    <virtual_wireless_interface.my_net_device.node.manager.last_name.AQ [Attr.Type.Querier String_FL]> -----
    <virtual_wireless_interface.my_net_device.node.manager.first_name.AQ [Attr.Type.Querier String_FL]> -----
    <virtual_wireless_interface.my_net_device.node.manager.middle_name.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.my_net_device.node.manager.title.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.my_net_device.node.manager.lifetime.AQ [Attr.Type.Querier Composite]> MOM.Date_Interval
    <virtual_wireless_interface.my_net_device.node.manager.lifetime.start.AQ [Attr.Type.Querier Date]> -----
    <virtual_wireless_interface.my_net_device.node.manager.lifetime.finish.AQ [Attr.Type.Querier Date]> -----
    <virtual_wireless_interface.my_net_device.node.manager.lifetime.alive.AQ [Attr.Type.Querier Boolean]> -----
    <virtual_wireless_interface.my_net_device.node.manager.sex.AQ [Attr.Type.Querier Ckd]> -----
    <virtual_wireless_interface.my_net_device.node.address.AQ [Attr.Type.Querier Id_Entity]> PAP.Address
    <virtual_wireless_interface.my_net_device.node.address.street.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.my_net_device.node.address.zip.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.my_net_device.node.address.city.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.my_net_device.node.address.country.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.my_net_device.node.address.desc.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.my_net_device.node.address.region.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.my_net_device.node.desc.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.my_net_device.node.owner.AQ [Attr.Type.Querier Id_Entity]> PAP.Subject
    <virtual_wireless_interface.my_net_device.node.position.AQ [Attr.Type.Querier Composite]> MOM.Position
    <virtual_wireless_interface.my_net_device.node.position.lat.AQ [Attr.Type.Querier Raw]> -----
    <virtual_wireless_interface.my_net_device.node.position.lon.AQ [Attr.Type.Querier Raw]> -----
    <virtual_wireless_interface.my_net_device.node.position.height.AQ [Attr.Type.Querier Ckd]> -----
    <virtual_wireless_interface.my_net_device.node.show_in_map.AQ [Attr.Type.Querier Boolean]> -----
    <virtual_wireless_interface.my_net_device.name.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.my_net_device.desc.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.my_net_device.my_node.AQ [Attr.Type.Querier Id_Entity]> FFM.Node
    <virtual_wireless_interface.my_net_device.my_node.name.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.my_net_device.my_node.manager.AQ [Attr.Type.Querier Id_Entity]> PAP.Person
    <virtual_wireless_interface.my_net_device.my_node.manager.last_name.AQ [Attr.Type.Querier String_FL]> -----
    <virtual_wireless_interface.my_net_device.my_node.manager.first_name.AQ [Attr.Type.Querier String_FL]> -----
    <virtual_wireless_interface.my_net_device.my_node.manager.middle_name.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.my_net_device.my_node.manager.title.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.my_net_device.my_node.manager.lifetime.AQ [Attr.Type.Querier Composite]> MOM.Date_Interval
    <virtual_wireless_interface.my_net_device.my_node.manager.lifetime.start.AQ [Attr.Type.Querier Date]> -----
    <virtual_wireless_interface.my_net_device.my_node.manager.lifetime.finish.AQ [Attr.Type.Querier Date]> -----
    <virtual_wireless_interface.my_net_device.my_node.manager.lifetime.alive.AQ [Attr.Type.Querier Boolean]> -----
    <virtual_wireless_interface.my_net_device.my_node.manager.sex.AQ [Attr.Type.Querier Ckd]> -----
    <virtual_wireless_interface.my_net_device.my_node.address.AQ [Attr.Type.Querier Id_Entity]> PAP.Address
    <virtual_wireless_interface.my_net_device.my_node.address.street.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.my_net_device.my_node.address.zip.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.my_net_device.my_node.address.city.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.my_net_device.my_node.address.country.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.my_net_device.my_node.address.desc.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.my_net_device.my_node.address.region.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.my_net_device.my_node.desc.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.my_net_device.my_node.owner.AQ [Attr.Type.Querier Id_Entity]> PAP.Subject
    <virtual_wireless_interface.my_net_device.my_node.position.AQ [Attr.Type.Querier Composite]> MOM.Position
    <virtual_wireless_interface.my_net_device.my_node.position.lat.AQ [Attr.Type.Querier Raw]> -----
    <virtual_wireless_interface.my_net_device.my_node.position.lon.AQ [Attr.Type.Querier Raw]> -----
    <virtual_wireless_interface.my_net_device.my_node.position.height.AQ [Attr.Type.Querier Ckd]> -----
    <virtual_wireless_interface.my_net_device.my_node.show_in_map.AQ [Attr.Type.Querier Boolean]> -----
    <virtual_wireless_interface.standard.AQ [Attr.Type.Querier Id_Entity]> FFM.Wireless_Standard
    <virtual_wireless_interface.standard.name.AQ [Attr.Type.Querier String]> -----
    <virtual_wireless_interface.standard.bandwidth.AQ [Attr.Type.Querier Raw]> -----
    <virtual_wireless_interface.txpower.AQ [Attr.Type.Querier Raw]> -----

    >>> for aq in AQ.Attrs_Transitive :
    ...     str (aq._ui_name_T)
    'Net address'
    'Description'
    'Owner'
    'Creation'
    'Creation/C time'
    'Creation/C user'
    'Creation/Kind'
    'Creation/Time'
    'Creation/User'
    'Last change'
    'Last change/C time'
    'Last change/C user'
    'Last change/Kind'
    'Last change/Time'
    'Last change/User'
    'Last cid'
    'Pid'
    'Type name'
    'Expiration date'
    'Has children'
    'Is free'
    'Parent'
    'Parent/Net address'
    'Parent/Description'
    'Parent/Owner'
    'Parent/Expiration date'
    'Parent/Has children'
    'Parent/Is free'
    'Parent/Parent'
    'Ip pool'
    'Ip pool/Netmask interval'
    'Ip pool/Netmask interval/Lower'
    'Ip pool/Netmask interval/Upper'
    'Ip pool/Netmask interval/Center'
    'Ip pool/Netmask interval/Length'
    'Ip pool/Node'
    'Ip pool/Node/Name'
    'Ip pool/Node/Manager'
    'Ip pool/Node/Manager/Last name'
    'Ip pool/Node/Manager/First name'
    'Ip pool/Node/Manager/Middle name'
    'Ip pool/Node/Manager/Academic title'
    'Ip pool/Node/Manager/Lifetime'
    'Ip pool/Node/Manager/Lifetime/Start'
    'Ip pool/Node/Manager/Lifetime/Finish'
    'Ip pool/Node/Manager/Lifetime/Alive'
    'Ip pool/Node/Manager/Sex'
    'Ip pool/Node/Address'
    'Ip pool/Node/Address/Street'
    'Ip pool/Node/Address/Zip code'
    'Ip pool/Node/Address/City'
    'Ip pool/Node/Address/Country'
    'Ip pool/Node/Address/Description'
    'Ip pool/Node/Address/Region'
    'Ip pool/Node/Description'
    'Ip pool/Node/Owner'
    'Ip pool/Node/Position'
    'Ip pool/Node/Position/Latitude'
    'Ip pool/Node/Position/Longitude'
    'Ip pool/Node/Position/Height'
    'Ip pool/Node/Show in map'
    'Net interface'
    'Documents'
    'Documents/Url'
    'Documents/Type'
    'Documents/Description'
    'Wired interface'
    'Wired interface/Net device'
    'Wired interface/Net device/Net device type'
    'Wired interface/Net device/Net device type/Name'
    'Wired interface/Net device/Net device type/Model no'
    'Wired interface/Net device/Net device type/Revision'
    'Wired interface/Net device/Net device type/Description'
    'Wired interface/Net device/Node'
    'Wired interface/Net device/Node/Name'
    'Wired interface/Net device/Node/Manager'
    'Wired interface/Net device/Node/Manager/Last name'
    'Wired interface/Net device/Node/Manager/First name'
    'Wired interface/Net device/Node/Manager/Middle name'
    'Wired interface/Net device/Node/Manager/Academic title'
    'Wired interface/Net device/Node/Manager/Lifetime'
    'Wired interface/Net device/Node/Manager/Lifetime/Start'
    'Wired interface/Net device/Node/Manager/Lifetime/Finish'
    'Wired interface/Net device/Node/Manager/Lifetime/Alive'
    'Wired interface/Net device/Node/Manager/Sex'
    'Wired interface/Net device/Node/Address'
    'Wired interface/Net device/Node/Address/Street'
    'Wired interface/Net device/Node/Address/Zip code'
    'Wired interface/Net device/Node/Address/City'
    'Wired interface/Net device/Node/Address/Country'
    'Wired interface/Net device/Node/Address/Description'
    'Wired interface/Net device/Node/Address/Region'
    'Wired interface/Net device/Node/Description'
    'Wired interface/Net device/Node/Owner'
    'Wired interface/Net device/Node/Position'
    'Wired interface/Net device/Node/Position/Latitude'
    'Wired interface/Net device/Node/Position/Longitude'
    'Wired interface/Net device/Node/Position/Height'
    'Wired interface/Net device/Node/Show in map'
    'Wired interface/Net device/Name'
    'Wired interface/Net device/Description'
    'Wired interface/Net device/My node'
    'Wired interface/Net device/My node/Name'
    'Wired interface/Net device/My node/Manager'
    'Wired interface/Net device/My node/Manager/Last name'
    'Wired interface/Net device/My node/Manager/First name'
    'Wired interface/Net device/My node/Manager/Middle name'
    'Wired interface/Net device/My node/Manager/Academic title'
    'Wired interface/Net device/My node/Manager/Lifetime'
    'Wired interface/Net device/My node/Manager/Lifetime/Start'
    'Wired interface/Net device/My node/Manager/Lifetime/Finish'
    'Wired interface/Net device/My node/Manager/Lifetime/Alive'
    'Wired interface/Net device/My node/Manager/Sex'
    'Wired interface/Net device/My node/Address'
    'Wired interface/Net device/My node/Address/Street'
    'Wired interface/Net device/My node/Address/Zip code'
    'Wired interface/Net device/My node/Address/City'
    'Wired interface/Net device/My node/Address/Country'
    'Wired interface/Net device/My node/Address/Description'
    'Wired interface/Net device/My node/Address/Region'
    'Wired interface/Net device/My node/Description'
    'Wired interface/Net device/My node/Owner'
    'Wired interface/Net device/My node/Position'
    'Wired interface/Net device/My node/Position/Latitude'
    'Wired interface/Net device/My node/Position/Longitude'
    'Wired interface/Net device/My node/Position/Height'
    'Wired interface/Net device/My node/Show in map'
    'Wired interface/Mac address'
    'Wired interface/Name'
    'Wired interface/Is active'
    'Wired interface/Description'
    'Wired interface/My node'
    'Wired interface/My node/Name'
    'Wired interface/My node/Manager'
    'Wired interface/My node/Manager/Last name'
    'Wired interface/My node/Manager/First name'
    'Wired interface/My node/Manager/Middle name'
    'Wired interface/My node/Manager/Academic title'
    'Wired interface/My node/Manager/Lifetime'
    'Wired interface/My node/Manager/Lifetime/Start'
    'Wired interface/My node/Manager/Lifetime/Finish'
    'Wired interface/My node/Manager/Lifetime/Alive'
    'Wired interface/My node/Manager/Sex'
    'Wired interface/My node/Address'
    'Wired interface/My node/Address/Street'
    'Wired interface/My node/Address/Zip code'
    'Wired interface/My node/Address/City'
    'Wired interface/My node/Address/Country'
    'Wired interface/My node/Address/Description'
    'Wired interface/My node/Address/Region'
    'Wired interface/My node/Description'
    'Wired interface/My node/Owner'
    'Wired interface/My node/Position'
    'Wired interface/My node/Position/Latitude'
    'Wired interface/My node/Position/Longitude'
    'Wired interface/My node/Position/Height'
    'Wired interface/My node/Show in map'
    'Wired interface/My net device'
    'Wired interface/My net device/Net device type'
    'Wired interface/My net device/Net device type/Name'
    'Wired interface/My net device/Net device type/Model no'
    'Wired interface/My net device/Net device type/Revision'
    'Wired interface/My net device/Net device type/Description'
    'Wired interface/My net device/Node'
    'Wired interface/My net device/Node/Name'
    'Wired interface/My net device/Node/Manager'
    'Wired interface/My net device/Node/Manager/Last name'
    'Wired interface/My net device/Node/Manager/First name'
    'Wired interface/My net device/Node/Manager/Middle name'
    'Wired interface/My net device/Node/Manager/Academic title'
    'Wired interface/My net device/Node/Manager/Lifetime'
    'Wired interface/My net device/Node/Manager/Lifetime/Start'
    'Wired interface/My net device/Node/Manager/Lifetime/Finish'
    'Wired interface/My net device/Node/Manager/Lifetime/Alive'
    'Wired interface/My net device/Node/Manager/Sex'
    'Wired interface/My net device/Node/Address'
    'Wired interface/My net device/Node/Address/Street'
    'Wired interface/My net device/Node/Address/Zip code'
    'Wired interface/My net device/Node/Address/City'
    'Wired interface/My net device/Node/Address/Country'
    'Wired interface/My net device/Node/Address/Description'
    'Wired interface/My net device/Node/Address/Region'
    'Wired interface/My net device/Node/Description'
    'Wired interface/My net device/Node/Owner'
    'Wired interface/My net device/Node/Position'
    'Wired interface/My net device/Node/Position/Latitude'
    'Wired interface/My net device/Node/Position/Longitude'
    'Wired interface/My net device/Node/Position/Height'
    'Wired interface/My net device/Node/Show in map'
    'Wired interface/My net device/Name'
    'Wired interface/My net device/Description'
    'Wired interface/My net device/My node'
    'Wired interface/My net device/My node/Name'
    'Wired interface/My net device/My node/Manager'
    'Wired interface/My net device/My node/Manager/Last name'
    'Wired interface/My net device/My node/Manager/First name'
    'Wired interface/My net device/My node/Manager/Middle name'
    'Wired interface/My net device/My node/Manager/Academic title'
    'Wired interface/My net device/My node/Manager/Lifetime'
    'Wired interface/My net device/My node/Manager/Lifetime/Start'
    'Wired interface/My net device/My node/Manager/Lifetime/Finish'
    'Wired interface/My net device/My node/Manager/Lifetime/Alive'
    'Wired interface/My net device/My node/Manager/Sex'
    'Wired interface/My net device/My node/Address'
    'Wired interface/My net device/My node/Address/Street'
    'Wired interface/My net device/My node/Address/Zip code'
    'Wired interface/My net device/My node/Address/City'
    'Wired interface/My net device/My node/Address/Country'
    'Wired interface/My net device/My node/Address/Description'
    'Wired interface/My net device/My node/Address/Region'
    'Wired interface/My net device/My node/Description'
    'Wired interface/My net device/My node/Owner'
    'Wired interface/My net device/My node/Position'
    'Wired interface/My net device/My node/Position/Latitude'
    'Wired interface/My net device/My node/Position/Longitude'
    'Wired interface/My net device/My node/Position/Height'
    'Wired interface/My net device/My node/Show in map'
    'Wireless interface'
    'Wireless interface/Net device'
    'Wireless interface/Net device/Net device type'
    'Wireless interface/Net device/Net device type/Name'
    'Wireless interface/Net device/Net device type/Model no'
    'Wireless interface/Net device/Net device type/Revision'
    'Wireless interface/Net device/Net device type/Description'
    'Wireless interface/Net device/Node'
    'Wireless interface/Net device/Node/Name'
    'Wireless interface/Net device/Node/Manager'
    'Wireless interface/Net device/Node/Manager/Last name'
    'Wireless interface/Net device/Node/Manager/First name'
    'Wireless interface/Net device/Node/Manager/Middle name'
    'Wireless interface/Net device/Node/Manager/Academic title'
    'Wireless interface/Net device/Node/Manager/Lifetime'
    'Wireless interface/Net device/Node/Manager/Lifetime/Start'
    'Wireless interface/Net device/Node/Manager/Lifetime/Finish'
    'Wireless interface/Net device/Node/Manager/Lifetime/Alive'
    'Wireless interface/Net device/Node/Manager/Sex'
    'Wireless interface/Net device/Node/Address'
    'Wireless interface/Net device/Node/Address/Street'
    'Wireless interface/Net device/Node/Address/Zip code'
    'Wireless interface/Net device/Node/Address/City'
    'Wireless interface/Net device/Node/Address/Country'
    'Wireless interface/Net device/Node/Address/Description'
    'Wireless interface/Net device/Node/Address/Region'
    'Wireless interface/Net device/Node/Description'
    'Wireless interface/Net device/Node/Owner'
    'Wireless interface/Net device/Node/Position'
    'Wireless interface/Net device/Node/Position/Latitude'
    'Wireless interface/Net device/Node/Position/Longitude'
    'Wireless interface/Net device/Node/Position/Height'
    'Wireless interface/Net device/Node/Show in map'
    'Wireless interface/Net device/Name'
    'Wireless interface/Net device/Description'
    'Wireless interface/Net device/My node'
    'Wireless interface/Net device/My node/Name'
    'Wireless interface/Net device/My node/Manager'
    'Wireless interface/Net device/My node/Manager/Last name'
    'Wireless interface/Net device/My node/Manager/First name'
    'Wireless interface/Net device/My node/Manager/Middle name'
    'Wireless interface/Net device/My node/Manager/Academic title'
    'Wireless interface/Net device/My node/Manager/Lifetime'
    'Wireless interface/Net device/My node/Manager/Lifetime/Start'
    'Wireless interface/Net device/My node/Manager/Lifetime/Finish'
    'Wireless interface/Net device/My node/Manager/Lifetime/Alive'
    'Wireless interface/Net device/My node/Manager/Sex'
    'Wireless interface/Net device/My node/Address'
    'Wireless interface/Net device/My node/Address/Street'
    'Wireless interface/Net device/My node/Address/Zip code'
    'Wireless interface/Net device/My node/Address/City'
    'Wireless interface/Net device/My node/Address/Country'
    'Wireless interface/Net device/My node/Address/Description'
    'Wireless interface/Net device/My node/Address/Region'
    'Wireless interface/Net device/My node/Description'
    'Wireless interface/Net device/My node/Owner'
    'Wireless interface/Net device/My node/Position'
    'Wireless interface/Net device/My node/Position/Latitude'
    'Wireless interface/Net device/My node/Position/Longitude'
    'Wireless interface/Net device/My node/Position/Height'
    'Wireless interface/Net device/My node/Show in map'
    'Wireless interface/Mac address'
    'Wireless interface/Name'
    'Wireless interface/Is active'
    'Wireless interface/Description'
    'Wireless interface/Mode'
    'Wireless interface/ESSID'
    'Wireless interface/BSSID'
    'Wireless interface/Standard'
    'Wireless interface/Standard/Name'
    'Wireless interface/Standard/Bandwidth'
    'Wireless interface/TX power'
    'Wireless interface/My node'
    'Wireless interface/My node/Name'
    'Wireless interface/My node/Manager'
    'Wireless interface/My node/Manager/Last name'
    'Wireless interface/My node/Manager/First name'
    'Wireless interface/My node/Manager/Middle name'
    'Wireless interface/My node/Manager/Academic title'
    'Wireless interface/My node/Manager/Lifetime'
    'Wireless interface/My node/Manager/Lifetime/Start'
    'Wireless interface/My node/Manager/Lifetime/Finish'
    'Wireless interface/My node/Manager/Lifetime/Alive'
    'Wireless interface/My node/Manager/Sex'
    'Wireless interface/My node/Address'
    'Wireless interface/My node/Address/Street'
    'Wireless interface/My node/Address/Zip code'
    'Wireless interface/My node/Address/City'
    'Wireless interface/My node/Address/Country'
    'Wireless interface/My node/Address/Description'
    'Wireless interface/My node/Address/Region'
    'Wireless interface/My node/Description'
    'Wireless interface/My node/Owner'
    'Wireless interface/My node/Position'
    'Wireless interface/My node/Position/Latitude'
    'Wireless interface/My node/Position/Longitude'
    'Wireless interface/My node/Position/Height'
    'Wireless interface/My node/Show in map'
    'Wireless interface/My net device'
    'Wireless interface/My net device/Net device type'
    'Wireless interface/My net device/Net device type/Name'
    'Wireless interface/My net device/Net device type/Model no'
    'Wireless interface/My net device/Net device type/Revision'
    'Wireless interface/My net device/Net device type/Description'
    'Wireless interface/My net device/Node'
    'Wireless interface/My net device/Node/Name'
    'Wireless interface/My net device/Node/Manager'
    'Wireless interface/My net device/Node/Manager/Last name'
    'Wireless interface/My net device/Node/Manager/First name'
    'Wireless interface/My net device/Node/Manager/Middle name'
    'Wireless interface/My net device/Node/Manager/Academic title'
    'Wireless interface/My net device/Node/Manager/Lifetime'
    'Wireless interface/My net device/Node/Manager/Lifetime/Start'
    'Wireless interface/My net device/Node/Manager/Lifetime/Finish'
    'Wireless interface/My net device/Node/Manager/Lifetime/Alive'
    'Wireless interface/My net device/Node/Manager/Sex'
    'Wireless interface/My net device/Node/Address'
    'Wireless interface/My net device/Node/Address/Street'
    'Wireless interface/My net device/Node/Address/Zip code'
    'Wireless interface/My net device/Node/Address/City'
    'Wireless interface/My net device/Node/Address/Country'
    'Wireless interface/My net device/Node/Address/Description'
    'Wireless interface/My net device/Node/Address/Region'
    'Wireless interface/My net device/Node/Description'
    'Wireless interface/My net device/Node/Owner'
    'Wireless interface/My net device/Node/Position'
    'Wireless interface/My net device/Node/Position/Latitude'
    'Wireless interface/My net device/Node/Position/Longitude'
    'Wireless interface/My net device/Node/Position/Height'
    'Wireless interface/My net device/Node/Show in map'
    'Wireless interface/My net device/Name'
    'Wireless interface/My net device/Description'
    'Wireless interface/My net device/My node'
    'Wireless interface/My net device/My node/Name'
    'Wireless interface/My net device/My node/Manager'
    'Wireless interface/My net device/My node/Manager/Last name'
    'Wireless interface/My net device/My node/Manager/First name'
    'Wireless interface/My net device/My node/Manager/Middle name'
    'Wireless interface/My net device/My node/Manager/Academic title'
    'Wireless interface/My net device/My node/Manager/Lifetime'
    'Wireless interface/My net device/My node/Manager/Lifetime/Start'
    'Wireless interface/My net device/My node/Manager/Lifetime/Finish'
    'Wireless interface/My net device/My node/Manager/Lifetime/Alive'
    'Wireless interface/My net device/My node/Manager/Sex'
    'Wireless interface/My net device/My node/Address'
    'Wireless interface/My net device/My node/Address/Street'
    'Wireless interface/My net device/My node/Address/Zip code'
    'Wireless interface/My net device/My node/Address/City'
    'Wireless interface/My net device/My node/Address/Country'
    'Wireless interface/My net device/My node/Address/Description'
    'Wireless interface/My net device/My node/Address/Region'
    'Wireless interface/My net device/My node/Description'
    'Wireless interface/My net device/My node/Owner'
    'Wireless interface/My net device/My node/Position'
    'Wireless interface/My net device/My node/Position/Latitude'
    'Wireless interface/My net device/My node/Position/Longitude'
    'Wireless interface/My net device/My node/Position/Height'
    'Wireless interface/My net device/My node/Show in map'
    'Virtual wireless interface'
    'Virtual wireless interface/Net device'
    'Virtual wireless interface/Net device/Net device type'
    'Virtual wireless interface/Net device/Net device type/Name'
    'Virtual wireless interface/Net device/Net device type/Model no'
    'Virtual wireless interface/Net device/Net device type/Revision'
    'Virtual wireless interface/Net device/Net device type/Description'
    'Virtual wireless interface/Net device/Node'
    'Virtual wireless interface/Net device/Node/Name'
    'Virtual wireless interface/Net device/Node/Manager'
    'Virtual wireless interface/Net device/Node/Manager/Last name'
    'Virtual wireless interface/Net device/Node/Manager/First name'
    'Virtual wireless interface/Net device/Node/Manager/Middle name'
    'Virtual wireless interface/Net device/Node/Manager/Academic title'
    'Virtual wireless interface/Net device/Node/Manager/Lifetime'
    'Virtual wireless interface/Net device/Node/Manager/Lifetime/Start'
    'Virtual wireless interface/Net device/Node/Manager/Lifetime/Finish'
    'Virtual wireless interface/Net device/Node/Manager/Lifetime/Alive'
    'Virtual wireless interface/Net device/Node/Manager/Sex'
    'Virtual wireless interface/Net device/Node/Address'
    'Virtual wireless interface/Net device/Node/Address/Street'
    'Virtual wireless interface/Net device/Node/Address/Zip code'
    'Virtual wireless interface/Net device/Node/Address/City'
    'Virtual wireless interface/Net device/Node/Address/Country'
    'Virtual wireless interface/Net device/Node/Address/Description'
    'Virtual wireless interface/Net device/Node/Address/Region'
    'Virtual wireless interface/Net device/Node/Description'
    'Virtual wireless interface/Net device/Node/Owner'
    'Virtual wireless interface/Net device/Node/Position'
    'Virtual wireless interface/Net device/Node/Position/Latitude'
    'Virtual wireless interface/Net device/Node/Position/Longitude'
    'Virtual wireless interface/Net device/Node/Position/Height'
    'Virtual wireless interface/Net device/Node/Show in map'
    'Virtual wireless interface/Net device/Name'
    'Virtual wireless interface/Net device/Description'
    'Virtual wireless interface/Net device/My node'
    'Virtual wireless interface/Net device/My node/Name'
    'Virtual wireless interface/Net device/My node/Manager'
    'Virtual wireless interface/Net device/My node/Manager/Last name'
    'Virtual wireless interface/Net device/My node/Manager/First name'
    'Virtual wireless interface/Net device/My node/Manager/Middle name'
    'Virtual wireless interface/Net device/My node/Manager/Academic title'
    'Virtual wireless interface/Net device/My node/Manager/Lifetime'
    'Virtual wireless interface/Net device/My node/Manager/Lifetime/Start'
    'Virtual wireless interface/Net device/My node/Manager/Lifetime/Finish'
    'Virtual wireless interface/Net device/My node/Manager/Lifetime/Alive'
    'Virtual wireless interface/Net device/My node/Manager/Sex'
    'Virtual wireless interface/Net device/My node/Address'
    'Virtual wireless interface/Net device/My node/Address/Street'
    'Virtual wireless interface/Net device/My node/Address/Zip code'
    'Virtual wireless interface/Net device/My node/Address/City'
    'Virtual wireless interface/Net device/My node/Address/Country'
    'Virtual wireless interface/Net device/My node/Address/Description'
    'Virtual wireless interface/Net device/My node/Address/Region'
    'Virtual wireless interface/Net device/My node/Description'
    'Virtual wireless interface/Net device/My node/Owner'
    'Virtual wireless interface/Net device/My node/Position'
    'Virtual wireless interface/Net device/My node/Position/Latitude'
    'Virtual wireless interface/Net device/My node/Position/Longitude'
    'Virtual wireless interface/Net device/My node/Position/Height'
    'Virtual wireless interface/Net device/My node/Show in map'
    'Virtual wireless interface/Hardware'
    'Virtual wireless interface/Hardware/Net device'
    'Virtual wireless interface/Hardware/Net device/Net device type'
    'Virtual wireless interface/Hardware/Net device/Net device type/Name'
    'Virtual wireless interface/Hardware/Net device/Net device type/Model no'
    'Virtual wireless interface/Hardware/Net device/Net device type/Revision'
    'Virtual wireless interface/Hardware/Net device/Net device type/Description'
    'Virtual wireless interface/Hardware/Net device/Node'
    'Virtual wireless interface/Hardware/Net device/Node/Name'
    'Virtual wireless interface/Hardware/Net device/Node/Manager'
    'Virtual wireless interface/Hardware/Net device/Node/Manager/Last name'
    'Virtual wireless interface/Hardware/Net device/Node/Manager/First name'
    'Virtual wireless interface/Hardware/Net device/Node/Manager/Middle name'
    'Virtual wireless interface/Hardware/Net device/Node/Manager/Academic title'
    'Virtual wireless interface/Hardware/Net device/Node/Manager/Lifetime'
    'Virtual wireless interface/Hardware/Net device/Node/Manager/Lifetime/Start'
    'Virtual wireless interface/Hardware/Net device/Node/Manager/Lifetime/Finish'
    'Virtual wireless interface/Hardware/Net device/Node/Manager/Lifetime/Alive'
    'Virtual wireless interface/Hardware/Net device/Node/Manager/Sex'
    'Virtual wireless interface/Hardware/Net device/Node/Address'
    'Virtual wireless interface/Hardware/Net device/Node/Address/Street'
    'Virtual wireless interface/Hardware/Net device/Node/Address/Zip code'
    'Virtual wireless interface/Hardware/Net device/Node/Address/City'
    'Virtual wireless interface/Hardware/Net device/Node/Address/Country'
    'Virtual wireless interface/Hardware/Net device/Node/Address/Description'
    'Virtual wireless interface/Hardware/Net device/Node/Address/Region'
    'Virtual wireless interface/Hardware/Net device/Node/Description'
    'Virtual wireless interface/Hardware/Net device/Node/Owner'
    'Virtual wireless interface/Hardware/Net device/Node/Position'
    'Virtual wireless interface/Hardware/Net device/Node/Position/Latitude'
    'Virtual wireless interface/Hardware/Net device/Node/Position/Longitude'
    'Virtual wireless interface/Hardware/Net device/Node/Position/Height'
    'Virtual wireless interface/Hardware/Net device/Node/Show in map'
    'Virtual wireless interface/Hardware/Net device/Name'
    'Virtual wireless interface/Hardware/Net device/Description'
    'Virtual wireless interface/Hardware/Net device/My node'
    'Virtual wireless interface/Hardware/Net device/My node/Name'
    'Virtual wireless interface/Hardware/Net device/My node/Manager'
    'Virtual wireless interface/Hardware/Net device/My node/Manager/Last name'
    'Virtual wireless interface/Hardware/Net device/My node/Manager/First name'
    'Virtual wireless interface/Hardware/Net device/My node/Manager/Middle name'
    'Virtual wireless interface/Hardware/Net device/My node/Manager/Academic title'
    'Virtual wireless interface/Hardware/Net device/My node/Manager/Lifetime'
    'Virtual wireless interface/Hardware/Net device/My node/Manager/Lifetime/Start'
    'Virtual wireless interface/Hardware/Net device/My node/Manager/Lifetime/Finish'
    'Virtual wireless interface/Hardware/Net device/My node/Manager/Lifetime/Alive'
    'Virtual wireless interface/Hardware/Net device/My node/Manager/Sex'
    'Virtual wireless interface/Hardware/Net device/My node/Address'
    'Virtual wireless interface/Hardware/Net device/My node/Address/Street'
    'Virtual wireless interface/Hardware/Net device/My node/Address/Zip code'
    'Virtual wireless interface/Hardware/Net device/My node/Address/City'
    'Virtual wireless interface/Hardware/Net device/My node/Address/Country'
    'Virtual wireless interface/Hardware/Net device/My node/Address/Description'
    'Virtual wireless interface/Hardware/Net device/My node/Address/Region'
    'Virtual wireless interface/Hardware/Net device/My node/Description'
    'Virtual wireless interface/Hardware/Net device/My node/Owner'
    'Virtual wireless interface/Hardware/Net device/My node/Position'
    'Virtual wireless interface/Hardware/Net device/My node/Position/Latitude'
    'Virtual wireless interface/Hardware/Net device/My node/Position/Longitude'
    'Virtual wireless interface/Hardware/Net device/My node/Position/Height'
    'Virtual wireless interface/Hardware/Net device/My node/Show in map'
    'Virtual wireless interface/Hardware/Mac address'
    'Virtual wireless interface/Hardware/Name'
    'Virtual wireless interface/Hardware/Is active'
    'Virtual wireless interface/Hardware/Description'
    'Virtual wireless interface/Hardware/Mode'
    'Virtual wireless interface/Hardware/ESSID'
    'Virtual wireless interface/Hardware/BSSID'
    'Virtual wireless interface/Hardware/Standard'
    'Virtual wireless interface/Hardware/Standard/Name'
    'Virtual wireless interface/Hardware/Standard/Bandwidth'
    'Virtual wireless interface/Hardware/TX power'
    'Virtual wireless interface/Hardware/My node'
    'Virtual wireless interface/Hardware/My node/Name'
    'Virtual wireless interface/Hardware/My node/Manager'
    'Virtual wireless interface/Hardware/My node/Manager/Last name'
    'Virtual wireless interface/Hardware/My node/Manager/First name'
    'Virtual wireless interface/Hardware/My node/Manager/Middle name'
    'Virtual wireless interface/Hardware/My node/Manager/Academic title'
    'Virtual wireless interface/Hardware/My node/Manager/Lifetime'
    'Virtual wireless interface/Hardware/My node/Manager/Lifetime/Start'
    'Virtual wireless interface/Hardware/My node/Manager/Lifetime/Finish'
    'Virtual wireless interface/Hardware/My node/Manager/Lifetime/Alive'
    'Virtual wireless interface/Hardware/My node/Manager/Sex'
    'Virtual wireless interface/Hardware/My node/Address'
    'Virtual wireless interface/Hardware/My node/Address/Street'
    'Virtual wireless interface/Hardware/My node/Address/Zip code'
    'Virtual wireless interface/Hardware/My node/Address/City'
    'Virtual wireless interface/Hardware/My node/Address/Country'
    'Virtual wireless interface/Hardware/My node/Address/Description'
    'Virtual wireless interface/Hardware/My node/Address/Region'
    'Virtual wireless interface/Hardware/My node/Description'
    'Virtual wireless interface/Hardware/My node/Owner'
    'Virtual wireless interface/Hardware/My node/Position'
    'Virtual wireless interface/Hardware/My node/Position/Latitude'
    'Virtual wireless interface/Hardware/My node/Position/Longitude'
    'Virtual wireless interface/Hardware/My node/Position/Height'
    'Virtual wireless interface/Hardware/My node/Show in map'
    'Virtual wireless interface/Hardware/My net device'
    'Virtual wireless interface/Hardware/My net device/Net device type'
    'Virtual wireless interface/Hardware/My net device/Net device type/Name'
    'Virtual wireless interface/Hardware/My net device/Net device type/Model no'
    'Virtual wireless interface/Hardware/My net device/Net device type/Revision'
    'Virtual wireless interface/Hardware/My net device/Net device type/Description'
    'Virtual wireless interface/Hardware/My net device/Node'
    'Virtual wireless interface/Hardware/My net device/Node/Name'
    'Virtual wireless interface/Hardware/My net device/Node/Manager'
    'Virtual wireless interface/Hardware/My net device/Node/Manager/Last name'
    'Virtual wireless interface/Hardware/My net device/Node/Manager/First name'
    'Virtual wireless interface/Hardware/My net device/Node/Manager/Middle name'
    'Virtual wireless interface/Hardware/My net device/Node/Manager/Academic title'
    'Virtual wireless interface/Hardware/My net device/Node/Manager/Lifetime'
    'Virtual wireless interface/Hardware/My net device/Node/Manager/Lifetime/Start'
    'Virtual wireless interface/Hardware/My net device/Node/Manager/Lifetime/Finish'
    'Virtual wireless interface/Hardware/My net device/Node/Manager/Lifetime/Alive'
    'Virtual wireless interface/Hardware/My net device/Node/Manager/Sex'
    'Virtual wireless interface/Hardware/My net device/Node/Address'
    'Virtual wireless interface/Hardware/My net device/Node/Address/Street'
    'Virtual wireless interface/Hardware/My net device/Node/Address/Zip code'
    'Virtual wireless interface/Hardware/My net device/Node/Address/City'
    'Virtual wireless interface/Hardware/My net device/Node/Address/Country'
    'Virtual wireless interface/Hardware/My net device/Node/Address/Description'
    'Virtual wireless interface/Hardware/My net device/Node/Address/Region'
    'Virtual wireless interface/Hardware/My net device/Node/Description'
    'Virtual wireless interface/Hardware/My net device/Node/Owner'
    'Virtual wireless interface/Hardware/My net device/Node/Position'
    'Virtual wireless interface/Hardware/My net device/Node/Position/Latitude'
    'Virtual wireless interface/Hardware/My net device/Node/Position/Longitude'
    'Virtual wireless interface/Hardware/My net device/Node/Position/Height'
    'Virtual wireless interface/Hardware/My net device/Node/Show in map'
    'Virtual wireless interface/Hardware/My net device/Name'
    'Virtual wireless interface/Hardware/My net device/Description'
    'Virtual wireless interface/Hardware/My net device/My node'
    'Virtual wireless interface/Hardware/My net device/My node/Name'
    'Virtual wireless interface/Hardware/My net device/My node/Manager'
    'Virtual wireless interface/Hardware/My net device/My node/Manager/Last name'
    'Virtual wireless interface/Hardware/My net device/My node/Manager/First name'
    'Virtual wireless interface/Hardware/My net device/My node/Manager/Middle name'
    'Virtual wireless interface/Hardware/My net device/My node/Manager/Academic title'
    'Virtual wireless interface/Hardware/My net device/My node/Manager/Lifetime'
    'Virtual wireless interface/Hardware/My net device/My node/Manager/Lifetime/Start'
    'Virtual wireless interface/Hardware/My net device/My node/Manager/Lifetime/Finish'
    'Virtual wireless interface/Hardware/My net device/My node/Manager/Lifetime/Alive'
    'Virtual wireless interface/Hardware/My net device/My node/Manager/Sex'
    'Virtual wireless interface/Hardware/My net device/My node/Address'
    'Virtual wireless interface/Hardware/My net device/My node/Address/Street'
    'Virtual wireless interface/Hardware/My net device/My node/Address/Zip code'
    'Virtual wireless interface/Hardware/My net device/My node/Address/City'
    'Virtual wireless interface/Hardware/My net device/My node/Address/Country'
    'Virtual wireless interface/Hardware/My net device/My node/Address/Description'
    'Virtual wireless interface/Hardware/My net device/My node/Address/Region'
    'Virtual wireless interface/Hardware/My net device/My node/Description'
    'Virtual wireless interface/Hardware/My net device/My node/Owner'
    'Virtual wireless interface/Hardware/My net device/My node/Position'
    'Virtual wireless interface/Hardware/My net device/My node/Position/Latitude'
    'Virtual wireless interface/Hardware/My net device/My node/Position/Longitude'
    'Virtual wireless interface/Hardware/My net device/My node/Position/Height'
    'Virtual wireless interface/Hardware/My net device/My node/Show in map'
    'Virtual wireless interface/Mac address'
    'Virtual wireless interface/Name'
    'Virtual wireless interface/Is active'
    'Virtual wireless interface/Description'
    'Virtual wireless interface/Mode'
    'Virtual wireless interface/ESSID'
    'Virtual wireless interface/BSSID'
    'Virtual wireless interface/My node'
    'Virtual wireless interface/My node/Name'
    'Virtual wireless interface/My node/Manager'
    'Virtual wireless interface/My node/Manager/Last name'
    'Virtual wireless interface/My node/Manager/First name'
    'Virtual wireless interface/My node/Manager/Middle name'
    'Virtual wireless interface/My node/Manager/Academic title'
    'Virtual wireless interface/My node/Manager/Lifetime'
    'Virtual wireless interface/My node/Manager/Lifetime/Start'
    'Virtual wireless interface/My node/Manager/Lifetime/Finish'
    'Virtual wireless interface/My node/Manager/Lifetime/Alive'
    'Virtual wireless interface/My node/Manager/Sex'
    'Virtual wireless interface/My node/Address'
    'Virtual wireless interface/My node/Address/Street'
    'Virtual wireless interface/My node/Address/Zip code'
    'Virtual wireless interface/My node/Address/City'
    'Virtual wireless interface/My node/Address/Country'
    'Virtual wireless interface/My node/Address/Description'
    'Virtual wireless interface/My node/Address/Region'
    'Virtual wireless interface/My node/Description'
    'Virtual wireless interface/My node/Owner'
    'Virtual wireless interface/My node/Position'
    'Virtual wireless interface/My node/Position/Latitude'
    'Virtual wireless interface/My node/Position/Longitude'
    'Virtual wireless interface/My node/Position/Height'
    'Virtual wireless interface/My node/Show in map'
    'Virtual wireless interface/My net device'
    'Virtual wireless interface/My net device/Net device type'
    'Virtual wireless interface/My net device/Net device type/Name'
    'Virtual wireless interface/My net device/Net device type/Model no'
    'Virtual wireless interface/My net device/Net device type/Revision'
    'Virtual wireless interface/My net device/Net device type/Description'
    'Virtual wireless interface/My net device/Node'
    'Virtual wireless interface/My net device/Node/Name'
    'Virtual wireless interface/My net device/Node/Manager'
    'Virtual wireless interface/My net device/Node/Manager/Last name'
    'Virtual wireless interface/My net device/Node/Manager/First name'
    'Virtual wireless interface/My net device/Node/Manager/Middle name'
    'Virtual wireless interface/My net device/Node/Manager/Academic title'
    'Virtual wireless interface/My net device/Node/Manager/Lifetime'
    'Virtual wireless interface/My net device/Node/Manager/Lifetime/Start'
    'Virtual wireless interface/My net device/Node/Manager/Lifetime/Finish'
    'Virtual wireless interface/My net device/Node/Manager/Lifetime/Alive'
    'Virtual wireless interface/My net device/Node/Manager/Sex'
    'Virtual wireless interface/My net device/Node/Address'
    'Virtual wireless interface/My net device/Node/Address/Street'
    'Virtual wireless interface/My net device/Node/Address/Zip code'
    'Virtual wireless interface/My net device/Node/Address/City'
    'Virtual wireless interface/My net device/Node/Address/Country'
    'Virtual wireless interface/My net device/Node/Address/Description'
    'Virtual wireless interface/My net device/Node/Address/Region'
    'Virtual wireless interface/My net device/Node/Description'
    'Virtual wireless interface/My net device/Node/Owner'
    'Virtual wireless interface/My net device/Node/Position'
    'Virtual wireless interface/My net device/Node/Position/Latitude'
    'Virtual wireless interface/My net device/Node/Position/Longitude'
    'Virtual wireless interface/My net device/Node/Position/Height'
    'Virtual wireless interface/My net device/Node/Show in map'
    'Virtual wireless interface/My net device/Name'
    'Virtual wireless interface/My net device/Description'
    'Virtual wireless interface/My net device/My node'
    'Virtual wireless interface/My net device/My node/Name'
    'Virtual wireless interface/My net device/My node/Manager'
    'Virtual wireless interface/My net device/My node/Manager/Last name'
    'Virtual wireless interface/My net device/My node/Manager/First name'
    'Virtual wireless interface/My net device/My node/Manager/Middle name'
    'Virtual wireless interface/My net device/My node/Manager/Academic title'
    'Virtual wireless interface/My net device/My node/Manager/Lifetime'
    'Virtual wireless interface/My net device/My node/Manager/Lifetime/Start'
    'Virtual wireless interface/My net device/My node/Manager/Lifetime/Finish'
    'Virtual wireless interface/My net device/My node/Manager/Lifetime/Alive'
    'Virtual wireless interface/My net device/My node/Manager/Sex'
    'Virtual wireless interface/My net device/My node/Address'
    'Virtual wireless interface/My net device/My node/Address/Street'
    'Virtual wireless interface/My net device/My node/Address/Zip code'
    'Virtual wireless interface/My net device/My node/Address/City'
    'Virtual wireless interface/My net device/My node/Address/Country'
    'Virtual wireless interface/My net device/My node/Address/Description'
    'Virtual wireless interface/My net device/My node/Address/Region'
    'Virtual wireless interface/My net device/My node/Description'
    'Virtual wireless interface/My net device/My node/Owner'
    'Virtual wireless interface/My net device/My node/Position'
    'Virtual wireless interface/My net device/My node/Position/Latitude'
    'Virtual wireless interface/My net device/My node/Position/Longitude'
    'Virtual wireless interface/My net device/My node/Position/Height'
    'Virtual wireless interface/My net device/My node/Show in map'
    'Virtual wireless interface/Standard'
    'Virtual wireless interface/Standard/Name'
    'Virtual wireless interface/Standard/Bandwidth'
    'Virtual wireless interface/TX power'

    >>> AQ.parent.parent.parent.owner
    <parent.parent.parent.owner.AQ [Attr.Type.Querier Id_Entity]>

    >>> for aq in AQ.Atoms :
    ...     print (aq)
    <net_address.AQ [Attr.Type.Querier Ckd]>
    <desc.AQ [Attr.Type.Querier String]>
    <creation.c_time.AQ [Attr.Type.Querier Ckd]>
    <creation.kind.AQ [Attr.Type.Querier String]>
    <creation.time.AQ [Attr.Type.Querier Ckd]>
    <last_change.c_time.AQ [Attr.Type.Querier Ckd]>
    <last_change.kind.AQ [Attr.Type.Querier String]>
    <last_change.time.AQ [Attr.Type.Querier Ckd]>
    <last_cid.AQ [Attr.Type.Querier Ckd]>
    <pid.AQ [Attr.Type.Querier Ckd]>
    <type_name.AQ [Attr.Type.Querier String]>
    <expiration_date.AQ [Attr.Type.Querier Ckd]>
    <has_children.AQ [Attr.Type.Querier Boolean]>
    <is_free.AQ [Attr.Type.Querier Boolean]>
    <parent.net_address.AQ [Attr.Type.Querier Ckd]>
    <parent.desc.AQ [Attr.Type.Querier String]>
    <parent.expiration_date.AQ [Attr.Type.Querier Ckd]>
    <parent.has_children.AQ [Attr.Type.Querier Boolean]>
    <parent.is_free.AQ [Attr.Type.Querier Boolean]>
    <ip_pool.netmask_interval.lower.AQ [Attr.Type.Querier Ckd]>
    <ip_pool.netmask_interval.upper.AQ [Attr.Type.Querier Ckd]>
    <ip_pool.netmask_interval.center.AQ [Attr.Type.Querier Ckd]>
    <ip_pool.netmask_interval.length.AQ [Attr.Type.Querier Ckd]>
    <ip_pool.node.name.AQ [Attr.Type.Querier String]>
    <ip_pool.node.manager.last_name.AQ [Attr.Type.Querier String_FL]>
    <ip_pool.node.manager.first_name.AQ [Attr.Type.Querier String_FL]>
    <ip_pool.node.manager.middle_name.AQ [Attr.Type.Querier String]>
    <ip_pool.node.manager.title.AQ [Attr.Type.Querier String]>
    <ip_pool.node.manager.lifetime.start.AQ [Attr.Type.Querier Date]>
    <ip_pool.node.manager.lifetime.finish.AQ [Attr.Type.Querier Date]>
    <ip_pool.node.manager.lifetime.alive.AQ [Attr.Type.Querier Boolean]>
    <ip_pool.node.manager.sex.AQ [Attr.Type.Querier Ckd]>
    <ip_pool.node.address.street.AQ [Attr.Type.Querier String]>
    <ip_pool.node.address.zip.AQ [Attr.Type.Querier String]>
    <ip_pool.node.address.city.AQ [Attr.Type.Querier String]>
    <ip_pool.node.address.country.AQ [Attr.Type.Querier String]>
    <ip_pool.node.address.desc.AQ [Attr.Type.Querier String]>
    <ip_pool.node.address.region.AQ [Attr.Type.Querier String]>
    <ip_pool.node.desc.AQ [Attr.Type.Querier String]>
    <ip_pool.node.position.lat.AQ [Attr.Type.Querier Raw]>
    <ip_pool.node.position.lon.AQ [Attr.Type.Querier Raw]>
    <ip_pool.node.position.height.AQ [Attr.Type.Querier Ckd]>
    <ip_pool.node.show_in_map.AQ [Attr.Type.Querier Boolean]>
    <documents.url.AQ [Attr.Type.Querier String]>
    <documents.type.AQ [Attr.Type.Querier String]>
    <documents.desc.AQ [Attr.Type.Querier String]>
    <wired_interface.left.left.name.AQ [Attr.Type.Querier String]>
    <wired_interface.left.left.model_no.AQ [Attr.Type.Querier String]>
    <wired_interface.left.left.revision.AQ [Attr.Type.Querier String]>
    <wired_interface.left.left.desc.AQ [Attr.Type.Querier String]>
    <wired_interface.left.node.name.AQ [Attr.Type.Querier String]>
    <wired_interface.left.node.manager.last_name.AQ [Attr.Type.Querier String_FL]>
    <wired_interface.left.node.manager.first_name.AQ [Attr.Type.Querier String_FL]>
    <wired_interface.left.node.manager.middle_name.AQ [Attr.Type.Querier String]>
    <wired_interface.left.node.manager.title.AQ [Attr.Type.Querier String]>
    <wired_interface.left.node.manager.lifetime.start.AQ [Attr.Type.Querier Date]>
    <wired_interface.left.node.manager.lifetime.finish.AQ [Attr.Type.Querier Date]>
    <wired_interface.left.node.manager.lifetime.alive.AQ [Attr.Type.Querier Boolean]>
    <wired_interface.left.node.manager.sex.AQ [Attr.Type.Querier Ckd]>
    <wired_interface.left.node.address.street.AQ [Attr.Type.Querier String]>
    <wired_interface.left.node.address.zip.AQ [Attr.Type.Querier String]>
    <wired_interface.left.node.address.city.AQ [Attr.Type.Querier String]>
    <wired_interface.left.node.address.country.AQ [Attr.Type.Querier String]>
    <wired_interface.left.node.address.desc.AQ [Attr.Type.Querier String]>
    <wired_interface.left.node.address.region.AQ [Attr.Type.Querier String]>
    <wired_interface.left.node.desc.AQ [Attr.Type.Querier String]>
    <wired_interface.left.node.position.lat.AQ [Attr.Type.Querier Raw]>
    <wired_interface.left.node.position.lon.AQ [Attr.Type.Querier Raw]>
    <wired_interface.left.node.position.height.AQ [Attr.Type.Querier Ckd]>
    <wired_interface.left.node.show_in_map.AQ [Attr.Type.Querier Boolean]>
    <wired_interface.left.name.AQ [Attr.Type.Querier String]>
    <wired_interface.left.desc.AQ [Attr.Type.Querier String]>
    <wired_interface.left.my_node.name.AQ [Attr.Type.Querier String]>
    <wired_interface.left.my_node.manager.last_name.AQ [Attr.Type.Querier String_FL]>
    <wired_interface.left.my_node.manager.first_name.AQ [Attr.Type.Querier String_FL]>
    <wired_interface.left.my_node.manager.middle_name.AQ [Attr.Type.Querier String]>
    <wired_interface.left.my_node.manager.title.AQ [Attr.Type.Querier String]>
    <wired_interface.left.my_node.manager.lifetime.start.AQ [Attr.Type.Querier Date]>
    <wired_interface.left.my_node.manager.lifetime.finish.AQ [Attr.Type.Querier Date]>
    <wired_interface.left.my_node.manager.lifetime.alive.AQ [Attr.Type.Querier Boolean]>
    <wired_interface.left.my_node.manager.sex.AQ [Attr.Type.Querier Ckd]>
    <wired_interface.left.my_node.address.street.AQ [Attr.Type.Querier String]>
    <wired_interface.left.my_node.address.zip.AQ [Attr.Type.Querier String]>
    <wired_interface.left.my_node.address.city.AQ [Attr.Type.Querier String]>
    <wired_interface.left.my_node.address.country.AQ [Attr.Type.Querier String]>
    <wired_interface.left.my_node.address.desc.AQ [Attr.Type.Querier String]>
    <wired_interface.left.my_node.address.region.AQ [Attr.Type.Querier String]>
    <wired_interface.left.my_node.desc.AQ [Attr.Type.Querier String]>
    <wired_interface.left.my_node.position.lat.AQ [Attr.Type.Querier Raw]>
    <wired_interface.left.my_node.position.lon.AQ [Attr.Type.Querier Raw]>
    <wired_interface.left.my_node.position.height.AQ [Attr.Type.Querier Ckd]>
    <wired_interface.left.my_node.show_in_map.AQ [Attr.Type.Querier Boolean]>
    <wired_interface.mac_address.AQ [Attr.Type.Querier String]>
    <wired_interface.name.AQ [Attr.Type.Querier String]>
    <wired_interface.is_active.AQ [Attr.Type.Querier Boolean]>
    <wired_interface.desc.AQ [Attr.Type.Querier String]>
    <wired_interface.my_node.name.AQ [Attr.Type.Querier String]>
    <wired_interface.my_node.manager.last_name.AQ [Attr.Type.Querier String_FL]>
    <wired_interface.my_node.manager.first_name.AQ [Attr.Type.Querier String_FL]>
    <wired_interface.my_node.manager.middle_name.AQ [Attr.Type.Querier String]>
    <wired_interface.my_node.manager.title.AQ [Attr.Type.Querier String]>
    <wired_interface.my_node.manager.lifetime.start.AQ [Attr.Type.Querier Date]>
    <wired_interface.my_node.manager.lifetime.finish.AQ [Attr.Type.Querier Date]>
    <wired_interface.my_node.manager.lifetime.alive.AQ [Attr.Type.Querier Boolean]>
    <wired_interface.my_node.manager.sex.AQ [Attr.Type.Querier Ckd]>
    <wired_interface.my_node.address.street.AQ [Attr.Type.Querier String]>
    <wired_interface.my_node.address.zip.AQ [Attr.Type.Querier String]>
    <wired_interface.my_node.address.city.AQ [Attr.Type.Querier String]>
    <wired_interface.my_node.address.country.AQ [Attr.Type.Querier String]>
    <wired_interface.my_node.address.desc.AQ [Attr.Type.Querier String]>
    <wired_interface.my_node.address.region.AQ [Attr.Type.Querier String]>
    <wired_interface.my_node.desc.AQ [Attr.Type.Querier String]>
    <wired_interface.my_node.position.lat.AQ [Attr.Type.Querier Raw]>
    <wired_interface.my_node.position.lon.AQ [Attr.Type.Querier Raw]>
    <wired_interface.my_node.position.height.AQ [Attr.Type.Querier Ckd]>
    <wired_interface.my_node.show_in_map.AQ [Attr.Type.Querier Boolean]>
    <wired_interface.my_net_device.left.name.AQ [Attr.Type.Querier String]>
    <wired_interface.my_net_device.left.model_no.AQ [Attr.Type.Querier String]>
    <wired_interface.my_net_device.left.revision.AQ [Attr.Type.Querier String]>
    <wired_interface.my_net_device.left.desc.AQ [Attr.Type.Querier String]>
    <wired_interface.my_net_device.node.name.AQ [Attr.Type.Querier String]>
    <wired_interface.my_net_device.node.manager.last_name.AQ [Attr.Type.Querier String_FL]>
    <wired_interface.my_net_device.node.manager.first_name.AQ [Attr.Type.Querier String_FL]>
    <wired_interface.my_net_device.node.manager.middle_name.AQ [Attr.Type.Querier String]>
    <wired_interface.my_net_device.node.manager.title.AQ [Attr.Type.Querier String]>
    <wired_interface.my_net_device.node.manager.lifetime.start.AQ [Attr.Type.Querier Date]>
    <wired_interface.my_net_device.node.manager.lifetime.finish.AQ [Attr.Type.Querier Date]>
    <wired_interface.my_net_device.node.manager.lifetime.alive.AQ [Attr.Type.Querier Boolean]>
    <wired_interface.my_net_device.node.manager.sex.AQ [Attr.Type.Querier Ckd]>
    <wired_interface.my_net_device.node.address.street.AQ [Attr.Type.Querier String]>
    <wired_interface.my_net_device.node.address.zip.AQ [Attr.Type.Querier String]>
    <wired_interface.my_net_device.node.address.city.AQ [Attr.Type.Querier String]>
    <wired_interface.my_net_device.node.address.country.AQ [Attr.Type.Querier String]>
    <wired_interface.my_net_device.node.address.desc.AQ [Attr.Type.Querier String]>
    <wired_interface.my_net_device.node.address.region.AQ [Attr.Type.Querier String]>
    <wired_interface.my_net_device.node.desc.AQ [Attr.Type.Querier String]>
    <wired_interface.my_net_device.node.position.lat.AQ [Attr.Type.Querier Raw]>
    <wired_interface.my_net_device.node.position.lon.AQ [Attr.Type.Querier Raw]>
    <wired_interface.my_net_device.node.position.height.AQ [Attr.Type.Querier Ckd]>
    <wired_interface.my_net_device.node.show_in_map.AQ [Attr.Type.Querier Boolean]>
    <wired_interface.my_net_device.name.AQ [Attr.Type.Querier String]>
    <wired_interface.my_net_device.desc.AQ [Attr.Type.Querier String]>
    <wired_interface.my_net_device.my_node.name.AQ [Attr.Type.Querier String]>
    <wired_interface.my_net_device.my_node.manager.last_name.AQ [Attr.Type.Querier String_FL]>
    <wired_interface.my_net_device.my_node.manager.first_name.AQ [Attr.Type.Querier String_FL]>
    <wired_interface.my_net_device.my_node.manager.middle_name.AQ [Attr.Type.Querier String]>
    <wired_interface.my_net_device.my_node.manager.title.AQ [Attr.Type.Querier String]>
    <wired_interface.my_net_device.my_node.manager.lifetime.start.AQ [Attr.Type.Querier Date]>
    <wired_interface.my_net_device.my_node.manager.lifetime.finish.AQ [Attr.Type.Querier Date]>
    <wired_interface.my_net_device.my_node.manager.lifetime.alive.AQ [Attr.Type.Querier Boolean]>
    <wired_interface.my_net_device.my_node.manager.sex.AQ [Attr.Type.Querier Ckd]>
    <wired_interface.my_net_device.my_node.address.street.AQ [Attr.Type.Querier String]>
    <wired_interface.my_net_device.my_node.address.zip.AQ [Attr.Type.Querier String]>
    <wired_interface.my_net_device.my_node.address.city.AQ [Attr.Type.Querier String]>
    <wired_interface.my_net_device.my_node.address.country.AQ [Attr.Type.Querier String]>
    <wired_interface.my_net_device.my_node.address.desc.AQ [Attr.Type.Querier String]>
    <wired_interface.my_net_device.my_node.address.region.AQ [Attr.Type.Querier String]>
    <wired_interface.my_net_device.my_node.desc.AQ [Attr.Type.Querier String]>
    <wired_interface.my_net_device.my_node.position.lat.AQ [Attr.Type.Querier Raw]>
    <wired_interface.my_net_device.my_node.position.lon.AQ [Attr.Type.Querier Raw]>
    <wired_interface.my_net_device.my_node.position.height.AQ [Attr.Type.Querier Ckd]>
    <wired_interface.my_net_device.my_node.show_in_map.AQ [Attr.Type.Querier Boolean]>
    <wireless_interface.left.left.name.AQ [Attr.Type.Querier String]>
    <wireless_interface.left.left.model_no.AQ [Attr.Type.Querier String]>
    <wireless_interface.left.left.revision.AQ [Attr.Type.Querier String]>
    <wireless_interface.left.left.desc.AQ [Attr.Type.Querier String]>
    <wireless_interface.left.node.name.AQ [Attr.Type.Querier String]>
    <wireless_interface.left.node.manager.last_name.AQ [Attr.Type.Querier String_FL]>
    <wireless_interface.left.node.manager.first_name.AQ [Attr.Type.Querier String_FL]>
    <wireless_interface.left.node.manager.middle_name.AQ [Attr.Type.Querier String]>
    <wireless_interface.left.node.manager.title.AQ [Attr.Type.Querier String]>
    <wireless_interface.left.node.manager.lifetime.start.AQ [Attr.Type.Querier Date]>
    <wireless_interface.left.node.manager.lifetime.finish.AQ [Attr.Type.Querier Date]>
    <wireless_interface.left.node.manager.lifetime.alive.AQ [Attr.Type.Querier Boolean]>
    <wireless_interface.left.node.manager.sex.AQ [Attr.Type.Querier Ckd]>
    <wireless_interface.left.node.address.street.AQ [Attr.Type.Querier String]>
    <wireless_interface.left.node.address.zip.AQ [Attr.Type.Querier String]>
    <wireless_interface.left.node.address.city.AQ [Attr.Type.Querier String]>
    <wireless_interface.left.node.address.country.AQ [Attr.Type.Querier String]>
    <wireless_interface.left.node.address.desc.AQ [Attr.Type.Querier String]>
    <wireless_interface.left.node.address.region.AQ [Attr.Type.Querier String]>
    <wireless_interface.left.node.desc.AQ [Attr.Type.Querier String]>
    <wireless_interface.left.node.position.lat.AQ [Attr.Type.Querier Raw]>
    <wireless_interface.left.node.position.lon.AQ [Attr.Type.Querier Raw]>
    <wireless_interface.left.node.position.height.AQ [Attr.Type.Querier Ckd]>
    <wireless_interface.left.node.show_in_map.AQ [Attr.Type.Querier Boolean]>
    <wireless_interface.left.name.AQ [Attr.Type.Querier String]>
    <wireless_interface.left.desc.AQ [Attr.Type.Querier String]>
    <wireless_interface.left.my_node.name.AQ [Attr.Type.Querier String]>
    <wireless_interface.left.my_node.manager.last_name.AQ [Attr.Type.Querier String_FL]>
    <wireless_interface.left.my_node.manager.first_name.AQ [Attr.Type.Querier String_FL]>
    <wireless_interface.left.my_node.manager.middle_name.AQ [Attr.Type.Querier String]>
    <wireless_interface.left.my_node.manager.title.AQ [Attr.Type.Querier String]>
    <wireless_interface.left.my_node.manager.lifetime.start.AQ [Attr.Type.Querier Date]>
    <wireless_interface.left.my_node.manager.lifetime.finish.AQ [Attr.Type.Querier Date]>
    <wireless_interface.left.my_node.manager.lifetime.alive.AQ [Attr.Type.Querier Boolean]>
    <wireless_interface.left.my_node.manager.sex.AQ [Attr.Type.Querier Ckd]>
    <wireless_interface.left.my_node.address.street.AQ [Attr.Type.Querier String]>
    <wireless_interface.left.my_node.address.zip.AQ [Attr.Type.Querier String]>
    <wireless_interface.left.my_node.address.city.AQ [Attr.Type.Querier String]>
    <wireless_interface.left.my_node.address.country.AQ [Attr.Type.Querier String]>
    <wireless_interface.left.my_node.address.desc.AQ [Attr.Type.Querier String]>
    <wireless_interface.left.my_node.address.region.AQ [Attr.Type.Querier String]>
    <wireless_interface.left.my_node.desc.AQ [Attr.Type.Querier String]>
    <wireless_interface.left.my_node.position.lat.AQ [Attr.Type.Querier Raw]>
    <wireless_interface.left.my_node.position.lon.AQ [Attr.Type.Querier Raw]>
    <wireless_interface.left.my_node.position.height.AQ [Attr.Type.Querier Ckd]>
    <wireless_interface.left.my_node.show_in_map.AQ [Attr.Type.Querier Boolean]>
    <wireless_interface.mac_address.AQ [Attr.Type.Querier String]>
    <wireless_interface.name.AQ [Attr.Type.Querier String]>
    <wireless_interface.is_active.AQ [Attr.Type.Querier Boolean]>
    <wireless_interface.desc.AQ [Attr.Type.Querier String]>
    <wireless_interface.mode.AQ [Attr.Type.Querier Ckd]>
    <wireless_interface.essid.AQ [Attr.Type.Querier String]>
    <wireless_interface.bssid.AQ [Attr.Type.Querier String]>
    <wireless_interface.standard.name.AQ [Attr.Type.Querier String]>
    <wireless_interface.standard.bandwidth.AQ [Attr.Type.Querier Raw]>
    <wireless_interface.txpower.AQ [Attr.Type.Querier Raw]>
    <wireless_interface.my_node.name.AQ [Attr.Type.Querier String]>
    <wireless_interface.my_node.manager.last_name.AQ [Attr.Type.Querier String_FL]>
    <wireless_interface.my_node.manager.first_name.AQ [Attr.Type.Querier String_FL]>
    <wireless_interface.my_node.manager.middle_name.AQ [Attr.Type.Querier String]>
    <wireless_interface.my_node.manager.title.AQ [Attr.Type.Querier String]>
    <wireless_interface.my_node.manager.lifetime.start.AQ [Attr.Type.Querier Date]>
    <wireless_interface.my_node.manager.lifetime.finish.AQ [Attr.Type.Querier Date]>
    <wireless_interface.my_node.manager.lifetime.alive.AQ [Attr.Type.Querier Boolean]>
    <wireless_interface.my_node.manager.sex.AQ [Attr.Type.Querier Ckd]>
    <wireless_interface.my_node.address.street.AQ [Attr.Type.Querier String]>
    <wireless_interface.my_node.address.zip.AQ [Attr.Type.Querier String]>
    <wireless_interface.my_node.address.city.AQ [Attr.Type.Querier String]>
    <wireless_interface.my_node.address.country.AQ [Attr.Type.Querier String]>
    <wireless_interface.my_node.address.desc.AQ [Attr.Type.Querier String]>
    <wireless_interface.my_node.address.region.AQ [Attr.Type.Querier String]>
    <wireless_interface.my_node.desc.AQ [Attr.Type.Querier String]>
    <wireless_interface.my_node.position.lat.AQ [Attr.Type.Querier Raw]>
    <wireless_interface.my_node.position.lon.AQ [Attr.Type.Querier Raw]>
    <wireless_interface.my_node.position.height.AQ [Attr.Type.Querier Ckd]>
    <wireless_interface.my_node.show_in_map.AQ [Attr.Type.Querier Boolean]>
    <wireless_interface.my_net_device.left.name.AQ [Attr.Type.Querier String]>
    <wireless_interface.my_net_device.left.model_no.AQ [Attr.Type.Querier String]>
    <wireless_interface.my_net_device.left.revision.AQ [Attr.Type.Querier String]>
    <wireless_interface.my_net_device.left.desc.AQ [Attr.Type.Querier String]>
    <wireless_interface.my_net_device.node.name.AQ [Attr.Type.Querier String]>
    <wireless_interface.my_net_device.node.manager.last_name.AQ [Attr.Type.Querier String_FL]>
    <wireless_interface.my_net_device.node.manager.first_name.AQ [Attr.Type.Querier String_FL]>
    <wireless_interface.my_net_device.node.manager.middle_name.AQ [Attr.Type.Querier String]>
    <wireless_interface.my_net_device.node.manager.title.AQ [Attr.Type.Querier String]>
    <wireless_interface.my_net_device.node.manager.lifetime.start.AQ [Attr.Type.Querier Date]>
    <wireless_interface.my_net_device.node.manager.lifetime.finish.AQ [Attr.Type.Querier Date]>
    <wireless_interface.my_net_device.node.manager.lifetime.alive.AQ [Attr.Type.Querier Boolean]>
    <wireless_interface.my_net_device.node.manager.sex.AQ [Attr.Type.Querier Ckd]>
    <wireless_interface.my_net_device.node.address.street.AQ [Attr.Type.Querier String]>
    <wireless_interface.my_net_device.node.address.zip.AQ [Attr.Type.Querier String]>
    <wireless_interface.my_net_device.node.address.city.AQ [Attr.Type.Querier String]>
    <wireless_interface.my_net_device.node.address.country.AQ [Attr.Type.Querier String]>
    <wireless_interface.my_net_device.node.address.desc.AQ [Attr.Type.Querier String]>
    <wireless_interface.my_net_device.node.address.region.AQ [Attr.Type.Querier String]>
    <wireless_interface.my_net_device.node.desc.AQ [Attr.Type.Querier String]>
    <wireless_interface.my_net_device.node.position.lat.AQ [Attr.Type.Querier Raw]>
    <wireless_interface.my_net_device.node.position.lon.AQ [Attr.Type.Querier Raw]>
    <wireless_interface.my_net_device.node.position.height.AQ [Attr.Type.Querier Ckd]>
    <wireless_interface.my_net_device.node.show_in_map.AQ [Attr.Type.Querier Boolean]>
    <wireless_interface.my_net_device.name.AQ [Attr.Type.Querier String]>
    <wireless_interface.my_net_device.desc.AQ [Attr.Type.Querier String]>
    <wireless_interface.my_net_device.my_node.name.AQ [Attr.Type.Querier String]>
    <wireless_interface.my_net_device.my_node.manager.last_name.AQ [Attr.Type.Querier String_FL]>
    <wireless_interface.my_net_device.my_node.manager.first_name.AQ [Attr.Type.Querier String_FL]>
    <wireless_interface.my_net_device.my_node.manager.middle_name.AQ [Attr.Type.Querier String]>
    <wireless_interface.my_net_device.my_node.manager.title.AQ [Attr.Type.Querier String]>
    <wireless_interface.my_net_device.my_node.manager.lifetime.start.AQ [Attr.Type.Querier Date]>
    <wireless_interface.my_net_device.my_node.manager.lifetime.finish.AQ [Attr.Type.Querier Date]>
    <wireless_interface.my_net_device.my_node.manager.lifetime.alive.AQ [Attr.Type.Querier Boolean]>
    <wireless_interface.my_net_device.my_node.manager.sex.AQ [Attr.Type.Querier Ckd]>
    <wireless_interface.my_net_device.my_node.address.street.AQ [Attr.Type.Querier String]>
    <wireless_interface.my_net_device.my_node.address.zip.AQ [Attr.Type.Querier String]>
    <wireless_interface.my_net_device.my_node.address.city.AQ [Attr.Type.Querier String]>
    <wireless_interface.my_net_device.my_node.address.country.AQ [Attr.Type.Querier String]>
    <wireless_interface.my_net_device.my_node.address.desc.AQ [Attr.Type.Querier String]>
    <wireless_interface.my_net_device.my_node.address.region.AQ [Attr.Type.Querier String]>
    <wireless_interface.my_net_device.my_node.desc.AQ [Attr.Type.Querier String]>
    <wireless_interface.my_net_device.my_node.position.lat.AQ [Attr.Type.Querier Raw]>
    <wireless_interface.my_net_device.my_node.position.lon.AQ [Attr.Type.Querier Raw]>
    <wireless_interface.my_net_device.my_node.position.height.AQ [Attr.Type.Querier Ckd]>
    <wireless_interface.my_net_device.my_node.show_in_map.AQ [Attr.Type.Querier Boolean]>
    <virtual_wireless_interface.left.left.name.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.left.left.model_no.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.left.left.revision.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.left.left.desc.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.left.node.name.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.left.node.manager.last_name.AQ [Attr.Type.Querier String_FL]>
    <virtual_wireless_interface.left.node.manager.first_name.AQ [Attr.Type.Querier String_FL]>
    <virtual_wireless_interface.left.node.manager.middle_name.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.left.node.manager.title.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.left.node.manager.lifetime.start.AQ [Attr.Type.Querier Date]>
    <virtual_wireless_interface.left.node.manager.lifetime.finish.AQ [Attr.Type.Querier Date]>
    <virtual_wireless_interface.left.node.manager.lifetime.alive.AQ [Attr.Type.Querier Boolean]>
    <virtual_wireless_interface.left.node.manager.sex.AQ [Attr.Type.Querier Ckd]>
    <virtual_wireless_interface.left.node.address.street.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.left.node.address.zip.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.left.node.address.city.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.left.node.address.country.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.left.node.address.desc.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.left.node.address.region.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.left.node.desc.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.left.node.position.lat.AQ [Attr.Type.Querier Raw]>
    <virtual_wireless_interface.left.node.position.lon.AQ [Attr.Type.Querier Raw]>
    <virtual_wireless_interface.left.node.position.height.AQ [Attr.Type.Querier Ckd]>
    <virtual_wireless_interface.left.node.show_in_map.AQ [Attr.Type.Querier Boolean]>
    <virtual_wireless_interface.left.name.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.left.desc.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.left.my_node.name.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.left.my_node.manager.last_name.AQ [Attr.Type.Querier String_FL]>
    <virtual_wireless_interface.left.my_node.manager.first_name.AQ [Attr.Type.Querier String_FL]>
    <virtual_wireless_interface.left.my_node.manager.middle_name.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.left.my_node.manager.title.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.left.my_node.manager.lifetime.start.AQ [Attr.Type.Querier Date]>
    <virtual_wireless_interface.left.my_node.manager.lifetime.finish.AQ [Attr.Type.Querier Date]>
    <virtual_wireless_interface.left.my_node.manager.lifetime.alive.AQ [Attr.Type.Querier Boolean]>
    <virtual_wireless_interface.left.my_node.manager.sex.AQ [Attr.Type.Querier Ckd]>
    <virtual_wireless_interface.left.my_node.address.street.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.left.my_node.address.zip.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.left.my_node.address.city.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.left.my_node.address.country.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.left.my_node.address.desc.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.left.my_node.address.region.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.left.my_node.desc.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.left.my_node.position.lat.AQ [Attr.Type.Querier Raw]>
    <virtual_wireless_interface.left.my_node.position.lon.AQ [Attr.Type.Querier Raw]>
    <virtual_wireless_interface.left.my_node.position.height.AQ [Attr.Type.Querier Ckd]>
    <virtual_wireless_interface.left.my_node.show_in_map.AQ [Attr.Type.Querier Boolean]>
    <virtual_wireless_interface.hardware.left.left.name.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.left.left.model_no.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.left.left.revision.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.left.left.desc.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.left.node.name.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.left.node.manager.last_name.AQ [Attr.Type.Querier String_FL]>
    <virtual_wireless_interface.hardware.left.node.manager.first_name.AQ [Attr.Type.Querier String_FL]>
    <virtual_wireless_interface.hardware.left.node.manager.middle_name.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.left.node.manager.title.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.left.node.manager.lifetime.start.AQ [Attr.Type.Querier Date]>
    <virtual_wireless_interface.hardware.left.node.manager.lifetime.finish.AQ [Attr.Type.Querier Date]>
    <virtual_wireless_interface.hardware.left.node.manager.lifetime.alive.AQ [Attr.Type.Querier Boolean]>
    <virtual_wireless_interface.hardware.left.node.manager.sex.AQ [Attr.Type.Querier Ckd]>
    <virtual_wireless_interface.hardware.left.node.address.street.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.left.node.address.zip.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.left.node.address.city.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.left.node.address.country.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.left.node.address.desc.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.left.node.address.region.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.left.node.desc.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.left.node.position.lat.AQ [Attr.Type.Querier Raw]>
    <virtual_wireless_interface.hardware.left.node.position.lon.AQ [Attr.Type.Querier Raw]>
    <virtual_wireless_interface.hardware.left.node.position.height.AQ [Attr.Type.Querier Ckd]>
    <virtual_wireless_interface.hardware.left.node.show_in_map.AQ [Attr.Type.Querier Boolean]>
    <virtual_wireless_interface.hardware.left.name.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.left.desc.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.left.my_node.name.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.left.my_node.manager.last_name.AQ [Attr.Type.Querier String_FL]>
    <virtual_wireless_interface.hardware.left.my_node.manager.first_name.AQ [Attr.Type.Querier String_FL]>
    <virtual_wireless_interface.hardware.left.my_node.manager.middle_name.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.left.my_node.manager.title.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.left.my_node.manager.lifetime.start.AQ [Attr.Type.Querier Date]>
    <virtual_wireless_interface.hardware.left.my_node.manager.lifetime.finish.AQ [Attr.Type.Querier Date]>
    <virtual_wireless_interface.hardware.left.my_node.manager.lifetime.alive.AQ [Attr.Type.Querier Boolean]>
    <virtual_wireless_interface.hardware.left.my_node.manager.sex.AQ [Attr.Type.Querier Ckd]>
    <virtual_wireless_interface.hardware.left.my_node.address.street.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.left.my_node.address.zip.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.left.my_node.address.city.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.left.my_node.address.country.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.left.my_node.address.desc.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.left.my_node.address.region.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.left.my_node.desc.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.left.my_node.position.lat.AQ [Attr.Type.Querier Raw]>
    <virtual_wireless_interface.hardware.left.my_node.position.lon.AQ [Attr.Type.Querier Raw]>
    <virtual_wireless_interface.hardware.left.my_node.position.height.AQ [Attr.Type.Querier Ckd]>
    <virtual_wireless_interface.hardware.left.my_node.show_in_map.AQ [Attr.Type.Querier Boolean]>
    <virtual_wireless_interface.hardware.mac_address.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.name.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.is_active.AQ [Attr.Type.Querier Boolean]>
    <virtual_wireless_interface.hardware.desc.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.mode.AQ [Attr.Type.Querier Ckd]>
    <virtual_wireless_interface.hardware.essid.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.bssid.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.standard.name.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.standard.bandwidth.AQ [Attr.Type.Querier Raw]>
    <virtual_wireless_interface.hardware.txpower.AQ [Attr.Type.Querier Raw]>
    <virtual_wireless_interface.hardware.my_node.name.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.my_node.manager.last_name.AQ [Attr.Type.Querier String_FL]>
    <virtual_wireless_interface.hardware.my_node.manager.first_name.AQ [Attr.Type.Querier String_FL]>
    <virtual_wireless_interface.hardware.my_node.manager.middle_name.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.my_node.manager.title.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.my_node.manager.lifetime.start.AQ [Attr.Type.Querier Date]>
    <virtual_wireless_interface.hardware.my_node.manager.lifetime.finish.AQ [Attr.Type.Querier Date]>
    <virtual_wireless_interface.hardware.my_node.manager.lifetime.alive.AQ [Attr.Type.Querier Boolean]>
    <virtual_wireless_interface.hardware.my_node.manager.sex.AQ [Attr.Type.Querier Ckd]>
    <virtual_wireless_interface.hardware.my_node.address.street.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.my_node.address.zip.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.my_node.address.city.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.my_node.address.country.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.my_node.address.desc.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.my_node.address.region.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.my_node.desc.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.my_node.position.lat.AQ [Attr.Type.Querier Raw]>
    <virtual_wireless_interface.hardware.my_node.position.lon.AQ [Attr.Type.Querier Raw]>
    <virtual_wireless_interface.hardware.my_node.position.height.AQ [Attr.Type.Querier Ckd]>
    <virtual_wireless_interface.hardware.my_node.show_in_map.AQ [Attr.Type.Querier Boolean]>
    <virtual_wireless_interface.hardware.my_net_device.left.name.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.my_net_device.left.model_no.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.my_net_device.left.revision.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.my_net_device.left.desc.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.my_net_device.node.name.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.my_net_device.node.manager.last_name.AQ [Attr.Type.Querier String_FL]>
    <virtual_wireless_interface.hardware.my_net_device.node.manager.first_name.AQ [Attr.Type.Querier String_FL]>
    <virtual_wireless_interface.hardware.my_net_device.node.manager.middle_name.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.my_net_device.node.manager.title.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.my_net_device.node.manager.lifetime.start.AQ [Attr.Type.Querier Date]>
    <virtual_wireless_interface.hardware.my_net_device.node.manager.lifetime.finish.AQ [Attr.Type.Querier Date]>
    <virtual_wireless_interface.hardware.my_net_device.node.manager.lifetime.alive.AQ [Attr.Type.Querier Boolean]>
    <virtual_wireless_interface.hardware.my_net_device.node.manager.sex.AQ [Attr.Type.Querier Ckd]>
    <virtual_wireless_interface.hardware.my_net_device.node.address.street.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.my_net_device.node.address.zip.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.my_net_device.node.address.city.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.my_net_device.node.address.country.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.my_net_device.node.address.desc.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.my_net_device.node.address.region.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.my_net_device.node.desc.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.my_net_device.node.position.lat.AQ [Attr.Type.Querier Raw]>
    <virtual_wireless_interface.hardware.my_net_device.node.position.lon.AQ [Attr.Type.Querier Raw]>
    <virtual_wireless_interface.hardware.my_net_device.node.position.height.AQ [Attr.Type.Querier Ckd]>
    <virtual_wireless_interface.hardware.my_net_device.node.show_in_map.AQ [Attr.Type.Querier Boolean]>
    <virtual_wireless_interface.hardware.my_net_device.name.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.my_net_device.desc.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.my_net_device.my_node.name.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.my_net_device.my_node.manager.last_name.AQ [Attr.Type.Querier String_FL]>
    <virtual_wireless_interface.hardware.my_net_device.my_node.manager.first_name.AQ [Attr.Type.Querier String_FL]>
    <virtual_wireless_interface.hardware.my_net_device.my_node.manager.middle_name.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.my_net_device.my_node.manager.title.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.my_net_device.my_node.manager.lifetime.start.AQ [Attr.Type.Querier Date]>
    <virtual_wireless_interface.hardware.my_net_device.my_node.manager.lifetime.finish.AQ [Attr.Type.Querier Date]>
    <virtual_wireless_interface.hardware.my_net_device.my_node.manager.lifetime.alive.AQ [Attr.Type.Querier Boolean]>
    <virtual_wireless_interface.hardware.my_net_device.my_node.manager.sex.AQ [Attr.Type.Querier Ckd]>
    <virtual_wireless_interface.hardware.my_net_device.my_node.address.street.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.my_net_device.my_node.address.zip.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.my_net_device.my_node.address.city.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.my_net_device.my_node.address.country.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.my_net_device.my_node.address.desc.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.my_net_device.my_node.address.region.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.my_net_device.my_node.desc.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.hardware.my_net_device.my_node.position.lat.AQ [Attr.Type.Querier Raw]>
    <virtual_wireless_interface.hardware.my_net_device.my_node.position.lon.AQ [Attr.Type.Querier Raw]>
    <virtual_wireless_interface.hardware.my_net_device.my_node.position.height.AQ [Attr.Type.Querier Ckd]>
    <virtual_wireless_interface.hardware.my_net_device.my_node.show_in_map.AQ [Attr.Type.Querier Boolean]>
    <virtual_wireless_interface.mac_address.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.name.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.is_active.AQ [Attr.Type.Querier Boolean]>
    <virtual_wireless_interface.desc.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.mode.AQ [Attr.Type.Querier Ckd]>
    <virtual_wireless_interface.essid.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.bssid.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.my_node.name.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.my_node.manager.last_name.AQ [Attr.Type.Querier String_FL]>
    <virtual_wireless_interface.my_node.manager.first_name.AQ [Attr.Type.Querier String_FL]>
    <virtual_wireless_interface.my_node.manager.middle_name.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.my_node.manager.title.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.my_node.manager.lifetime.start.AQ [Attr.Type.Querier Date]>
    <virtual_wireless_interface.my_node.manager.lifetime.finish.AQ [Attr.Type.Querier Date]>
    <virtual_wireless_interface.my_node.manager.lifetime.alive.AQ [Attr.Type.Querier Boolean]>
    <virtual_wireless_interface.my_node.manager.sex.AQ [Attr.Type.Querier Ckd]>
    <virtual_wireless_interface.my_node.address.street.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.my_node.address.zip.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.my_node.address.city.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.my_node.address.country.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.my_node.address.desc.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.my_node.address.region.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.my_node.desc.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.my_node.position.lat.AQ [Attr.Type.Querier Raw]>
    <virtual_wireless_interface.my_node.position.lon.AQ [Attr.Type.Querier Raw]>
    <virtual_wireless_interface.my_node.position.height.AQ [Attr.Type.Querier Ckd]>
    <virtual_wireless_interface.my_node.show_in_map.AQ [Attr.Type.Querier Boolean]>
    <virtual_wireless_interface.my_net_device.left.name.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.my_net_device.left.model_no.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.my_net_device.left.revision.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.my_net_device.left.desc.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.my_net_device.node.name.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.my_net_device.node.manager.last_name.AQ [Attr.Type.Querier String_FL]>
    <virtual_wireless_interface.my_net_device.node.manager.first_name.AQ [Attr.Type.Querier String_FL]>
    <virtual_wireless_interface.my_net_device.node.manager.middle_name.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.my_net_device.node.manager.title.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.my_net_device.node.manager.lifetime.start.AQ [Attr.Type.Querier Date]>
    <virtual_wireless_interface.my_net_device.node.manager.lifetime.finish.AQ [Attr.Type.Querier Date]>
    <virtual_wireless_interface.my_net_device.node.manager.lifetime.alive.AQ [Attr.Type.Querier Boolean]>
    <virtual_wireless_interface.my_net_device.node.manager.sex.AQ [Attr.Type.Querier Ckd]>
    <virtual_wireless_interface.my_net_device.node.address.street.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.my_net_device.node.address.zip.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.my_net_device.node.address.city.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.my_net_device.node.address.country.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.my_net_device.node.address.desc.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.my_net_device.node.address.region.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.my_net_device.node.desc.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.my_net_device.node.position.lat.AQ [Attr.Type.Querier Raw]>
    <virtual_wireless_interface.my_net_device.node.position.lon.AQ [Attr.Type.Querier Raw]>
    <virtual_wireless_interface.my_net_device.node.position.height.AQ [Attr.Type.Querier Ckd]>
    <virtual_wireless_interface.my_net_device.node.show_in_map.AQ [Attr.Type.Querier Boolean]>
    <virtual_wireless_interface.my_net_device.name.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.my_net_device.desc.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.my_net_device.my_node.name.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.my_net_device.my_node.manager.last_name.AQ [Attr.Type.Querier String_FL]>
    <virtual_wireless_interface.my_net_device.my_node.manager.first_name.AQ [Attr.Type.Querier String_FL]>
    <virtual_wireless_interface.my_net_device.my_node.manager.middle_name.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.my_net_device.my_node.manager.title.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.my_net_device.my_node.manager.lifetime.start.AQ [Attr.Type.Querier Date]>
    <virtual_wireless_interface.my_net_device.my_node.manager.lifetime.finish.AQ [Attr.Type.Querier Date]>
    <virtual_wireless_interface.my_net_device.my_node.manager.lifetime.alive.AQ [Attr.Type.Querier Boolean]>
    <virtual_wireless_interface.my_net_device.my_node.manager.sex.AQ [Attr.Type.Querier Ckd]>
    <virtual_wireless_interface.my_net_device.my_node.address.street.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.my_net_device.my_node.address.zip.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.my_net_device.my_node.address.city.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.my_net_device.my_node.address.country.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.my_net_device.my_node.address.desc.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.my_net_device.my_node.address.region.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.my_net_device.my_node.desc.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.my_net_device.my_node.position.lat.AQ [Attr.Type.Querier Raw]>
    <virtual_wireless_interface.my_net_device.my_node.position.lon.AQ [Attr.Type.Querier Raw]>
    <virtual_wireless_interface.my_net_device.my_node.position.height.AQ [Attr.Type.Querier Ckd]>
    <virtual_wireless_interface.my_net_device.my_node.show_in_map.AQ [Attr.Type.Querier Boolean]>
    <virtual_wireless_interface.standard.name.AQ [Attr.Type.Querier String]>
    <virtual_wireless_interface.standard.bandwidth.AQ [Attr.Type.Querier Raw]>
    <virtual_wireless_interface.txpower.AQ [Attr.Type.Querier Raw]>

    >>> print (formatted (AQ.As_Json_Cargo))
    { 'filters' :
        [ { 'name' : 'net_address'
          , 'sig_key' : 0
          , 'ui_name' : 'Net address'
          }
        , { 'name' : 'desc'
          , 'sig_key' : 3
          , 'ui_name' : 'Description'
          }
        , { 'Class' : 'Entity'
          , 'children_np' :
              [ { 'Class' : 'Entity'
                , 'attrs' :
                    [ { 'name' : 'name'
                      , 'sig_key' : 3
                      , 'ui_name' : 'Name'
                      }
                    ]
                , 'name' : 'owner'
                , 'sig_key' : 2
                , 'type_name' : 'PAP.Adhoc_Group'
                , 'ui_name' : 'Owner'
                , 'ui_type_name' : 'Adhoc_Group'
                }
              , { 'Class' : 'Entity'
                , 'attrs' :
                    [ { 'name' : 'name'
                      , 'sig_key' : 3
                      , 'ui_name' : 'Name'
                      }
                    ]
                , 'name' : 'owner'
                , 'sig_key' : 2
                , 'type_name' : 'PAP.Association'
                , 'ui_name' : 'Owner'
                , 'ui_type_name' : 'Association'
                }
              , { 'Class' : 'Entity'
                , 'attrs' :
                    [ { 'name' : 'name'
                      , 'sig_key' : 3
                      , 'ui_name' : 'Name'
                      }
                    , { 'name' : 'registered_in'
                      , 'sig_key' : 3
                      , 'ui_name' : 'Registered in'
                      }
                    ]
                , 'name' : 'owner'
                , 'sig_key' : 2
                , 'type_name' : 'PAP.Company'
                , 'ui_name' : 'Owner'
                , 'ui_type_name' : 'Company'
                }
              , { 'Class' : 'Entity'
                , 'attrs' :
                    [ { 'name' : 'last_name'
                      , 'sig_key' : 3
                      , 'ui_name' : 'Last name'
                      }
                    , { 'name' : 'first_name'
                      , 'sig_key' : 3
                      , 'ui_name' : 'First name'
                      }
                    , { 'name' : 'middle_name'
                      , 'sig_key' : 3
                      , 'ui_name' : 'Middle name'
                      }
                    , { 'name' : 'title'
                      , 'sig_key' : 3
                      , 'ui_name' : 'Academic title'
                      }
                    ]
                , 'name' : 'owner'
                , 'sig_key' : 2
                , 'type_name' : 'PAP.Person'
                , 'ui_name' : 'Owner'
                , 'ui_type_name' : 'Person'
                }
              ]
          , 'default_child' : 'PAP.Person'
          , 'name' : 'owner'
          , 'sig_key' : 2
          , 'ui_name' : 'Owner'
          }
        , { 'Class' : 'Entity'
          , 'attrs' :
              [ { 'name' : 'c_time'
                , 'sig_key' : 0
                , 'ui_name' : 'C time'
                }
              , { 'Class' : 'Entity'
                , 'children_np' :
                    [ { 'Class' : 'Entity'
                      , 'attrs' :
                          [ { 'name' : 'name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Name'
                            }
                          ]
                      , 'name' : 'c_user'
                      , 'sig_key' : 2
                      , 'type_name' : 'Auth.Account'
                      , 'ui_name' : 'C user'
                      , 'ui_type_name' : 'Account'
                      }
                    , { 'Class' : 'Entity'
                      , 'attrs' :
                          [ { 'name' : 'last_name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Last name'
                            }
                          , { 'name' : 'first_name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'First name'
                            }
                          , { 'name' : 'middle_name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Middle name'
                            }
                          , { 'name' : 'title'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Academic title'
                            }
                          ]
                      , 'name' : 'c_user'
                      , 'sig_key' : 2
                      , 'type_name' : 'PAP.Person'
                      , 'ui_name' : 'C user'
                      , 'ui_type_name' : 'Person'
                      }
                    ]
                , 'name' : 'c_user'
                , 'sig_key' : 2
                , 'ui_name' : 'C user'
                }
              , { 'name' : 'kind'
                , 'sig_key' : 3
                , 'ui_name' : 'Kind'
                }
              , { 'name' : 'time'
                , 'sig_key' : 0
                , 'ui_name' : 'Time'
                }
              , { 'Class' : 'Entity'
                , 'children_np' :
                    [ { 'Class' : 'Entity'
                      , 'attrs' :
                          [ { 'name' : 'name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Name'
                            }
                          ]
                      , 'name' : 'user'
                      , 'sig_key' : 2
                      , 'type_name' : 'Auth.Account'
                      , 'ui_name' : 'User'
                      , 'ui_type_name' : 'Account'
                      }
                    , { 'Class' : 'Entity'
                      , 'attrs' :
                          [ { 'name' : 'last_name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Last name'
                            }
                          , { 'name' : 'first_name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'First name'
                            }
                          , { 'name' : 'middle_name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Middle name'
                            }
                          , { 'name' : 'title'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Academic title'
                            }
                          ]
                      , 'name' : 'user'
                      , 'sig_key' : 2
                      , 'type_name' : 'PAP.Person'
                      , 'ui_name' : 'User'
                      , 'ui_type_name' : 'Person'
                      }
                    ]
                , 'name' : 'user'
                , 'sig_key' : 2
                , 'ui_name' : 'User'
                }
              ]
          , 'name' : 'creation'
          , 'sig_key' : 2
          , 'ui_name' : 'Creation'
          }
        , { 'Class' : 'Entity'
          , 'attrs' :
              [ { 'name' : 'c_time'
                , 'sig_key' : 0
                , 'ui_name' : 'C time'
                }
              , { 'Class' : 'Entity'
                , 'children_np' :
                    [ { 'Class' : 'Entity'
                      , 'attrs' :
                          [ { 'name' : 'name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Name'
                            }
                          ]
                      , 'name' : 'c_user'
                      , 'sig_key' : 2
                      , 'type_name' : 'Auth.Account'
                      , 'ui_name' : 'C user'
                      , 'ui_type_name' : 'Account'
                      }
                    , { 'Class' : 'Entity'
                      , 'attrs' :
                          [ { 'name' : 'last_name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Last name'
                            }
                          , { 'name' : 'first_name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'First name'
                            }
                          , { 'name' : 'middle_name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Middle name'
                            }
                          , { 'name' : 'title'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Academic title'
                            }
                          ]
                      , 'name' : 'c_user'
                      , 'sig_key' : 2
                      , 'type_name' : 'PAP.Person'
                      , 'ui_name' : 'C user'
                      , 'ui_type_name' : 'Person'
                      }
                    ]
                , 'name' : 'c_user'
                , 'sig_key' : 2
                , 'ui_name' : 'C user'
                }
              , { 'name' : 'kind'
                , 'sig_key' : 3
                , 'ui_name' : 'Kind'
                }
              , { 'name' : 'time'
                , 'sig_key' : 0
                , 'ui_name' : 'Time'
                }
              , { 'Class' : 'Entity'
                , 'children_np' :
                    [ { 'Class' : 'Entity'
                      , 'attrs' :
                          [ { 'name' : 'name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Name'
                            }
                          ]
                      , 'name' : 'user'
                      , 'sig_key' : 2
                      , 'type_name' : 'Auth.Account'
                      , 'ui_name' : 'User'
                      , 'ui_type_name' : 'Account'
                      }
                    , { 'Class' : 'Entity'
                      , 'attrs' :
                          [ { 'name' : 'last_name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Last name'
                            }
                          , { 'name' : 'first_name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'First name'
                            }
                          , { 'name' : 'middle_name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Middle name'
                            }
                          , { 'name' : 'title'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Academic title'
                            }
                          ]
                      , 'name' : 'user'
                      , 'sig_key' : 2
                      , 'type_name' : 'PAP.Person'
                      , 'ui_name' : 'User'
                      , 'ui_type_name' : 'Person'
                      }
                    ]
                , 'name' : 'user'
                , 'sig_key' : 2
                , 'ui_name' : 'User'
                }
              ]
          , 'name' : 'last_change'
          , 'sig_key' : 2
          , 'ui_name' : 'Last change'
          }
        , { 'name' : 'last_cid'
          , 'sig_key' : 0
          , 'ui_name' : 'Last cid'
          }
        , { 'name' : 'pid'
          , 'sig_key' : 0
          , 'ui_name' : 'Pid'
          }
        , { 'name' : 'type_name'
          , 'sig_key' : 3
          , 'ui_name' : 'Type name'
          }
        , { 'name' : 'expiration_date'
          , 'sig_key' : 0
          , 'ui_name' : 'Expiration date'
          }
        , { 'name' : 'has_children'
          , 'sig_key' : 1
          , 'ui_name' : 'Has children'
          }
        , { 'name' : 'is_free'
          , 'sig_key' : 1
          , 'ui_name' : 'Is free'
          }
        , { 'Class' : 'Entity'
          , 'attrs' :
              [ { 'name' : 'net_address'
                , 'sig_key' : 0
                , 'ui_name' : 'Net address'
                }
              , { 'name' : 'desc'
                , 'sig_key' : 3
                , 'ui_name' : 'Description'
                }
              , { 'Class' : 'Entity'
                , 'children_np' :
                    [ { 'Class' : 'Entity'
                      , 'attrs' :
                          [ { 'name' : 'name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Name'
                            }
                          ]
                      , 'name' : 'owner'
                      , 'sig_key' : 2
                      , 'type_name' : 'PAP.Adhoc_Group'
                      , 'ui_name' : 'Owner'
                      , 'ui_type_name' : 'Adhoc_Group'
                      }
                    , { 'Class' : 'Entity'
                      , 'attrs' :
                          [ { 'name' : 'name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Name'
                            }
                          ]
                      , 'name' : 'owner'
                      , 'sig_key' : 2
                      , 'type_name' : 'PAP.Association'
                      , 'ui_name' : 'Owner'
                      , 'ui_type_name' : 'Association'
                      }
                    , { 'Class' : 'Entity'
                      , 'attrs' :
                          [ { 'name' : 'name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Name'
                            }
                          , { 'name' : 'registered_in'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Registered in'
                            }
                          ]
                      , 'name' : 'owner'
                      , 'sig_key' : 2
                      , 'type_name' : 'PAP.Company'
                      , 'ui_name' : 'Owner'
                      , 'ui_type_name' : 'Company'
                      }
                    , { 'Class' : 'Entity'
                      , 'attrs' :
                          [ { 'name' : 'last_name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Last name'
                            }
                          , { 'name' : 'first_name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'First name'
                            }
                          , { 'name' : 'middle_name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Middle name'
                            }
                          , { 'name' : 'title'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Academic title'
                            }
                          ]
                      , 'name' : 'owner'
                      , 'sig_key' : 2
                      , 'type_name' : 'PAP.Person'
                      , 'ui_name' : 'Owner'
                      , 'ui_type_name' : 'Person'
                      }
                    ]
                , 'default_child' : 'PAP.Person'
                , 'name' : 'owner'
                , 'sig_key' : 2
                , 'ui_name' : 'Owner'
                }
              , { 'name' : 'expiration_date'
                , 'sig_key' : 0
                , 'ui_name' : 'Expiration date'
                }
              , { 'name' : 'has_children'
                , 'sig_key' : 1
                , 'ui_name' : 'Has children'
                }
              , { 'name' : 'is_free'
                , 'sig_key' : 1
                , 'ui_name' : 'Is free'
                }
              , { 'Class' : 'Entity'
                , 'name' : 'parent'
                , 'sig_key' : 2
                , 'ui_name' : 'Parent'
                }
              ]
          , 'name' : 'parent'
          , 'sig_key' : 2
          , 'ui_name' : 'Parent'
          }
        , { 'Class' : 'Entity'
          , 'attrs' :
              [ { 'attrs' :
                    [ { 'name' : 'lower'
                      , 'sig_key' : 0
                      , 'ui_name' : 'Lower'
                      }
                    , { 'name' : 'upper'
                      , 'sig_key' : 0
                      , 'ui_name' : 'Upper'
                      }
                    , { 'name' : 'center'
                      , 'sig_key' : 0
                      , 'ui_name' : 'Center'
                      }
                    , { 'name' : 'length'
                      , 'sig_key' : 0
                      , 'ui_name' : 'Length'
                      }
                    ]
                , 'name' : 'netmask_interval'
                , 'ui_name' : 'Netmask interval'
                }
              , { 'Class' : 'Entity'
                , 'attrs' :
                    [ { 'name' : 'name'
                      , 'sig_key' : 3
                      , 'ui_name' : 'Name'
                      }
                    , { 'Class' : 'Entity'
                      , 'attrs' :
                          [ { 'name' : 'last_name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Last name'
                            }
                          , { 'name' : 'first_name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'First name'
                            }
                          , { 'name' : 'middle_name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Middle name'
                            }
                          , { 'name' : 'title'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Academic title'
                            }
                          , { 'attrs' :
                                [ { 'name' : 'start'
                                  , 'sig_key' : 0
                                  , 'ui_name' : 'Start'
                                  }
                                , { 'name' : 'finish'
                                  , 'sig_key' : 0
                                  , 'ui_name' : 'Finish'
                                  }
                                , { 'name' : 'alive'
                                  , 'sig_key' : 1
                                  , 'ui_name' : 'Alive'
                                  }
                                ]
                            , 'name' : 'lifetime'
                            , 'ui_name' : 'Lifetime'
                            }
                          , { 'name' : 'sex'
                            , 'sig_key' : 0
                            , 'ui_name' : 'Sex'
                            }
                          ]
                      , 'name' : 'manager'
                      , 'sig_key' : 2
                      , 'ui_name' : 'Manager'
                      }
                    , { 'Class' : 'Entity'
                      , 'attrs' :
                          [ { 'name' : 'street'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Street'
                            }
                          , { 'name' : 'zip'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Zip code'
                            }
                          , { 'name' : 'city'
                            , 'sig_key' : 3
                            , 'ui_name' : 'City'
                            }
                          , { 'name' : 'country'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Country'
                            }
                          , { 'name' : 'desc'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Description'
                            }
                          , { 'name' : 'region'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Region'
                            }
                          ]
                      , 'name' : 'address'
                      , 'sig_key' : 2
                      , 'ui_name' : 'Address'
                      }
                    , { 'name' : 'desc'
                      , 'sig_key' : 3
                      , 'ui_name' : 'Description'
                      }
                    , { 'Class' : 'Entity'
                      , 'children_np' :
                          [ { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Name'
                                  }
                                ]
                            , 'name' : 'owner'
                            , 'sig_key' : 2
                            , 'type_name' : 'PAP.Adhoc_Group'
                            , 'ui_name' : 'Owner'
                            , 'ui_type_name' : 'Adhoc_Group'
                            }
                          , { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Name'
                                  }
                                ]
                            , 'name' : 'owner'
                            , 'sig_key' : 2
                            , 'type_name' : 'PAP.Association'
                            , 'ui_name' : 'Owner'
                            , 'ui_type_name' : 'Association'
                            }
                          , { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Name'
                                  }
                                , { 'name' : 'registered_in'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Registered in'
                                  }
                                ]
                            , 'name' : 'owner'
                            , 'sig_key' : 2
                            , 'type_name' : 'PAP.Company'
                            , 'ui_name' : 'Owner'
                            , 'ui_type_name' : 'Company'
                            }
                          , { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'last_name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Last name'
                                  }
                                , { 'name' : 'first_name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'First name'
                                  }
                                , { 'name' : 'middle_name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Middle name'
                                  }
                                , { 'name' : 'title'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Academic title'
                                  }
                                ]
                            , 'name' : 'owner'
                            , 'sig_key' : 2
                            , 'type_name' : 'PAP.Person'
                            , 'ui_name' : 'Owner'
                            , 'ui_type_name' : 'Person'
                            }
                          ]
                      , 'default_child' : 'PAP.Person'
                      , 'name' : 'owner'
                      , 'sig_key' : 2
                      , 'ui_name' : 'Owner'
                      }
                    , { 'attrs' :
                          [ { 'name' : 'lat'
                            , 'sig_key' : 4
                            , 'ui_name' : 'Latitude'
                            }
                          , { 'name' : 'lon'
                            , 'sig_key' : 4
                            , 'ui_name' : 'Longitude'
                            }
                          , { 'name' : 'height'
                            , 'sig_key' : 0
                            , 'ui_name' : 'Height'
                            }
                          ]
                      , 'name' : 'position'
                      , 'ui_name' : 'Position'
                      }
                    , { 'name' : 'show_in_map'
                      , 'sig_key' : 1
                      , 'ui_name' : 'Show in map'
                      }
                    ]
                , 'name' : 'node'
                , 'sig_key' : 2
                , 'ui_name' : 'Node'
                }
              ]
          , 'name' : 'ip_pool'
          , 'sig_key' : 2
          , 'ui_name' : 'Ip pool'
          }
        , { 'Class' : 'Entity'
          , 'name' : 'net_interface'
          , 'sig_key' : 2
          , 'ui_name' : 'Net interface'
          }
        , { 'Class' : 'Entity'
          , 'attrs' :
              [ { 'name' : 'url'
                , 'sig_key' : 3
                , 'ui_name' : 'Url'
                }
              , { 'name' : 'type'
                , 'sig_key' : 3
                , 'ui_name' : 'Type'
                }
              , { 'name' : 'desc'
                , 'sig_key' : 3
                , 'ui_name' : 'Description'
                }
              ]
          , 'name' : 'documents'
          , 'sig_key' : 2
          , 'ui_name' : 'Documents'
          }
        , { 'Class' : 'Entity'
          , 'attrs' :
              [ { 'Class' : 'Entity'
                , 'attrs' :
                    [ { 'Class' : 'Entity'
                      , 'attrs' :
                          [ { 'name' : 'name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Name'
                            }
                          , { 'name' : 'model_no'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Model no'
                            }
                          , { 'name' : 'revision'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Revision'
                            }
                          , { 'name' : 'desc'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Description'
                            }
                          ]
                      , 'name' : 'left'
                      , 'sig_key' : 2
                      , 'ui_name' : 'Net device type'
                      }
                    , { 'Class' : 'Entity'
                      , 'attrs' :
                          [ { 'name' : 'name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Name'
                            }
                          , { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'last_name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Last name'
                                  }
                                , { 'name' : 'first_name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'First name'
                                  }
                                , { 'name' : 'middle_name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Middle name'
                                  }
                                , { 'name' : 'title'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Academic title'
                                  }
                                , { 'attrs' :
                                      [ { 'name' : 'start'
                                        , 'sig_key' : 0
                                        , 'ui_name' : 'Start'
                                        }
                                      , { 'name' : 'finish'
                                        , 'sig_key' : 0
                                        , 'ui_name' : 'Finish'
                                        }
                                      , { 'name' : 'alive'
                                        , 'sig_key' : 1
                                        , 'ui_name' : 'Alive'
                                        }
                                      ]
                                  , 'name' : 'lifetime'
                                  , 'ui_name' : 'Lifetime'
                                  }
                                , { 'name' : 'sex'
                                  , 'sig_key' : 0
                                  , 'ui_name' : 'Sex'
                                  }
                                ]
                            , 'name' : 'manager'
                            , 'sig_key' : 2
                            , 'ui_name' : 'Manager'
                            }
                          , { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'street'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Street'
                                  }
                                , { 'name' : 'zip'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Zip code'
                                  }
                                , { 'name' : 'city'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'City'
                                  }
                                , { 'name' : 'country'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Country'
                                  }
                                , { 'name' : 'desc'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Description'
                                  }
                                , { 'name' : 'region'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Region'
                                  }
                                ]
                            , 'name' : 'address'
                            , 'sig_key' : 2
                            , 'ui_name' : 'Address'
                            }
                          , { 'name' : 'desc'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Description'
                            }
                          , { 'Class' : 'Entity'
                            , 'children_np' :
                                [ { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Adhoc_Group'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Adhoc_Group'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Association'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Association'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      , { 'name' : 'registered_in'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Registered in'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Company'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Company'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'last_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Last name'
                                        }
                                      , { 'name' : 'first_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'First name'
                                        }
                                      , { 'name' : 'middle_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Middle name'
                                        }
                                      , { 'name' : 'title'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Academic title'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Person'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Person'
                                  }
                                ]
                            , 'default_child' : 'PAP.Person'
                            , 'name' : 'owner'
                            , 'sig_key' : 2
                            , 'ui_name' : 'Owner'
                            }
                          , { 'attrs' :
                                [ { 'name' : 'lat'
                                  , 'sig_key' : 4
                                  , 'ui_name' : 'Latitude'
                                  }
                                , { 'name' : 'lon'
                                  , 'sig_key' : 4
                                  , 'ui_name' : 'Longitude'
                                  }
                                , { 'name' : 'height'
                                  , 'sig_key' : 0
                                  , 'ui_name' : 'Height'
                                  }
                                ]
                            , 'name' : 'position'
                            , 'ui_name' : 'Position'
                            }
                          , { 'name' : 'show_in_map'
                            , 'sig_key' : 1
                            , 'ui_name' : 'Show in map'
                            }
                          ]
                      , 'name' : 'node'
                      , 'sig_key' : 2
                      , 'ui_name' : 'Node'
                      }
                    , { 'name' : 'name'
                      , 'sig_key' : 3
                      , 'ui_name' : 'Name'
                      }
                    , { 'name' : 'desc'
                      , 'sig_key' : 3
                      , 'ui_name' : 'Description'
                      }
                    , { 'Class' : 'Entity'
                      , 'attrs' :
                          [ { 'name' : 'name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Name'
                            }
                          , { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'last_name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Last name'
                                  }
                                , { 'name' : 'first_name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'First name'
                                  }
                                , { 'name' : 'middle_name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Middle name'
                                  }
                                , { 'name' : 'title'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Academic title'
                                  }
                                , { 'attrs' :
                                      [ { 'name' : 'start'
                                        , 'sig_key' : 0
                                        , 'ui_name' : 'Start'
                                        }
                                      , { 'name' : 'finish'
                                        , 'sig_key' : 0
                                        , 'ui_name' : 'Finish'
                                        }
                                      , { 'name' : 'alive'
                                        , 'sig_key' : 1
                                        , 'ui_name' : 'Alive'
                                        }
                                      ]
                                  , 'name' : 'lifetime'
                                  , 'ui_name' : 'Lifetime'
                                  }
                                , { 'name' : 'sex'
                                  , 'sig_key' : 0
                                  , 'ui_name' : 'Sex'
                                  }
                                ]
                            , 'name' : 'manager'
                            , 'sig_key' : 2
                            , 'ui_name' : 'Manager'
                            }
                          , { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'street'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Street'
                                  }
                                , { 'name' : 'zip'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Zip code'
                                  }
                                , { 'name' : 'city'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'City'
                                  }
                                , { 'name' : 'country'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Country'
                                  }
                                , { 'name' : 'desc'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Description'
                                  }
                                , { 'name' : 'region'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Region'
                                  }
                                ]
                            , 'name' : 'address'
                            , 'sig_key' : 2
                            , 'ui_name' : 'Address'
                            }
                          , { 'name' : 'desc'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Description'
                            }
                          , { 'Class' : 'Entity'
                            , 'children_np' :
                                [ { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Adhoc_Group'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Adhoc_Group'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Association'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Association'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      , { 'name' : 'registered_in'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Registered in'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Company'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Company'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'last_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Last name'
                                        }
                                      , { 'name' : 'first_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'First name'
                                        }
                                      , { 'name' : 'middle_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Middle name'
                                        }
                                      , { 'name' : 'title'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Academic title'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Person'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Person'
                                  }
                                ]
                            , 'default_child' : 'PAP.Person'
                            , 'name' : 'owner'
                            , 'sig_key' : 2
                            , 'ui_name' : 'Owner'
                            }
                          , { 'attrs' :
                                [ { 'name' : 'lat'
                                  , 'sig_key' : 4
                                  , 'ui_name' : 'Latitude'
                                  }
                                , { 'name' : 'lon'
                                  , 'sig_key' : 4
                                  , 'ui_name' : 'Longitude'
                                  }
                                , { 'name' : 'height'
                                  , 'sig_key' : 0
                                  , 'ui_name' : 'Height'
                                  }
                                ]
                            , 'name' : 'position'
                            , 'ui_name' : 'Position'
                            }
                          , { 'name' : 'show_in_map'
                            , 'sig_key' : 1
                            , 'ui_name' : 'Show in map'
                            }
                          ]
                      , 'name' : 'my_node'
                      , 'sig_key' : 2
                      , 'ui_name' : 'My node'
                      }
                    ]
                , 'name' : 'left'
                , 'sig_key' : 2
                , 'ui_name' : 'Net device'
                }
              , { 'name' : 'mac_address'
                , 'sig_key' : 3
                , 'ui_name' : 'Mac address'
                }
              , { 'name' : 'name'
                , 'sig_key' : 3
                , 'ui_name' : 'Name'
                }
              , { 'name' : 'is_active'
                , 'sig_key' : 1
                , 'ui_name' : 'Is active'
                }
              , { 'name' : 'desc'
                , 'sig_key' : 3
                , 'ui_name' : 'Description'
                }
              , { 'Class' : 'Entity'
                , 'attrs' :
                    [ { 'name' : 'name'
                      , 'sig_key' : 3
                      , 'ui_name' : 'Name'
                      }
                    , { 'Class' : 'Entity'
                      , 'attrs' :
                          [ { 'name' : 'last_name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Last name'
                            }
                          , { 'name' : 'first_name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'First name'
                            }
                          , { 'name' : 'middle_name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Middle name'
                            }
                          , { 'name' : 'title'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Academic title'
                            }
                          , { 'attrs' :
                                [ { 'name' : 'start'
                                  , 'sig_key' : 0
                                  , 'ui_name' : 'Start'
                                  }
                                , { 'name' : 'finish'
                                  , 'sig_key' : 0
                                  , 'ui_name' : 'Finish'
                                  }
                                , { 'name' : 'alive'
                                  , 'sig_key' : 1
                                  , 'ui_name' : 'Alive'
                                  }
                                ]
                            , 'name' : 'lifetime'
                            , 'ui_name' : 'Lifetime'
                            }
                          , { 'name' : 'sex'
                            , 'sig_key' : 0
                            , 'ui_name' : 'Sex'
                            }
                          ]
                      , 'name' : 'manager'
                      , 'sig_key' : 2
                      , 'ui_name' : 'Manager'
                      }
                    , { 'Class' : 'Entity'
                      , 'attrs' :
                          [ { 'name' : 'street'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Street'
                            }
                          , { 'name' : 'zip'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Zip code'
                            }
                          , { 'name' : 'city'
                            , 'sig_key' : 3
                            , 'ui_name' : 'City'
                            }
                          , { 'name' : 'country'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Country'
                            }
                          , { 'name' : 'desc'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Description'
                            }
                          , { 'name' : 'region'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Region'
                            }
                          ]
                      , 'name' : 'address'
                      , 'sig_key' : 2
                      , 'ui_name' : 'Address'
                      }
                    , { 'name' : 'desc'
                      , 'sig_key' : 3
                      , 'ui_name' : 'Description'
                      }
                    , { 'Class' : 'Entity'
                      , 'children_np' :
                          [ { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Name'
                                  }
                                ]
                            , 'name' : 'owner'
                            , 'sig_key' : 2
                            , 'type_name' : 'PAP.Adhoc_Group'
                            , 'ui_name' : 'Owner'
                            , 'ui_type_name' : 'Adhoc_Group'
                            }
                          , { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Name'
                                  }
                                ]
                            , 'name' : 'owner'
                            , 'sig_key' : 2
                            , 'type_name' : 'PAP.Association'
                            , 'ui_name' : 'Owner'
                            , 'ui_type_name' : 'Association'
                            }
                          , { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Name'
                                  }
                                , { 'name' : 'registered_in'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Registered in'
                                  }
                                ]
                            , 'name' : 'owner'
                            , 'sig_key' : 2
                            , 'type_name' : 'PAP.Company'
                            , 'ui_name' : 'Owner'
                            , 'ui_type_name' : 'Company'
                            }
                          , { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'last_name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Last name'
                                  }
                                , { 'name' : 'first_name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'First name'
                                  }
                                , { 'name' : 'middle_name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Middle name'
                                  }
                                , { 'name' : 'title'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Academic title'
                                  }
                                ]
                            , 'name' : 'owner'
                            , 'sig_key' : 2
                            , 'type_name' : 'PAP.Person'
                            , 'ui_name' : 'Owner'
                            , 'ui_type_name' : 'Person'
                            }
                          ]
                      , 'default_child' : 'PAP.Person'
                      , 'name' : 'owner'
                      , 'sig_key' : 2
                      , 'ui_name' : 'Owner'
                      }
                    , { 'attrs' :
                          [ { 'name' : 'lat'
                            , 'sig_key' : 4
                            , 'ui_name' : 'Latitude'
                            }
                          , { 'name' : 'lon'
                            , 'sig_key' : 4
                            , 'ui_name' : 'Longitude'
                            }
                          , { 'name' : 'height'
                            , 'sig_key' : 0
                            , 'ui_name' : 'Height'
                            }
                          ]
                      , 'name' : 'position'
                      , 'ui_name' : 'Position'
                      }
                    , { 'name' : 'show_in_map'
                      , 'sig_key' : 1
                      , 'ui_name' : 'Show in map'
                      }
                    ]
                , 'name' : 'my_node'
                , 'sig_key' : 2
                , 'ui_name' : 'My node'
                }
              , { 'Class' : 'Entity'
                , 'attrs' :
                    [ { 'Class' : 'Entity'
                      , 'attrs' :
                          [ { 'name' : 'name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Name'
                            }
                          , { 'name' : 'model_no'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Model no'
                            }
                          , { 'name' : 'revision'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Revision'
                            }
                          , { 'name' : 'desc'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Description'
                            }
                          ]
                      , 'name' : 'left'
                      , 'sig_key' : 2
                      , 'ui_name' : 'Net device type'
                      }
                    , { 'Class' : 'Entity'
                      , 'attrs' :
                          [ { 'name' : 'name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Name'
                            }
                          , { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'last_name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Last name'
                                  }
                                , { 'name' : 'first_name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'First name'
                                  }
                                , { 'name' : 'middle_name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Middle name'
                                  }
                                , { 'name' : 'title'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Academic title'
                                  }
                                , { 'attrs' :
                                      [ { 'name' : 'start'
                                        , 'sig_key' : 0
                                        , 'ui_name' : 'Start'
                                        }
                                      , { 'name' : 'finish'
                                        , 'sig_key' : 0
                                        , 'ui_name' : 'Finish'
                                        }
                                      , { 'name' : 'alive'
                                        , 'sig_key' : 1
                                        , 'ui_name' : 'Alive'
                                        }
                                      ]
                                  , 'name' : 'lifetime'
                                  , 'ui_name' : 'Lifetime'
                                  }
                                , { 'name' : 'sex'
                                  , 'sig_key' : 0
                                  , 'ui_name' : 'Sex'
                                  }
                                ]
                            , 'name' : 'manager'
                            , 'sig_key' : 2
                            , 'ui_name' : 'Manager'
                            }
                          , { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'street'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Street'
                                  }
                                , { 'name' : 'zip'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Zip code'
                                  }
                                , { 'name' : 'city'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'City'
                                  }
                                , { 'name' : 'country'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Country'
                                  }
                                , { 'name' : 'desc'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Description'
                                  }
                                , { 'name' : 'region'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Region'
                                  }
                                ]
                            , 'name' : 'address'
                            , 'sig_key' : 2
                            , 'ui_name' : 'Address'
                            }
                          , { 'name' : 'desc'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Description'
                            }
                          , { 'Class' : 'Entity'
                            , 'children_np' :
                                [ { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Adhoc_Group'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Adhoc_Group'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Association'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Association'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      , { 'name' : 'registered_in'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Registered in'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Company'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Company'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'last_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Last name'
                                        }
                                      , { 'name' : 'first_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'First name'
                                        }
                                      , { 'name' : 'middle_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Middle name'
                                        }
                                      , { 'name' : 'title'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Academic title'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Person'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Person'
                                  }
                                ]
                            , 'default_child' : 'PAP.Person'
                            , 'name' : 'owner'
                            , 'sig_key' : 2
                            , 'ui_name' : 'Owner'
                            }
                          , { 'attrs' :
                                [ { 'name' : 'lat'
                                  , 'sig_key' : 4
                                  , 'ui_name' : 'Latitude'
                                  }
                                , { 'name' : 'lon'
                                  , 'sig_key' : 4
                                  , 'ui_name' : 'Longitude'
                                  }
                                , { 'name' : 'height'
                                  , 'sig_key' : 0
                                  , 'ui_name' : 'Height'
                                  }
                                ]
                            , 'name' : 'position'
                            , 'ui_name' : 'Position'
                            }
                          , { 'name' : 'show_in_map'
                            , 'sig_key' : 1
                            , 'ui_name' : 'Show in map'
                            }
                          ]
                      , 'name' : 'node'
                      , 'sig_key' : 2
                      , 'ui_name' : 'Node'
                      }
                    , { 'name' : 'name'
                      , 'sig_key' : 3
                      , 'ui_name' : 'Name'
                      }
                    , { 'name' : 'desc'
                      , 'sig_key' : 3
                      , 'ui_name' : 'Description'
                      }
                    , { 'Class' : 'Entity'
                      , 'attrs' :
                          [ { 'name' : 'name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Name'
                            }
                          , { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'last_name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Last name'
                                  }
                                , { 'name' : 'first_name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'First name'
                                  }
                                , { 'name' : 'middle_name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Middle name'
                                  }
                                , { 'name' : 'title'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Academic title'
                                  }
                                , { 'attrs' :
                                      [ { 'name' : 'start'
                                        , 'sig_key' : 0
                                        , 'ui_name' : 'Start'
                                        }
                                      , { 'name' : 'finish'
                                        , 'sig_key' : 0
                                        , 'ui_name' : 'Finish'
                                        }
                                      , { 'name' : 'alive'
                                        , 'sig_key' : 1
                                        , 'ui_name' : 'Alive'
                                        }
                                      ]
                                  , 'name' : 'lifetime'
                                  , 'ui_name' : 'Lifetime'
                                  }
                                , { 'name' : 'sex'
                                  , 'sig_key' : 0
                                  , 'ui_name' : 'Sex'
                                  }
                                ]
                            , 'name' : 'manager'
                            , 'sig_key' : 2
                            , 'ui_name' : 'Manager'
                            }
                          , { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'street'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Street'
                                  }
                                , { 'name' : 'zip'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Zip code'
                                  }
                                , { 'name' : 'city'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'City'
                                  }
                                , { 'name' : 'country'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Country'
                                  }
                                , { 'name' : 'desc'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Description'
                                  }
                                , { 'name' : 'region'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Region'
                                  }
                                ]
                            , 'name' : 'address'
                            , 'sig_key' : 2
                            , 'ui_name' : 'Address'
                            }
                          , { 'name' : 'desc'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Description'
                            }
                          , { 'Class' : 'Entity'
                            , 'children_np' :
                                [ { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Adhoc_Group'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Adhoc_Group'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Association'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Association'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      , { 'name' : 'registered_in'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Registered in'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Company'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Company'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'last_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Last name'
                                        }
                                      , { 'name' : 'first_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'First name'
                                        }
                                      , { 'name' : 'middle_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Middle name'
                                        }
                                      , { 'name' : 'title'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Academic title'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Person'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Person'
                                  }
                                ]
                            , 'default_child' : 'PAP.Person'
                            , 'name' : 'owner'
                            , 'sig_key' : 2
                            , 'ui_name' : 'Owner'
                            }
                          , { 'attrs' :
                                [ { 'name' : 'lat'
                                  , 'sig_key' : 4
                                  , 'ui_name' : 'Latitude'
                                  }
                                , { 'name' : 'lon'
                                  , 'sig_key' : 4
                                  , 'ui_name' : 'Longitude'
                                  }
                                , { 'name' : 'height'
                                  , 'sig_key' : 0
                                  , 'ui_name' : 'Height'
                                  }
                                ]
                            , 'name' : 'position'
                            , 'ui_name' : 'Position'
                            }
                          , { 'name' : 'show_in_map'
                            , 'sig_key' : 1
                            , 'ui_name' : 'Show in map'
                            }
                          ]
                      , 'name' : 'my_node'
                      , 'sig_key' : 2
                      , 'ui_name' : 'My node'
                      }
                    ]
                , 'name' : 'my_net_device'
                , 'sig_key' : 2
                , 'ui_name' : 'My net device'
                }
              ]
          , 'name' : 'wired_interface'
          , 'sig_key' : 2
          , 'ui_name' : 'Wired interface'
          }
        , { 'Class' : 'Entity'
          , 'attrs' :
              [ { 'Class' : 'Entity'
                , 'attrs' :
                    [ { 'Class' : 'Entity'
                      , 'attrs' :
                          [ { 'name' : 'name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Name'
                            }
                          , { 'name' : 'model_no'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Model no'
                            }
                          , { 'name' : 'revision'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Revision'
                            }
                          , { 'name' : 'desc'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Description'
                            }
                          ]
                      , 'name' : 'left'
                      , 'sig_key' : 2
                      , 'ui_name' : 'Net device type'
                      }
                    , { 'Class' : 'Entity'
                      , 'attrs' :
                          [ { 'name' : 'name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Name'
                            }
                          , { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'last_name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Last name'
                                  }
                                , { 'name' : 'first_name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'First name'
                                  }
                                , { 'name' : 'middle_name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Middle name'
                                  }
                                , { 'name' : 'title'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Academic title'
                                  }
                                , { 'attrs' :
                                      [ { 'name' : 'start'
                                        , 'sig_key' : 0
                                        , 'ui_name' : 'Start'
                                        }
                                      , { 'name' : 'finish'
                                        , 'sig_key' : 0
                                        , 'ui_name' : 'Finish'
                                        }
                                      , { 'name' : 'alive'
                                        , 'sig_key' : 1
                                        , 'ui_name' : 'Alive'
                                        }
                                      ]
                                  , 'name' : 'lifetime'
                                  , 'ui_name' : 'Lifetime'
                                  }
                                , { 'name' : 'sex'
                                  , 'sig_key' : 0
                                  , 'ui_name' : 'Sex'
                                  }
                                ]
                            , 'name' : 'manager'
                            , 'sig_key' : 2
                            , 'ui_name' : 'Manager'
                            }
                          , { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'street'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Street'
                                  }
                                , { 'name' : 'zip'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Zip code'
                                  }
                                , { 'name' : 'city'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'City'
                                  }
                                , { 'name' : 'country'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Country'
                                  }
                                , { 'name' : 'desc'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Description'
                                  }
                                , { 'name' : 'region'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Region'
                                  }
                                ]
                            , 'name' : 'address'
                            , 'sig_key' : 2
                            , 'ui_name' : 'Address'
                            }
                          , { 'name' : 'desc'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Description'
                            }
                          , { 'Class' : 'Entity'
                            , 'children_np' :
                                [ { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Adhoc_Group'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Adhoc_Group'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Association'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Association'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      , { 'name' : 'registered_in'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Registered in'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Company'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Company'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'last_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Last name'
                                        }
                                      , { 'name' : 'first_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'First name'
                                        }
                                      , { 'name' : 'middle_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Middle name'
                                        }
                                      , { 'name' : 'title'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Academic title'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Person'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Person'
                                  }
                                ]
                            , 'default_child' : 'PAP.Person'
                            , 'name' : 'owner'
                            , 'sig_key' : 2
                            , 'ui_name' : 'Owner'
                            }
                          , { 'attrs' :
                                [ { 'name' : 'lat'
                                  , 'sig_key' : 4
                                  , 'ui_name' : 'Latitude'
                                  }
                                , { 'name' : 'lon'
                                  , 'sig_key' : 4
                                  , 'ui_name' : 'Longitude'
                                  }
                                , { 'name' : 'height'
                                  , 'sig_key' : 0
                                  , 'ui_name' : 'Height'
                                  }
                                ]
                            , 'name' : 'position'
                            , 'ui_name' : 'Position'
                            }
                          , { 'name' : 'show_in_map'
                            , 'sig_key' : 1
                            , 'ui_name' : 'Show in map'
                            }
                          ]
                      , 'name' : 'node'
                      , 'sig_key' : 2
                      , 'ui_name' : 'Node'
                      }
                    , { 'name' : 'name'
                      , 'sig_key' : 3
                      , 'ui_name' : 'Name'
                      }
                    , { 'name' : 'desc'
                      , 'sig_key' : 3
                      , 'ui_name' : 'Description'
                      }
                    , { 'Class' : 'Entity'
                      , 'attrs' :
                          [ { 'name' : 'name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Name'
                            }
                          , { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'last_name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Last name'
                                  }
                                , { 'name' : 'first_name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'First name'
                                  }
                                , { 'name' : 'middle_name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Middle name'
                                  }
                                , { 'name' : 'title'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Academic title'
                                  }
                                , { 'attrs' :
                                      [ { 'name' : 'start'
                                        , 'sig_key' : 0
                                        , 'ui_name' : 'Start'
                                        }
                                      , { 'name' : 'finish'
                                        , 'sig_key' : 0
                                        , 'ui_name' : 'Finish'
                                        }
                                      , { 'name' : 'alive'
                                        , 'sig_key' : 1
                                        , 'ui_name' : 'Alive'
                                        }
                                      ]
                                  , 'name' : 'lifetime'
                                  , 'ui_name' : 'Lifetime'
                                  }
                                , { 'name' : 'sex'
                                  , 'sig_key' : 0
                                  , 'ui_name' : 'Sex'
                                  }
                                ]
                            , 'name' : 'manager'
                            , 'sig_key' : 2
                            , 'ui_name' : 'Manager'
                            }
                          , { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'street'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Street'
                                  }
                                , { 'name' : 'zip'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Zip code'
                                  }
                                , { 'name' : 'city'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'City'
                                  }
                                , { 'name' : 'country'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Country'
                                  }
                                , { 'name' : 'desc'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Description'
                                  }
                                , { 'name' : 'region'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Region'
                                  }
                                ]
                            , 'name' : 'address'
                            , 'sig_key' : 2
                            , 'ui_name' : 'Address'
                            }
                          , { 'name' : 'desc'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Description'
                            }
                          , { 'Class' : 'Entity'
                            , 'children_np' :
                                [ { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Adhoc_Group'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Adhoc_Group'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Association'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Association'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      , { 'name' : 'registered_in'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Registered in'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Company'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Company'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'last_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Last name'
                                        }
                                      , { 'name' : 'first_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'First name'
                                        }
                                      , { 'name' : 'middle_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Middle name'
                                        }
                                      , { 'name' : 'title'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Academic title'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Person'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Person'
                                  }
                                ]
                            , 'default_child' : 'PAP.Person'
                            , 'name' : 'owner'
                            , 'sig_key' : 2
                            , 'ui_name' : 'Owner'
                            }
                          , { 'attrs' :
                                [ { 'name' : 'lat'
                                  , 'sig_key' : 4
                                  , 'ui_name' : 'Latitude'
                                  }
                                , { 'name' : 'lon'
                                  , 'sig_key' : 4
                                  , 'ui_name' : 'Longitude'
                                  }
                                , { 'name' : 'height'
                                  , 'sig_key' : 0
                                  , 'ui_name' : 'Height'
                                  }
                                ]
                            , 'name' : 'position'
                            , 'ui_name' : 'Position'
                            }
                          , { 'name' : 'show_in_map'
                            , 'sig_key' : 1
                            , 'ui_name' : 'Show in map'
                            }
                          ]
                      , 'name' : 'my_node'
                      , 'sig_key' : 2
                      , 'ui_name' : 'My node'
                      }
                    ]
                , 'name' : 'left'
                , 'sig_key' : 2
                , 'ui_name' : 'Net device'
                }
              , { 'name' : 'mac_address'
                , 'sig_key' : 3
                , 'ui_name' : 'Mac address'
                }
              , { 'name' : 'name'
                , 'sig_key' : 3
                , 'ui_name' : 'Name'
                }
              , { 'name' : 'is_active'
                , 'sig_key' : 1
                , 'ui_name' : 'Is active'
                }
              , { 'name' : 'desc'
                , 'sig_key' : 3
                , 'ui_name' : 'Description'
                }
              , { 'name' : 'mode'
                , 'sig_key' : 0
                , 'ui_name' : 'Mode'
                }
              , { 'name' : 'essid'
                , 'sig_key' : 3
                , 'ui_name' : 'ESSID'
                }
              , { 'name' : 'bssid'
                , 'sig_key' : 3
                , 'ui_name' : 'BSSID'
                }
              , { 'Class' : 'Entity'
                , 'attrs' :
                    [ { 'name' : 'name'
                      , 'sig_key' : 3
                      , 'ui_name' : 'Name'
                      }
                    , { 'name' : 'bandwidth'
                      , 'sig_key' : 4
                      , 'ui_name' : 'Bandwidth'
                      }
                    ]
                , 'name' : 'standard'
                , 'sig_key' : 2
                , 'ui_name' : 'Standard'
                }
              , { 'name' : 'txpower'
                , 'sig_key' : 4
                , 'ui_name' : 'TX power'
                }
              , { 'Class' : 'Entity'
                , 'attrs' :
                    [ { 'name' : 'name'
                      , 'sig_key' : 3
                      , 'ui_name' : 'Name'
                      }
                    , { 'Class' : 'Entity'
                      , 'attrs' :
                          [ { 'name' : 'last_name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Last name'
                            }
                          , { 'name' : 'first_name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'First name'
                            }
                          , { 'name' : 'middle_name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Middle name'
                            }
                          , { 'name' : 'title'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Academic title'
                            }
                          , { 'attrs' :
                                [ { 'name' : 'start'
                                  , 'sig_key' : 0
                                  , 'ui_name' : 'Start'
                                  }
                                , { 'name' : 'finish'
                                  , 'sig_key' : 0
                                  , 'ui_name' : 'Finish'
                                  }
                                , { 'name' : 'alive'
                                  , 'sig_key' : 1
                                  , 'ui_name' : 'Alive'
                                  }
                                ]
                            , 'name' : 'lifetime'
                            , 'ui_name' : 'Lifetime'
                            }
                          , { 'name' : 'sex'
                            , 'sig_key' : 0
                            , 'ui_name' : 'Sex'
                            }
                          ]
                      , 'name' : 'manager'
                      , 'sig_key' : 2
                      , 'ui_name' : 'Manager'
                      }
                    , { 'Class' : 'Entity'
                      , 'attrs' :
                          [ { 'name' : 'street'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Street'
                            }
                          , { 'name' : 'zip'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Zip code'
                            }
                          , { 'name' : 'city'
                            , 'sig_key' : 3
                            , 'ui_name' : 'City'
                            }
                          , { 'name' : 'country'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Country'
                            }
                          , { 'name' : 'desc'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Description'
                            }
                          , { 'name' : 'region'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Region'
                            }
                          ]
                      , 'name' : 'address'
                      , 'sig_key' : 2
                      , 'ui_name' : 'Address'
                      }
                    , { 'name' : 'desc'
                      , 'sig_key' : 3
                      , 'ui_name' : 'Description'
                      }
                    , { 'Class' : 'Entity'
                      , 'children_np' :
                          [ { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Name'
                                  }
                                ]
                            , 'name' : 'owner'
                            , 'sig_key' : 2
                            , 'type_name' : 'PAP.Adhoc_Group'
                            , 'ui_name' : 'Owner'
                            , 'ui_type_name' : 'Adhoc_Group'
                            }
                          , { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Name'
                                  }
                                ]
                            , 'name' : 'owner'
                            , 'sig_key' : 2
                            , 'type_name' : 'PAP.Association'
                            , 'ui_name' : 'Owner'
                            , 'ui_type_name' : 'Association'
                            }
                          , { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Name'
                                  }
                                , { 'name' : 'registered_in'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Registered in'
                                  }
                                ]
                            , 'name' : 'owner'
                            , 'sig_key' : 2
                            , 'type_name' : 'PAP.Company'
                            , 'ui_name' : 'Owner'
                            , 'ui_type_name' : 'Company'
                            }
                          , { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'last_name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Last name'
                                  }
                                , { 'name' : 'first_name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'First name'
                                  }
                                , { 'name' : 'middle_name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Middle name'
                                  }
                                , { 'name' : 'title'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Academic title'
                                  }
                                ]
                            , 'name' : 'owner'
                            , 'sig_key' : 2
                            , 'type_name' : 'PAP.Person'
                            , 'ui_name' : 'Owner'
                            , 'ui_type_name' : 'Person'
                            }
                          ]
                      , 'default_child' : 'PAP.Person'
                      , 'name' : 'owner'
                      , 'sig_key' : 2
                      , 'ui_name' : 'Owner'
                      }
                    , { 'attrs' :
                          [ { 'name' : 'lat'
                            , 'sig_key' : 4
                            , 'ui_name' : 'Latitude'
                            }
                          , { 'name' : 'lon'
                            , 'sig_key' : 4
                            , 'ui_name' : 'Longitude'
                            }
                          , { 'name' : 'height'
                            , 'sig_key' : 0
                            , 'ui_name' : 'Height'
                            }
                          ]
                      , 'name' : 'position'
                      , 'ui_name' : 'Position'
                      }
                    , { 'name' : 'show_in_map'
                      , 'sig_key' : 1
                      , 'ui_name' : 'Show in map'
                      }
                    ]
                , 'name' : 'my_node'
                , 'sig_key' : 2
                , 'ui_name' : 'My node'
                }
              , { 'Class' : 'Entity'
                , 'attrs' :
                    [ { 'Class' : 'Entity'
                      , 'attrs' :
                          [ { 'name' : 'name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Name'
                            }
                          , { 'name' : 'model_no'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Model no'
                            }
                          , { 'name' : 'revision'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Revision'
                            }
                          , { 'name' : 'desc'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Description'
                            }
                          ]
                      , 'name' : 'left'
                      , 'sig_key' : 2
                      , 'ui_name' : 'Net device type'
                      }
                    , { 'Class' : 'Entity'
                      , 'attrs' :
                          [ { 'name' : 'name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Name'
                            }
                          , { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'last_name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Last name'
                                  }
                                , { 'name' : 'first_name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'First name'
                                  }
                                , { 'name' : 'middle_name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Middle name'
                                  }
                                , { 'name' : 'title'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Academic title'
                                  }
                                , { 'attrs' :
                                      [ { 'name' : 'start'
                                        , 'sig_key' : 0
                                        , 'ui_name' : 'Start'
                                        }
                                      , { 'name' : 'finish'
                                        , 'sig_key' : 0
                                        , 'ui_name' : 'Finish'
                                        }
                                      , { 'name' : 'alive'
                                        , 'sig_key' : 1
                                        , 'ui_name' : 'Alive'
                                        }
                                      ]
                                  , 'name' : 'lifetime'
                                  , 'ui_name' : 'Lifetime'
                                  }
                                , { 'name' : 'sex'
                                  , 'sig_key' : 0
                                  , 'ui_name' : 'Sex'
                                  }
                                ]
                            , 'name' : 'manager'
                            , 'sig_key' : 2
                            , 'ui_name' : 'Manager'
                            }
                          , { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'street'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Street'
                                  }
                                , { 'name' : 'zip'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Zip code'
                                  }
                                , { 'name' : 'city'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'City'
                                  }
                                , { 'name' : 'country'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Country'
                                  }
                                , { 'name' : 'desc'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Description'
                                  }
                                , { 'name' : 'region'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Region'
                                  }
                                ]
                            , 'name' : 'address'
                            , 'sig_key' : 2
                            , 'ui_name' : 'Address'
                            }
                          , { 'name' : 'desc'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Description'
                            }
                          , { 'Class' : 'Entity'
                            , 'children_np' :
                                [ { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Adhoc_Group'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Adhoc_Group'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Association'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Association'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      , { 'name' : 'registered_in'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Registered in'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Company'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Company'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'last_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Last name'
                                        }
                                      , { 'name' : 'first_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'First name'
                                        }
                                      , { 'name' : 'middle_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Middle name'
                                        }
                                      , { 'name' : 'title'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Academic title'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Person'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Person'
                                  }
                                ]
                            , 'default_child' : 'PAP.Person'
                            , 'name' : 'owner'
                            , 'sig_key' : 2
                            , 'ui_name' : 'Owner'
                            }
                          , { 'attrs' :
                                [ { 'name' : 'lat'
                                  , 'sig_key' : 4
                                  , 'ui_name' : 'Latitude'
                                  }
                                , { 'name' : 'lon'
                                  , 'sig_key' : 4
                                  , 'ui_name' : 'Longitude'
                                  }
                                , { 'name' : 'height'
                                  , 'sig_key' : 0
                                  , 'ui_name' : 'Height'
                                  }
                                ]
                            , 'name' : 'position'
                            , 'ui_name' : 'Position'
                            }
                          , { 'name' : 'show_in_map'
                            , 'sig_key' : 1
                            , 'ui_name' : 'Show in map'
                            }
                          ]
                      , 'name' : 'node'
                      , 'sig_key' : 2
                      , 'ui_name' : 'Node'
                      }
                    , { 'name' : 'name'
                      , 'sig_key' : 3
                      , 'ui_name' : 'Name'
                      }
                    , { 'name' : 'desc'
                      , 'sig_key' : 3
                      , 'ui_name' : 'Description'
                      }
                    , { 'Class' : 'Entity'
                      , 'attrs' :
                          [ { 'name' : 'name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Name'
                            }
                          , { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'last_name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Last name'
                                  }
                                , { 'name' : 'first_name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'First name'
                                  }
                                , { 'name' : 'middle_name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Middle name'
                                  }
                                , { 'name' : 'title'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Academic title'
                                  }
                                , { 'attrs' :
                                      [ { 'name' : 'start'
                                        , 'sig_key' : 0
                                        , 'ui_name' : 'Start'
                                        }
                                      , { 'name' : 'finish'
                                        , 'sig_key' : 0
                                        , 'ui_name' : 'Finish'
                                        }
                                      , { 'name' : 'alive'
                                        , 'sig_key' : 1
                                        , 'ui_name' : 'Alive'
                                        }
                                      ]
                                  , 'name' : 'lifetime'
                                  , 'ui_name' : 'Lifetime'
                                  }
                                , { 'name' : 'sex'
                                  , 'sig_key' : 0
                                  , 'ui_name' : 'Sex'
                                  }
                                ]
                            , 'name' : 'manager'
                            , 'sig_key' : 2
                            , 'ui_name' : 'Manager'
                            }
                          , { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'street'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Street'
                                  }
                                , { 'name' : 'zip'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Zip code'
                                  }
                                , { 'name' : 'city'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'City'
                                  }
                                , { 'name' : 'country'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Country'
                                  }
                                , { 'name' : 'desc'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Description'
                                  }
                                , { 'name' : 'region'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Region'
                                  }
                                ]
                            , 'name' : 'address'
                            , 'sig_key' : 2
                            , 'ui_name' : 'Address'
                            }
                          , { 'name' : 'desc'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Description'
                            }
                          , { 'Class' : 'Entity'
                            , 'children_np' :
                                [ { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Adhoc_Group'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Adhoc_Group'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Association'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Association'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      , { 'name' : 'registered_in'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Registered in'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Company'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Company'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'last_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Last name'
                                        }
                                      , { 'name' : 'first_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'First name'
                                        }
                                      , { 'name' : 'middle_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Middle name'
                                        }
                                      , { 'name' : 'title'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Academic title'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Person'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Person'
                                  }
                                ]
                            , 'default_child' : 'PAP.Person'
                            , 'name' : 'owner'
                            , 'sig_key' : 2
                            , 'ui_name' : 'Owner'
                            }
                          , { 'attrs' :
                                [ { 'name' : 'lat'
                                  , 'sig_key' : 4
                                  , 'ui_name' : 'Latitude'
                                  }
                                , { 'name' : 'lon'
                                  , 'sig_key' : 4
                                  , 'ui_name' : 'Longitude'
                                  }
                                , { 'name' : 'height'
                                  , 'sig_key' : 0
                                  , 'ui_name' : 'Height'
                                  }
                                ]
                            , 'name' : 'position'
                            , 'ui_name' : 'Position'
                            }
                          , { 'name' : 'show_in_map'
                            , 'sig_key' : 1
                            , 'ui_name' : 'Show in map'
                            }
                          ]
                      , 'name' : 'my_node'
                      , 'sig_key' : 2
                      , 'ui_name' : 'My node'
                      }
                    ]
                , 'name' : 'my_net_device'
                , 'sig_key' : 2
                , 'ui_name' : 'My net device'
                }
              ]
          , 'name' : 'wireless_interface'
          , 'sig_key' : 2
          , 'ui_name' : 'Wireless interface'
          }
        , { 'Class' : 'Entity'
          , 'attrs' :
              [ { 'Class' : 'Entity'
                , 'attrs' :
                    [ { 'Class' : 'Entity'
                      , 'attrs' :
                          [ { 'name' : 'name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Name'
                            }
                          , { 'name' : 'model_no'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Model no'
                            }
                          , { 'name' : 'revision'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Revision'
                            }
                          , { 'name' : 'desc'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Description'
                            }
                          ]
                      , 'name' : 'left'
                      , 'sig_key' : 2
                      , 'ui_name' : 'Net device type'
                      }
                    , { 'Class' : 'Entity'
                      , 'attrs' :
                          [ { 'name' : 'name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Name'
                            }
                          , { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'last_name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Last name'
                                  }
                                , { 'name' : 'first_name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'First name'
                                  }
                                , { 'name' : 'middle_name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Middle name'
                                  }
                                , { 'name' : 'title'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Academic title'
                                  }
                                , { 'attrs' :
                                      [ { 'name' : 'start'
                                        , 'sig_key' : 0
                                        , 'ui_name' : 'Start'
                                        }
                                      , { 'name' : 'finish'
                                        , 'sig_key' : 0
                                        , 'ui_name' : 'Finish'
                                        }
                                      , { 'name' : 'alive'
                                        , 'sig_key' : 1
                                        , 'ui_name' : 'Alive'
                                        }
                                      ]
                                  , 'name' : 'lifetime'
                                  , 'ui_name' : 'Lifetime'
                                  }
                                , { 'name' : 'sex'
                                  , 'sig_key' : 0
                                  , 'ui_name' : 'Sex'
                                  }
                                ]
                            , 'name' : 'manager'
                            , 'sig_key' : 2
                            , 'ui_name' : 'Manager'
                            }
                          , { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'street'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Street'
                                  }
                                , { 'name' : 'zip'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Zip code'
                                  }
                                , { 'name' : 'city'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'City'
                                  }
                                , { 'name' : 'country'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Country'
                                  }
                                , { 'name' : 'desc'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Description'
                                  }
                                , { 'name' : 'region'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Region'
                                  }
                                ]
                            , 'name' : 'address'
                            , 'sig_key' : 2
                            , 'ui_name' : 'Address'
                            }
                          , { 'name' : 'desc'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Description'
                            }
                          , { 'Class' : 'Entity'
                            , 'children_np' :
                                [ { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Adhoc_Group'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Adhoc_Group'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Association'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Association'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      , { 'name' : 'registered_in'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Registered in'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Company'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Company'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'last_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Last name'
                                        }
                                      , { 'name' : 'first_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'First name'
                                        }
                                      , { 'name' : 'middle_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Middle name'
                                        }
                                      , { 'name' : 'title'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Academic title'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Person'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Person'
                                  }
                                ]
                            , 'default_child' : 'PAP.Person'
                            , 'name' : 'owner'
                            , 'sig_key' : 2
                            , 'ui_name' : 'Owner'
                            }
                          , { 'attrs' :
                                [ { 'name' : 'lat'
                                  , 'sig_key' : 4
                                  , 'ui_name' : 'Latitude'
                                  }
                                , { 'name' : 'lon'
                                  , 'sig_key' : 4
                                  , 'ui_name' : 'Longitude'
                                  }
                                , { 'name' : 'height'
                                  , 'sig_key' : 0
                                  , 'ui_name' : 'Height'
                                  }
                                ]
                            , 'name' : 'position'
                            , 'ui_name' : 'Position'
                            }
                          , { 'name' : 'show_in_map'
                            , 'sig_key' : 1
                            , 'ui_name' : 'Show in map'
                            }
                          ]
                      , 'name' : 'node'
                      , 'sig_key' : 2
                      , 'ui_name' : 'Node'
                      }
                    , { 'name' : 'name'
                      , 'sig_key' : 3
                      , 'ui_name' : 'Name'
                      }
                    , { 'name' : 'desc'
                      , 'sig_key' : 3
                      , 'ui_name' : 'Description'
                      }
                    , { 'Class' : 'Entity'
                      , 'attrs' :
                          [ { 'name' : 'name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Name'
                            }
                          , { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'last_name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Last name'
                                  }
                                , { 'name' : 'first_name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'First name'
                                  }
                                , { 'name' : 'middle_name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Middle name'
                                  }
                                , { 'name' : 'title'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Academic title'
                                  }
                                , { 'attrs' :
                                      [ { 'name' : 'start'
                                        , 'sig_key' : 0
                                        , 'ui_name' : 'Start'
                                        }
                                      , { 'name' : 'finish'
                                        , 'sig_key' : 0
                                        , 'ui_name' : 'Finish'
                                        }
                                      , { 'name' : 'alive'
                                        , 'sig_key' : 1
                                        , 'ui_name' : 'Alive'
                                        }
                                      ]
                                  , 'name' : 'lifetime'
                                  , 'ui_name' : 'Lifetime'
                                  }
                                , { 'name' : 'sex'
                                  , 'sig_key' : 0
                                  , 'ui_name' : 'Sex'
                                  }
                                ]
                            , 'name' : 'manager'
                            , 'sig_key' : 2
                            , 'ui_name' : 'Manager'
                            }
                          , { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'street'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Street'
                                  }
                                , { 'name' : 'zip'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Zip code'
                                  }
                                , { 'name' : 'city'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'City'
                                  }
                                , { 'name' : 'country'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Country'
                                  }
                                , { 'name' : 'desc'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Description'
                                  }
                                , { 'name' : 'region'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Region'
                                  }
                                ]
                            , 'name' : 'address'
                            , 'sig_key' : 2
                            , 'ui_name' : 'Address'
                            }
                          , { 'name' : 'desc'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Description'
                            }
                          , { 'Class' : 'Entity'
                            , 'children_np' :
                                [ { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Adhoc_Group'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Adhoc_Group'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Association'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Association'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      , { 'name' : 'registered_in'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Registered in'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Company'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Company'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'last_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Last name'
                                        }
                                      , { 'name' : 'first_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'First name'
                                        }
                                      , { 'name' : 'middle_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Middle name'
                                        }
                                      , { 'name' : 'title'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Academic title'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Person'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Person'
                                  }
                                ]
                            , 'default_child' : 'PAP.Person'
                            , 'name' : 'owner'
                            , 'sig_key' : 2
                            , 'ui_name' : 'Owner'
                            }
                          , { 'attrs' :
                                [ { 'name' : 'lat'
                                  , 'sig_key' : 4
                                  , 'ui_name' : 'Latitude'
                                  }
                                , { 'name' : 'lon'
                                  , 'sig_key' : 4
                                  , 'ui_name' : 'Longitude'
                                  }
                                , { 'name' : 'height'
                                  , 'sig_key' : 0
                                  , 'ui_name' : 'Height'
                                  }
                                ]
                            , 'name' : 'position'
                            , 'ui_name' : 'Position'
                            }
                          , { 'name' : 'show_in_map'
                            , 'sig_key' : 1
                            , 'ui_name' : 'Show in map'
                            }
                          ]
                      , 'name' : 'my_node'
                      , 'sig_key' : 2
                      , 'ui_name' : 'My node'
                      }
                    ]
                , 'name' : 'left'
                , 'sig_key' : 2
                , 'ui_name' : 'Net device'
                }
              , { 'Class' : 'Entity'
                , 'attrs' :
                    [ { 'Class' : 'Entity'
                      , 'attrs' :
                          [ { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Name'
                                  }
                                , { 'name' : 'model_no'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Model no'
                                  }
                                , { 'name' : 'revision'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Revision'
                                  }
                                , { 'name' : 'desc'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Description'
                                  }
                                ]
                            , 'name' : 'left'
                            , 'sig_key' : 2
                            , 'ui_name' : 'Net device type'
                            }
                          , { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Name'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'last_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Last name'
                                        }
                                      , { 'name' : 'first_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'First name'
                                        }
                                      , { 'name' : 'middle_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Middle name'
                                        }
                                      , { 'name' : 'title'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Academic title'
                                        }
                                      , { 'attrs' :
                                            [ { 'name' : 'start'
                                              , 'sig_key' : 0
                                              , 'ui_name' : 'Start'
                                              }
                                            , { 'name' : 'finish'
                                              , 'sig_key' : 0
                                              , 'ui_name' : 'Finish'
                                              }
                                            , { 'name' : 'alive'
                                              , 'sig_key' : 1
                                              , 'ui_name' : 'Alive'
                                              }
                                            ]
                                        , 'name' : 'lifetime'
                                        , 'ui_name' : 'Lifetime'
                                        }
                                      , { 'name' : 'sex'
                                        , 'sig_key' : 0
                                        , 'ui_name' : 'Sex'
                                        }
                                      ]
                                  , 'name' : 'manager'
                                  , 'sig_key' : 2
                                  , 'ui_name' : 'Manager'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'street'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Street'
                                        }
                                      , { 'name' : 'zip'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Zip code'
                                        }
                                      , { 'name' : 'city'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'City'
                                        }
                                      , { 'name' : 'country'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Country'
                                        }
                                      , { 'name' : 'desc'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Description'
                                        }
                                      , { 'name' : 'region'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Region'
                                        }
                                      ]
                                  , 'name' : 'address'
                                  , 'sig_key' : 2
                                  , 'ui_name' : 'Address'
                                  }
                                , { 'name' : 'desc'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Description'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'children_np' :
                                      [ { 'Class' : 'Entity'
                                        , 'attrs' :
                                            [ { 'name' : 'name'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'Name'
                                              }
                                            ]
                                        , 'name' : 'owner'
                                        , 'sig_key' : 2
                                        , 'type_name' : 'PAP.Adhoc_Group'
                                        , 'ui_name' : 'Owner'
                                        , 'ui_type_name' : 'Adhoc_Group'
                                        }
                                      , { 'Class' : 'Entity'
                                        , 'attrs' :
                                            [ { 'name' : 'name'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'Name'
                                              }
                                            ]
                                        , 'name' : 'owner'
                                        , 'sig_key' : 2
                                        , 'type_name' : 'PAP.Association'
                                        , 'ui_name' : 'Owner'
                                        , 'ui_type_name' : 'Association'
                                        }
                                      , { 'Class' : 'Entity'
                                        , 'attrs' :
                                            [ { 'name' : 'name'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'Name'
                                              }
                                            , { 'name' : 'registered_in'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'Registered in'
                                              }
                                            ]
                                        , 'name' : 'owner'
                                        , 'sig_key' : 2
                                        , 'type_name' : 'PAP.Company'
                                        , 'ui_name' : 'Owner'
                                        , 'ui_type_name' : 'Company'
                                        }
                                      , { 'Class' : 'Entity'
                                        , 'attrs' :
                                            [ { 'name' : 'last_name'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'Last name'
                                              }
                                            , { 'name' : 'first_name'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'First name'
                                              }
                                            , { 'name' : 'middle_name'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'Middle name'
                                              }
                                            , { 'name' : 'title'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'Academic title'
                                              }
                                            ]
                                        , 'name' : 'owner'
                                        , 'sig_key' : 2
                                        , 'type_name' : 'PAP.Person'
                                        , 'ui_name' : 'Owner'
                                        , 'ui_type_name' : 'Person'
                                        }
                                      ]
                                  , 'default_child' : 'PAP.Person'
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'ui_name' : 'Owner'
                                  }
                                , { 'attrs' :
                                      [ { 'name' : 'lat'
                                        , 'sig_key' : 4
                                        , 'ui_name' : 'Latitude'
                                        }
                                      , { 'name' : 'lon'
                                        , 'sig_key' : 4
                                        , 'ui_name' : 'Longitude'
                                        }
                                      , { 'name' : 'height'
                                        , 'sig_key' : 0
                                        , 'ui_name' : 'Height'
                                        }
                                      ]
                                  , 'name' : 'position'
                                  , 'ui_name' : 'Position'
                                  }
                                , { 'name' : 'show_in_map'
                                  , 'sig_key' : 1
                                  , 'ui_name' : 'Show in map'
                                  }
                                ]
                            , 'name' : 'node'
                            , 'sig_key' : 2
                            , 'ui_name' : 'Node'
                            }
                          , { 'name' : 'name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Name'
                            }
                          , { 'name' : 'desc'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Description'
                            }
                          , { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Name'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'last_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Last name'
                                        }
                                      , { 'name' : 'first_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'First name'
                                        }
                                      , { 'name' : 'middle_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Middle name'
                                        }
                                      , { 'name' : 'title'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Academic title'
                                        }
                                      , { 'attrs' :
                                            [ { 'name' : 'start'
                                              , 'sig_key' : 0
                                              , 'ui_name' : 'Start'
                                              }
                                            , { 'name' : 'finish'
                                              , 'sig_key' : 0
                                              , 'ui_name' : 'Finish'
                                              }
                                            , { 'name' : 'alive'
                                              , 'sig_key' : 1
                                              , 'ui_name' : 'Alive'
                                              }
                                            ]
                                        , 'name' : 'lifetime'
                                        , 'ui_name' : 'Lifetime'
                                        }
                                      , { 'name' : 'sex'
                                        , 'sig_key' : 0
                                        , 'ui_name' : 'Sex'
                                        }
                                      ]
                                  , 'name' : 'manager'
                                  , 'sig_key' : 2
                                  , 'ui_name' : 'Manager'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'street'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Street'
                                        }
                                      , { 'name' : 'zip'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Zip code'
                                        }
                                      , { 'name' : 'city'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'City'
                                        }
                                      , { 'name' : 'country'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Country'
                                        }
                                      , { 'name' : 'desc'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Description'
                                        }
                                      , { 'name' : 'region'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Region'
                                        }
                                      ]
                                  , 'name' : 'address'
                                  , 'sig_key' : 2
                                  , 'ui_name' : 'Address'
                                  }
                                , { 'name' : 'desc'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Description'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'children_np' :
                                      [ { 'Class' : 'Entity'
                                        , 'attrs' :
                                            [ { 'name' : 'name'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'Name'
                                              }
                                            ]
                                        , 'name' : 'owner'
                                        , 'sig_key' : 2
                                        , 'type_name' : 'PAP.Adhoc_Group'
                                        , 'ui_name' : 'Owner'
                                        , 'ui_type_name' : 'Adhoc_Group'
                                        }
                                      , { 'Class' : 'Entity'
                                        , 'attrs' :
                                            [ { 'name' : 'name'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'Name'
                                              }
                                            ]
                                        , 'name' : 'owner'
                                        , 'sig_key' : 2
                                        , 'type_name' : 'PAP.Association'
                                        , 'ui_name' : 'Owner'
                                        , 'ui_type_name' : 'Association'
                                        }
                                      , { 'Class' : 'Entity'
                                        , 'attrs' :
                                            [ { 'name' : 'name'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'Name'
                                              }
                                            , { 'name' : 'registered_in'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'Registered in'
                                              }
                                            ]
                                        , 'name' : 'owner'
                                        , 'sig_key' : 2
                                        , 'type_name' : 'PAP.Company'
                                        , 'ui_name' : 'Owner'
                                        , 'ui_type_name' : 'Company'
                                        }
                                      , { 'Class' : 'Entity'
                                        , 'attrs' :
                                            [ { 'name' : 'last_name'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'Last name'
                                              }
                                            , { 'name' : 'first_name'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'First name'
                                              }
                                            , { 'name' : 'middle_name'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'Middle name'
                                              }
                                            , { 'name' : 'title'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'Academic title'
                                              }
                                            ]
                                        , 'name' : 'owner'
                                        , 'sig_key' : 2
                                        , 'type_name' : 'PAP.Person'
                                        , 'ui_name' : 'Owner'
                                        , 'ui_type_name' : 'Person'
                                        }
                                      ]
                                  , 'default_child' : 'PAP.Person'
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'ui_name' : 'Owner'
                                  }
                                , { 'attrs' :
                                      [ { 'name' : 'lat'
                                        , 'sig_key' : 4
                                        , 'ui_name' : 'Latitude'
                                        }
                                      , { 'name' : 'lon'
                                        , 'sig_key' : 4
                                        , 'ui_name' : 'Longitude'
                                        }
                                      , { 'name' : 'height'
                                        , 'sig_key' : 0
                                        , 'ui_name' : 'Height'
                                        }
                                      ]
                                  , 'name' : 'position'
                                  , 'ui_name' : 'Position'
                                  }
                                , { 'name' : 'show_in_map'
                                  , 'sig_key' : 1
                                  , 'ui_name' : 'Show in map'
                                  }
                                ]
                            , 'name' : 'my_node'
                            , 'sig_key' : 2
                            , 'ui_name' : 'My node'
                            }
                          ]
                      , 'name' : 'left'
                      , 'sig_key' : 2
                      , 'ui_name' : 'Net device'
                      }
                    , { 'name' : 'mac_address'
                      , 'sig_key' : 3
                      , 'ui_name' : 'Mac address'
                      }
                    , { 'name' : 'name'
                      , 'sig_key' : 3
                      , 'ui_name' : 'Name'
                      }
                    , { 'name' : 'is_active'
                      , 'sig_key' : 1
                      , 'ui_name' : 'Is active'
                      }
                    , { 'name' : 'desc'
                      , 'sig_key' : 3
                      , 'ui_name' : 'Description'
                      }
                    , { 'name' : 'mode'
                      , 'sig_key' : 0
                      , 'ui_name' : 'Mode'
                      }
                    , { 'name' : 'essid'
                      , 'sig_key' : 3
                      , 'ui_name' : 'ESSID'
                      }
                    , { 'name' : 'bssid'
                      , 'sig_key' : 3
                      , 'ui_name' : 'BSSID'
                      }
                    , { 'Class' : 'Entity'
                      , 'attrs' :
                          [ { 'name' : 'name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Name'
                            }
                          , { 'name' : 'bandwidth'
                            , 'sig_key' : 4
                            , 'ui_name' : 'Bandwidth'
                            }
                          ]
                      , 'name' : 'standard'
                      , 'sig_key' : 2
                      , 'ui_name' : 'Standard'
                      }
                    , { 'name' : 'txpower'
                      , 'sig_key' : 4
                      , 'ui_name' : 'TX power'
                      }
                    , { 'Class' : 'Entity'
                      , 'attrs' :
                          [ { 'name' : 'name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Name'
                            }
                          , { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'last_name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Last name'
                                  }
                                , { 'name' : 'first_name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'First name'
                                  }
                                , { 'name' : 'middle_name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Middle name'
                                  }
                                , { 'name' : 'title'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Academic title'
                                  }
                                , { 'attrs' :
                                      [ { 'name' : 'start'
                                        , 'sig_key' : 0
                                        , 'ui_name' : 'Start'
                                        }
                                      , { 'name' : 'finish'
                                        , 'sig_key' : 0
                                        , 'ui_name' : 'Finish'
                                        }
                                      , { 'name' : 'alive'
                                        , 'sig_key' : 1
                                        , 'ui_name' : 'Alive'
                                        }
                                      ]
                                  , 'name' : 'lifetime'
                                  , 'ui_name' : 'Lifetime'
                                  }
                                , { 'name' : 'sex'
                                  , 'sig_key' : 0
                                  , 'ui_name' : 'Sex'
                                  }
                                ]
                            , 'name' : 'manager'
                            , 'sig_key' : 2
                            , 'ui_name' : 'Manager'
                            }
                          , { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'street'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Street'
                                  }
                                , { 'name' : 'zip'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Zip code'
                                  }
                                , { 'name' : 'city'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'City'
                                  }
                                , { 'name' : 'country'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Country'
                                  }
                                , { 'name' : 'desc'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Description'
                                  }
                                , { 'name' : 'region'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Region'
                                  }
                                ]
                            , 'name' : 'address'
                            , 'sig_key' : 2
                            , 'ui_name' : 'Address'
                            }
                          , { 'name' : 'desc'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Description'
                            }
                          , { 'Class' : 'Entity'
                            , 'children_np' :
                                [ { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Adhoc_Group'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Adhoc_Group'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Association'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Association'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      , { 'name' : 'registered_in'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Registered in'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Company'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Company'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'last_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Last name'
                                        }
                                      , { 'name' : 'first_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'First name'
                                        }
                                      , { 'name' : 'middle_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Middle name'
                                        }
                                      , { 'name' : 'title'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Academic title'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Person'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Person'
                                  }
                                ]
                            , 'default_child' : 'PAP.Person'
                            , 'name' : 'owner'
                            , 'sig_key' : 2
                            , 'ui_name' : 'Owner'
                            }
                          , { 'attrs' :
                                [ { 'name' : 'lat'
                                  , 'sig_key' : 4
                                  , 'ui_name' : 'Latitude'
                                  }
                                , { 'name' : 'lon'
                                  , 'sig_key' : 4
                                  , 'ui_name' : 'Longitude'
                                  }
                                , { 'name' : 'height'
                                  , 'sig_key' : 0
                                  , 'ui_name' : 'Height'
                                  }
                                ]
                            , 'name' : 'position'
                            , 'ui_name' : 'Position'
                            }
                          , { 'name' : 'show_in_map'
                            , 'sig_key' : 1
                            , 'ui_name' : 'Show in map'
                            }
                          ]
                      , 'name' : 'my_node'
                      , 'sig_key' : 2
                      , 'ui_name' : 'My node'
                      }
                    , { 'Class' : 'Entity'
                      , 'attrs' :
                          [ { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Name'
                                  }
                                , { 'name' : 'model_no'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Model no'
                                  }
                                , { 'name' : 'revision'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Revision'
                                  }
                                , { 'name' : 'desc'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Description'
                                  }
                                ]
                            , 'name' : 'left'
                            , 'sig_key' : 2
                            , 'ui_name' : 'Net device type'
                            }
                          , { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Name'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'last_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Last name'
                                        }
                                      , { 'name' : 'first_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'First name'
                                        }
                                      , { 'name' : 'middle_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Middle name'
                                        }
                                      , { 'name' : 'title'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Academic title'
                                        }
                                      , { 'attrs' :
                                            [ { 'name' : 'start'
                                              , 'sig_key' : 0
                                              , 'ui_name' : 'Start'
                                              }
                                            , { 'name' : 'finish'
                                              , 'sig_key' : 0
                                              , 'ui_name' : 'Finish'
                                              }
                                            , { 'name' : 'alive'
                                              , 'sig_key' : 1
                                              , 'ui_name' : 'Alive'
                                              }
                                            ]
                                        , 'name' : 'lifetime'
                                        , 'ui_name' : 'Lifetime'
                                        }
                                      , { 'name' : 'sex'
                                        , 'sig_key' : 0
                                        , 'ui_name' : 'Sex'
                                        }
                                      ]
                                  , 'name' : 'manager'
                                  , 'sig_key' : 2
                                  , 'ui_name' : 'Manager'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'street'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Street'
                                        }
                                      , { 'name' : 'zip'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Zip code'
                                        }
                                      , { 'name' : 'city'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'City'
                                        }
                                      , { 'name' : 'country'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Country'
                                        }
                                      , { 'name' : 'desc'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Description'
                                        }
                                      , { 'name' : 'region'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Region'
                                        }
                                      ]
                                  , 'name' : 'address'
                                  , 'sig_key' : 2
                                  , 'ui_name' : 'Address'
                                  }
                                , { 'name' : 'desc'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Description'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'children_np' :
                                      [ { 'Class' : 'Entity'
                                        , 'attrs' :
                                            [ { 'name' : 'name'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'Name'
                                              }
                                            ]
                                        , 'name' : 'owner'
                                        , 'sig_key' : 2
                                        , 'type_name' : 'PAP.Adhoc_Group'
                                        , 'ui_name' : 'Owner'
                                        , 'ui_type_name' : 'Adhoc_Group'
                                        }
                                      , { 'Class' : 'Entity'
                                        , 'attrs' :
                                            [ { 'name' : 'name'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'Name'
                                              }
                                            ]
                                        , 'name' : 'owner'
                                        , 'sig_key' : 2
                                        , 'type_name' : 'PAP.Association'
                                        , 'ui_name' : 'Owner'
                                        , 'ui_type_name' : 'Association'
                                        }
                                      , { 'Class' : 'Entity'
                                        , 'attrs' :
                                            [ { 'name' : 'name'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'Name'
                                              }
                                            , { 'name' : 'registered_in'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'Registered in'
                                              }
                                            ]
                                        , 'name' : 'owner'
                                        , 'sig_key' : 2
                                        , 'type_name' : 'PAP.Company'
                                        , 'ui_name' : 'Owner'
                                        , 'ui_type_name' : 'Company'
                                        }
                                      , { 'Class' : 'Entity'
                                        , 'attrs' :
                                            [ { 'name' : 'last_name'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'Last name'
                                              }
                                            , { 'name' : 'first_name'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'First name'
                                              }
                                            , { 'name' : 'middle_name'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'Middle name'
                                              }
                                            , { 'name' : 'title'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'Academic title'
                                              }
                                            ]
                                        , 'name' : 'owner'
                                        , 'sig_key' : 2
                                        , 'type_name' : 'PAP.Person'
                                        , 'ui_name' : 'Owner'
                                        , 'ui_type_name' : 'Person'
                                        }
                                      ]
                                  , 'default_child' : 'PAP.Person'
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'ui_name' : 'Owner'
                                  }
                                , { 'attrs' :
                                      [ { 'name' : 'lat'
                                        , 'sig_key' : 4
                                        , 'ui_name' : 'Latitude'
                                        }
                                      , { 'name' : 'lon'
                                        , 'sig_key' : 4
                                        , 'ui_name' : 'Longitude'
                                        }
                                      , { 'name' : 'height'
                                        , 'sig_key' : 0
                                        , 'ui_name' : 'Height'
                                        }
                                      ]
                                  , 'name' : 'position'
                                  , 'ui_name' : 'Position'
                                  }
                                , { 'name' : 'show_in_map'
                                  , 'sig_key' : 1
                                  , 'ui_name' : 'Show in map'
                                  }
                                ]
                            , 'name' : 'node'
                            , 'sig_key' : 2
                            , 'ui_name' : 'Node'
                            }
                          , { 'name' : 'name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Name'
                            }
                          , { 'name' : 'desc'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Description'
                            }
                          , { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Name'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'last_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Last name'
                                        }
                                      , { 'name' : 'first_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'First name'
                                        }
                                      , { 'name' : 'middle_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Middle name'
                                        }
                                      , { 'name' : 'title'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Academic title'
                                        }
                                      , { 'attrs' :
                                            [ { 'name' : 'start'
                                              , 'sig_key' : 0
                                              , 'ui_name' : 'Start'
                                              }
                                            , { 'name' : 'finish'
                                              , 'sig_key' : 0
                                              , 'ui_name' : 'Finish'
                                              }
                                            , { 'name' : 'alive'
                                              , 'sig_key' : 1
                                              , 'ui_name' : 'Alive'
                                              }
                                            ]
                                        , 'name' : 'lifetime'
                                        , 'ui_name' : 'Lifetime'
                                        }
                                      , { 'name' : 'sex'
                                        , 'sig_key' : 0
                                        , 'ui_name' : 'Sex'
                                        }
                                      ]
                                  , 'name' : 'manager'
                                  , 'sig_key' : 2
                                  , 'ui_name' : 'Manager'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'street'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Street'
                                        }
                                      , { 'name' : 'zip'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Zip code'
                                        }
                                      , { 'name' : 'city'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'City'
                                        }
                                      , { 'name' : 'country'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Country'
                                        }
                                      , { 'name' : 'desc'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Description'
                                        }
                                      , { 'name' : 'region'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Region'
                                        }
                                      ]
                                  , 'name' : 'address'
                                  , 'sig_key' : 2
                                  , 'ui_name' : 'Address'
                                  }
                                , { 'name' : 'desc'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Description'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'children_np' :
                                      [ { 'Class' : 'Entity'
                                        , 'attrs' :
                                            [ { 'name' : 'name'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'Name'
                                              }
                                            ]
                                        , 'name' : 'owner'
                                        , 'sig_key' : 2
                                        , 'type_name' : 'PAP.Adhoc_Group'
                                        , 'ui_name' : 'Owner'
                                        , 'ui_type_name' : 'Adhoc_Group'
                                        }
                                      , { 'Class' : 'Entity'
                                        , 'attrs' :
                                            [ { 'name' : 'name'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'Name'
                                              }
                                            ]
                                        , 'name' : 'owner'
                                        , 'sig_key' : 2
                                        , 'type_name' : 'PAP.Association'
                                        , 'ui_name' : 'Owner'
                                        , 'ui_type_name' : 'Association'
                                        }
                                      , { 'Class' : 'Entity'
                                        , 'attrs' :
                                            [ { 'name' : 'name'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'Name'
                                              }
                                            , { 'name' : 'registered_in'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'Registered in'
                                              }
                                            ]
                                        , 'name' : 'owner'
                                        , 'sig_key' : 2
                                        , 'type_name' : 'PAP.Company'
                                        , 'ui_name' : 'Owner'
                                        , 'ui_type_name' : 'Company'
                                        }
                                      , { 'Class' : 'Entity'
                                        , 'attrs' :
                                            [ { 'name' : 'last_name'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'Last name'
                                              }
                                            , { 'name' : 'first_name'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'First name'
                                              }
                                            , { 'name' : 'middle_name'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'Middle name'
                                              }
                                            , { 'name' : 'title'
                                              , 'sig_key' : 3
                                              , 'ui_name' : 'Academic title'
                                              }
                                            ]
                                        , 'name' : 'owner'
                                        , 'sig_key' : 2
                                        , 'type_name' : 'PAP.Person'
                                        , 'ui_name' : 'Owner'
                                        , 'ui_type_name' : 'Person'
                                        }
                                      ]
                                  , 'default_child' : 'PAP.Person'
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'ui_name' : 'Owner'
                                  }
                                , { 'attrs' :
                                      [ { 'name' : 'lat'
                                        , 'sig_key' : 4
                                        , 'ui_name' : 'Latitude'
                                        }
                                      , { 'name' : 'lon'
                                        , 'sig_key' : 4
                                        , 'ui_name' : 'Longitude'
                                        }
                                      , { 'name' : 'height'
                                        , 'sig_key' : 0
                                        , 'ui_name' : 'Height'
                                        }
                                      ]
                                  , 'name' : 'position'
                                  , 'ui_name' : 'Position'
                                  }
                                , { 'name' : 'show_in_map'
                                  , 'sig_key' : 1
                                  , 'ui_name' : 'Show in map'
                                  }
                                ]
                            , 'name' : 'my_node'
                            , 'sig_key' : 2
                            , 'ui_name' : 'My node'
                            }
                          ]
                      , 'name' : 'my_net_device'
                      , 'sig_key' : 2
                      , 'ui_name' : 'My net device'
                      }
                    ]
                , 'name' : 'hardware'
                , 'sig_key' : 2
                , 'ui_name' : 'Hardware'
                }
              , { 'name' : 'mac_address'
                , 'sig_key' : 3
                , 'ui_name' : 'Mac address'
                }
              , { 'name' : 'name'
                , 'sig_key' : 3
                , 'ui_name' : 'Name'
                }
              , { 'name' : 'is_active'
                , 'sig_key' : 1
                , 'ui_name' : 'Is active'
                }
              , { 'name' : 'desc'
                , 'sig_key' : 3
                , 'ui_name' : 'Description'
                }
              , { 'name' : 'mode'
                , 'sig_key' : 0
                , 'ui_name' : 'Mode'
                }
              , { 'name' : 'essid'
                , 'sig_key' : 3
                , 'ui_name' : 'ESSID'
                }
              , { 'name' : 'bssid'
                , 'sig_key' : 3
                , 'ui_name' : 'BSSID'
                }
              , { 'Class' : 'Entity'
                , 'attrs' :
                    [ { 'name' : 'name'
                      , 'sig_key' : 3
                      , 'ui_name' : 'Name'
                      }
                    , { 'Class' : 'Entity'
                      , 'attrs' :
                          [ { 'name' : 'last_name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Last name'
                            }
                          , { 'name' : 'first_name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'First name'
                            }
                          , { 'name' : 'middle_name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Middle name'
                            }
                          , { 'name' : 'title'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Academic title'
                            }
                          , { 'attrs' :
                                [ { 'name' : 'start'
                                  , 'sig_key' : 0
                                  , 'ui_name' : 'Start'
                                  }
                                , { 'name' : 'finish'
                                  , 'sig_key' : 0
                                  , 'ui_name' : 'Finish'
                                  }
                                , { 'name' : 'alive'
                                  , 'sig_key' : 1
                                  , 'ui_name' : 'Alive'
                                  }
                                ]
                            , 'name' : 'lifetime'
                            , 'ui_name' : 'Lifetime'
                            }
                          , { 'name' : 'sex'
                            , 'sig_key' : 0
                            , 'ui_name' : 'Sex'
                            }
                          ]
                      , 'name' : 'manager'
                      , 'sig_key' : 2
                      , 'ui_name' : 'Manager'
                      }
                    , { 'Class' : 'Entity'
                      , 'attrs' :
                          [ { 'name' : 'street'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Street'
                            }
                          , { 'name' : 'zip'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Zip code'
                            }
                          , { 'name' : 'city'
                            , 'sig_key' : 3
                            , 'ui_name' : 'City'
                            }
                          , { 'name' : 'country'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Country'
                            }
                          , { 'name' : 'desc'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Description'
                            }
                          , { 'name' : 'region'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Region'
                            }
                          ]
                      , 'name' : 'address'
                      , 'sig_key' : 2
                      , 'ui_name' : 'Address'
                      }
                    , { 'name' : 'desc'
                      , 'sig_key' : 3
                      , 'ui_name' : 'Description'
                      }
                    , { 'Class' : 'Entity'
                      , 'children_np' :
                          [ { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Name'
                                  }
                                ]
                            , 'name' : 'owner'
                            , 'sig_key' : 2
                            , 'type_name' : 'PAP.Adhoc_Group'
                            , 'ui_name' : 'Owner'
                            , 'ui_type_name' : 'Adhoc_Group'
                            }
                          , { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Name'
                                  }
                                ]
                            , 'name' : 'owner'
                            , 'sig_key' : 2
                            , 'type_name' : 'PAP.Association'
                            , 'ui_name' : 'Owner'
                            , 'ui_type_name' : 'Association'
                            }
                          , { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Name'
                                  }
                                , { 'name' : 'registered_in'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Registered in'
                                  }
                                ]
                            , 'name' : 'owner'
                            , 'sig_key' : 2
                            , 'type_name' : 'PAP.Company'
                            , 'ui_name' : 'Owner'
                            , 'ui_type_name' : 'Company'
                            }
                          , { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'last_name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Last name'
                                  }
                                , { 'name' : 'first_name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'First name'
                                  }
                                , { 'name' : 'middle_name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Middle name'
                                  }
                                , { 'name' : 'title'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Academic title'
                                  }
                                ]
                            , 'name' : 'owner'
                            , 'sig_key' : 2
                            , 'type_name' : 'PAP.Person'
                            , 'ui_name' : 'Owner'
                            , 'ui_type_name' : 'Person'
                            }
                          ]
                      , 'default_child' : 'PAP.Person'
                      , 'name' : 'owner'
                      , 'sig_key' : 2
                      , 'ui_name' : 'Owner'
                      }
                    , { 'attrs' :
                          [ { 'name' : 'lat'
                            , 'sig_key' : 4
                            , 'ui_name' : 'Latitude'
                            }
                          , { 'name' : 'lon'
                            , 'sig_key' : 4
                            , 'ui_name' : 'Longitude'
                            }
                          , { 'name' : 'height'
                            , 'sig_key' : 0
                            , 'ui_name' : 'Height'
                            }
                          ]
                      , 'name' : 'position'
                      , 'ui_name' : 'Position'
                      }
                    , { 'name' : 'show_in_map'
                      , 'sig_key' : 1
                      , 'ui_name' : 'Show in map'
                      }
                    ]
                , 'name' : 'my_node'
                , 'sig_key' : 2
                , 'ui_name' : 'My node'
                }
              , { 'Class' : 'Entity'
                , 'attrs' :
                    [ { 'Class' : 'Entity'
                      , 'attrs' :
                          [ { 'name' : 'name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Name'
                            }
                          , { 'name' : 'model_no'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Model no'
                            }
                          , { 'name' : 'revision'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Revision'
                            }
                          , { 'name' : 'desc'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Description'
                            }
                          ]
                      , 'name' : 'left'
                      , 'sig_key' : 2
                      , 'ui_name' : 'Net device type'
                      }
                    , { 'Class' : 'Entity'
                      , 'attrs' :
                          [ { 'name' : 'name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Name'
                            }
                          , { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'last_name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Last name'
                                  }
                                , { 'name' : 'first_name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'First name'
                                  }
                                , { 'name' : 'middle_name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Middle name'
                                  }
                                , { 'name' : 'title'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Academic title'
                                  }
                                , { 'attrs' :
                                      [ { 'name' : 'start'
                                        , 'sig_key' : 0
                                        , 'ui_name' : 'Start'
                                        }
                                      , { 'name' : 'finish'
                                        , 'sig_key' : 0
                                        , 'ui_name' : 'Finish'
                                        }
                                      , { 'name' : 'alive'
                                        , 'sig_key' : 1
                                        , 'ui_name' : 'Alive'
                                        }
                                      ]
                                  , 'name' : 'lifetime'
                                  , 'ui_name' : 'Lifetime'
                                  }
                                , { 'name' : 'sex'
                                  , 'sig_key' : 0
                                  , 'ui_name' : 'Sex'
                                  }
                                ]
                            , 'name' : 'manager'
                            , 'sig_key' : 2
                            , 'ui_name' : 'Manager'
                            }
                          , { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'street'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Street'
                                  }
                                , { 'name' : 'zip'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Zip code'
                                  }
                                , { 'name' : 'city'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'City'
                                  }
                                , { 'name' : 'country'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Country'
                                  }
                                , { 'name' : 'desc'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Description'
                                  }
                                , { 'name' : 'region'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Region'
                                  }
                                ]
                            , 'name' : 'address'
                            , 'sig_key' : 2
                            , 'ui_name' : 'Address'
                            }
                          , { 'name' : 'desc'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Description'
                            }
                          , { 'Class' : 'Entity'
                            , 'children_np' :
                                [ { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Adhoc_Group'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Adhoc_Group'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Association'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Association'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      , { 'name' : 'registered_in'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Registered in'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Company'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Company'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'last_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Last name'
                                        }
                                      , { 'name' : 'first_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'First name'
                                        }
                                      , { 'name' : 'middle_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Middle name'
                                        }
                                      , { 'name' : 'title'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Academic title'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Person'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Person'
                                  }
                                ]
                            , 'default_child' : 'PAP.Person'
                            , 'name' : 'owner'
                            , 'sig_key' : 2
                            , 'ui_name' : 'Owner'
                            }
                          , { 'attrs' :
                                [ { 'name' : 'lat'
                                  , 'sig_key' : 4
                                  , 'ui_name' : 'Latitude'
                                  }
                                , { 'name' : 'lon'
                                  , 'sig_key' : 4
                                  , 'ui_name' : 'Longitude'
                                  }
                                , { 'name' : 'height'
                                  , 'sig_key' : 0
                                  , 'ui_name' : 'Height'
                                  }
                                ]
                            , 'name' : 'position'
                            , 'ui_name' : 'Position'
                            }
                          , { 'name' : 'show_in_map'
                            , 'sig_key' : 1
                            , 'ui_name' : 'Show in map'
                            }
                          ]
                      , 'name' : 'node'
                      , 'sig_key' : 2
                      , 'ui_name' : 'Node'
                      }
                    , { 'name' : 'name'
                      , 'sig_key' : 3
                      , 'ui_name' : 'Name'
                      }
                    , { 'name' : 'desc'
                      , 'sig_key' : 3
                      , 'ui_name' : 'Description'
                      }
                    , { 'Class' : 'Entity'
                      , 'attrs' :
                          [ { 'name' : 'name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Name'
                            }
                          , { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'last_name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Last name'
                                  }
                                , { 'name' : 'first_name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'First name'
                                  }
                                , { 'name' : 'middle_name'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Middle name'
                                  }
                                , { 'name' : 'title'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Academic title'
                                  }
                                , { 'attrs' :
                                      [ { 'name' : 'start'
                                        , 'sig_key' : 0
                                        , 'ui_name' : 'Start'
                                        }
                                      , { 'name' : 'finish'
                                        , 'sig_key' : 0
                                        , 'ui_name' : 'Finish'
                                        }
                                      , { 'name' : 'alive'
                                        , 'sig_key' : 1
                                        , 'ui_name' : 'Alive'
                                        }
                                      ]
                                  , 'name' : 'lifetime'
                                  , 'ui_name' : 'Lifetime'
                                  }
                                , { 'name' : 'sex'
                                  , 'sig_key' : 0
                                  , 'ui_name' : 'Sex'
                                  }
                                ]
                            , 'name' : 'manager'
                            , 'sig_key' : 2
                            , 'ui_name' : 'Manager'
                            }
                          , { 'Class' : 'Entity'
                            , 'attrs' :
                                [ { 'name' : 'street'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Street'
                                  }
                                , { 'name' : 'zip'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Zip code'
                                  }
                                , { 'name' : 'city'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'City'
                                  }
                                , { 'name' : 'country'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Country'
                                  }
                                , { 'name' : 'desc'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Description'
                                  }
                                , { 'name' : 'region'
                                  , 'sig_key' : 3
                                  , 'ui_name' : 'Region'
                                  }
                                ]
                            , 'name' : 'address'
                            , 'sig_key' : 2
                            , 'ui_name' : 'Address'
                            }
                          , { 'name' : 'desc'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Description'
                            }
                          , { 'Class' : 'Entity'
                            , 'children_np' :
                                [ { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Adhoc_Group'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Adhoc_Group'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Association'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Association'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Name'
                                        }
                                      , { 'name' : 'registered_in'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Registered in'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Company'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Company'
                                  }
                                , { 'Class' : 'Entity'
                                  , 'attrs' :
                                      [ { 'name' : 'last_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Last name'
                                        }
                                      , { 'name' : 'first_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'First name'
                                        }
                                      , { 'name' : 'middle_name'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Middle name'
                                        }
                                      , { 'name' : 'title'
                                        , 'sig_key' : 3
                                        , 'ui_name' : 'Academic title'
                                        }
                                      ]
                                  , 'name' : 'owner'
                                  , 'sig_key' : 2
                                  , 'type_name' : 'PAP.Person'
                                  , 'ui_name' : 'Owner'
                                  , 'ui_type_name' : 'Person'
                                  }
                                ]
                            , 'default_child' : 'PAP.Person'
                            , 'name' : 'owner'
                            , 'sig_key' : 2
                            , 'ui_name' : 'Owner'
                            }
                          , { 'attrs' :
                                [ { 'name' : 'lat'
                                  , 'sig_key' : 4
                                  , 'ui_name' : 'Latitude'
                                  }
                                , { 'name' : 'lon'
                                  , 'sig_key' : 4
                                  , 'ui_name' : 'Longitude'
                                  }
                                , { 'name' : 'height'
                                  , 'sig_key' : 0
                                  , 'ui_name' : 'Height'
                                  }
                                ]
                            , 'name' : 'position'
                            , 'ui_name' : 'Position'
                            }
                          , { 'name' : 'show_in_map'
                            , 'sig_key' : 1
                            , 'ui_name' : 'Show in map'
                            }
                          ]
                      , 'name' : 'my_node'
                      , 'sig_key' : 2
                      , 'ui_name' : 'My node'
                      }
                    ]
                , 'name' : 'my_net_device'
                , 'sig_key' : 2
                , 'ui_name' : 'My net device'
                }
              , { 'Class' : 'Entity'
                , 'attrs' :
                    [ { 'name' : 'name'
                      , 'sig_key' : 3
                      , 'ui_name' : 'Name'
                      }
                    , { 'name' : 'bandwidth'
                      , 'sig_key' : 4
                      , 'ui_name' : 'Bandwidth'
                      }
                    ]
                , 'name' : 'standard'
                , 'sig_key' : 2
                , 'ui_name' : 'Standard'
                }
              , { 'name' : 'txpower'
                , 'sig_key' : 4
                , 'ui_name' : 'TX power'
                }
              ]
          , 'name' : 'virtual_wireless_interface'
          , 'sig_key' : 2
          , 'ui_name' : 'Virtual wireless interface'
          }
        ]
    , 'name_sep' : '__'
    , 'op_map' :
        { 'CONTAINS' :
            { 'desc' : 'Select entities where the attribute contains the specified value'
            , 'sym' : 'contains'
            }
        , 'ENDSWITH' :
            { 'desc' : 'Select entities where the attribute value ends with the specified value'
            , 'sym' : 'ends-with'
            }
        , 'EQ' :
            { 'desc' : 'Select entities where the attribute is equal to the specified value'
            , 'sym' : '=='
            }
        , 'EQS' :
            { 'desc' : 'Select entities where the attribute is equal to the specified string value'
            , 'sym' : 'EQS'
            }
        , 'GE' :
            { 'desc' : 'Select entities where the attribute is greater than, or equal to, the specified value'
            , 'sym' : '>='
            }
        , 'GT' :
            { 'desc' : 'Select entities where the attribute is greater than the specified value'
            , 'sym' : '>'
            }
        , 'IN' :
            { 'desc' : 'Select entities where the attribute is a member of the specified list of values'
            , 'sym' : 'in'
            }
        , 'LE' :
            { 'desc' : 'Select entities where the attribute is less than, or equal to, the specified value'
            , 'sym' : '<='
            }
        , 'LT' :
            { 'desc' : 'Select entities where the attribute is less than the specified value'
            , 'sym' : '<'
            }
        , 'NE' :
            { 'desc' : 'Select entities where the attribute is not equal to the specified value'
            , 'sym' : '!='
            }
        , 'NES' :
            { 'desc' : 'Select entities where the attribute is not equal to the specified string value'
            , 'sym' : 'NES'
            }
        , 'STARTSWITH' :
            { 'desc' : 'Select entities where the attribute value starts with the specified value'
            , 'sym' : 'starts-with'
            }
        }
    , 'op_sep' : '___'
    , 'sig_map' :
        { 0 :
            ( 'EQ'
            , 'GE'
            , 'GT'
            , 'IN'
            , 'LE'
            , 'LT'
            , 'NE'
            )
        , 1 :
    ( 'EQ' ,)
        , 2 :
            ( 'EQ'
            , 'IN'
            , 'NE'
            )
        , 3 :
            ( 'CONTAINS'
            , 'ENDSWITH'
            , 'EQ'
            , 'GE'
            , 'GT'
            , 'IN'
            , 'LE'
            , 'LT'
            , 'NE'
            , 'STARTSWITH'
            )
        , 4 :
            ( 'CONTAINS'
            , 'ENDSWITH'
            , 'EQ'
            , 'EQS'
            , 'GE'
            , 'GT'
            , 'IN'
            , 'LE'
            , 'LT'
            , 'NE'
            , 'NES'
            , 'STARTSWITH'
            )
        }
    , 'ui_sep' : '/'
    }

    >>> print (formatted (AQ.As_Template_Elem))
    [ Record
      ( attr = IP4-network `net_address`
      , full_name = 'net_address'
      , id = 'net_address'
      , name = 'net_address'
      , sig_key = 0
      , ui_name = 'Net address'
      )
    , Record
      ( attr = String `desc`
      , full_name = 'desc'
      , id = 'desc'
      , name = 'desc'
      , sig_key = 3
      , ui_name = 'Description'
      )
    , Record
      ( Class = 'Entity'
      , attr = Entity `owner`
      , children_np =
          [ Record
            ( Class = 'Entity'
            , attr = Entity `owner`
            , attrs =
                [ Record
                  ( attr = String `name`
                  , full_name = 'owner.name'
                  , id = 'owner__name'
                  , name = 'name'
                  , sig_key = 3
                  , ui_name = 'Owner[Adhoc_Group]/Name'
                  )
                ]
            , full_name = 'owner'
            , id = 'owner'
            , name = 'owner'
            , sig_key = 2
            , type_name = 'PAP.Adhoc_Group'
            , ui_name = 'Owner[Adhoc_Group]'
            , ui_type_name = 'Adhoc_Group'
            )
          , Record
            ( Class = 'Entity'
            , attr = Entity `owner`
            , attrs =
                [ Record
                  ( attr = String `name`
                  , full_name = 'owner.name'
                  , id = 'owner__name'
                  , name = 'name'
                  , sig_key = 3
                  , ui_name = 'Owner[Association]/Name'
                  )
                ]
            , full_name = 'owner'
            , id = 'owner'
            , name = 'owner'
            , sig_key = 2
            , type_name = 'PAP.Association'
            , ui_name = 'Owner[Association]'
            , ui_type_name = 'Association'
            )
          , Record
            ( Class = 'Entity'
            , attr = Entity `owner`
            , attrs =
                [ Record
                  ( attr = String `name`
                  , full_name = 'owner.name'
                  , id = 'owner__name'
                  , name = 'name'
                  , sig_key = 3
                  , ui_name = 'Owner[Company]/Name'
                  )
                , Record
                  ( attr = String `registered_in`
                  , full_name = 'owner.registered_in'
                  , id = 'owner__registered_in'
                  , name = 'registered_in'
                  , sig_key = 3
                  , ui_name = 'Owner[Company]/Registered in'
                  )
                ]
            , full_name = 'owner'
            , id = 'owner'
            , name = 'owner'
            , sig_key = 2
            , type_name = 'PAP.Company'
            , ui_name = 'Owner[Company]'
            , ui_type_name = 'Company'
            )
          , Record
            ( Class = 'Entity'
            , attr = Entity `owner`
            , attrs =
                [ Record
                  ( attr = String `last_name`
                  , full_name = 'owner.last_name'
                  , id = 'owner__last_name'
                  , name = 'last_name'
                  , sig_key = 3
                  , ui_name = 'Owner[Person]/Last name'
                  )
                , Record
                  ( attr = String `first_name`
                  , full_name = 'owner.first_name'
                  , id = 'owner__first_name'
                  , name = 'first_name'
                  , sig_key = 3
                  , ui_name = 'Owner[Person]/First name'
                  )
                , Record
                  ( attr = String `middle_name`
                  , full_name = 'owner.middle_name'
                  , id = 'owner__middle_name'
                  , name = 'middle_name'
                  , sig_key = 3
                  , ui_name = 'Owner[Person]/Middle name'
                  )
                , Record
                  ( attr = String `title`
                  , full_name = 'owner.title'
                  , id = 'owner__title'
                  , name = 'title'
                  , sig_key = 3
                  , ui_name = 'Owner[Person]/Academic title'
                  )
                ]
            , full_name = 'owner'
            , id = 'owner'
            , name = 'owner'
            , sig_key = 2
            , type_name = 'PAP.Person'
            , ui_name = 'Owner[Person]'
            , ui_type_name = 'Person'
            )
          ]
      , default_child = 'PAP.Person'
      , full_name = 'owner'
      , id = 'owner'
      , name = 'owner'
      , sig_key = 2
      , type_name = 'PAP.Subject'
      , ui_name = 'Owner'
      , ui_type_name = 'Subject'
      )
    , Record
      ( Class = 'Entity'
      , attr = Rev_Ref `creation`
      , attrs =
          [ Record
            ( attr = Date-Time `c_time`
            , full_name = 'creation.c_time'
            , id = 'creation__c_time'
            , name = 'c_time'
            , sig_key = 0
            , ui_name = 'Creation/C time'
            )
          , Record
            ( Class = 'Entity'
            , attr = Entity `c_user`
            , children_np =
                [ Record
                  ( Class = 'Entity'
                  , attr = Entity `c_user`
                  , attrs =
                      [ Record
                        ( attr = Email `name`
                        , full_name = 'c_user.name'
                        , id = 'c_user__name'
                        , name = 'name'
                        , sig_key = 3
                        , ui_name = 'C user[Account]/Name'
                        )
                      ]
                  , full_name = 'c_user'
                  , id = 'c_user'
                  , name = 'c_user'
                  , sig_key = 2
                  , type_name = 'Auth.Account'
                  , ui_name = 'C user[Account]'
                  , ui_type_name = 'Account'
                  )
                , Record
                  ( Class = 'Entity'
                  , attr = Entity `c_user`
                  , attrs =
                      [ Record
                        ( attr = String `last_name`
                        , full_name = 'c_user.last_name'
                        , id = 'c_user__last_name'
                        , name = 'last_name'
                        , sig_key = 3
                        , ui_name = 'C user[Person]/Last name'
                        )
                      , Record
                        ( attr = String `first_name`
                        , full_name = 'c_user.first_name'
                        , id = 'c_user__first_name'
                        , name = 'first_name'
                        , sig_key = 3
                        , ui_name = 'C user[Person]/First name'
                        )
                      , Record
                        ( attr = String `middle_name`
                        , full_name = 'c_user.middle_name'
                        , id = 'c_user__middle_name'
                        , name = 'middle_name'
                        , sig_key = 3
                        , ui_name = 'C user[Person]/Middle name'
                        )
                      , Record
                        ( attr = String `title`
                        , full_name = 'c_user.title'
                        , id = 'c_user__title'
                        , name = 'title'
                        , sig_key = 3
                        , ui_name = 'C user[Person]/Academic title'
                        )
                      ]
                  , full_name = 'c_user'
                  , id = 'c_user'
                  , name = 'c_user'
                  , sig_key = 2
                  , type_name = 'PAP.Person'
                  , ui_name = 'C user[Person]'
                  , ui_type_name = 'Person'
                  )
                ]
            , full_name = 'creation.c_user'
            , id = 'creation__c_user'
            , name = 'c_user'
            , sig_key = 2
            , type_name = 'MOM.Id_Entity'
            , ui_name = 'Creation/C user'
            , ui_type_name = 'Id_Entity'
            )
          , Record
            ( attr = String `kind`
            , full_name = 'creation.kind'
            , id = 'creation__kind'
            , name = 'kind'
            , sig_key = 3
            , ui_name = 'Creation/Kind'
            )
          , Record
            ( attr = Date-Time `time`
            , full_name = 'creation.time'
            , id = 'creation__time'
            , name = 'time'
            , sig_key = 0
            , ui_name = 'Creation/Time'
            )
          , Record
            ( Class = 'Entity'
            , attr = Entity `user`
            , children_np =
                [ Record
                  ( Class = 'Entity'
                  , attr = Entity `user`
                  , attrs =
                      [ Record
                        ( attr = Email `name`
                        , full_name = 'user.name'
                        , id = 'user__name'
                        , name = 'name'
                        , sig_key = 3
                        , ui_name = 'User[Account]/Name'
                        )
                      ]
                  , full_name = 'user'
                  , id = 'user'
                  , name = 'user'
                  , sig_key = 2
                  , type_name = 'Auth.Account'
                  , ui_name = 'User[Account]'
                  , ui_type_name = 'Account'
                  )
                , Record
                  ( Class = 'Entity'
                  , attr = Entity `user`
                  , attrs =
                      [ Record
                        ( attr = String `last_name`
                        , full_name = 'user.last_name'
                        , id = 'user__last_name'
                        , name = 'last_name'
                        , sig_key = 3
                        , ui_name = 'User[Person]/Last name'
                        )
                      , Record
                        ( attr = String `first_name`
                        , full_name = 'user.first_name'
                        , id = 'user__first_name'
                        , name = 'first_name'
                        , sig_key = 3
                        , ui_name = 'User[Person]/First name'
                        )
                      , Record
                        ( attr = String `middle_name`
                        , full_name = 'user.middle_name'
                        , id = 'user__middle_name'
                        , name = 'middle_name'
                        , sig_key = 3
                        , ui_name = 'User[Person]/Middle name'
                        )
                      , Record
                        ( attr = String `title`
                        , full_name = 'user.title'
                        , id = 'user__title'
                        , name = 'title'
                        , sig_key = 3
                        , ui_name = 'User[Person]/Academic title'
                        )
                      ]
                  , full_name = 'user'
                  , id = 'user'
                  , name = 'user'
                  , sig_key = 2
                  , type_name = 'PAP.Person'
                  , ui_name = 'User[Person]'
                  , ui_type_name = 'Person'
                  )
                ]
            , full_name = 'creation.user'
            , id = 'creation__user'
            , name = 'user'
            , sig_key = 2
            , type_name = 'MOM.Id_Entity'
            , ui_name = 'Creation/User'
            , ui_type_name = 'Id_Entity'
            )
          ]
      , full_name = 'creation'
      , id = 'creation'
      , name = 'creation'
      , sig_key = 2
      , type_name = 'MOM.MD_Change'
      , ui_name = 'Creation'
      , ui_type_name = 'MD_Change'
      )
    , Record
      ( Class = 'Entity'
      , attr = Rev_Ref `last_change`
      , attrs =
          [ Record
            ( attr = Date-Time `c_time`
            , full_name = 'last_change.c_time'
            , id = 'last_change__c_time'
            , name = 'c_time'
            , sig_key = 0
            , ui_name = 'Last change/C time'
            )
          , Record
            ( Class = 'Entity'
            , attr = Entity `c_user`
            , children_np =
                [ Record
                  ( Class = 'Entity'
                  , attr = Entity `c_user`
                  , attrs =
                      [ Record
                        ( attr = Email `name`
                        , full_name = 'c_user.name'
                        , id = 'c_user__name'
                        , name = 'name'
                        , sig_key = 3
                        , ui_name = 'C user[Account]/Name'
                        )
                      ]
                  , full_name = 'c_user'
                  , id = 'c_user'
                  , name = 'c_user'
                  , sig_key = 2
                  , type_name = 'Auth.Account'
                  , ui_name = 'C user[Account]'
                  , ui_type_name = 'Account'
                  )
                , Record
                  ( Class = 'Entity'
                  , attr = Entity `c_user`
                  , attrs =
                      [ Record
                        ( attr = String `last_name`
                        , full_name = 'c_user.last_name'
                        , id = 'c_user__last_name'
                        , name = 'last_name'
                        , sig_key = 3
                        , ui_name = 'C user[Person]/Last name'
                        )
                      , Record
                        ( attr = String `first_name`
                        , full_name = 'c_user.first_name'
                        , id = 'c_user__first_name'
                        , name = 'first_name'
                        , sig_key = 3
                        , ui_name = 'C user[Person]/First name'
                        )
                      , Record
                        ( attr = String `middle_name`
                        , full_name = 'c_user.middle_name'
                        , id = 'c_user__middle_name'
                        , name = 'middle_name'
                        , sig_key = 3
                        , ui_name = 'C user[Person]/Middle name'
                        )
                      , Record
                        ( attr = String `title`
                        , full_name = 'c_user.title'
                        , id = 'c_user__title'
                        , name = 'title'
                        , sig_key = 3
                        , ui_name = 'C user[Person]/Academic title'
                        )
                      ]
                  , full_name = 'c_user'
                  , id = 'c_user'
                  , name = 'c_user'
                  , sig_key = 2
                  , type_name = 'PAP.Person'
                  , ui_name = 'C user[Person]'
                  , ui_type_name = 'Person'
                  )
                ]
            , full_name = 'last_change.c_user'
            , id = 'last_change__c_user'
            , name = 'c_user'
            , sig_key = 2
            , type_name = 'MOM.Id_Entity'
            , ui_name = 'Last change/C user'
            , ui_type_name = 'Id_Entity'
            )
          , Record
            ( attr = String `kind`
            , full_name = 'last_change.kind'
            , id = 'last_change__kind'
            , name = 'kind'
            , sig_key = 3
            , ui_name = 'Last change/Kind'
            )
          , Record
            ( attr = Date-Time `time`
            , full_name = 'last_change.time'
            , id = 'last_change__time'
            , name = 'time'
            , sig_key = 0
            , ui_name = 'Last change/Time'
            )
          , Record
            ( Class = 'Entity'
            , attr = Entity `user`
            , children_np =
                [ Record
                  ( Class = 'Entity'
                  , attr = Entity `user`
                  , attrs =
                      [ Record
                        ( attr = Email `name`
                        , full_name = 'user.name'
                        , id = 'user__name'
                        , name = 'name'
                        , sig_key = 3
                        , ui_name = 'User[Account]/Name'
                        )
                      ]
                  , full_name = 'user'
                  , id = 'user'
                  , name = 'user'
                  , sig_key = 2
                  , type_name = 'Auth.Account'
                  , ui_name = 'User[Account]'
                  , ui_type_name = 'Account'
                  )
                , Record
                  ( Class = 'Entity'
                  , attr = Entity `user`
                  , attrs =
                      [ Record
                        ( attr = String `last_name`
                        , full_name = 'user.last_name'
                        , id = 'user__last_name'
                        , name = 'last_name'
                        , sig_key = 3
                        , ui_name = 'User[Person]/Last name'
                        )
                      , Record
                        ( attr = String `first_name`
                        , full_name = 'user.first_name'
                        , id = 'user__first_name'
                        , name = 'first_name'
                        , sig_key = 3
                        , ui_name = 'User[Person]/First name'
                        )
                      , Record
                        ( attr = String `middle_name`
                        , full_name = 'user.middle_name'
                        , id = 'user__middle_name'
                        , name = 'middle_name'
                        , sig_key = 3
                        , ui_name = 'User[Person]/Middle name'
                        )
                      , Record
                        ( attr = String `title`
                        , full_name = 'user.title'
                        , id = 'user__title'
                        , name = 'title'
                        , sig_key = 3
                        , ui_name = 'User[Person]/Academic title'
                        )
                      ]
                  , full_name = 'user'
                  , id = 'user'
                  , name = 'user'
                  , sig_key = 2
                  , type_name = 'PAP.Person'
                  , ui_name = 'User[Person]'
                  , ui_type_name = 'Person'
                  )
                ]
            , full_name = 'last_change.user'
            , id = 'last_change__user'
            , name = 'user'
            , sig_key = 2
            , type_name = 'MOM.Id_Entity'
            , ui_name = 'Last change/User'
            , ui_type_name = 'Id_Entity'
            )
          ]
      , full_name = 'last_change'
      , id = 'last_change'
      , name = 'last_change'
      , sig_key = 2
      , type_name = 'MOM.MD_Change'
      , ui_name = 'Last change'
      , ui_type_name = 'MD_Change'
      )
    , Record
      ( attr = Int `last_cid`
      , full_name = 'last_cid'
      , id = 'last_cid'
      , name = 'last_cid'
      , sig_key = 0
      , ui_name = 'Last cid'
      )
    , Record
      ( attr = Surrogate `pid`
      , full_name = 'pid'
      , id = 'pid'
      , name = 'pid'
      , sig_key = 0
      , ui_name = 'Pid'
      )
    , Record
      ( attr = String `type_name`
      , full_name = 'type_name'
      , id = 'type_name'
      , name = 'type_name'
      , sig_key = 3
      , ui_name = 'Type name'
      )
    , Record
      ( attr = Date-Time `expiration_date`
      , full_name = 'expiration_date'
      , id = 'expiration_date'
      , name = 'expiration_date'
      , sig_key = 0
      , ui_name = 'Expiration date'
      )
    , Record
      ( attr = Boolean `has_children`
      , choices =
          [ 'no'
          , 'yes'
          ]
      , full_name = 'has_children'
      , id = 'has_children'
      , name = 'has_children'
      , sig_key = 1
      , ui_name = 'Has children'
      )
    , Record
      ( attr = Boolean `is_free`
      , choices =
          [ 'no'
          , 'yes'
          ]
      , full_name = 'is_free'
      , id = 'is_free'
      , name = 'is_free'
      , sig_key = 1
      , ui_name = 'Is free'
      )
    , Record
      ( Class = 'Entity'
      , attr = Entity `parent`
      , attrs =
          [ Record
            ( attr = IP4-network `net_address`
            , full_name = 'parent.net_address'
            , id = 'parent__net_address'
            , name = 'net_address'
            , sig_key = 0
            , ui_name = 'Parent/Net address'
            )
          , Record
            ( attr = String `desc`
            , full_name = 'parent.desc'
            , id = 'parent__desc'
            , name = 'desc'
            , sig_key = 3
            , ui_name = 'Parent/Description'
            )
          , Record
            ( Class = 'Entity'
            , attr = Entity `owner`
            , children_np =
                [ Record
                  ( Class = 'Entity'
                  , attr = Entity `owner`
                  , attrs =
                      [ Record
                        ( attr = String `name`
                        , full_name = 'owner.name'
                        , id = 'owner__name'
                        , name = 'name'
                        , sig_key = 3
                        , ui_name = 'Owner[Adhoc_Group]/Name'
                        )
                      ]
                  , full_name = 'owner'
                  , id = 'owner'
                  , name = 'owner'
                  , sig_key = 2
                  , type_name = 'PAP.Adhoc_Group'
                  , ui_name = 'Owner[Adhoc_Group]'
                  , ui_type_name = 'Adhoc_Group'
                  )
                , Record
                  ( Class = 'Entity'
                  , attr = Entity `owner`
                  , attrs =
                      [ Record
                        ( attr = String `name`
                        , full_name = 'owner.name'
                        , id = 'owner__name'
                        , name = 'name'
                        , sig_key = 3
                        , ui_name = 'Owner[Association]/Name'
                        )
                      ]
                  , full_name = 'owner'
                  , id = 'owner'
                  , name = 'owner'
                  , sig_key = 2
                  , type_name = 'PAP.Association'
                  , ui_name = 'Owner[Association]'
                  , ui_type_name = 'Association'
                  )
                , Record
                  ( Class = 'Entity'
                  , attr = Entity `owner`
                  , attrs =
                      [ Record
                        ( attr = String `name`
                        , full_name = 'owner.name'
                        , id = 'owner__name'
                        , name = 'name'
                        , sig_key = 3
                        , ui_name = 'Owner[Company]/Name'
                        )
                      , Record
                        ( attr = String `registered_in`
                        , full_name = 'owner.registered_in'
                        , id = 'owner__registered_in'
                        , name = 'registered_in'
                        , sig_key = 3
                        , ui_name = 'Owner[Company]/Registered in'
                        )
                      ]
                  , full_name = 'owner'
                  , id = 'owner'
                  , name = 'owner'
                  , sig_key = 2
                  , type_name = 'PAP.Company'
                  , ui_name = 'Owner[Company]'
                  , ui_type_name = 'Company'
                  )
                , Record
                  ( Class = 'Entity'
                  , attr = Entity `owner`
                  , attrs =
                      [ Record
                        ( attr = String `last_name`
                        , full_name = 'owner.last_name'
                        , id = 'owner__last_name'
                        , name = 'last_name'
                        , sig_key = 3
                        , ui_name = 'Owner[Person]/Last name'
                        )
                      , Record
                        ( attr = String `first_name`
                        , full_name = 'owner.first_name'
                        , id = 'owner__first_name'
                        , name = 'first_name'
                        , sig_key = 3
                        , ui_name = 'Owner[Person]/First name'
                        )
                      , Record
                        ( attr = String `middle_name`
                        , full_name = 'owner.middle_name'
                        , id = 'owner__middle_name'
                        , name = 'middle_name'
                        , sig_key = 3
                        , ui_name = 'Owner[Person]/Middle name'
                        )
                      , Record
                        ( attr = String `title`
                        , full_name = 'owner.title'
                        , id = 'owner__title'
                        , name = 'title'
                        , sig_key = 3
                        , ui_name = 'Owner[Person]/Academic title'
                        )
                      ]
                  , full_name = 'owner'
                  , id = 'owner'
                  , name = 'owner'
                  , sig_key = 2
                  , type_name = 'PAP.Person'
                  , ui_name = 'Owner[Person]'
                  , ui_type_name = 'Person'
                  )
                ]
            , default_child = 'PAP.Person'
            , full_name = 'parent.owner'
            , id = 'parent__owner'
            , name = 'owner'
            , sig_key = 2
            , type_name = 'PAP.Subject'
            , ui_name = 'Parent/Owner'
            , ui_type_name = 'Subject'
            )
          , Record
            ( attr = Date-Time `expiration_date`
            , full_name = 'parent.expiration_date'
            , id = 'parent__expiration_date'
            , name = 'expiration_date'
            , sig_key = 0
            , ui_name = 'Parent/Expiration date'
            )
          , Record
            ( attr = Boolean `has_children`
            , choices = <Recursion on list...>
            , full_name = 'parent.has_children'
            , id = 'parent__has_children'
            , name = 'has_children'
            , sig_key = 1
            , ui_name = 'Parent/Has children'
            )
          , Record
            ( attr = Boolean `is_free`
            , choices = <Recursion on list...>
            , full_name = 'parent.is_free'
            , id = 'parent__is_free'
            , name = 'is_free'
            , sig_key = 1
            , ui_name = 'Parent/Is free'
            )
          , Record
            ( Class = 'Entity'
            , attr = Entity `parent`
            , full_name = 'parent.parent'
            , id = 'parent__parent'
            , name = 'parent'
            , sig_key = 2
            , type_name = 'FFM.IP4_Network'
            , ui_name = 'Parent/Parent'
            , ui_type_name = 'IP4_Network'
            )
          ]
      , full_name = 'parent'
      , id = 'parent'
      , name = 'parent'
      , sig_key = 2
      , type_name = 'FFM.IP4_Network'
      , ui_name = 'Parent'
      , ui_type_name = 'IP4_Network'
      )
    , Record
      ( Class = 'Entity'
      , attr = Link_Ref `ip_pool`
      , attrs =
          [ Record
            ( attr = Int_Interval `netmask_interval`
            , attrs =
                [ Record
                  ( attr = Int `lower`
                  , full_name = 'ip_pool.netmask_interval.lower'
                  , id = 'ip_pool__netmask_interval__lower'
                  , name = 'lower'
                  , sig_key = 0
                  , ui_name = 'Ip pool/Netmask interval/Lower'
                  )
                , Record
                  ( attr = Int `upper`
                  , full_name = 'ip_pool.netmask_interval.upper'
                  , id = 'ip_pool__netmask_interval__upper'
                  , name = 'upper'
                  , sig_key = 0
                  , ui_name = 'Ip pool/Netmask interval/Upper'
                  )
                , Record
                  ( attr = Int `center`
                  , full_name = 'ip_pool.netmask_interval.center'
                  , id = 'ip_pool__netmask_interval__center'
                  , name = 'center'
                  , sig_key = 0
                  , ui_name = 'Ip pool/Netmask interval/Center'
                  )
                , Record
                  ( attr = Int `length`
                  , full_name = 'ip_pool.netmask_interval.length'
                  , id = 'ip_pool__netmask_interval__length'
                  , name = 'length'
                  , sig_key = 0
                  , ui_name = 'Ip pool/Netmask interval/Length'
                  )
                ]
            , full_name = 'ip_pool.netmask_interval'
            , id = 'ip_pool__netmask_interval'
            , name = 'netmask_interval'
            , ui_name = 'Ip pool/Netmask interval'
            )
          , Record
            ( Class = 'Entity'
            , attr = Entity `node`
            , attrs =
                [ Record
                  ( attr = String `name`
                  , full_name = 'ip_pool.node.name'
                  , id = 'ip_pool__node__name'
                  , name = 'name'
                  , sig_key = 3
                  , ui_name = 'Ip pool/Node/Name'
                  )
                , Record
                  ( Class = 'Entity'
                  , attr = Entity `manager`
                  , attrs =
                      [ Record
                        ( attr = String `last_name`
                        , full_name = 'ip_pool.node.manager.last_name'
                        , id = 'ip_pool__node__manager__last_name'
                        , name = 'last_name'
                        , sig_key = 3
                        , ui_name = 'Ip pool/Node/Manager/Last name'
                        )
                      , Record
                        ( attr = String `first_name`
                        , full_name = 'ip_pool.node.manager.first_name'
                        , id = 'ip_pool__node__manager__first_name'
                        , name = 'first_name'
                        , sig_key = 3
                        , ui_name = 'Ip pool/Node/Manager/First name'
                        )
                      , Record
                        ( attr = String `middle_name`
                        , full_name = 'ip_pool.node.manager.middle_name'
                        , id = 'ip_pool__node__manager__middle_name'
                        , name = 'middle_name'
                        , sig_key = 3
                        , ui_name = 'Ip pool/Node/Manager/Middle name'
                        )
                      , Record
                        ( attr = String `title`
                        , full_name = 'ip_pool.node.manager.title'
                        , id = 'ip_pool__node__manager__title'
                        , name = 'title'
                        , sig_key = 3
                        , ui_name = 'Ip pool/Node/Manager/Academic title'
                        )
                      , Record
                        ( attr = Date_Interval `lifetime`
                        , attrs =
                            [ Record
                              ( attr = Date `start`
                              , full_name = 'ip_pool.node.manager.lifetime.start'
                              , id = 'ip_pool__node__manager__lifetime__start'
                              , name = 'start'
                              , sig_key = 0
                              , ui_name = 'Ip pool/Node/Manager/Lifetime/Start'
                              )
                            , Record
                              ( attr = Date `finish`
                              , full_name = 'ip_pool.node.manager.lifetime.finish'
                              , id = 'ip_pool__node__manager__lifetime__finish'
                              , name = 'finish'
                              , sig_key = 0
                              , ui_name = 'Ip pool/Node/Manager/Lifetime/Finish'
                              )
                            , Record
                              ( attr = Boolean `alive`
                              , choices =
                                  [ 'no'
                                  , 'yes'
                                  ]
                              , full_name = 'ip_pool.node.manager.lifetime.alive'
                              , id = 'ip_pool__node__manager__lifetime__alive'
                              , name = 'alive'
                              , sig_key = 1
                              , ui_name = 'Ip pool/Node/Manager/Lifetime/Alive'
                              )
                            ]
                        , full_name = 'ip_pool.node.manager.lifetime'
                        , id = 'ip_pool__node__manager__lifetime'
                        , name = 'lifetime'
                        , ui_name = 'Ip pool/Node/Manager/Lifetime'
                        )
                      , Record
                        ( attr = Sex `sex`
                        , choices =
                            [
                              ( 'F'
                              , 'Female'
                              )
                            ,
                              ( 'M'
                              , 'Male'
                              )
                            ]
                        , full_name = 'ip_pool.node.manager.sex'
                        , id = 'ip_pool__node__manager__sex'
                        , name = 'sex'
                        , sig_key = 0
                        , ui_name = 'Ip pool/Node/Manager/Sex'
                        )
                      ]
                  , full_name = 'ip_pool.node.manager'
                  , id = 'ip_pool__node__manager'
                  , name = 'manager'
                  , sig_key = 2
                  , type_name = 'PAP.Person'
                  , ui_name = 'Ip pool/Node/Manager'
                  , ui_type_name = 'Person'
                  )
                , Record
                  ( Class = 'Entity'
                  , attr = Entity `address`
                  , attrs =
                      [ Record
                        ( attr = String `street`
                        , full_name = 'ip_pool.node.address.street'
                        , id = 'ip_pool__node__address__street'
                        , name = 'street'
                        , sig_key = 3
                        , ui_name = 'Ip pool/Node/Address/Street'
                        )
                      , Record
                        ( attr = String `zip`
                        , full_name = 'ip_pool.node.address.zip'
                        , id = 'ip_pool__node__address__zip'
                        , name = 'zip'
                        , sig_key = 3
                        , ui_name = 'Ip pool/Node/Address/Zip code'
                        )
                      , Record
                        ( attr = String `city`
                        , full_name = 'ip_pool.node.address.city'
                        , id = 'ip_pool__node__address__city'
                        , name = 'city'
                        , sig_key = 3
                        , ui_name = 'Ip pool/Node/Address/City'
                        )
                      , Record
                        ( attr = String `country`
                        , full_name = 'ip_pool.node.address.country'
                        , id = 'ip_pool__node__address__country'
                        , name = 'country'
                        , sig_key = 3
                        , ui_name = 'Ip pool/Node/Address/Country'
                        )
                      , Record
                        ( attr = String `desc`
                        , full_name = 'ip_pool.node.address.desc'
                        , id = 'ip_pool__node__address__desc'
                        , name = 'desc'
                        , sig_key = 3
                        , ui_name = 'Ip pool/Node/Address/Description'
                        )
                      , Record
                        ( attr = String `region`
                        , full_name = 'ip_pool.node.address.region'
                        , id = 'ip_pool__node__address__region'
                        , name = 'region'
                        , sig_key = 3
                        , ui_name = 'Ip pool/Node/Address/Region'
                        )
                      ]
                  , full_name = 'ip_pool.node.address'
                  , id = 'ip_pool__node__address'
                  , name = 'address'
                  , sig_key = 2
                  , type_name = 'PAP.Address'
                  , ui_name = 'Ip pool/Node/Address'
                  , ui_type_name = 'Address'
                  )
                , Record
                  ( attr = Text `desc`
                  , full_name = 'ip_pool.node.desc'
                  , id = 'ip_pool__node__desc'
                  , name = 'desc'
                  , sig_key = 3
                  , ui_name = 'Ip pool/Node/Description'
                  )
                , Record
                  ( Class = 'Entity'
                  , attr = Entity `owner`
                  , children_np =
                      [ Record
                        ( Class = 'Entity'
                        , attr = Entity `owner`
                        , attrs =
                            [ Record
                              ( attr = String `name`
                              , full_name = 'owner.name'
                              , id = 'owner__name'
                              , name = 'name'
                              , sig_key = 3
                              , ui_name = 'Owner[Adhoc_Group]/Name'
                              )
                            ]
                        , full_name = 'owner'
                        , id = 'owner'
                        , name = 'owner'
                        , sig_key = 2
                        , type_name = 'PAP.Adhoc_Group'
                        , ui_name = 'Owner[Adhoc_Group]'
                        , ui_type_name = 'Adhoc_Group'
                        )
                      , Record
                        ( Class = 'Entity'
                        , attr = Entity `owner`
                        , attrs =
                            [ Record
                              ( attr = String `name`
                              , full_name = 'owner.name'
                              , id = 'owner__name'
                              , name = 'name'
                              , sig_key = 3
                              , ui_name = 'Owner[Association]/Name'
                              )
                            ]
                        , full_name = 'owner'
                        , id = 'owner'
                        , name = 'owner'
                        , sig_key = 2
                        , type_name = 'PAP.Association'
                        , ui_name = 'Owner[Association]'
                        , ui_type_name = 'Association'
                        )
                      , Record
                        ( Class = 'Entity'
                        , attr = Entity `owner`
                        , attrs =
                            [ Record
                              ( attr = String `name`
                              , full_name = 'owner.name'
                              , id = 'owner__name'
                              , name = 'name'
                              , sig_key = 3
                              , ui_name = 'Owner[Company]/Name'
                              )
                            , Record
                              ( attr = String `registered_in`
                              , full_name = 'owner.registered_in'
                              , id = 'owner__registered_in'
                              , name = 'registered_in'
                              , sig_key = 3
                              , ui_name = 'Owner[Company]/Registered in'
                              )
                            ]
                        , full_name = 'owner'
                        , id = 'owner'
                        , name = 'owner'
                        , sig_key = 2
                        , type_name = 'PAP.Company'
                        , ui_name = 'Owner[Company]'
                        , ui_type_name = 'Company'
                        )
                      , Record
                        ( Class = 'Entity'
                        , attr = Entity `owner`
                        , attrs =
                            [ Record
                              ( attr = String `last_name`
                              , full_name = 'owner.last_name'
                              , id = 'owner__last_name'
                              , name = 'last_name'
                              , sig_key = 3
                              , ui_name = 'Owner[Person]/Last name'
                              )
                            , Record
                              ( attr = String `first_name`
                              , full_name = 'owner.first_name'
                              , id = 'owner__first_name'
                              , name = 'first_name'
                              , sig_key = 3
                              , ui_name = 'Owner[Person]/First name'
                              )
                            , Record
                              ( attr = String `middle_name`
                              , full_name = 'owner.middle_name'
                              , id = 'owner__middle_name'
                              , name = 'middle_name'
                              , sig_key = 3
                              , ui_name = 'Owner[Person]/Middle name'
                              )
                            , Record
                              ( attr = String `title`
                              , full_name = 'owner.title'
                              , id = 'owner__title'
                              , name = 'title'
                              , sig_key = 3
                              , ui_name = 'Owner[Person]/Academic title'
                              )
                            ]
                        , full_name = 'owner'
                        , id = 'owner'
                        , name = 'owner'
                        , sig_key = 2
                        , type_name = 'PAP.Person'
                        , ui_name = 'Owner[Person]'
                        , ui_type_name = 'Person'
                        )
                      ]
                  , default_child = 'PAP.Person'
                  , full_name = 'ip_pool.node.owner'
                  , id = 'ip_pool__node__owner'
                  , name = 'owner'
                  , sig_key = 2
                  , type_name = 'PAP.Subject'
                  , ui_name = 'Ip pool/Node/Owner'
                  , ui_type_name = 'Subject'
                  )
                , Record
                  ( attr = Position `position`
                  , attrs =
                      [ Record
                        ( attr = Angle `lat`
                        , full_name = 'ip_pool.node.position.lat'
                        , id = 'ip_pool__node__position__lat'
                        , name = 'lat'
                        , sig_key = 4
                        , ui_name = 'Ip pool/Node/Position/Latitude'
                        )
                      , Record
                        ( attr = Angle `lon`
                        , full_name = 'ip_pool.node.position.lon'
                        , id = 'ip_pool__node__position__lon'
                        , name = 'lon'
                        , sig_key = 4
                        , ui_name = 'Ip pool/Node/Position/Longitude'
                        )
                      , Record
                        ( attr = Float `height`
                        , full_name = 'ip_pool.node.position.height'
                        , id = 'ip_pool__node__position__height'
                        , name = 'height'
                        , sig_key = 0
                        , ui_name = 'Ip pool/Node/Position/Height'
                        )
                      ]
                  , full_name = 'ip_pool.node.position'
                  , id = 'ip_pool__node__position'
                  , name = 'position'
                  , ui_name = 'Ip pool/Node/Position'
                  )
                , Record
                  ( attr = Boolean `show_in_map`
                  , choices =
                      [ 'no'
                      , 'yes'
                      ]
                  , full_name = 'ip_pool.node.show_in_map'
                  , id = 'ip_pool__node__show_in_map'
                  , name = 'show_in_map'
                  , sig_key = 1
                  , ui_name = 'Ip pool/Node/Show in map'
                  )
                ]
            , full_name = 'ip_pool.node'
            , id = 'ip_pool__node'
            , name = 'node'
            , sig_key = 2
            , type_name = 'FFM.Node'
            , ui_name = 'Ip pool/Node'
            , ui_type_name = 'Node'
            )
          ]
      , full_name = 'ip_pool'
      , id = 'ip_pool'
      , name = 'ip_pool'
      , sig_key = 2
      , type_name = 'FFM.IP_Pool'
      , ui_name = 'Ip pool'
      , ui_type_name = 'IP_Pool'
      )
    , Record
      ( Class = 'Entity'
      , attr = Role_Ref `net_interface`
      , full_name = 'net_interface'
      , id = 'net_interface'
      , name = 'net_interface'
      , sig_key = 2
      , type_name = 'FFM.Net_Interface'
      , ui_name = 'Net interface'
      , ui_type_name = 'Net_Interface'
      )
    , Record
      ( Class = 'Entity'
      , attr = Link_Ref_List `documents`
      , attrs =
          [ Record
            ( attr = Url `url`
            , full_name = 'documents.url'
            , id = 'documents__url'
            , name = 'url'
            , sig_key = 3
            , ui_name = 'Documents/Url'
            )
          , Record
            ( attr = String `type`
            , full_name = 'documents.type'
            , id = 'documents__type'
            , name = 'type'
            , sig_key = 3
            , ui_name = 'Documents/Type'
            )
          , Record
            ( attr = String `desc`
            , full_name = 'documents.desc'
            , id = 'documents__desc'
            , name = 'desc'
            , sig_key = 3
            , ui_name = 'Documents/Description'
            )
          ]
      , full_name = 'documents'
      , id = 'documents'
      , name = 'documents'
      , sig_key = 2
      , type_name = 'MOM.Document'
      , ui_name = 'Documents'
      , ui_type_name = 'Document'
      )
    , Record
      ( Class = 'Entity'
      , attr = Role_Ref `wired_interface`
      , attrs =
          [ Record
            ( Class = 'Entity'
            , attr = Net_Device `left`
            , attrs =
                [ Record
                  ( Class = 'Entity'
                  , attr = Net_Device_Type `left`
                  , attrs =
                      [ Record
                        ( attr = String `name`
                        , full_name = 'wired_interface.left.left.name'
                        , id = 'wired_interface__left__left__name'
                        , name = 'name'
                        , sig_key = 3
                        , ui_name = 'Wired interface/Net device/Net device type/Name'
                        )
                      , Record
                        ( attr = String `model_no`
                        , full_name = 'wired_interface.left.left.model_no'
                        , id = 'wired_interface__left__left__model_no'
                        , name = 'model_no'
                        , sig_key = 3
                        , ui_name = 'Wired interface/Net device/Net device type/Model no'
                        )
                      , Record
                        ( attr = String `revision`
                        , full_name = 'wired_interface.left.left.revision'
                        , id = 'wired_interface__left__left__revision'
                        , name = 'revision'
                        , sig_key = 3
                        , ui_name = 'Wired interface/Net device/Net device type/Revision'
                        )
                      , Record
                        ( attr = Text `desc`
                        , full_name = 'wired_interface.left.left.desc'
                        , id = 'wired_interface__left__left__desc'
                        , name = 'desc'
                        , sig_key = 3
                        , ui_name = 'Wired interface/Net device/Net device type/Description'
                        )
                      ]
                  , full_name = 'wired_interface.left.left'
                  , id = 'wired_interface__left__left'
                  , name = 'left'
                  , sig_key = 2
                  , type_name = 'FFM.Net_Device_Type'
                  , ui_name = 'Wired interface/Net device/Net device type'
                  , ui_type_name = 'Net_Device_Type'
                  )
                , Record
                  ( Class = 'Entity'
                  , attr = Entity `node`
                  , attrs =
                      [ Record
                        ( attr = String `name`
                        , full_name = 'wired_interface.left.node.name'
                        , id = 'wired_interface__left__node__name'
                        , name = 'name'
                        , sig_key = 3
                        , ui_name = 'Wired interface/Net device/Node/Name'
                        )
                      , Record
                        ( Class = 'Entity'
                        , attr = Entity `manager`
                        , attrs =
                            [ Record
                              ( attr = String `last_name`
                              , full_name = 'wired_interface.left.node.manager.last_name'
                              , id = 'wired_interface__left__node__manager__last_name'
                              , name = 'last_name'
                              , sig_key = 3
                              , ui_name = 'Wired interface/Net device/Node/Manager/Last name'
                              )
                            , Record
                              ( attr = String `first_name`
                              , full_name = 'wired_interface.left.node.manager.first_name'
                              , id = 'wired_interface__left__node__manager__first_name'
                              , name = 'first_name'
                              , sig_key = 3
                              , ui_name = 'Wired interface/Net device/Node/Manager/First name'
                              )
                            , Record
                              ( attr = String `middle_name`
                              , full_name = 'wired_interface.left.node.manager.middle_name'
                              , id = 'wired_interface__left__node__manager__middle_name'
                              , name = 'middle_name'
                              , sig_key = 3
                              , ui_name = 'Wired interface/Net device/Node/Manager/Middle name'
                              )
                            , Record
                              ( attr = String `title`
                              , full_name = 'wired_interface.left.node.manager.title'
                              , id = 'wired_interface__left__node__manager__title'
                              , name = 'title'
                              , sig_key = 3
                              , ui_name = 'Wired interface/Net device/Node/Manager/Academic title'
                              )
                            , Record
                              ( attr = Date_Interval `lifetime`
                              , attrs =
                                  [ Record
                                    ( attr = Date `start`
                                    , full_name = 'wired_interface.left.node.manager.lifetime.start'
                                    , id = 'wired_interface__left__node__manager__lifetime__start'
                                    , name = 'start'
                                    , sig_key = 0
                                    , ui_name = 'Wired interface/Net device/Node/Manager/Lifetime/Start'
                                    )
                                  , Record
                                    ( attr = Date `finish`
                                    , full_name = 'wired_interface.left.node.manager.lifetime.finish'
                                    , id = 'wired_interface__left__node__manager__lifetime__finish'
                                    , name = 'finish'
                                    , sig_key = 0
                                    , ui_name = 'Wired interface/Net device/Node/Manager/Lifetime/Finish'
                                    )
                                  , Record
                                    ( attr = Boolean `alive`
                                    , choices = <Recursion on list...>
                                    , full_name = 'wired_interface.left.node.manager.lifetime.alive'
                                    , id = 'wired_interface__left__node__manager__lifetime__alive'
                                    , name = 'alive'
                                    , sig_key = 1
                                    , ui_name = 'Wired interface/Net device/Node/Manager/Lifetime/Alive'
                                    )
                                  ]
                              , full_name = 'wired_interface.left.node.manager.lifetime'
                              , id = 'wired_interface__left__node__manager__lifetime'
                              , name = 'lifetime'
                              , ui_name = 'Wired interface/Net device/Node/Manager/Lifetime'
                              )
                            , Record
                              ( attr = Sex `sex`
                              , choices = <Recursion on list...>
                              , full_name = 'wired_interface.left.node.manager.sex'
                              , id = 'wired_interface__left__node__manager__sex'
                              , name = 'sex'
                              , sig_key = 0
                              , ui_name = 'Wired interface/Net device/Node/Manager/Sex'
                              )
                            ]
                        , full_name = 'wired_interface.left.node.manager'
                        , id = 'wired_interface__left__node__manager'
                        , name = 'manager'
                        , sig_key = 2
                        , type_name = 'PAP.Person'
                        , ui_name = 'Wired interface/Net device/Node/Manager'
                        , ui_type_name = 'Person'
                        )
                      , Record
                        ( Class = 'Entity'
                        , attr = Entity `address`
                        , attrs =
                            [ Record
                              ( attr = String `street`
                              , full_name = 'wired_interface.left.node.address.street'
                              , id = 'wired_interface__left__node__address__street'
                              , name = 'street'
                              , sig_key = 3
                              , ui_name = 'Wired interface/Net device/Node/Address/Street'
                              )
                            , Record
                              ( attr = String `zip`
                              , full_name = 'wired_interface.left.node.address.zip'
                              , id = 'wired_interface__left__node__address__zip'
                              , name = 'zip'
                              , sig_key = 3
                              , ui_name = 'Wired interface/Net device/Node/Address/Zip code'
                              )
                            , Record
                              ( attr = String `city`
                              , full_name = 'wired_interface.left.node.address.city'
                              , id = 'wired_interface__left__node__address__city'
                              , name = 'city'
                              , sig_key = 3
                              , ui_name = 'Wired interface/Net device/Node/Address/City'
                              )
                            , Record
                              ( attr = String `country`
                              , full_name = 'wired_interface.left.node.address.country'
                              , id = 'wired_interface__left__node__address__country'
                              , name = 'country'
                              , sig_key = 3
                              , ui_name = 'Wired interface/Net device/Node/Address/Country'
                              )
                            , Record
                              ( attr = String `desc`
                              , full_name = 'wired_interface.left.node.address.desc'
                              , id = 'wired_interface__left__node__address__desc'
                              , name = 'desc'
                              , sig_key = 3
                              , ui_name = 'Wired interface/Net device/Node/Address/Description'
                              )
                            , Record
                              ( attr = String `region`
                              , full_name = 'wired_interface.left.node.address.region'
                              , id = 'wired_interface__left__node__address__region'
                              , name = 'region'
                              , sig_key = 3
                              , ui_name = 'Wired interface/Net device/Node/Address/Region'
                              )
                            ]
                        , full_name = 'wired_interface.left.node.address'
                        , id = 'wired_interface__left__node__address'
                        , name = 'address'
                        , sig_key = 2
                        , type_name = 'PAP.Address'
                        , ui_name = 'Wired interface/Net device/Node/Address'
                        , ui_type_name = 'Address'
                        )
                      , Record
                        ( attr = Text `desc`
                        , full_name = 'wired_interface.left.node.desc'
                        , id = 'wired_interface__left__node__desc'
                        , name = 'desc'
                        , sig_key = 3
                        , ui_name = 'Wired interface/Net device/Node/Description'
                        )
                      , Record
                        ( Class = 'Entity'
                        , attr = Entity `owner`
                        , children_np =
                            [ Record
                              ( Class = 'Entity'
                              , attr = Entity `owner`
                              , attrs =
                                  [ Record
                                    ( attr = String `name`
                                    , full_name = 'owner.name'
                                    , id = 'owner__name'
                                    , name = 'name'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Adhoc_Group]/Name'
                                    )
                                  ]
                              , full_name = 'owner'
                              , id = 'owner'
                              , name = 'owner'
                              , sig_key = 2
                              , type_name = 'PAP.Adhoc_Group'
                              , ui_name = 'Owner[Adhoc_Group]'
                              , ui_type_name = 'Adhoc_Group'
                              )
                            , Record
                              ( Class = 'Entity'
                              , attr = Entity `owner`
                              , attrs =
                                  [ Record
                                    ( attr = String `name`
                                    , full_name = 'owner.name'
                                    , id = 'owner__name'
                                    , name = 'name'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Association]/Name'
                                    )
                                  ]
                              , full_name = 'owner'
                              , id = 'owner'
                              , name = 'owner'
                              , sig_key = 2
                              , type_name = 'PAP.Association'
                              , ui_name = 'Owner[Association]'
                              , ui_type_name = 'Association'
                              )
                            , Record
                              ( Class = 'Entity'
                              , attr = Entity `owner`
                              , attrs =
                                  [ Record
                                    ( attr = String `name`
                                    , full_name = 'owner.name'
                                    , id = 'owner__name'
                                    , name = 'name'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Company]/Name'
                                    )
                                  , Record
                                    ( attr = String `registered_in`
                                    , full_name = 'owner.registered_in'
                                    , id = 'owner__registered_in'
                                    , name = 'registered_in'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Company]/Registered in'
                                    )
                                  ]
                              , full_name = 'owner'
                              , id = 'owner'
                              , name = 'owner'
                              , sig_key = 2
                              , type_name = 'PAP.Company'
                              , ui_name = 'Owner[Company]'
                              , ui_type_name = 'Company'
                              )
                            , Record
                              ( Class = 'Entity'
                              , attr = Entity `owner`
                              , attrs =
                                  [ Record
                                    ( attr = String `last_name`
                                    , full_name = 'owner.last_name'
                                    , id = 'owner__last_name'
                                    , name = 'last_name'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Person]/Last name'
                                    )
                                  , Record
                                    ( attr = String `first_name`
                                    , full_name = 'owner.first_name'
                                    , id = 'owner__first_name'
                                    , name = 'first_name'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Person]/First name'
                                    )
                                  , Record
                                    ( attr = String `middle_name`
                                    , full_name = 'owner.middle_name'
                                    , id = 'owner__middle_name'
                                    , name = 'middle_name'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Person]/Middle name'
                                    )
                                  , Record
                                    ( attr = String `title`
                                    , full_name = 'owner.title'
                                    , id = 'owner__title'
                                    , name = 'title'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Person]/Academic title'
                                    )
                                  ]
                              , full_name = 'owner'
                              , id = 'owner'
                              , name = 'owner'
                              , sig_key = 2
                              , type_name = 'PAP.Person'
                              , ui_name = 'Owner[Person]'
                              , ui_type_name = 'Person'
                              )
                            ]
                        , default_child = 'PAP.Person'
                        , full_name = 'wired_interface.left.node.owner'
                        , id = 'wired_interface__left__node__owner'
                        , name = 'owner'
                        , sig_key = 2
                        , type_name = 'PAP.Subject'
                        , ui_name = 'Wired interface/Net device/Node/Owner'
                        , ui_type_name = 'Subject'
                        )
                      , Record
                        ( attr = Position `position`
                        , attrs =
                            [ Record
                              ( attr = Angle `lat`
                              , full_name = 'wired_interface.left.node.position.lat'
                              , id = 'wired_interface__left__node__position__lat'
                              , name = 'lat'
                              , sig_key = 4
                              , ui_name = 'Wired interface/Net device/Node/Position/Latitude'
                              )
                            , Record
                              ( attr = Angle `lon`
                              , full_name = 'wired_interface.left.node.position.lon'
                              , id = 'wired_interface__left__node__position__lon'
                              , name = 'lon'
                              , sig_key = 4
                              , ui_name = 'Wired interface/Net device/Node/Position/Longitude'
                              )
                            , Record
                              ( attr = Float `height`
                              , full_name = 'wired_interface.left.node.position.height'
                              , id = 'wired_interface__left__node__position__height'
                              , name = 'height'
                              , sig_key = 0
                              , ui_name = 'Wired interface/Net device/Node/Position/Height'
                              )
                            ]
                        , full_name = 'wired_interface.left.node.position'
                        , id = 'wired_interface__left__node__position'
                        , name = 'position'
                        , ui_name = 'Wired interface/Net device/Node/Position'
                        )
                      , Record
                        ( attr = Boolean `show_in_map`
                        , choices = <Recursion on list...>
                        , full_name = 'wired_interface.left.node.show_in_map'
                        , id = 'wired_interface__left__node__show_in_map'
                        , name = 'show_in_map'
                        , sig_key = 1
                        , ui_name = 'Wired interface/Net device/Node/Show in map'
                        )
                      ]
                  , full_name = 'wired_interface.left.node'
                  , id = 'wired_interface__left__node'
                  , name = 'node'
                  , sig_key = 2
                  , type_name = 'FFM.Node'
                  , ui_name = 'Wired interface/Net device/Node'
                  , ui_type_name = 'Node'
                  )
                , Record
                  ( attr = String `name`
                  , full_name = 'wired_interface.left.name'
                  , id = 'wired_interface__left__name'
                  , name = 'name'
                  , sig_key = 3
                  , ui_name = 'Wired interface/Net device/Name'
                  )
                , Record
                  ( attr = Text `desc`
                  , full_name = 'wired_interface.left.desc'
                  , id = 'wired_interface__left__desc'
                  , name = 'desc'
                  , sig_key = 3
                  , ui_name = 'Wired interface/Net device/Description'
                  )
                , Record
                  ( Class = 'Entity'
                  , attr = Entity `my_node`
                  , attrs =
                      [ Record
                        ( attr = String `name`
                        , full_name = 'wired_interface.left.my_node.name'
                        , id = 'wired_interface__left__my_node__name'
                        , name = 'name'
                        , sig_key = 3
                        , ui_name = 'Wired interface/Net device/My node/Name'
                        )
                      , Record
                        ( Class = 'Entity'
                        , attr = Entity `manager`
                        , attrs =
                            [ Record
                              ( attr = String `last_name`
                              , full_name = 'wired_interface.left.my_node.manager.last_name'
                              , id = 'wired_interface__left__my_node__manager__last_name'
                              , name = 'last_name'
                              , sig_key = 3
                              , ui_name = 'Wired interface/Net device/My node/Manager/Last name'
                              )
                            , Record
                              ( attr = String `first_name`
                              , full_name = 'wired_interface.left.my_node.manager.first_name'
                              , id = 'wired_interface__left__my_node__manager__first_name'
                              , name = 'first_name'
                              , sig_key = 3
                              , ui_name = 'Wired interface/Net device/My node/Manager/First name'
                              )
                            , Record
                              ( attr = String `middle_name`
                              , full_name = 'wired_interface.left.my_node.manager.middle_name'
                              , id = 'wired_interface__left__my_node__manager__middle_name'
                              , name = 'middle_name'
                              , sig_key = 3
                              , ui_name = 'Wired interface/Net device/My node/Manager/Middle name'
                              )
                            , Record
                              ( attr = String `title`
                              , full_name = 'wired_interface.left.my_node.manager.title'
                              , id = 'wired_interface__left__my_node__manager__title'
                              , name = 'title'
                              , sig_key = 3
                              , ui_name = 'Wired interface/Net device/My node/Manager/Academic title'
                              )
                            , Record
                              ( attr = Date_Interval `lifetime`
                              , attrs =
                                  [ Record
                                    ( attr = Date `start`
                                    , full_name = 'wired_interface.left.my_node.manager.lifetime.start'
                                    , id = 'wired_interface__left__my_node__manager__lifetime__start'
                                    , name = 'start'
                                    , sig_key = 0
                                    , ui_name = 'Wired interface/Net device/My node/Manager/Lifetime/Start'
                                    )
                                  , Record
                                    ( attr = Date `finish`
                                    , full_name = 'wired_interface.left.my_node.manager.lifetime.finish'
                                    , id = 'wired_interface__left__my_node__manager__lifetime__finish'
                                    , name = 'finish'
                                    , sig_key = 0
                                    , ui_name = 'Wired interface/Net device/My node/Manager/Lifetime/Finish'
                                    )
                                  , Record
                                    ( attr = Boolean `alive`
                                    , choices = <Recursion on list...>
                                    , full_name = 'wired_interface.left.my_node.manager.lifetime.alive'
                                    , id = 'wired_interface__left__my_node__manager__lifetime__alive'
                                    , name = 'alive'
                                    , sig_key = 1
                                    , ui_name = 'Wired interface/Net device/My node/Manager/Lifetime/Alive'
                                    )
                                  ]
                              , full_name = 'wired_interface.left.my_node.manager.lifetime'
                              , id = 'wired_interface__left__my_node__manager__lifetime'
                              , name = 'lifetime'
                              , ui_name = 'Wired interface/Net device/My node/Manager/Lifetime'
                              )
                            , Record
                              ( attr = Sex `sex`
                              , choices = <Recursion on list...>
                              , full_name = 'wired_interface.left.my_node.manager.sex'
                              , id = 'wired_interface__left__my_node__manager__sex'
                              , name = 'sex'
                              , sig_key = 0
                              , ui_name = 'Wired interface/Net device/My node/Manager/Sex'
                              )
                            ]
                        , full_name = 'wired_interface.left.my_node.manager'
                        , id = 'wired_interface__left__my_node__manager'
                        , name = 'manager'
                        , sig_key = 2
                        , type_name = 'PAP.Person'
                        , ui_name = 'Wired interface/Net device/My node/Manager'
                        , ui_type_name = 'Person'
                        )
                      , Record
                        ( Class = 'Entity'
                        , attr = Entity `address`
                        , attrs =
                            [ Record
                              ( attr = String `street`
                              , full_name = 'wired_interface.left.my_node.address.street'
                              , id = 'wired_interface__left__my_node__address__street'
                              , name = 'street'
                              , sig_key = 3
                              , ui_name = 'Wired interface/Net device/My node/Address/Street'
                              )
                            , Record
                              ( attr = String `zip`
                              , full_name = 'wired_interface.left.my_node.address.zip'
                              , id = 'wired_interface__left__my_node__address__zip'
                              , name = 'zip'
                              , sig_key = 3
                              , ui_name = 'Wired interface/Net device/My node/Address/Zip code'
                              )
                            , Record
                              ( attr = String `city`
                              , full_name = 'wired_interface.left.my_node.address.city'
                              , id = 'wired_interface__left__my_node__address__city'
                              , name = 'city'
                              , sig_key = 3
                              , ui_name = 'Wired interface/Net device/My node/Address/City'
                              )
                            , Record
                              ( attr = String `country`
                              , full_name = 'wired_interface.left.my_node.address.country'
                              , id = 'wired_interface__left__my_node__address__country'
                              , name = 'country'
                              , sig_key = 3
                              , ui_name = 'Wired interface/Net device/My node/Address/Country'
                              )
                            , Record
                              ( attr = String `desc`
                              , full_name = 'wired_interface.left.my_node.address.desc'
                              , id = 'wired_interface__left__my_node__address__desc'
                              , name = 'desc'
                              , sig_key = 3
                              , ui_name = 'Wired interface/Net device/My node/Address/Description'
                              )
                            , Record
                              ( attr = String `region`
                              , full_name = 'wired_interface.left.my_node.address.region'
                              , id = 'wired_interface__left__my_node__address__region'
                              , name = 'region'
                              , sig_key = 3
                              , ui_name = 'Wired interface/Net device/My node/Address/Region'
                              )
                            ]
                        , full_name = 'wired_interface.left.my_node.address'
                        , id = 'wired_interface__left__my_node__address'
                        , name = 'address'
                        , sig_key = 2
                        , type_name = 'PAP.Address'
                        , ui_name = 'Wired interface/Net device/My node/Address'
                        , ui_type_name = 'Address'
                        )
                      , Record
                        ( attr = Text `desc`
                        , full_name = 'wired_interface.left.my_node.desc'
                        , id = 'wired_interface__left__my_node__desc'
                        , name = 'desc'
                        , sig_key = 3
                        , ui_name = 'Wired interface/Net device/My node/Description'
                        )
                      , Record
                        ( Class = 'Entity'
                        , attr = Entity `owner`
                        , children_np =
                            [ Record
                              ( Class = 'Entity'
                              , attr = Entity `owner`
                              , attrs =
                                  [ Record
                                    ( attr = String `name`
                                    , full_name = 'owner.name'
                                    , id = 'owner__name'
                                    , name = 'name'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Adhoc_Group]/Name'
                                    )
                                  ]
                              , full_name = 'owner'
                              , id = 'owner'
                              , name = 'owner'
                              , sig_key = 2
                              , type_name = 'PAP.Adhoc_Group'
                              , ui_name = 'Owner[Adhoc_Group]'
                              , ui_type_name = 'Adhoc_Group'
                              )
                            , Record
                              ( Class = 'Entity'
                              , attr = Entity `owner`
                              , attrs =
                                  [ Record
                                    ( attr = String `name`
                                    , full_name = 'owner.name'
                                    , id = 'owner__name'
                                    , name = 'name'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Association]/Name'
                                    )
                                  ]
                              , full_name = 'owner'
                              , id = 'owner'
                              , name = 'owner'
                              , sig_key = 2
                              , type_name = 'PAP.Association'
                              , ui_name = 'Owner[Association]'
                              , ui_type_name = 'Association'
                              )
                            , Record
                              ( Class = 'Entity'
                              , attr = Entity `owner`
                              , attrs =
                                  [ Record
                                    ( attr = String `name`
                                    , full_name = 'owner.name'
                                    , id = 'owner__name'
                                    , name = 'name'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Company]/Name'
                                    )
                                  , Record
                                    ( attr = String `registered_in`
                                    , full_name = 'owner.registered_in'
                                    , id = 'owner__registered_in'
                                    , name = 'registered_in'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Company]/Registered in'
                                    )
                                  ]
                              , full_name = 'owner'
                              , id = 'owner'
                              , name = 'owner'
                              , sig_key = 2
                              , type_name = 'PAP.Company'
                              , ui_name = 'Owner[Company]'
                              , ui_type_name = 'Company'
                              )
                            , Record
                              ( Class = 'Entity'
                              , attr = Entity `owner`
                              , attrs =
                                  [ Record
                                    ( attr = String `last_name`
                                    , full_name = 'owner.last_name'
                                    , id = 'owner__last_name'
                                    , name = 'last_name'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Person]/Last name'
                                    )
                                  , Record
                                    ( attr = String `first_name`
                                    , full_name = 'owner.first_name'
                                    , id = 'owner__first_name'
                                    , name = 'first_name'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Person]/First name'
                                    )
                                  , Record
                                    ( attr = String `middle_name`
                                    , full_name = 'owner.middle_name'
                                    , id = 'owner__middle_name'
                                    , name = 'middle_name'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Person]/Middle name'
                                    )
                                  , Record
                                    ( attr = String `title`
                                    , full_name = 'owner.title'
                                    , id = 'owner__title'
                                    , name = 'title'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Person]/Academic title'
                                    )
                                  ]
                              , full_name = 'owner'
                              , id = 'owner'
                              , name = 'owner'
                              , sig_key = 2
                              , type_name = 'PAP.Person'
                              , ui_name = 'Owner[Person]'
                              , ui_type_name = 'Person'
                              )
                            ]
                        , default_child = 'PAP.Person'
                        , full_name = 'wired_interface.left.my_node.owner'
                        , id = 'wired_interface__left__my_node__owner'
                        , name = 'owner'
                        , sig_key = 2
                        , type_name = 'PAP.Subject'
                        , ui_name = 'Wired interface/Net device/My node/Owner'
                        , ui_type_name = 'Subject'
                        )
                      , Record
                        ( attr = Position `position`
                        , attrs =
                            [ Record
                              ( attr = Angle `lat`
                              , full_name = 'wired_interface.left.my_node.position.lat'
                              , id = 'wired_interface__left__my_node__position__lat'
                              , name = 'lat'
                              , sig_key = 4
                              , ui_name = 'Wired interface/Net device/My node/Position/Latitude'
                              )
                            , Record
                              ( attr = Angle `lon`
                              , full_name = 'wired_interface.left.my_node.position.lon'
                              , id = 'wired_interface__left__my_node__position__lon'
                              , name = 'lon'
                              , sig_key = 4
                              , ui_name = 'Wired interface/Net device/My node/Position/Longitude'
                              )
                            , Record
                              ( attr = Float `height`
                              , full_name = 'wired_interface.left.my_node.position.height'
                              , id = 'wired_interface__left__my_node__position__height'
                              , name = 'height'
                              , sig_key = 0
                              , ui_name = 'Wired interface/Net device/My node/Position/Height'
                              )
                            ]
                        , full_name = 'wired_interface.left.my_node.position'
                        , id = 'wired_interface__left__my_node__position'
                        , name = 'position'
                        , ui_name = 'Wired interface/Net device/My node/Position'
                        )
                      , Record
                        ( attr = Boolean `show_in_map`
                        , choices = <Recursion on list...>
                        , full_name = 'wired_interface.left.my_node.show_in_map'
                        , id = 'wired_interface__left__my_node__show_in_map'
                        , name = 'show_in_map'
                        , sig_key = 1
                        , ui_name = 'Wired interface/Net device/My node/Show in map'
                        )
                      ]
                  , full_name = 'wired_interface.left.my_node'
                  , id = 'wired_interface__left__my_node'
                  , name = 'my_node'
                  , sig_key = 2
                  , type_name = 'FFM.Node'
                  , ui_name = 'Wired interface/Net device/My node'
                  , ui_type_name = 'Node'
                  )
                ]
            , full_name = 'wired_interface.left'
            , id = 'wired_interface__left'
            , name = 'left'
            , sig_key = 2
            , type_name = 'FFM.Net_Device'
            , ui_name = 'Wired interface/Net device'
            , ui_type_name = 'Net_Device'
            )
          , Record
            ( attr = MAC-address `mac_address`
            , full_name = 'wired_interface.mac_address'
            , id = 'wired_interface__mac_address'
            , name = 'mac_address'
            , sig_key = 3
            , ui_name = 'Wired interface/Mac address'
            )
          , Record
            ( attr = String `name`
            , full_name = 'wired_interface.name'
            , id = 'wired_interface__name'
            , name = 'name'
            , sig_key = 3
            , ui_name = 'Wired interface/Name'
            )
          , Record
            ( attr = Boolean `is_active`
            , choices =
                [ 'no'
                , 'yes'
                ]
            , full_name = 'wired_interface.is_active'
            , id = 'wired_interface__is_active'
            , name = 'is_active'
            , sig_key = 1
            , ui_name = 'Wired interface/Is active'
            )
          , Record
            ( attr = Text `desc`
            , full_name = 'wired_interface.desc'
            , id = 'wired_interface__desc'
            , name = 'desc'
            , sig_key = 3
            , ui_name = 'Wired interface/Description'
            )
          , Record
            ( Class = 'Entity'
            , attr = Entity `my_node`
            , attrs =
                [ Record
                  ( attr = String `name`
                  , full_name = 'wired_interface.my_node.name'
                  , id = 'wired_interface__my_node__name'
                  , name = 'name'
                  , sig_key = 3
                  , ui_name = 'Wired interface/My node/Name'
                  )
                , Record
                  ( Class = 'Entity'
                  , attr = Entity `manager`
                  , attrs =
                      [ Record
                        ( attr = String `last_name`
                        , full_name = 'wired_interface.my_node.manager.last_name'
                        , id = 'wired_interface__my_node__manager__last_name'
                        , name = 'last_name'
                        , sig_key = 3
                        , ui_name = 'Wired interface/My node/Manager/Last name'
                        )
                      , Record
                        ( attr = String `first_name`
                        , full_name = 'wired_interface.my_node.manager.first_name'
                        , id = 'wired_interface__my_node__manager__first_name'
                        , name = 'first_name'
                        , sig_key = 3
                        , ui_name = 'Wired interface/My node/Manager/First name'
                        )
                      , Record
                        ( attr = String `middle_name`
                        , full_name = 'wired_interface.my_node.manager.middle_name'
                        , id = 'wired_interface__my_node__manager__middle_name'
                        , name = 'middle_name'
                        , sig_key = 3
                        , ui_name = 'Wired interface/My node/Manager/Middle name'
                        )
                      , Record
                        ( attr = String `title`
                        , full_name = 'wired_interface.my_node.manager.title'
                        , id = 'wired_interface__my_node__manager__title'
                        , name = 'title'
                        , sig_key = 3
                        , ui_name = 'Wired interface/My node/Manager/Academic title'
                        )
                      , Record
                        ( attr = Date_Interval `lifetime`
                        , attrs =
                            [ Record
                              ( attr = Date `start`
                              , full_name = 'wired_interface.my_node.manager.lifetime.start'
                              , id = 'wired_interface__my_node__manager__lifetime__start'
                              , name = 'start'
                              , sig_key = 0
                              , ui_name = 'Wired interface/My node/Manager/Lifetime/Start'
                              )
                            , Record
                              ( attr = Date `finish`
                              , full_name = 'wired_interface.my_node.manager.lifetime.finish'
                              , id = 'wired_interface__my_node__manager__lifetime__finish'
                              , name = 'finish'
                              , sig_key = 0
                              , ui_name = 'Wired interface/My node/Manager/Lifetime/Finish'
                              )
                            , Record
                              ( attr = Boolean `alive`
                              , choices = <Recursion on list...>
                              , full_name = 'wired_interface.my_node.manager.lifetime.alive'
                              , id = 'wired_interface__my_node__manager__lifetime__alive'
                              , name = 'alive'
                              , sig_key = 1
                              , ui_name = 'Wired interface/My node/Manager/Lifetime/Alive'
                              )
                            ]
                        , full_name = 'wired_interface.my_node.manager.lifetime'
                        , id = 'wired_interface__my_node__manager__lifetime'
                        , name = 'lifetime'
                        , ui_name = 'Wired interface/My node/Manager/Lifetime'
                        )
                      , Record
                        ( attr = Sex `sex`
                        , choices = <Recursion on list...>
                        , full_name = 'wired_interface.my_node.manager.sex'
                        , id = 'wired_interface__my_node__manager__sex'
                        , name = 'sex'
                        , sig_key = 0
                        , ui_name = 'Wired interface/My node/Manager/Sex'
                        )
                      ]
                  , full_name = 'wired_interface.my_node.manager'
                  , id = 'wired_interface__my_node__manager'
                  , name = 'manager'
                  , sig_key = 2
                  , type_name = 'PAP.Person'
                  , ui_name = 'Wired interface/My node/Manager'
                  , ui_type_name = 'Person'
                  )
                , Record
                  ( Class = 'Entity'
                  , attr = Entity `address`
                  , attrs =
                      [ Record
                        ( attr = String `street`
                        , full_name = 'wired_interface.my_node.address.street'
                        , id = 'wired_interface__my_node__address__street'
                        , name = 'street'
                        , sig_key = 3
                        , ui_name = 'Wired interface/My node/Address/Street'
                        )
                      , Record
                        ( attr = String `zip`
                        , full_name = 'wired_interface.my_node.address.zip'
                        , id = 'wired_interface__my_node__address__zip'
                        , name = 'zip'
                        , sig_key = 3
                        , ui_name = 'Wired interface/My node/Address/Zip code'
                        )
                      , Record
                        ( attr = String `city`
                        , full_name = 'wired_interface.my_node.address.city'
                        , id = 'wired_interface__my_node__address__city'
                        , name = 'city'
                        , sig_key = 3
                        , ui_name = 'Wired interface/My node/Address/City'
                        )
                      , Record
                        ( attr = String `country`
                        , full_name = 'wired_interface.my_node.address.country'
                        , id = 'wired_interface__my_node__address__country'
                        , name = 'country'
                        , sig_key = 3
                        , ui_name = 'Wired interface/My node/Address/Country'
                        )
                      , Record
                        ( attr = String `desc`
                        , full_name = 'wired_interface.my_node.address.desc'
                        , id = 'wired_interface__my_node__address__desc'
                        , name = 'desc'
                        , sig_key = 3
                        , ui_name = 'Wired interface/My node/Address/Description'
                        )
                      , Record
                        ( attr = String `region`
                        , full_name = 'wired_interface.my_node.address.region'
                        , id = 'wired_interface__my_node__address__region'
                        , name = 'region'
                        , sig_key = 3
                        , ui_name = 'Wired interface/My node/Address/Region'
                        )
                      ]
                  , full_name = 'wired_interface.my_node.address'
                  , id = 'wired_interface__my_node__address'
                  , name = 'address'
                  , sig_key = 2
                  , type_name = 'PAP.Address'
                  , ui_name = 'Wired interface/My node/Address'
                  , ui_type_name = 'Address'
                  )
                , Record
                  ( attr = Text `desc`
                  , full_name = 'wired_interface.my_node.desc'
                  , id = 'wired_interface__my_node__desc'
                  , name = 'desc'
                  , sig_key = 3
                  , ui_name = 'Wired interface/My node/Description'
                  )
                , Record
                  ( Class = 'Entity'
                  , attr = Entity `owner`
                  , children_np =
                      [ Record
                        ( Class = 'Entity'
                        , attr = Entity `owner`
                        , attrs =
                            [ Record
                              ( attr = String `name`
                              , full_name = 'owner.name'
                              , id = 'owner__name'
                              , name = 'name'
                              , sig_key = 3
                              , ui_name = 'Owner[Adhoc_Group]/Name'
                              )
                            ]
                        , full_name = 'owner'
                        , id = 'owner'
                        , name = 'owner'
                        , sig_key = 2
                        , type_name = 'PAP.Adhoc_Group'
                        , ui_name = 'Owner[Adhoc_Group]'
                        , ui_type_name = 'Adhoc_Group'
                        )
                      , Record
                        ( Class = 'Entity'
                        , attr = Entity `owner`
                        , attrs =
                            [ Record
                              ( attr = String `name`
                              , full_name = 'owner.name'
                              , id = 'owner__name'
                              , name = 'name'
                              , sig_key = 3
                              , ui_name = 'Owner[Association]/Name'
                              )
                            ]
                        , full_name = 'owner'
                        , id = 'owner'
                        , name = 'owner'
                        , sig_key = 2
                        , type_name = 'PAP.Association'
                        , ui_name = 'Owner[Association]'
                        , ui_type_name = 'Association'
                        )
                      , Record
                        ( Class = 'Entity'
                        , attr = Entity `owner`
                        , attrs =
                            [ Record
                              ( attr = String `name`
                              , full_name = 'owner.name'
                              , id = 'owner__name'
                              , name = 'name'
                              , sig_key = 3
                              , ui_name = 'Owner[Company]/Name'
                              )
                            , Record
                              ( attr = String `registered_in`
                              , full_name = 'owner.registered_in'
                              , id = 'owner__registered_in'
                              , name = 'registered_in'
                              , sig_key = 3
                              , ui_name = 'Owner[Company]/Registered in'
                              )
                            ]
                        , full_name = 'owner'
                        , id = 'owner'
                        , name = 'owner'
                        , sig_key = 2
                        , type_name = 'PAP.Company'
                        , ui_name = 'Owner[Company]'
                        , ui_type_name = 'Company'
                        )
                      , Record
                        ( Class = 'Entity'
                        , attr = Entity `owner`
                        , attrs =
                            [ Record
                              ( attr = String `last_name`
                              , full_name = 'owner.last_name'
                              , id = 'owner__last_name'
                              , name = 'last_name'
                              , sig_key = 3
                              , ui_name = 'Owner[Person]/Last name'
                              )
                            , Record
                              ( attr = String `first_name`
                              , full_name = 'owner.first_name'
                              , id = 'owner__first_name'
                              , name = 'first_name'
                              , sig_key = 3
                              , ui_name = 'Owner[Person]/First name'
                              )
                            , Record
                              ( attr = String `middle_name`
                              , full_name = 'owner.middle_name'
                              , id = 'owner__middle_name'
                              , name = 'middle_name'
                              , sig_key = 3
                              , ui_name = 'Owner[Person]/Middle name'
                              )
                            , Record
                              ( attr = String `title`
                              , full_name = 'owner.title'
                              , id = 'owner__title'
                              , name = 'title'
                              , sig_key = 3
                              , ui_name = 'Owner[Person]/Academic title'
                              )
                            ]
                        , full_name = 'owner'
                        , id = 'owner'
                        , name = 'owner'
                        , sig_key = 2
                        , type_name = 'PAP.Person'
                        , ui_name = 'Owner[Person]'
                        , ui_type_name = 'Person'
                        )
                      ]
                  , default_child = 'PAP.Person'
                  , full_name = 'wired_interface.my_node.owner'
                  , id = 'wired_interface__my_node__owner'
                  , name = 'owner'
                  , sig_key = 2
                  , type_name = 'PAP.Subject'
                  , ui_name = 'Wired interface/My node/Owner'
                  , ui_type_name = 'Subject'
                  )
                , Record
                  ( attr = Position `position`
                  , attrs =
                      [ Record
                        ( attr = Angle `lat`
                        , full_name = 'wired_interface.my_node.position.lat'
                        , id = 'wired_interface__my_node__position__lat'
                        , name = 'lat'
                        , sig_key = 4
                        , ui_name = 'Wired interface/My node/Position/Latitude'
                        )
                      , Record
                        ( attr = Angle `lon`
                        , full_name = 'wired_interface.my_node.position.lon'
                        , id = 'wired_interface__my_node__position__lon'
                        , name = 'lon'
                        , sig_key = 4
                        , ui_name = 'Wired interface/My node/Position/Longitude'
                        )
                      , Record
                        ( attr = Float `height`
                        , full_name = 'wired_interface.my_node.position.height'
                        , id = 'wired_interface__my_node__position__height'
                        , name = 'height'
                        , sig_key = 0
                        , ui_name = 'Wired interface/My node/Position/Height'
                        )
                      ]
                  , full_name = 'wired_interface.my_node.position'
                  , id = 'wired_interface__my_node__position'
                  , name = 'position'
                  , ui_name = 'Wired interface/My node/Position'
                  )
                , Record
                  ( attr = Boolean `show_in_map`
                  , choices = <Recursion on list...>
                  , full_name = 'wired_interface.my_node.show_in_map'
                  , id = 'wired_interface__my_node__show_in_map'
                  , name = 'show_in_map'
                  , sig_key = 1
                  , ui_name = 'Wired interface/My node/Show in map'
                  )
                ]
            , full_name = 'wired_interface.my_node'
            , id = 'wired_interface__my_node'
            , name = 'my_node'
            , sig_key = 2
            , type_name = 'FFM.Node'
            , ui_name = 'Wired interface/My node'
            , ui_type_name = 'Node'
            )
          , Record
            ( Class = 'Entity'
            , attr = Entity `my_net_device`
            , attrs =
                [ Record
                  ( Class = 'Entity'
                  , attr = Net_Device_Type `left`
                  , attrs =
                      [ Record
                        ( attr = String `name`
                        , full_name = 'wired_interface.my_net_device.left.name'
                        , id = 'wired_interface__my_net_device__left__name'
                        , name = 'name'
                        , sig_key = 3
                        , ui_name = 'Wired interface/My net device/Net device type/Name'
                        )
                      , Record
                        ( attr = String `model_no`
                        , full_name = 'wired_interface.my_net_device.left.model_no'
                        , id = 'wired_interface__my_net_device__left__model_no'
                        , name = 'model_no'
                        , sig_key = 3
                        , ui_name = 'Wired interface/My net device/Net device type/Model no'
                        )
                      , Record
                        ( attr = String `revision`
                        , full_name = 'wired_interface.my_net_device.left.revision'
                        , id = 'wired_interface__my_net_device__left__revision'
                        , name = 'revision'
                        , sig_key = 3
                        , ui_name = 'Wired interface/My net device/Net device type/Revision'
                        )
                      , Record
                        ( attr = Text `desc`
                        , full_name = 'wired_interface.my_net_device.left.desc'
                        , id = 'wired_interface__my_net_device__left__desc'
                        , name = 'desc'
                        , sig_key = 3
                        , ui_name = 'Wired interface/My net device/Net device type/Description'
                        )
                      ]
                  , full_name = 'wired_interface.my_net_device.left'
                  , id = 'wired_interface__my_net_device__left'
                  , name = 'left'
                  , sig_key = 2
                  , type_name = 'FFM.Net_Device_Type'
                  , ui_name = 'Wired interface/My net device/Net device type'
                  , ui_type_name = 'Net_Device_Type'
                  )
                , Record
                  ( Class = 'Entity'
                  , attr = Entity `node`
                  , attrs =
                      [ Record
                        ( attr = String `name`
                        , full_name = 'wired_interface.my_net_device.node.name'
                        , id = 'wired_interface__my_net_device__node__name'
                        , name = 'name'
                        , sig_key = 3
                        , ui_name = 'Wired interface/My net device/Node/Name'
                        )
                      , Record
                        ( Class = 'Entity'
                        , attr = Entity `manager`
                        , attrs =
                            [ Record
                              ( attr = String `last_name`
                              , full_name = 'wired_interface.my_net_device.node.manager.last_name'
                              , id = 'wired_interface__my_net_device__node__manager__last_name'
                              , name = 'last_name'
                              , sig_key = 3
                              , ui_name = 'Wired interface/My net device/Node/Manager/Last name'
                              )
                            , Record
                              ( attr = String `first_name`
                              , full_name = 'wired_interface.my_net_device.node.manager.first_name'
                              , id = 'wired_interface__my_net_device__node__manager__first_name'
                              , name = 'first_name'
                              , sig_key = 3
                              , ui_name = 'Wired interface/My net device/Node/Manager/First name'
                              )
                            , Record
                              ( attr = String `middle_name`
                              , full_name = 'wired_interface.my_net_device.node.manager.middle_name'
                              , id = 'wired_interface__my_net_device__node__manager__middle_name'
                              , name = 'middle_name'
                              , sig_key = 3
                              , ui_name = 'Wired interface/My net device/Node/Manager/Middle name'
                              )
                            , Record
                              ( attr = String `title`
                              , full_name = 'wired_interface.my_net_device.node.manager.title'
                              , id = 'wired_interface__my_net_device__node__manager__title'
                              , name = 'title'
                              , sig_key = 3
                              , ui_name = 'Wired interface/My net device/Node/Manager/Academic title'
                              )
                            , Record
                              ( attr = Date_Interval `lifetime`
                              , attrs =
                                  [ Record
                                    ( attr = Date `start`
                                    , full_name = 'wired_interface.my_net_device.node.manager.lifetime.start'
                                    , id = 'wired_interface__my_net_device__node__manager__lifetime__start'
                                    , name = 'start'
                                    , sig_key = 0
                                    , ui_name = 'Wired interface/My net device/Node/Manager/Lifetime/Start'
                                    )
                                  , Record
                                    ( attr = Date `finish`
                                    , full_name = 'wired_interface.my_net_device.node.manager.lifetime.finish'
                                    , id = 'wired_interface__my_net_device__node__manager__lifetime__finish'
                                    , name = 'finish'
                                    , sig_key = 0
                                    , ui_name = 'Wired interface/My net device/Node/Manager/Lifetime/Finish'
                                    )
                                  , Record
                                    ( attr = Boolean `alive`
                                    , choices = <Recursion on list...>
                                    , full_name = 'wired_interface.my_net_device.node.manager.lifetime.alive'
                                    , id = 'wired_interface__my_net_device__node__manager__lifetime__alive'
                                    , name = 'alive'
                                    , sig_key = 1
                                    , ui_name = 'Wired interface/My net device/Node/Manager/Lifetime/Alive'
                                    )
                                  ]
                              , full_name = 'wired_interface.my_net_device.node.manager.lifetime'
                              , id = 'wired_interface__my_net_device__node__manager__lifetime'
                              , name = 'lifetime'
                              , ui_name = 'Wired interface/My net device/Node/Manager/Lifetime'
                              )
                            , Record
                              ( attr = Sex `sex`
                              , choices = <Recursion on list...>
                              , full_name = 'wired_interface.my_net_device.node.manager.sex'
                              , id = 'wired_interface__my_net_device__node__manager__sex'
                              , name = 'sex'
                              , sig_key = 0
                              , ui_name = 'Wired interface/My net device/Node/Manager/Sex'
                              )
                            ]
                        , full_name = 'wired_interface.my_net_device.node.manager'
                        , id = 'wired_interface__my_net_device__node__manager'
                        , name = 'manager'
                        , sig_key = 2
                        , type_name = 'PAP.Person'
                        , ui_name = 'Wired interface/My net device/Node/Manager'
                        , ui_type_name = 'Person'
                        )
                      , Record
                        ( Class = 'Entity'
                        , attr = Entity `address`
                        , attrs =
                            [ Record
                              ( attr = String `street`
                              , full_name = 'wired_interface.my_net_device.node.address.street'
                              , id = 'wired_interface__my_net_device__node__address__street'
                              , name = 'street'
                              , sig_key = 3
                              , ui_name = 'Wired interface/My net device/Node/Address/Street'
                              )
                            , Record
                              ( attr = String `zip`
                              , full_name = 'wired_interface.my_net_device.node.address.zip'
                              , id = 'wired_interface__my_net_device__node__address__zip'
                              , name = 'zip'
                              , sig_key = 3
                              , ui_name = 'Wired interface/My net device/Node/Address/Zip code'
                              )
                            , Record
                              ( attr = String `city`
                              , full_name = 'wired_interface.my_net_device.node.address.city'
                              , id = 'wired_interface__my_net_device__node__address__city'
                              , name = 'city'
                              , sig_key = 3
                              , ui_name = 'Wired interface/My net device/Node/Address/City'
                              )
                            , Record
                              ( attr = String `country`
                              , full_name = 'wired_interface.my_net_device.node.address.country'
                              , id = 'wired_interface__my_net_device__node__address__country'
                              , name = 'country'
                              , sig_key = 3
                              , ui_name = 'Wired interface/My net device/Node/Address/Country'
                              )
                            , Record
                              ( attr = String `desc`
                              , full_name = 'wired_interface.my_net_device.node.address.desc'
                              , id = 'wired_interface__my_net_device__node__address__desc'
                              , name = 'desc'
                              , sig_key = 3
                              , ui_name = 'Wired interface/My net device/Node/Address/Description'
                              )
                            , Record
                              ( attr = String `region`
                              , full_name = 'wired_interface.my_net_device.node.address.region'
                              , id = 'wired_interface__my_net_device__node__address__region'
                              , name = 'region'
                              , sig_key = 3
                              , ui_name = 'Wired interface/My net device/Node/Address/Region'
                              )
                            ]
                        , full_name = 'wired_interface.my_net_device.node.address'
                        , id = 'wired_interface__my_net_device__node__address'
                        , name = 'address'
                        , sig_key = 2
                        , type_name = 'PAP.Address'
                        , ui_name = 'Wired interface/My net device/Node/Address'
                        , ui_type_name = 'Address'
                        )
                      , Record
                        ( attr = Text `desc`
                        , full_name = 'wired_interface.my_net_device.node.desc'
                        , id = 'wired_interface__my_net_device__node__desc'
                        , name = 'desc'
                        , sig_key = 3
                        , ui_name = 'Wired interface/My net device/Node/Description'
                        )
                      , Record
                        ( Class = 'Entity'
                        , attr = Entity `owner`
                        , children_np =
                            [ Record
                              ( Class = 'Entity'
                              , attr = Entity `owner`
                              , attrs =
                                  [ Record
                                    ( attr = String `name`
                                    , full_name = 'owner.name'
                                    , id = 'owner__name'
                                    , name = 'name'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Adhoc_Group]/Name'
                                    )
                                  ]
                              , full_name = 'owner'
                              , id = 'owner'
                              , name = 'owner'
                              , sig_key = 2
                              , type_name = 'PAP.Adhoc_Group'
                              , ui_name = 'Owner[Adhoc_Group]'
                              , ui_type_name = 'Adhoc_Group'
                              )
                            , Record
                              ( Class = 'Entity'
                              , attr = Entity `owner`
                              , attrs =
                                  [ Record
                                    ( attr = String `name`
                                    , full_name = 'owner.name'
                                    , id = 'owner__name'
                                    , name = 'name'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Association]/Name'
                                    )
                                  ]
                              , full_name = 'owner'
                              , id = 'owner'
                              , name = 'owner'
                              , sig_key = 2
                              , type_name = 'PAP.Association'
                              , ui_name = 'Owner[Association]'
                              , ui_type_name = 'Association'
                              )
                            , Record
                              ( Class = 'Entity'
                              , attr = Entity `owner`
                              , attrs =
                                  [ Record
                                    ( attr = String `name`
                                    , full_name = 'owner.name'
                                    , id = 'owner__name'
                                    , name = 'name'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Company]/Name'
                                    )
                                  , Record
                                    ( attr = String `registered_in`
                                    , full_name = 'owner.registered_in'
                                    , id = 'owner__registered_in'
                                    , name = 'registered_in'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Company]/Registered in'
                                    )
                                  ]
                              , full_name = 'owner'
                              , id = 'owner'
                              , name = 'owner'
                              , sig_key = 2
                              , type_name = 'PAP.Company'
                              , ui_name = 'Owner[Company]'
                              , ui_type_name = 'Company'
                              )
                            , Record
                              ( Class = 'Entity'
                              , attr = Entity `owner`
                              , attrs =
                                  [ Record
                                    ( attr = String `last_name`
                                    , full_name = 'owner.last_name'
                                    , id = 'owner__last_name'
                                    , name = 'last_name'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Person]/Last name'
                                    )
                                  , Record
                                    ( attr = String `first_name`
                                    , full_name = 'owner.first_name'
                                    , id = 'owner__first_name'
                                    , name = 'first_name'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Person]/First name'
                                    )
                                  , Record
                                    ( attr = String `middle_name`
                                    , full_name = 'owner.middle_name'
                                    , id = 'owner__middle_name'
                                    , name = 'middle_name'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Person]/Middle name'
                                    )
                                  , Record
                                    ( attr = String `title`
                                    , full_name = 'owner.title'
                                    , id = 'owner__title'
                                    , name = 'title'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Person]/Academic title'
                                    )
                                  ]
                              , full_name = 'owner'
                              , id = 'owner'
                              , name = 'owner'
                              , sig_key = 2
                              , type_name = 'PAP.Person'
                              , ui_name = 'Owner[Person]'
                              , ui_type_name = 'Person'
                              )
                            ]
                        , default_child = 'PAP.Person'
                        , full_name = 'wired_interface.my_net_device.node.owner'
                        , id = 'wired_interface__my_net_device__node__owner'
                        , name = 'owner'
                        , sig_key = 2
                        , type_name = 'PAP.Subject'
                        , ui_name = 'Wired interface/My net device/Node/Owner'
                        , ui_type_name = 'Subject'
                        )
                      , Record
                        ( attr = Position `position`
                        , attrs =
                            [ Record
                              ( attr = Angle `lat`
                              , full_name = 'wired_interface.my_net_device.node.position.lat'
                              , id = 'wired_interface__my_net_device__node__position__lat'
                              , name = 'lat'
                              , sig_key = 4
                              , ui_name = 'Wired interface/My net device/Node/Position/Latitude'
                              )
                            , Record
                              ( attr = Angle `lon`
                              , full_name = 'wired_interface.my_net_device.node.position.lon'
                              , id = 'wired_interface__my_net_device__node__position__lon'
                              , name = 'lon'
                              , sig_key = 4
                              , ui_name = 'Wired interface/My net device/Node/Position/Longitude'
                              )
                            , Record
                              ( attr = Float `height`
                              , full_name = 'wired_interface.my_net_device.node.position.height'
                              , id = 'wired_interface__my_net_device__node__position__height'
                              , name = 'height'
                              , sig_key = 0
                              , ui_name = 'Wired interface/My net device/Node/Position/Height'
                              )
                            ]
                        , full_name = 'wired_interface.my_net_device.node.position'
                        , id = 'wired_interface__my_net_device__node__position'
                        , name = 'position'
                        , ui_name = 'Wired interface/My net device/Node/Position'
                        )
                      , Record
                        ( attr = Boolean `show_in_map`
                        , choices = <Recursion on list...>
                        , full_name = 'wired_interface.my_net_device.node.show_in_map'
                        , id = 'wired_interface__my_net_device__node__show_in_map'
                        , name = 'show_in_map'
                        , sig_key = 1
                        , ui_name = 'Wired interface/My net device/Node/Show in map'
                        )
                      ]
                  , full_name = 'wired_interface.my_net_device.node'
                  , id = 'wired_interface__my_net_device__node'
                  , name = 'node'
                  , sig_key = 2
                  , type_name = 'FFM.Node'
                  , ui_name = 'Wired interface/My net device/Node'
                  , ui_type_name = 'Node'
                  )
                , Record
                  ( attr = String `name`
                  , full_name = 'wired_interface.my_net_device.name'
                  , id = 'wired_interface__my_net_device__name'
                  , name = 'name'
                  , sig_key = 3
                  , ui_name = 'Wired interface/My net device/Name'
                  )
                , Record
                  ( attr = Text `desc`
                  , full_name = 'wired_interface.my_net_device.desc'
                  , id = 'wired_interface__my_net_device__desc'
                  , name = 'desc'
                  , sig_key = 3
                  , ui_name = 'Wired interface/My net device/Description'
                  )
                , Record
                  ( Class = 'Entity'
                  , attr = Entity `my_node`
                  , attrs =
                      [ Record
                        ( attr = String `name`
                        , full_name = 'wired_interface.my_net_device.my_node.name'
                        , id = 'wired_interface__my_net_device__my_node__name'
                        , name = 'name'
                        , sig_key = 3
                        , ui_name = 'Wired interface/My net device/My node/Name'
                        )
                      , Record
                        ( Class = 'Entity'
                        , attr = Entity `manager`
                        , attrs =
                            [ Record
                              ( attr = String `last_name`
                              , full_name = 'wired_interface.my_net_device.my_node.manager.last_name'
                              , id = 'wired_interface__my_net_device__my_node__manager__last_name'
                              , name = 'last_name'
                              , sig_key = 3
                              , ui_name = 'Wired interface/My net device/My node/Manager/Last name'
                              )
                            , Record
                              ( attr = String `first_name`
                              , full_name = 'wired_interface.my_net_device.my_node.manager.first_name'
                              , id = 'wired_interface__my_net_device__my_node__manager__first_name'
                              , name = 'first_name'
                              , sig_key = 3
                              , ui_name = 'Wired interface/My net device/My node/Manager/First name'
                              )
                            , Record
                              ( attr = String `middle_name`
                              , full_name = 'wired_interface.my_net_device.my_node.manager.middle_name'
                              , id = 'wired_interface__my_net_device__my_node__manager__middle_name'
                              , name = 'middle_name'
                              , sig_key = 3
                              , ui_name = 'Wired interface/My net device/My node/Manager/Middle name'
                              )
                            , Record
                              ( attr = String `title`
                              , full_name = 'wired_interface.my_net_device.my_node.manager.title'
                              , id = 'wired_interface__my_net_device__my_node__manager__title'
                              , name = 'title'
                              , sig_key = 3
                              , ui_name = 'Wired interface/My net device/My node/Manager/Academic title'
                              )
                            , Record
                              ( attr = Date_Interval `lifetime`
                              , attrs =
                                  [ Record
                                    ( attr = Date `start`
                                    , full_name = 'wired_interface.my_net_device.my_node.manager.lifetime.start'
                                    , id = 'wired_interface__my_net_device__my_node__manager__lifetime__start'
                                    , name = 'start'
                                    , sig_key = 0
                                    , ui_name = 'Wired interface/My net device/My node/Manager/Lifetime/Start'
                                    )
                                  , Record
                                    ( attr = Date `finish`
                                    , full_name = 'wired_interface.my_net_device.my_node.manager.lifetime.finish'
                                    , id = 'wired_interface__my_net_device__my_node__manager__lifetime__finish'
                                    , name = 'finish'
                                    , sig_key = 0
                                    , ui_name = 'Wired interface/My net device/My node/Manager/Lifetime/Finish'
                                    )
                                  , Record
                                    ( attr = Boolean `alive`
                                    , choices = <Recursion on list...>
                                    , full_name = 'wired_interface.my_net_device.my_node.manager.lifetime.alive'
                                    , id = 'wired_interface__my_net_device__my_node__manager__lifetime__alive'
                                    , name = 'alive'
                                    , sig_key = 1
                                    , ui_name = 'Wired interface/My net device/My node/Manager/Lifetime/Alive'
                                    )
                                  ]
                              , full_name = 'wired_interface.my_net_device.my_node.manager.lifetime'
                              , id = 'wired_interface__my_net_device__my_node__manager__lifetime'
                              , name = 'lifetime'
                              , ui_name = 'Wired interface/My net device/My node/Manager/Lifetime'
                              )
                            , Record
                              ( attr = Sex `sex`
                              , choices = <Recursion on list...>
                              , full_name = 'wired_interface.my_net_device.my_node.manager.sex'
                              , id = 'wired_interface__my_net_device__my_node__manager__sex'
                              , name = 'sex'
                              , sig_key = 0
                              , ui_name = 'Wired interface/My net device/My node/Manager/Sex'
                              )
                            ]
                        , full_name = 'wired_interface.my_net_device.my_node.manager'
                        , id = 'wired_interface__my_net_device__my_node__manager'
                        , name = 'manager'
                        , sig_key = 2
                        , type_name = 'PAP.Person'
                        , ui_name = 'Wired interface/My net device/My node/Manager'
                        , ui_type_name = 'Person'
                        )
                      , Record
                        ( Class = 'Entity'
                        , attr = Entity `address`
                        , attrs =
                            [ Record
                              ( attr = String `street`
                              , full_name = 'wired_interface.my_net_device.my_node.address.street'
                              , id = 'wired_interface__my_net_device__my_node__address__street'
                              , name = 'street'
                              , sig_key = 3
                              , ui_name = 'Wired interface/My net device/My node/Address/Street'
                              )
                            , Record
                              ( attr = String `zip`
                              , full_name = 'wired_interface.my_net_device.my_node.address.zip'
                              , id = 'wired_interface__my_net_device__my_node__address__zip'
                              , name = 'zip'
                              , sig_key = 3
                              , ui_name = 'Wired interface/My net device/My node/Address/Zip code'
                              )
                            , Record
                              ( attr = String `city`
                              , full_name = 'wired_interface.my_net_device.my_node.address.city'
                              , id = 'wired_interface__my_net_device__my_node__address__city'
                              , name = 'city'
                              , sig_key = 3
                              , ui_name = 'Wired interface/My net device/My node/Address/City'
                              )
                            , Record
                              ( attr = String `country`
                              , full_name = 'wired_interface.my_net_device.my_node.address.country'
                              , id = 'wired_interface__my_net_device__my_node__address__country'
                              , name = 'country'
                              , sig_key = 3
                              , ui_name = 'Wired interface/My net device/My node/Address/Country'
                              )
                            , Record
                              ( attr = String `desc`
                              , full_name = 'wired_interface.my_net_device.my_node.address.desc'
                              , id = 'wired_interface__my_net_device__my_node__address__desc'
                              , name = 'desc'
                              , sig_key = 3
                              , ui_name = 'Wired interface/My net device/My node/Address/Description'
                              )
                            , Record
                              ( attr = String `region`
                              , full_name = 'wired_interface.my_net_device.my_node.address.region'
                              , id = 'wired_interface__my_net_device__my_node__address__region'
                              , name = 'region'
                              , sig_key = 3
                              , ui_name = 'Wired interface/My net device/My node/Address/Region'
                              )
                            ]
                        , full_name = 'wired_interface.my_net_device.my_node.address'
                        , id = 'wired_interface__my_net_device__my_node__address'
                        , name = 'address'
                        , sig_key = 2
                        , type_name = 'PAP.Address'
                        , ui_name = 'Wired interface/My net device/My node/Address'
                        , ui_type_name = 'Address'
                        )
                      , Record
                        ( attr = Text `desc`
                        , full_name = 'wired_interface.my_net_device.my_node.desc'
                        , id = 'wired_interface__my_net_device__my_node__desc'
                        , name = 'desc'
                        , sig_key = 3
                        , ui_name = 'Wired interface/My net device/My node/Description'
                        )
                      , Record
                        ( Class = 'Entity'
                        , attr = Entity `owner`
                        , children_np =
                            [ Record
                              ( Class = 'Entity'
                              , attr = Entity `owner`
                              , attrs =
                                  [ Record
                                    ( attr = String `name`
                                    , full_name = 'owner.name'
                                    , id = 'owner__name'
                                    , name = 'name'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Adhoc_Group]/Name'
                                    )
                                  ]
                              , full_name = 'owner'
                              , id = 'owner'
                              , name = 'owner'
                              , sig_key = 2
                              , type_name = 'PAP.Adhoc_Group'
                              , ui_name = 'Owner[Adhoc_Group]'
                              , ui_type_name = 'Adhoc_Group'
                              )
                            , Record
                              ( Class = 'Entity'
                              , attr = Entity `owner`
                              , attrs =
                                  [ Record
                                    ( attr = String `name`
                                    , full_name = 'owner.name'
                                    , id = 'owner__name'
                                    , name = 'name'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Association]/Name'
                                    )
                                  ]
                              , full_name = 'owner'
                              , id = 'owner'
                              , name = 'owner'
                              , sig_key = 2
                              , type_name = 'PAP.Association'
                              , ui_name = 'Owner[Association]'
                              , ui_type_name = 'Association'
                              )
                            , Record
                              ( Class = 'Entity'
                              , attr = Entity `owner`
                              , attrs =
                                  [ Record
                                    ( attr = String `name`
                                    , full_name = 'owner.name'
                                    , id = 'owner__name'
                                    , name = 'name'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Company]/Name'
                                    )
                                  , Record
                                    ( attr = String `registered_in`
                                    , full_name = 'owner.registered_in'
                                    , id = 'owner__registered_in'
                                    , name = 'registered_in'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Company]/Registered in'
                                    )
                                  ]
                              , full_name = 'owner'
                              , id = 'owner'
                              , name = 'owner'
                              , sig_key = 2
                              , type_name = 'PAP.Company'
                              , ui_name = 'Owner[Company]'
                              , ui_type_name = 'Company'
                              )
                            , Record
                              ( Class = 'Entity'
                              , attr = Entity `owner`
                              , attrs =
                                  [ Record
                                    ( attr = String `last_name`
                                    , full_name = 'owner.last_name'
                                    , id = 'owner__last_name'
                                    , name = 'last_name'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Person]/Last name'
                                    )
                                  , Record
                                    ( attr = String `first_name`
                                    , full_name = 'owner.first_name'
                                    , id = 'owner__first_name'
                                    , name = 'first_name'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Person]/First name'
                                    )
                                  , Record
                                    ( attr = String `middle_name`
                                    , full_name = 'owner.middle_name'
                                    , id = 'owner__middle_name'
                                    , name = 'middle_name'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Person]/Middle name'
                                    )
                                  , Record
                                    ( attr = String `title`
                                    , full_name = 'owner.title'
                                    , id = 'owner__title'
                                    , name = 'title'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Person]/Academic title'
                                    )
                                  ]
                              , full_name = 'owner'
                              , id = 'owner'
                              , name = 'owner'
                              , sig_key = 2
                              , type_name = 'PAP.Person'
                              , ui_name = 'Owner[Person]'
                              , ui_type_name = 'Person'
                              )
                            ]
                        , default_child = 'PAP.Person'
                        , full_name = 'wired_interface.my_net_device.my_node.owner'
                        , id = 'wired_interface__my_net_device__my_node__owner'
                        , name = 'owner'
                        , sig_key = 2
                        , type_name = 'PAP.Subject'
                        , ui_name = 'Wired interface/My net device/My node/Owner'
                        , ui_type_name = 'Subject'
                        )
                      , Record
                        ( attr = Position `position`
                        , attrs =
                            [ Record
                              ( attr = Angle `lat`
                              , full_name = 'wired_interface.my_net_device.my_node.position.lat'
                              , id = 'wired_interface__my_net_device__my_node__position__lat'
                              , name = 'lat'
                              , sig_key = 4
                              , ui_name = 'Wired interface/My net device/My node/Position/Latitude'
                              )
                            , Record
                              ( attr = Angle `lon`
                              , full_name = 'wired_interface.my_net_device.my_node.position.lon'
                              , id = 'wired_interface__my_net_device__my_node__position__lon'
                              , name = 'lon'
                              , sig_key = 4
                              , ui_name = 'Wired interface/My net device/My node/Position/Longitude'
                              )
                            , Record
                              ( attr = Float `height`
                              , full_name = 'wired_interface.my_net_device.my_node.position.height'
                              , id = 'wired_interface__my_net_device__my_node__position__height'
                              , name = 'height'
                              , sig_key = 0
                              , ui_name = 'Wired interface/My net device/My node/Position/Height'
                              )
                            ]
                        , full_name = 'wired_interface.my_net_device.my_node.position'
                        , id = 'wired_interface__my_net_device__my_node__position'
                        , name = 'position'
                        , ui_name = 'Wired interface/My net device/My node/Position'
                        )
                      , Record
                        ( attr = Boolean `show_in_map`
                        , choices = <Recursion on list...>
                        , full_name = 'wired_interface.my_net_device.my_node.show_in_map'
                        , id = 'wired_interface__my_net_device__my_node__show_in_map'
                        , name = 'show_in_map'
                        , sig_key = 1
                        , ui_name = 'Wired interface/My net device/My node/Show in map'
                        )
                      ]
                  , full_name = 'wired_interface.my_net_device.my_node'
                  , id = 'wired_interface__my_net_device__my_node'
                  , name = 'my_node'
                  , sig_key = 2
                  , type_name = 'FFM.Node'
                  , ui_name = 'Wired interface/My net device/My node'
                  , ui_type_name = 'Node'
                  )
                ]
            , full_name = 'wired_interface.my_net_device'
            , id = 'wired_interface__my_net_device'
            , name = 'my_net_device'
            , sig_key = 2
            , type_name = 'FFM.Net_Device'
            , ui_name = 'Wired interface/My net device'
            , ui_type_name = 'Net_Device'
            )
          ]
      , full_name = 'wired_interface'
      , id = 'wired_interface'
      , name = 'wired_interface'
      , sig_key = 2
      , type_name = 'FFM.Wired_Interface'
      , ui_name = 'Wired interface'
      , ui_type_name = 'Wired_Interface'
      )
    , Record
      ( Class = 'Entity'
      , attr = Role_Ref `wireless_interface`
      , attrs =
          [ Record
            ( Class = 'Entity'
            , attr = Net_Device `left`
            , attrs =
                [ Record
                  ( Class = 'Entity'
                  , attr = Net_Device_Type `left`
                  , attrs =
                      [ Record
                        ( attr = String `name`
                        , full_name = 'wireless_interface.left.left.name'
                        , id = 'wireless_interface__left__left__name'
                        , name = 'name'
                        , sig_key = 3
                        , ui_name = 'Wireless interface/Net device/Net device type/Name'
                        )
                      , Record
                        ( attr = String `model_no`
                        , full_name = 'wireless_interface.left.left.model_no'
                        , id = 'wireless_interface__left__left__model_no'
                        , name = 'model_no'
                        , sig_key = 3
                        , ui_name = 'Wireless interface/Net device/Net device type/Model no'
                        )
                      , Record
                        ( attr = String `revision`
                        , full_name = 'wireless_interface.left.left.revision'
                        , id = 'wireless_interface__left__left__revision'
                        , name = 'revision'
                        , sig_key = 3
                        , ui_name = 'Wireless interface/Net device/Net device type/Revision'
                        )
                      , Record
                        ( attr = Text `desc`
                        , full_name = 'wireless_interface.left.left.desc'
                        , id = 'wireless_interface__left__left__desc'
                        , name = 'desc'
                        , sig_key = 3
                        , ui_name = 'Wireless interface/Net device/Net device type/Description'
                        )
                      ]
                  , full_name = 'wireless_interface.left.left'
                  , id = 'wireless_interface__left__left'
                  , name = 'left'
                  , sig_key = 2
                  , type_name = 'FFM.Net_Device_Type'
                  , ui_name = 'Wireless interface/Net device/Net device type'
                  , ui_type_name = 'Net_Device_Type'
                  )
                , Record
                  ( Class = 'Entity'
                  , attr = Entity `node`
                  , attrs =
                      [ Record
                        ( attr = String `name`
                        , full_name = 'wireless_interface.left.node.name'
                        , id = 'wireless_interface__left__node__name'
                        , name = 'name'
                        , sig_key = 3
                        , ui_name = 'Wireless interface/Net device/Node/Name'
                        )
                      , Record
                        ( Class = 'Entity'
                        , attr = Entity `manager`
                        , attrs =
                            [ Record
                              ( attr = String `last_name`
                              , full_name = 'wireless_interface.left.node.manager.last_name'
                              , id = 'wireless_interface__left__node__manager__last_name'
                              , name = 'last_name'
                              , sig_key = 3
                              , ui_name = 'Wireless interface/Net device/Node/Manager/Last name'
                              )
                            , Record
                              ( attr = String `first_name`
                              , full_name = 'wireless_interface.left.node.manager.first_name'
                              , id = 'wireless_interface__left__node__manager__first_name'
                              , name = 'first_name'
                              , sig_key = 3
                              , ui_name = 'Wireless interface/Net device/Node/Manager/First name'
                              )
                            , Record
                              ( attr = String `middle_name`
                              , full_name = 'wireless_interface.left.node.manager.middle_name'
                              , id = 'wireless_interface__left__node__manager__middle_name'
                              , name = 'middle_name'
                              , sig_key = 3
                              , ui_name = 'Wireless interface/Net device/Node/Manager/Middle name'
                              )
                            , Record
                              ( attr = String `title`
                              , full_name = 'wireless_interface.left.node.manager.title'
                              , id = 'wireless_interface__left__node__manager__title'
                              , name = 'title'
                              , sig_key = 3
                              , ui_name = 'Wireless interface/Net device/Node/Manager/Academic title'
                              )
                            , Record
                              ( attr = Date_Interval `lifetime`
                              , attrs =
                                  [ Record
                                    ( attr = Date `start`
                                    , full_name = 'wireless_interface.left.node.manager.lifetime.start'
                                    , id = 'wireless_interface__left__node__manager__lifetime__start'
                                    , name = 'start'
                                    , sig_key = 0
                                    , ui_name = 'Wireless interface/Net device/Node/Manager/Lifetime/Start'
                                    )
                                  , Record
                                    ( attr = Date `finish`
                                    , full_name = 'wireless_interface.left.node.manager.lifetime.finish'
                                    , id = 'wireless_interface__left__node__manager__lifetime__finish'
                                    , name = 'finish'
                                    , sig_key = 0
                                    , ui_name = 'Wireless interface/Net device/Node/Manager/Lifetime/Finish'
                                    )
                                  , Record
                                    ( attr = Boolean `alive`
                                    , choices = <Recursion on list...>
                                    , full_name = 'wireless_interface.left.node.manager.lifetime.alive'
                                    , id = 'wireless_interface__left__node__manager__lifetime__alive'
                                    , name = 'alive'
                                    , sig_key = 1
                                    , ui_name = 'Wireless interface/Net device/Node/Manager/Lifetime/Alive'
                                    )
                                  ]
                              , full_name = 'wireless_interface.left.node.manager.lifetime'
                              , id = 'wireless_interface__left__node__manager__lifetime'
                              , name = 'lifetime'
                              , ui_name = 'Wireless interface/Net device/Node/Manager/Lifetime'
                              )
                            , Record
                              ( attr = Sex `sex`
                              , choices = <Recursion on list...>
                              , full_name = 'wireless_interface.left.node.manager.sex'
                              , id = 'wireless_interface__left__node__manager__sex'
                              , name = 'sex'
                              , sig_key = 0
                              , ui_name = 'Wireless interface/Net device/Node/Manager/Sex'
                              )
                            ]
                        , full_name = 'wireless_interface.left.node.manager'
                        , id = 'wireless_interface__left__node__manager'
                        , name = 'manager'
                        , sig_key = 2
                        , type_name = 'PAP.Person'
                        , ui_name = 'Wireless interface/Net device/Node/Manager'
                        , ui_type_name = 'Person'
                        )
                      , Record
                        ( Class = 'Entity'
                        , attr = Entity `address`
                        , attrs =
                            [ Record
                              ( attr = String `street`
                              , full_name = 'wireless_interface.left.node.address.street'
                              , id = 'wireless_interface__left__node__address__street'
                              , name = 'street'
                              , sig_key = 3
                              , ui_name = 'Wireless interface/Net device/Node/Address/Street'
                              )
                            , Record
                              ( attr = String `zip`
                              , full_name = 'wireless_interface.left.node.address.zip'
                              , id = 'wireless_interface__left__node__address__zip'
                              , name = 'zip'
                              , sig_key = 3
                              , ui_name = 'Wireless interface/Net device/Node/Address/Zip code'
                              )
                            , Record
                              ( attr = String `city`
                              , full_name = 'wireless_interface.left.node.address.city'
                              , id = 'wireless_interface__left__node__address__city'
                              , name = 'city'
                              , sig_key = 3
                              , ui_name = 'Wireless interface/Net device/Node/Address/City'
                              )
                            , Record
                              ( attr = String `country`
                              , full_name = 'wireless_interface.left.node.address.country'
                              , id = 'wireless_interface__left__node__address__country'
                              , name = 'country'
                              , sig_key = 3
                              , ui_name = 'Wireless interface/Net device/Node/Address/Country'
                              )
                            , Record
                              ( attr = String `desc`
                              , full_name = 'wireless_interface.left.node.address.desc'
                              , id = 'wireless_interface__left__node__address__desc'
                              , name = 'desc'
                              , sig_key = 3
                              , ui_name = 'Wireless interface/Net device/Node/Address/Description'
                              )
                            , Record
                              ( attr = String `region`
                              , full_name = 'wireless_interface.left.node.address.region'
                              , id = 'wireless_interface__left__node__address__region'
                              , name = 'region'
                              , sig_key = 3
                              , ui_name = 'Wireless interface/Net device/Node/Address/Region'
                              )
                            ]
                        , full_name = 'wireless_interface.left.node.address'
                        , id = 'wireless_interface__left__node__address'
                        , name = 'address'
                        , sig_key = 2
                        , type_name = 'PAP.Address'
                        , ui_name = 'Wireless interface/Net device/Node/Address'
                        , ui_type_name = 'Address'
                        )
                      , Record
                        ( attr = Text `desc`
                        , full_name = 'wireless_interface.left.node.desc'
                        , id = 'wireless_interface__left__node__desc'
                        , name = 'desc'
                        , sig_key = 3
                        , ui_name = 'Wireless interface/Net device/Node/Description'
                        )
                      , Record
                        ( Class = 'Entity'
                        , attr = Entity `owner`
                        , children_np =
                            [ Record
                              ( Class = 'Entity'
                              , attr = Entity `owner`
                              , attrs =
                                  [ Record
                                    ( attr = String `name`
                                    , full_name = 'owner.name'
                                    , id = 'owner__name'
                                    , name = 'name'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Adhoc_Group]/Name'
                                    )
                                  ]
                              , full_name = 'owner'
                              , id = 'owner'
                              , name = 'owner'
                              , sig_key = 2
                              , type_name = 'PAP.Adhoc_Group'
                              , ui_name = 'Owner[Adhoc_Group]'
                              , ui_type_name = 'Adhoc_Group'
                              )
                            , Record
                              ( Class = 'Entity'
                              , attr = Entity `owner`
                              , attrs =
                                  [ Record
                                    ( attr = String `name`
                                    , full_name = 'owner.name'
                                    , id = 'owner__name'
                                    , name = 'name'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Association]/Name'
                                    )
                                  ]
                              , full_name = 'owner'
                              , id = 'owner'
                              , name = 'owner'
                              , sig_key = 2
                              , type_name = 'PAP.Association'
                              , ui_name = 'Owner[Association]'
                              , ui_type_name = 'Association'
                              )
                            , Record
                              ( Class = 'Entity'
                              , attr = Entity `owner`
                              , attrs =
                                  [ Record
                                    ( attr = String `name`
                                    , full_name = 'owner.name'
                                    , id = 'owner__name'
                                    , name = 'name'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Company]/Name'
                                    )
                                  , Record
                                    ( attr = String `registered_in`
                                    , full_name = 'owner.registered_in'
                                    , id = 'owner__registered_in'
                                    , name = 'registered_in'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Company]/Registered in'
                                    )
                                  ]
                              , full_name = 'owner'
                              , id = 'owner'
                              , name = 'owner'
                              , sig_key = 2
                              , type_name = 'PAP.Company'
                              , ui_name = 'Owner[Company]'
                              , ui_type_name = 'Company'
                              )
                            , Record
                              ( Class = 'Entity'
                              , attr = Entity `owner`
                              , attrs =
                                  [ Record
                                    ( attr = String `last_name`
                                    , full_name = 'owner.last_name'
                                    , id = 'owner__last_name'
                                    , name = 'last_name'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Person]/Last name'
                                    )
                                  , Record
                                    ( attr = String `first_name`
                                    , full_name = 'owner.first_name'
                                    , id = 'owner__first_name'
                                    , name = 'first_name'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Person]/First name'
                                    )
                                  , Record
                                    ( attr = String `middle_name`
                                    , full_name = 'owner.middle_name'
                                    , id = 'owner__middle_name'
                                    , name = 'middle_name'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Person]/Middle name'
                                    )
                                  , Record
                                    ( attr = String `title`
                                    , full_name = 'owner.title'
                                    , id = 'owner__title'
                                    , name = 'title'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Person]/Academic title'
                                    )
                                  ]
                              , full_name = 'owner'
                              , id = 'owner'
                              , name = 'owner'
                              , sig_key = 2
                              , type_name = 'PAP.Person'
                              , ui_name = 'Owner[Person]'
                              , ui_type_name = 'Person'
                              )
                            ]
                        , default_child = 'PAP.Person'
                        , full_name = 'wireless_interface.left.node.owner'
                        , id = 'wireless_interface__left__node__owner'
                        , name = 'owner'
                        , sig_key = 2
                        , type_name = 'PAP.Subject'
                        , ui_name = 'Wireless interface/Net device/Node/Owner'
                        , ui_type_name = 'Subject'
                        )
                      , Record
                        ( attr = Position `position`
                        , attrs =
                            [ Record
                              ( attr = Angle `lat`
                              , full_name = 'wireless_interface.left.node.position.lat'
                              , id = 'wireless_interface__left__node__position__lat'
                              , name = 'lat'
                              , sig_key = 4
                              , ui_name = 'Wireless interface/Net device/Node/Position/Latitude'
                              )
                            , Record
                              ( attr = Angle `lon`
                              , full_name = 'wireless_interface.left.node.position.lon'
                              , id = 'wireless_interface__left__node__position__lon'
                              , name = 'lon'
                              , sig_key = 4
                              , ui_name = 'Wireless interface/Net device/Node/Position/Longitude'
                              )
                            , Record
                              ( attr = Float `height`
                              , full_name = 'wireless_interface.left.node.position.height'
                              , id = 'wireless_interface__left__node__position__height'
                              , name = 'height'
                              , sig_key = 0
                              , ui_name = 'Wireless interface/Net device/Node/Position/Height'
                              )
                            ]
                        , full_name = 'wireless_interface.left.node.position'
                        , id = 'wireless_interface__left__node__position'
                        , name = 'position'
                        , ui_name = 'Wireless interface/Net device/Node/Position'
                        )
                      , Record
                        ( attr = Boolean `show_in_map`
                        , choices = <Recursion on list...>
                        , full_name = 'wireless_interface.left.node.show_in_map'
                        , id = 'wireless_interface__left__node__show_in_map'
                        , name = 'show_in_map'
                        , sig_key = 1
                        , ui_name = 'Wireless interface/Net device/Node/Show in map'
                        )
                      ]
                  , full_name = 'wireless_interface.left.node'
                  , id = 'wireless_interface__left__node'
                  , name = 'node'
                  , sig_key = 2
                  , type_name = 'FFM.Node'
                  , ui_name = 'Wireless interface/Net device/Node'
                  , ui_type_name = 'Node'
                  )
                , Record
                  ( attr = String `name`
                  , full_name = 'wireless_interface.left.name'
                  , id = 'wireless_interface__left__name'
                  , name = 'name'
                  , sig_key = 3
                  , ui_name = 'Wireless interface/Net device/Name'
                  )
                , Record
                  ( attr = Text `desc`
                  , full_name = 'wireless_interface.left.desc'
                  , id = 'wireless_interface__left__desc'
                  , name = 'desc'
                  , sig_key = 3
                  , ui_name = 'Wireless interface/Net device/Description'
                  )
                , Record
                  ( Class = 'Entity'
                  , attr = Entity `my_node`
                  , attrs =
                      [ Record
                        ( attr = String `name`
                        , full_name = 'wireless_interface.left.my_node.name'
                        , id = 'wireless_interface__left__my_node__name'
                        , name = 'name'
                        , sig_key = 3
                        , ui_name = 'Wireless interface/Net device/My node/Name'
                        )
                      , Record
                        ( Class = 'Entity'
                        , attr = Entity `manager`
                        , attrs =
                            [ Record
                              ( attr = String `last_name`
                              , full_name = 'wireless_interface.left.my_node.manager.last_name'
                              , id = 'wireless_interface__left__my_node__manager__last_name'
                              , name = 'last_name'
                              , sig_key = 3
                              , ui_name = 'Wireless interface/Net device/My node/Manager/Last name'
                              )
                            , Record
                              ( attr = String `first_name`
                              , full_name = 'wireless_interface.left.my_node.manager.first_name'
                              , id = 'wireless_interface__left__my_node__manager__first_name'
                              , name = 'first_name'
                              , sig_key = 3
                              , ui_name = 'Wireless interface/Net device/My node/Manager/First name'
                              )
                            , Record
                              ( attr = String `middle_name`
                              , full_name = 'wireless_interface.left.my_node.manager.middle_name'
                              , id = 'wireless_interface__left__my_node__manager__middle_name'
                              , name = 'middle_name'
                              , sig_key = 3
                              , ui_name = 'Wireless interface/Net device/My node/Manager/Middle name'
                              )
                            , Record
                              ( attr = String `title`
                              , full_name = 'wireless_interface.left.my_node.manager.title'
                              , id = 'wireless_interface__left__my_node__manager__title'
                              , name = 'title'
                              , sig_key = 3
                              , ui_name = 'Wireless interface/Net device/My node/Manager/Academic title'
                              )
                            , Record
                              ( attr = Date_Interval `lifetime`
                              , attrs =
                                  [ Record
                                    ( attr = Date `start`
                                    , full_name = 'wireless_interface.left.my_node.manager.lifetime.start'
                                    , id = 'wireless_interface__left__my_node__manager__lifetime__start'
                                    , name = 'start'
                                    , sig_key = 0
                                    , ui_name = 'Wireless interface/Net device/My node/Manager/Lifetime/Start'
                                    )
                                  , Record
                                    ( attr = Date `finish`
                                    , full_name = 'wireless_interface.left.my_node.manager.lifetime.finish'
                                    , id = 'wireless_interface__left__my_node__manager__lifetime__finish'
                                    , name = 'finish'
                                    , sig_key = 0
                                    , ui_name = 'Wireless interface/Net device/My node/Manager/Lifetime/Finish'
                                    )
                                  , Record
                                    ( attr = Boolean `alive`
                                    , choices = <Recursion on list...>
                                    , full_name = 'wireless_interface.left.my_node.manager.lifetime.alive'
                                    , id = 'wireless_interface__left__my_node__manager__lifetime__alive'
                                    , name = 'alive'
                                    , sig_key = 1
                                    , ui_name = 'Wireless interface/Net device/My node/Manager/Lifetime/Alive'
                                    )
                                  ]
                              , full_name = 'wireless_interface.left.my_node.manager.lifetime'
                              , id = 'wireless_interface__left__my_node__manager__lifetime'
                              , name = 'lifetime'
                              , ui_name = 'Wireless interface/Net device/My node/Manager/Lifetime'
                              )
                            , Record
                              ( attr = Sex `sex`
                              , choices = <Recursion on list...>
                              , full_name = 'wireless_interface.left.my_node.manager.sex'
                              , id = 'wireless_interface__left__my_node__manager__sex'
                              , name = 'sex'
                              , sig_key = 0
                              , ui_name = 'Wireless interface/Net device/My node/Manager/Sex'
                              )
                            ]
                        , full_name = 'wireless_interface.left.my_node.manager'
                        , id = 'wireless_interface__left__my_node__manager'
                        , name = 'manager'
                        , sig_key = 2
                        , type_name = 'PAP.Person'
                        , ui_name = 'Wireless interface/Net device/My node/Manager'
                        , ui_type_name = 'Person'
                        )
                      , Record
                        ( Class = 'Entity'
                        , attr = Entity `address`
                        , attrs =
                            [ Record
                              ( attr = String `street`
                              , full_name = 'wireless_interface.left.my_node.address.street'
                              , id = 'wireless_interface__left__my_node__address__street'
                              , name = 'street'
                              , sig_key = 3
                              , ui_name = 'Wireless interface/Net device/My node/Address/Street'
                              )
                            , Record
                              ( attr = String `zip`
                              , full_name = 'wireless_interface.left.my_node.address.zip'
                              , id = 'wireless_interface__left__my_node__address__zip'
                              , name = 'zip'
                              , sig_key = 3
                              , ui_name = 'Wireless interface/Net device/My node/Address/Zip code'
                              )
                            , Record
                              ( attr = String `city`
                              , full_name = 'wireless_interface.left.my_node.address.city'
                              , id = 'wireless_interface__left__my_node__address__city'
                              , name = 'city'
                              , sig_key = 3
                              , ui_name = 'Wireless interface/Net device/My node/Address/City'
                              )
                            , Record
                              ( attr = String `country`
                              , full_name = 'wireless_interface.left.my_node.address.country'
                              , id = 'wireless_interface__left__my_node__address__country'
                              , name = 'country'
                              , sig_key = 3
                              , ui_name = 'Wireless interface/Net device/My node/Address/Country'
                              )
                            , Record
                              ( attr = String `desc`
                              , full_name = 'wireless_interface.left.my_node.address.desc'
                              , id = 'wireless_interface__left__my_node__address__desc'
                              , name = 'desc'
                              , sig_key = 3
                              , ui_name = 'Wireless interface/Net device/My node/Address/Description'
                              )
                            , Record
                              ( attr = String `region`
                              , full_name = 'wireless_interface.left.my_node.address.region'
                              , id = 'wireless_interface__left__my_node__address__region'
                              , name = 'region'
                              , sig_key = 3
                              , ui_name = 'Wireless interface/Net device/My node/Address/Region'
                              )
                            ]
                        , full_name = 'wireless_interface.left.my_node.address'
                        , id = 'wireless_interface__left__my_node__address'
                        , name = 'address'
                        , sig_key = 2
                        , type_name = 'PAP.Address'
                        , ui_name = 'Wireless interface/Net device/My node/Address'
                        , ui_type_name = 'Address'
                        )
                      , Record
                        ( attr = Text `desc`
                        , full_name = 'wireless_interface.left.my_node.desc'
                        , id = 'wireless_interface__left__my_node__desc'
                        , name = 'desc'
                        , sig_key = 3
                        , ui_name = 'Wireless interface/Net device/My node/Description'
                        )
                      , Record
                        ( Class = 'Entity'
                        , attr = Entity `owner`
                        , children_np =
                            [ Record
                              ( Class = 'Entity'
                              , attr = Entity `owner`
                              , attrs =
                                  [ Record
                                    ( attr = String `name`
                                    , full_name = 'owner.name'
                                    , id = 'owner__name'
                                    , name = 'name'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Adhoc_Group]/Name'
                                    )
                                  ]
                              , full_name = 'owner'
                              , id = 'owner'
                              , name = 'owner'
                              , sig_key = 2
                              , type_name = 'PAP.Adhoc_Group'
                              , ui_name = 'Owner[Adhoc_Group]'
                              , ui_type_name = 'Adhoc_Group'
                              )
                            , Record
                              ( Class = 'Entity'
                              , attr = Entity `owner`
                              , attrs =
                                  [ Record
                                    ( attr = String `name`
                                    , full_name = 'owner.name'
                                    , id = 'owner__name'
                                    , name = 'name'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Association]/Name'
                                    )
                                  ]
                              , full_name = 'owner'
                              , id = 'owner'
                              , name = 'owner'
                              , sig_key = 2
                              , type_name = 'PAP.Association'
                              , ui_name = 'Owner[Association]'
                              , ui_type_name = 'Association'
                              )
                            , Record
                              ( Class = 'Entity'
                              , attr = Entity `owner`
                              , attrs =
                                  [ Record
                                    ( attr = String `name`
                                    , full_name = 'owner.name'
                                    , id = 'owner__name'
                                    , name = 'name'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Company]/Name'
                                    )
                                  , Record
                                    ( attr = String `registered_in`
                                    , full_name = 'owner.registered_in'
                                    , id = 'owner__registered_in'
                                    , name = 'registered_in'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Company]/Registered in'
                                    )
                                  ]
                              , full_name = 'owner'
                              , id = 'owner'
                              , name = 'owner'
                              , sig_key = 2
                              , type_name = 'PAP.Company'
                              , ui_name = 'Owner[Company]'
                              , ui_type_name = 'Company'
                              )
                            , Record
                              ( Class = 'Entity'
                              , attr = Entity `owner`
                              , attrs =
                                  [ Record
                                    ( attr = String `last_name`
                                    , full_name = 'owner.last_name'
                                    , id = 'owner__last_name'
                                    , name = 'last_name'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Person]/Last name'
                                    )
                                  , Record
                                    ( attr = String `first_name`
                                    , full_name = 'owner.first_name'
                                    , id = 'owner__first_name'
                                    , name = 'first_name'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Person]/First name'
                                    )
                                  , Record
                                    ( attr = String `middle_name`
                                    , full_name = 'owner.middle_name'
                                    , id = 'owner__middle_name'
                                    , name = 'middle_name'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Person]/Middle name'
                                    )
                                  , Record
                                    ( attr = String `title`
                                    , full_name = 'owner.title'
                                    , id = 'owner__title'
                                    , name = 'title'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Person]/Academic title'
                                    )
                                  ]
                              , full_name = 'owner'
                              , id = 'owner'
                              , name = 'owner'
                              , sig_key = 2
                              , type_name = 'PAP.Person'
                              , ui_name = 'Owner[Person]'
                              , ui_type_name = 'Person'
                              )
                            ]
                        , default_child = 'PAP.Person'
                        , full_name = 'wireless_interface.left.my_node.owner'
                        , id = 'wireless_interface__left__my_node__owner'
                        , name = 'owner'
                        , sig_key = 2
                        , type_name = 'PAP.Subject'
                        , ui_name = 'Wireless interface/Net device/My node/Owner'
                        , ui_type_name = 'Subject'
                        )
                      , Record
                        ( attr = Position `position`
                        , attrs =
                            [ Record
                              ( attr = Angle `lat`
                              , full_name = 'wireless_interface.left.my_node.position.lat'
                              , id = 'wireless_interface__left__my_node__position__lat'
                              , name = 'lat'
                              , sig_key = 4
                              , ui_name = 'Wireless interface/Net device/My node/Position/Latitude'
                              )
                            , Record
                              ( attr = Angle `lon`
                              , full_name = 'wireless_interface.left.my_node.position.lon'
                              , id = 'wireless_interface__left__my_node__position__lon'
                              , name = 'lon'
                              , sig_key = 4
                              , ui_name = 'Wireless interface/Net device/My node/Position/Longitude'
                              )
                            , Record
                              ( attr = Float `height`
                              , full_name = 'wireless_interface.left.my_node.position.height'
                              , id = 'wireless_interface__left__my_node__position__height'
                              , name = 'height'
                              , sig_key = 0
                              , ui_name = 'Wireless interface/Net device/My node/Position/Height'
                              )
                            ]
                        , full_name = 'wireless_interface.left.my_node.position'
                        , id = 'wireless_interface__left__my_node__position'
                        , name = 'position'
                        , ui_name = 'Wireless interface/Net device/My node/Position'
                        )
                      , Record
                        ( attr = Boolean `show_in_map`
                        , choices = <Recursion on list...>
                        , full_name = 'wireless_interface.left.my_node.show_in_map'
                        , id = 'wireless_interface__left__my_node__show_in_map'
                        , name = 'show_in_map'
                        , sig_key = 1
                        , ui_name = 'Wireless interface/Net device/My node/Show in map'
                        )
                      ]
                  , full_name = 'wireless_interface.left.my_node'
                  , id = 'wireless_interface__left__my_node'
                  , name = 'my_node'
                  , sig_key = 2
                  , type_name = 'FFM.Node'
                  , ui_name = 'Wireless interface/Net device/My node'
                  , ui_type_name = 'Node'
                  )
                ]
            , full_name = 'wireless_interface.left'
            , id = 'wireless_interface__left'
            , name = 'left'
            , sig_key = 2
            , type_name = 'FFM.Net_Device'
            , ui_name = 'Wireless interface/Net device'
            , ui_type_name = 'Net_Device'
            )
          , Record
            ( attr = MAC-address `mac_address`
            , full_name = 'wireless_interface.mac_address'
            , id = 'wireless_interface__mac_address'
            , name = 'mac_address'
            , sig_key = 3
            , ui_name = 'Wireless interface/Mac address'
            )
          , Record
            ( attr = String `name`
            , full_name = 'wireless_interface.name'
            , id = 'wireless_interface__name'
            , name = 'name'
            , sig_key = 3
            , ui_name = 'Wireless interface/Name'
            )
          , Record
            ( attr = Boolean `is_active`
            , choices = <Recursion on list...>
            , full_name = 'wireless_interface.is_active'
            , id = 'wireless_interface__is_active'
            , name = 'is_active'
            , sig_key = 1
            , ui_name = 'Wireless interface/Is active'
            )
          , Record
            ( attr = Text `desc`
            , full_name = 'wireless_interface.desc'
            , id = 'wireless_interface__desc'
            , name = 'desc'
            , sig_key = 3
            , ui_name = 'Wireless interface/Description'
            )
          , Record
            ( attr = wl-mode `mode`
            , choices =
                [
                  ( 'AP'
                  , 'AP'
                  )
                ,
                  ( 'Ad_Hoc'
                  , 'Ad_Hoc'
                  )
                ,
                  ( 'Client'
                  , 'Client'
                  )
                ]
            , full_name = 'wireless_interface.mode'
            , id = 'wireless_interface__mode'
            , name = 'mode'
            , sig_key = 0
            , ui_name = 'Wireless interface/Mode'
            )
          , Record
            ( attr = String `essid`
            , full_name = 'wireless_interface.essid'
            , id = 'wireless_interface__essid'
            , name = 'essid'
            , sig_key = 3
            , ui_name = 'Wireless interface/ESSID'
            )
          , Record
            ( attr = MAC-address `bssid`
            , full_name = 'wireless_interface.bssid'
            , id = 'wireless_interface__bssid'
            , name = 'bssid'
            , sig_key = 3
            , ui_name = 'Wireless interface/BSSID'
            )
          , Record
            ( Class = 'Entity'
            , attr = Entity `standard`
            , attrs =
                [ Record
                  ( attr = String `name`
                  , full_name = 'wireless_interface.standard.name'
                  , id = 'wireless_interface__standard__name'
                  , name = 'name'
                  , sig_key = 3
                  , ui_name = 'Wireless interface/Standard/Name'
                  )
                , Record
                  ( attr = Frequency `bandwidth`
                  , full_name = 'wireless_interface.standard.bandwidth'
                  , id = 'wireless_interface__standard__bandwidth'
                  , name = 'bandwidth'
                  , sig_key = 4
                  , ui_name = 'Wireless interface/Standard/Bandwidth'
                  )
                ]
            , full_name = 'wireless_interface.standard'
            , id = 'wireless_interface__standard'
            , name = 'standard'
            , sig_key = 2
            , type_name = 'FFM.Wireless_Standard'
            , ui_name = 'Wireless interface/Standard'
            , ui_type_name = 'Wireless_Standard'
            )
          , Record
            ( attr = TX Power `txpower`
            , full_name = 'wireless_interface.txpower'
            , id = 'wireless_interface__txpower'
            , name = 'txpower'
            , sig_key = 4
            , ui_name = 'Wireless interface/TX power'
            )
          , Record
            ( Class = 'Entity'
            , attr = Entity `my_node`
            , attrs =
                [ Record
                  ( attr = String `name`
                  , full_name = 'wireless_interface.my_node.name'
                  , id = 'wireless_interface__my_node__name'
                  , name = 'name'
                  , sig_key = 3
                  , ui_name = 'Wireless interface/My node/Name'
                  )
                , Record
                  ( Class = 'Entity'
                  , attr = Entity `manager`
                  , attrs =
                      [ Record
                        ( attr = String `last_name`
                        , full_name = 'wireless_interface.my_node.manager.last_name'
                        , id = 'wireless_interface__my_node__manager__last_name'
                        , name = 'last_name'
                        , sig_key = 3
                        , ui_name = 'Wireless interface/My node/Manager/Last name'
                        )
                      , Record
                        ( attr = String `first_name`
                        , full_name = 'wireless_interface.my_node.manager.first_name'
                        , id = 'wireless_interface__my_node__manager__first_name'
                        , name = 'first_name'
                        , sig_key = 3
                        , ui_name = 'Wireless interface/My node/Manager/First name'
                        )
                      , Record
                        ( attr = String `middle_name`
                        , full_name = 'wireless_interface.my_node.manager.middle_name'
                        , id = 'wireless_interface__my_node__manager__middle_name'
                        , name = 'middle_name'
                        , sig_key = 3
                        , ui_name = 'Wireless interface/My node/Manager/Middle name'
                        )
                      , Record
                        ( attr = String `title`
                        , full_name = 'wireless_interface.my_node.manager.title'
                        , id = 'wireless_interface__my_node__manager__title'
                        , name = 'title'
                        , sig_key = 3
                        , ui_name = 'Wireless interface/My node/Manager/Academic title'
                        )
                      , Record
                        ( attr = Date_Interval `lifetime`
                        , attrs =
                            [ Record
                              ( attr = Date `start`
                              , full_name = 'wireless_interface.my_node.manager.lifetime.start'
                              , id = 'wireless_interface__my_node__manager__lifetime__start'
                              , name = 'start'
                              , sig_key = 0
                              , ui_name = 'Wireless interface/My node/Manager/Lifetime/Start'
                              )
                            , Record
                              ( attr = Date `finish`
                              , full_name = 'wireless_interface.my_node.manager.lifetime.finish'
                              , id = 'wireless_interface__my_node__manager__lifetime__finish'
                              , name = 'finish'
                              , sig_key = 0
                              , ui_name = 'Wireless interface/My node/Manager/Lifetime/Finish'
                              )
                            , Record
                              ( attr = Boolean `alive`
                              , choices = <Recursion on list...>
                              , full_name = 'wireless_interface.my_node.manager.lifetime.alive'
                              , id = 'wireless_interface__my_node__manager__lifetime__alive'
                              , name = 'alive'
                              , sig_key = 1
                              , ui_name = 'Wireless interface/My node/Manager/Lifetime/Alive'
                              )
                            ]
                        , full_name = 'wireless_interface.my_node.manager.lifetime'
                        , id = 'wireless_interface__my_node__manager__lifetime'
                        , name = 'lifetime'
                        , ui_name = 'Wireless interface/My node/Manager/Lifetime'
                        )
                      , Record
                        ( attr = Sex `sex`
                        , choices = <Recursion on list...>
                        , full_name = 'wireless_interface.my_node.manager.sex'
                        , id = 'wireless_interface__my_node__manager__sex'
                        , name = 'sex'
                        , sig_key = 0
                        , ui_name = 'Wireless interface/My node/Manager/Sex'
                        )
                      ]
                  , full_name = 'wireless_interface.my_node.manager'
                  , id = 'wireless_interface__my_node__manager'
                  , name = 'manager'
                  , sig_key = 2
                  , type_name = 'PAP.Person'
                  , ui_name = 'Wireless interface/My node/Manager'
                  , ui_type_name = 'Person'
                  )
                , Record
                  ( Class = 'Entity'
                  , attr = Entity `address`
                  , attrs =
                      [ Record
                        ( attr = String `street`
                        , full_name = 'wireless_interface.my_node.address.street'
                        , id = 'wireless_interface__my_node__address__street'
                        , name = 'street'
                        , sig_key = 3
                        , ui_name = 'Wireless interface/My node/Address/Street'
                        )
                      , Record
                        ( attr = String `zip`
                        , full_name = 'wireless_interface.my_node.address.zip'
                        , id = 'wireless_interface__my_node__address__zip'
                        , name = 'zip'
                        , sig_key = 3
                        , ui_name = 'Wireless interface/My node/Address/Zip code'
                        )
                      , Record
                        ( attr = String `city`
                        , full_name = 'wireless_interface.my_node.address.city'
                        , id = 'wireless_interface__my_node__address__city'
                        , name = 'city'
                        , sig_key = 3
                        , ui_name = 'Wireless interface/My node/Address/City'
                        )
                      , Record
                        ( attr = String `country`
                        , full_name = 'wireless_interface.my_node.address.country'
                        , id = 'wireless_interface__my_node__address__country'
                        , name = 'country'
                        , sig_key = 3
                        , ui_name = 'Wireless interface/My node/Address/Country'
                        )
                      , Record
                        ( attr = String `desc`
                        , full_name = 'wireless_interface.my_node.address.desc'
                        , id = 'wireless_interface__my_node__address__desc'
                        , name = 'desc'
                        , sig_key = 3
                        , ui_name = 'Wireless interface/My node/Address/Description'
                        )
                      , Record
                        ( attr = String `region`
                        , full_name = 'wireless_interface.my_node.address.region'
                        , id = 'wireless_interface__my_node__address__region'
                        , name = 'region'
                        , sig_key = 3
                        , ui_name = 'Wireless interface/My node/Address/Region'
                        )
                      ]
                  , full_name = 'wireless_interface.my_node.address'
                  , id = 'wireless_interface__my_node__address'
                  , name = 'address'
                  , sig_key = 2
                  , type_name = 'PAP.Address'
                  , ui_name = 'Wireless interface/My node/Address'
                  , ui_type_name = 'Address'
                  )
                , Record
                  ( attr = Text `desc`
                  , full_name = 'wireless_interface.my_node.desc'
                  , id = 'wireless_interface__my_node__desc'
                  , name = 'desc'
                  , sig_key = 3
                  , ui_name = 'Wireless interface/My node/Description'
                  )
                , Record
                  ( Class = 'Entity'
                  , attr = Entity `owner`
                  , children_np =
                      [ Record
                        ( Class = 'Entity'
                        , attr = Entity `owner`
                        , attrs =
                            [ Record
                              ( attr = String `name`
                              , full_name = 'owner.name'
                              , id = 'owner__name'
                              , name = 'name'
                              , sig_key = 3
                              , ui_name = 'Owner[Adhoc_Group]/Name'
                              )
                            ]
                        , full_name = 'owner'
                        , id = 'owner'
                        , name = 'owner'
                        , sig_key = 2
                        , type_name = 'PAP.Adhoc_Group'
                        , ui_name = 'Owner[Adhoc_Group]'
                        , ui_type_name = 'Adhoc_Group'
                        )
                      , Record
                        ( Class = 'Entity'
                        , attr = Entity `owner`
                        , attrs =
                            [ Record
                              ( attr = String `name`
                              , full_name = 'owner.name'
                              , id = 'owner__name'
                              , name = 'name'
                              , sig_key = 3
                              , ui_name = 'Owner[Association]/Name'
                              )
                            ]
                        , full_name = 'owner'
                        , id = 'owner'
                        , name = 'owner'
                        , sig_key = 2
                        , type_name = 'PAP.Association'
                        , ui_name = 'Owner[Association]'
                        , ui_type_name = 'Association'
                        )
                      , Record
                        ( Class = 'Entity'
                        , attr = Entity `owner`
                        , attrs =
                            [ Record
                              ( attr = String `name`
                              , full_name = 'owner.name'
                              , id = 'owner__name'
                              , name = 'name'
                              , sig_key = 3
                              , ui_name = 'Owner[Company]/Name'
                              )
                            , Record
                              ( attr = String `registered_in`
                              , full_name = 'owner.registered_in'
                              , id = 'owner__registered_in'
                              , name = 'registered_in'
                              , sig_key = 3
                              , ui_name = 'Owner[Company]/Registered in'
                              )
                            ]
                        , full_name = 'owner'
                        , id = 'owner'
                        , name = 'owner'
                        , sig_key = 2
                        , type_name = 'PAP.Company'
                        , ui_name = 'Owner[Company]'
                        , ui_type_name = 'Company'
                        )
                      , Record
                        ( Class = 'Entity'
                        , attr = Entity `owner`
                        , attrs =
                            [ Record
                              ( attr = String `last_name`
                              , full_name = 'owner.last_name'
                              , id = 'owner__last_name'
                              , name = 'last_name'
                              , sig_key = 3
                              , ui_name = 'Owner[Person]/Last name'
                              )
                            , Record
                              ( attr = String `first_name`
                              , full_name = 'owner.first_name'
                              , id = 'owner__first_name'
                              , name = 'first_name'
                              , sig_key = 3
                              , ui_name = 'Owner[Person]/First name'
                              )
                            , Record
                              ( attr = String `middle_name`
                              , full_name = 'owner.middle_name'
                              , id = 'owner__middle_name'
                              , name = 'middle_name'
                              , sig_key = 3
                              , ui_name = 'Owner[Person]/Middle name'
                              )
                            , Record
                              ( attr = String `title`
                              , full_name = 'owner.title'
                              , id = 'owner__title'
                              , name = 'title'
                              , sig_key = 3
                              , ui_name = 'Owner[Person]/Academic title'
                              )
                            ]
                        , full_name = 'owner'
                        , id = 'owner'
                        , name = 'owner'
                        , sig_key = 2
                        , type_name = 'PAP.Person'
                        , ui_name = 'Owner[Person]'
                        , ui_type_name = 'Person'
                        )
                      ]
                  , default_child = 'PAP.Person'
                  , full_name = 'wireless_interface.my_node.owner'
                  , id = 'wireless_interface__my_node__owner'
                  , name = 'owner'
                  , sig_key = 2
                  , type_name = 'PAP.Subject'
                  , ui_name = 'Wireless interface/My node/Owner'
                  , ui_type_name = 'Subject'
                  )
                , Record
                  ( attr = Position `position`
                  , attrs =
                      [ Record
                        ( attr = Angle `lat`
                        , full_name = 'wireless_interface.my_node.position.lat'
                        , id = 'wireless_interface__my_node__position__lat'
                        , name = 'lat'
                        , sig_key = 4
                        , ui_name = 'Wireless interface/My node/Position/Latitude'
                        )
                      , Record
                        ( attr = Angle `lon`
                        , full_name = 'wireless_interface.my_node.position.lon'
                        , id = 'wireless_interface__my_node__position__lon'
                        , name = 'lon'
                        , sig_key = 4
                        , ui_name = 'Wireless interface/My node/Position/Longitude'
                        )
                      , Record
                        ( attr = Float `height`
                        , full_name = 'wireless_interface.my_node.position.height'
                        , id = 'wireless_interface__my_node__position__height'
                        , name = 'height'
                        , sig_key = 0
                        , ui_name = 'Wireless interface/My node/Position/Height'
                        )
                      ]
                  , full_name = 'wireless_interface.my_node.position'
                  , id = 'wireless_interface__my_node__position'
                  , name = 'position'
                  , ui_name = 'Wireless interface/My node/Position'
                  )
                , Record
                  ( attr = Boolean `show_in_map`
                  , choices = <Recursion on list...>
                  , full_name = 'wireless_interface.my_node.show_in_map'
                  , id = 'wireless_interface__my_node__show_in_map'
                  , name = 'show_in_map'
                  , sig_key = 1
                  , ui_name = 'Wireless interface/My node/Show in map'
                  )
                ]
            , full_name = 'wireless_interface.my_node'
            , id = 'wireless_interface__my_node'
            , name = 'my_node'
            , sig_key = 2
            , type_name = 'FFM.Node'
            , ui_name = 'Wireless interface/My node'
            , ui_type_name = 'Node'
            )
          , Record
            ( Class = 'Entity'
            , attr = Entity `my_net_device`
            , attrs =
                [ Record
                  ( Class = 'Entity'
                  , attr = Net_Device_Type `left`
                  , attrs =
                      [ Record
                        ( attr = String `name`
                        , full_name = 'wireless_interface.my_net_device.left.name'
                        , id = 'wireless_interface__my_net_device__left__name'
                        , name = 'name'
                        , sig_key = 3
                        , ui_name = 'Wireless interface/My net device/Net device type/Name'
                        )
                      , Record
                        ( attr = String `model_no`
                        , full_name = 'wireless_interface.my_net_device.left.model_no'
                        , id = 'wireless_interface__my_net_device__left__model_no'
                        , name = 'model_no'
                        , sig_key = 3
                        , ui_name = 'Wireless interface/My net device/Net device type/Model no'
                        )
                      , Record
                        ( attr = String `revision`
                        , full_name = 'wireless_interface.my_net_device.left.revision'
                        , id = 'wireless_interface__my_net_device__left__revision'
                        , name = 'revision'
                        , sig_key = 3
                        , ui_name = 'Wireless interface/My net device/Net device type/Revision'
                        )
                      , Record
                        ( attr = Text `desc`
                        , full_name = 'wireless_interface.my_net_device.left.desc'
                        , id = 'wireless_interface__my_net_device__left__desc'
                        , name = 'desc'
                        , sig_key = 3
                        , ui_name = 'Wireless interface/My net device/Net device type/Description'
                        )
                      ]
                  , full_name = 'wireless_interface.my_net_device.left'
                  , id = 'wireless_interface__my_net_device__left'
                  , name = 'left'
                  , sig_key = 2
                  , type_name = 'FFM.Net_Device_Type'
                  , ui_name = 'Wireless interface/My net device/Net device type'
                  , ui_type_name = 'Net_Device_Type'
                  )
                , Record
                  ( Class = 'Entity'
                  , attr = Entity `node`
                  , attrs =
                      [ Record
                        ( attr = String `name`
                        , full_name = 'wireless_interface.my_net_device.node.name'
                        , id = 'wireless_interface__my_net_device__node__name'
                        , name = 'name'
                        , sig_key = 3
                        , ui_name = 'Wireless interface/My net device/Node/Name'
                        )
                      , Record
                        ( Class = 'Entity'
                        , attr = Entity `manager`
                        , attrs =
                            [ Record
                              ( attr = String `last_name`
                              , full_name = 'wireless_interface.my_net_device.node.manager.last_name'
                              , id = 'wireless_interface__my_net_device__node__manager__last_name'
                              , name = 'last_name'
                              , sig_key = 3
                              , ui_name = 'Wireless interface/My net device/Node/Manager/Last name'
                              )
                            , Record
                              ( attr = String `first_name`
                              , full_name = 'wireless_interface.my_net_device.node.manager.first_name'
                              , id = 'wireless_interface__my_net_device__node__manager__first_name'
                              , name = 'first_name'
                              , sig_key = 3
                              , ui_name = 'Wireless interface/My net device/Node/Manager/First name'
                              )
                            , Record
                              ( attr = String `middle_name`
                              , full_name = 'wireless_interface.my_net_device.node.manager.middle_name'
                              , id = 'wireless_interface__my_net_device__node__manager__middle_name'
                              , name = 'middle_name'
                              , sig_key = 3
                              , ui_name = 'Wireless interface/My net device/Node/Manager/Middle name'
                              )
                            , Record
                              ( attr = String `title`
                              , full_name = 'wireless_interface.my_net_device.node.manager.title'
                              , id = 'wireless_interface__my_net_device__node__manager__title'
                              , name = 'title'
                              , sig_key = 3
                              , ui_name = 'Wireless interface/My net device/Node/Manager/Academic title'
                              )
                            , Record
                              ( attr = Date_Interval `lifetime`
                              , attrs =
                                  [ Record
                                    ( attr = Date `start`
                                    , full_name = 'wireless_interface.my_net_device.node.manager.lifetime.start'
                                    , id = 'wireless_interface__my_net_device__node__manager__lifetime__start'
                                    , name = 'start'
                                    , sig_key = 0
                                    , ui_name = 'Wireless interface/My net device/Node/Manager/Lifetime/Start'
                                    )
                                  , Record
                                    ( attr = Date `finish`
                                    , full_name = 'wireless_interface.my_net_device.node.manager.lifetime.finish'
                                    , id = 'wireless_interface__my_net_device__node__manager__lifetime__finish'
                                    , name = 'finish'
                                    , sig_key = 0
                                    , ui_name = 'Wireless interface/My net device/Node/Manager/Lifetime/Finish'
                                    )
                                  , Record
                                    ( attr = Boolean `alive`
                                    , choices = <Recursion on list...>
                                    , full_name = 'wireless_interface.my_net_device.node.manager.lifetime.alive'
                                    , id = 'wireless_interface__my_net_device__node__manager__lifetime__alive'
                                    , name = 'alive'
                                    , sig_key = 1
                                    , ui_name = 'Wireless interface/My net device/Node/Manager/Lifetime/Alive'
                                    )
                                  ]
                              , full_name = 'wireless_interface.my_net_device.node.manager.lifetime'
                              , id = 'wireless_interface__my_net_device__node__manager__lifetime'
                              , name = 'lifetime'
                              , ui_name = 'Wireless interface/My net device/Node/Manager/Lifetime'
                              )
                            , Record
                              ( attr = Sex `sex`
                              , choices = <Recursion on list...>
                              , full_name = 'wireless_interface.my_net_device.node.manager.sex'
                              , id = 'wireless_interface__my_net_device__node__manager__sex'
                              , name = 'sex'
                              , sig_key = 0
                              , ui_name = 'Wireless interface/My net device/Node/Manager/Sex'
                              )
                            ]
                        , full_name = 'wireless_interface.my_net_device.node.manager'
                        , id = 'wireless_interface__my_net_device__node__manager'
                        , name = 'manager'
                        , sig_key = 2
                        , type_name = 'PAP.Person'
                        , ui_name = 'Wireless interface/My net device/Node/Manager'
                        , ui_type_name = 'Person'
                        )
                      , Record
                        ( Class = 'Entity'
                        , attr = Entity `address`
                        , attrs =
                            [ Record
                              ( attr = String `street`
                              , full_name = 'wireless_interface.my_net_device.node.address.street'
                              , id = 'wireless_interface__my_net_device__node__address__street'
                              , name = 'street'
                              , sig_key = 3
                              , ui_name = 'Wireless interface/My net device/Node/Address/Street'
                              )
                            , Record
                              ( attr = String `zip`
                              , full_name = 'wireless_interface.my_net_device.node.address.zip'
                              , id = 'wireless_interface__my_net_device__node__address__zip'
                              , name = 'zip'
                              , sig_key = 3
                              , ui_name = 'Wireless interface/My net device/Node/Address/Zip code'
                              )
                            , Record
                              ( attr = String `city`
                              , full_name = 'wireless_interface.my_net_device.node.address.city'
                              , id = 'wireless_interface__my_net_device__node__address__city'
                              , name = 'city'
                              , sig_key = 3
                              , ui_name = 'Wireless interface/My net device/Node/Address/City'
                              )
                            , Record
                              ( attr = String `country`
                              , full_name = 'wireless_interface.my_net_device.node.address.country'
                              , id = 'wireless_interface__my_net_device__node__address__country'
                              , name = 'country'
                              , sig_key = 3
                              , ui_name = 'Wireless interface/My net device/Node/Address/Country'
                              )
                            , Record
                              ( attr = String `desc`
                              , full_name = 'wireless_interface.my_net_device.node.address.desc'
                              , id = 'wireless_interface__my_net_device__node__address__desc'
                              , name = 'desc'
                              , sig_key = 3
                              , ui_name = 'Wireless interface/My net device/Node/Address/Description'
                              )
                            , Record
                              ( attr = String `region`
                              , full_name = 'wireless_interface.my_net_device.node.address.region'
                              , id = 'wireless_interface__my_net_device__node__address__region'
                              , name = 'region'
                              , sig_key = 3
                              , ui_name = 'Wireless interface/My net device/Node/Address/Region'
                              )
                            ]
                        , full_name = 'wireless_interface.my_net_device.node.address'
                        , id = 'wireless_interface__my_net_device__node__address'
                        , name = 'address'
                        , sig_key = 2
                        , type_name = 'PAP.Address'
                        , ui_name = 'Wireless interface/My net device/Node/Address'
                        , ui_type_name = 'Address'
                        )
                      , Record
                        ( attr = Text `desc`
                        , full_name = 'wireless_interface.my_net_device.node.desc'
                        , id = 'wireless_interface__my_net_device__node__desc'
                        , name = 'desc'
                        , sig_key = 3
                        , ui_name = 'Wireless interface/My net device/Node/Description'
                        )
                      , Record
                        ( Class = 'Entity'
                        , attr = Entity `owner`
                        , children_np =
                            [ Record
                              ( Class = 'Entity'
                              , attr = Entity `owner`
                              , attrs =
                                  [ Record
                                    ( attr = String `name`
                                    , full_name = 'owner.name'
                                    , id = 'owner__name'
                                    , name = 'name'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Adhoc_Group]/Name'
                                    )
                                  ]
                              , full_name = 'owner'
                              , id = 'owner'
                              , name = 'owner'
                              , sig_key = 2
                              , type_name = 'PAP.Adhoc_Group'
                              , ui_name = 'Owner[Adhoc_Group]'
                              , ui_type_name = 'Adhoc_Group'
                              )
                            , Record
                              ( Class = 'Entity'
                              , attr = Entity `owner`
                              , attrs =
                                  [ Record
                                    ( attr = String `name`
                                    , full_name = 'owner.name'
                                    , id = 'owner__name'
                                    , name = 'name'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Association]/Name'
                                    )
                                  ]
                              , full_name = 'owner'
                              , id = 'owner'
                              , name = 'owner'
                              , sig_key = 2
                              , type_name = 'PAP.Association'
                              , ui_name = 'Owner[Association]'
                              , ui_type_name = 'Association'
                              )
                            , Record
                              ( Class = 'Entity'
                              , attr = Entity `owner`
                              , attrs =
                                  [ Record
                                    ( attr = String `name`
                                    , full_name = 'owner.name'
                                    , id = 'owner__name'
                                    , name = 'name'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Company]/Name'
                                    )
                                  , Record
                                    ( attr = String `registered_in`
                                    , full_name = 'owner.registered_in'
                                    , id = 'owner__registered_in'
                                    , name = 'registered_in'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Company]/Registered in'
                                    )
                                  ]
                              , full_name = 'owner'
                              , id = 'owner'
                              , name = 'owner'
                              , sig_key = 2
                              , type_name = 'PAP.Company'
                              , ui_name = 'Owner[Company]'
                              , ui_type_name = 'Company'
                              )
                            , Record
                              ( Class = 'Entity'
                              , attr = Entity `owner`
                              , attrs =
                                  [ Record
                                    ( attr = String `last_name`
                                    , full_name = 'owner.last_name'
                                    , id = 'owner__last_name'
                                    , name = 'last_name'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Person]/Last name'
                                    )
                                  , Record
                                    ( attr = String `first_name`
                                    , full_name = 'owner.first_name'
                                    , id = 'owner__first_name'
                                    , name = 'first_name'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Person]/First name'
                                    )
                                  , Record
                                    ( attr = String `middle_name`
                                    , full_name = 'owner.middle_name'
                                    , id = 'owner__middle_name'
                                    , name = 'middle_name'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Person]/Middle name'
                                    )
                                  , Record
                                    ( attr = String `title`
                                    , full_name = 'owner.title'
                                    , id = 'owner__title'
                                    , name = 'title'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Person]/Academic title'
                                    )
                                  ]
                              , full_name = 'owner'
                              , id = 'owner'
                              , name = 'owner'
                              , sig_key = 2
                              , type_name = 'PAP.Person'
                              , ui_name = 'Owner[Person]'
                              , ui_type_name = 'Person'
                              )
                            ]
                        , default_child = 'PAP.Person'
                        , full_name = 'wireless_interface.my_net_device.node.owner'
                        , id = 'wireless_interface__my_net_device__node__owner'
                        , name = 'owner'
                        , sig_key = 2
                        , type_name = 'PAP.Subject'
                        , ui_name = 'Wireless interface/My net device/Node/Owner'
                        , ui_type_name = 'Subject'
                        )
                      , Record
                        ( attr = Position `position`
                        , attrs =
                            [ Record
                              ( attr = Angle `lat`
                              , full_name = 'wireless_interface.my_net_device.node.position.lat'
                              , id = 'wireless_interface__my_net_device__node__position__lat'
                              , name = 'lat'
                              , sig_key = 4
                              , ui_name = 'Wireless interface/My net device/Node/Position/Latitude'
                              )
                            , Record
                              ( attr = Angle `lon`
                              , full_name = 'wireless_interface.my_net_device.node.position.lon'
                              , id = 'wireless_interface__my_net_device__node__position__lon'
                              , name = 'lon'
                              , sig_key = 4
                              , ui_name = 'Wireless interface/My net device/Node/Position/Longitude'
                              )
                            , Record
                              ( attr = Float `height`
                              , full_name = 'wireless_interface.my_net_device.node.position.height'
                              , id = 'wireless_interface__my_net_device__node__position__height'
                              , name = 'height'
                              , sig_key = 0
                              , ui_name = 'Wireless interface/My net device/Node/Position/Height'
                              )
                            ]
                        , full_name = 'wireless_interface.my_net_device.node.position'
                        , id = 'wireless_interface__my_net_device__node__position'
                        , name = 'position'
                        , ui_name = 'Wireless interface/My net device/Node/Position'
                        )
                      , Record
                        ( attr = Boolean `show_in_map`
                        , choices = <Recursion on list...>
                        , full_name = 'wireless_interface.my_net_device.node.show_in_map'
                        , id = 'wireless_interface__my_net_device__node__show_in_map'
                        , name = 'show_in_map'
                        , sig_key = 1
                        , ui_name = 'Wireless interface/My net device/Node/Show in map'
                        )
                      ]
                  , full_name = 'wireless_interface.my_net_device.node'
                  , id = 'wireless_interface__my_net_device__node'
                  , name = 'node'
                  , sig_key = 2
                  , type_name = 'FFM.Node'
                  , ui_name = 'Wireless interface/My net device/Node'
                  , ui_type_name = 'Node'
                  )
                , Record
                  ( attr = String `name`
                  , full_name = 'wireless_interface.my_net_device.name'
                  , id = 'wireless_interface__my_net_device__name'
                  , name = 'name'
                  , sig_key = 3
                  , ui_name = 'Wireless interface/My net device/Name'
                  )
                , Record
                  ( attr = Text `desc`
                  , full_name = 'wireless_interface.my_net_device.desc'
                  , id = 'wireless_interface__my_net_device__desc'
                  , name = 'desc'
                  , sig_key = 3
                  , ui_name = 'Wireless interface/My net device/Description'
                  )
                , Record
                  ( Class = 'Entity'
                  , attr = Entity `my_node`
                  , attrs =
                      [ Record
                        ( attr = String `name`
                        , full_name = 'wireless_interface.my_net_device.my_node.name'
                        , id = 'wireless_interface__my_net_device__my_node__name'
                        , name = 'name'
                        , sig_key = 3
                        , ui_name = 'Wireless interface/My net device/My node/Name'
                        )
                      , Record
                        ( Class = 'Entity'
                        , attr = Entity `manager`
                        , attrs =
                            [ Record
                              ( attr = String `last_name`
                              , full_name = 'wireless_interface.my_net_device.my_node.manager.last_name'
                              , id = 'wireless_interface__my_net_device__my_node__manager__last_name'
                              , name = 'last_name'
                              , sig_key = 3
                              , ui_name = 'Wireless interface/My net device/My node/Manager/Last name'
                              )
                            , Record
                              ( attr = String `first_name`
                              , full_name = 'wireless_interface.my_net_device.my_node.manager.first_name'
                              , id = 'wireless_interface__my_net_device__my_node__manager__first_name'
                              , name = 'first_name'
                              , sig_key = 3
                              , ui_name = 'Wireless interface/My net device/My node/Manager/First name'
                              )
                            , Record
                              ( attr = String `middle_name`
                              , full_name = 'wireless_interface.my_net_device.my_node.manager.middle_name'
                              , id = 'wireless_interface__my_net_device__my_node__manager__middle_name'
                              , name = 'middle_name'
                              , sig_key = 3
                              , ui_name = 'Wireless interface/My net device/My node/Manager/Middle name'
                              )
                            , Record
                              ( attr = String `title`
                              , full_name = 'wireless_interface.my_net_device.my_node.manager.title'
                              , id = 'wireless_interface__my_net_device__my_node__manager__title'
                              , name = 'title'
                              , sig_key = 3
                              , ui_name = 'Wireless interface/My net device/My node/Manager/Academic title'
                              )
                            , Record
                              ( attr = Date_Interval `lifetime`
                              , attrs =
                                  [ Record
                                    ( attr = Date `start`
                                    , full_name = 'wireless_interface.my_net_device.my_node.manager.lifetime.start'
                                    , id = 'wireless_interface__my_net_device__my_node__manager__lifetime__start'
                                    , name = 'start'
                                    , sig_key = 0
                                    , ui_name = 'Wireless interface/My net device/My node/Manager/Lifetime/Start'
                                    )
                                  , Record
                                    ( attr = Date `finish`
                                    , full_name = 'wireless_interface.my_net_device.my_node.manager.lifetime.finish'
                                    , id = 'wireless_interface__my_net_device__my_node__manager__lifetime__finish'
                                    , name = 'finish'
                                    , sig_key = 0
                                    , ui_name = 'Wireless interface/My net device/My node/Manager/Lifetime/Finish'
                                    )
                                  , Record
                                    ( attr = Boolean `alive`
                                    , choices = <Recursion on list...>
                                    , full_name = 'wireless_interface.my_net_device.my_node.manager.lifetime.alive'
                                    , id = 'wireless_interface__my_net_device__my_node__manager__lifetime__alive'
                                    , name = 'alive'
                                    , sig_key = 1
                                    , ui_name = 'Wireless interface/My net device/My node/Manager/Lifetime/Alive'
                                    )
                                  ]
                              , full_name = 'wireless_interface.my_net_device.my_node.manager.lifetime'
                              , id = 'wireless_interface__my_net_device__my_node__manager__lifetime'
                              , name = 'lifetime'
                              , ui_name = 'Wireless interface/My net device/My node/Manager/Lifetime'
                              )
                            , Record
                              ( attr = Sex `sex`
                              , choices = <Recursion on list...>
                              , full_name = 'wireless_interface.my_net_device.my_node.manager.sex'
                              , id = 'wireless_interface__my_net_device__my_node__manager__sex'
                              , name = 'sex'
                              , sig_key = 0
                              , ui_name = 'Wireless interface/My net device/My node/Manager/Sex'
                              )
                            ]
                        , full_name = 'wireless_interface.my_net_device.my_node.manager'
                        , id = 'wireless_interface__my_net_device__my_node__manager'
                        , name = 'manager'
                        , sig_key = 2
                        , type_name = 'PAP.Person'
                        , ui_name = 'Wireless interface/My net device/My node/Manager'
                        , ui_type_name = 'Person'
                        )
                      , Record
                        ( Class = 'Entity'
                        , attr = Entity `address`
                        , attrs =
                            [ Record
                              ( attr = String `street`
                              , full_name = 'wireless_interface.my_net_device.my_node.address.street'
                              , id = 'wireless_interface__my_net_device__my_node__address__street'
                              , name = 'street'
                              , sig_key = 3
                              , ui_name = 'Wireless interface/My net device/My node/Address/Street'
                              )
                            , Record
                              ( attr = String `zip`
                              , full_name = 'wireless_interface.my_net_device.my_node.address.zip'
                              , id = 'wireless_interface__my_net_device__my_node__address__zip'
                              , name = 'zip'
                              , sig_key = 3
                              , ui_name = 'Wireless interface/My net device/My node/Address/Zip code'
                              )
                            , Record
                              ( attr = String `city`
                              , full_name = 'wireless_interface.my_net_device.my_node.address.city'
                              , id = 'wireless_interface__my_net_device__my_node__address__city'
                              , name = 'city'
                              , sig_key = 3
                              , ui_name = 'Wireless interface/My net device/My node/Address/City'
                              )
                            , Record
                              ( attr = String `country`
                              , full_name = 'wireless_interface.my_net_device.my_node.address.country'
                              , id = 'wireless_interface__my_net_device__my_node__address__country'
                              , name = 'country'
                              , sig_key = 3
                              , ui_name = 'Wireless interface/My net device/My node/Address/Country'
                              )
                            , Record
                              ( attr = String `desc`
                              , full_name = 'wireless_interface.my_net_device.my_node.address.desc'
                              , id = 'wireless_interface__my_net_device__my_node__address__desc'
                              , name = 'desc'
                              , sig_key = 3
                              , ui_name = 'Wireless interface/My net device/My node/Address/Description'
                              )
                            , Record
                              ( attr = String `region`
                              , full_name = 'wireless_interface.my_net_device.my_node.address.region'
                              , id = 'wireless_interface__my_net_device__my_node__address__region'
                              , name = 'region'
                              , sig_key = 3
                              , ui_name = 'Wireless interface/My net device/My node/Address/Region'
                              )
                            ]
                        , full_name = 'wireless_interface.my_net_device.my_node.address'
                        , id = 'wireless_interface__my_net_device__my_node__address'
                        , name = 'address'
                        , sig_key = 2
                        , type_name = 'PAP.Address'
                        , ui_name = 'Wireless interface/My net device/My node/Address'
                        , ui_type_name = 'Address'
                        )
                      , Record
                        ( attr = Text `desc`
                        , full_name = 'wireless_interface.my_net_device.my_node.desc'
                        , id = 'wireless_interface__my_net_device__my_node__desc'
                        , name = 'desc'
                        , sig_key = 3
                        , ui_name = 'Wireless interface/My net device/My node/Description'
                        )
                      , Record
                        ( Class = 'Entity'
                        , attr = Entity `owner`
                        , children_np =
                            [ Record
                              ( Class = 'Entity'
                              , attr = Entity `owner`
                              , attrs =
                                  [ Record
                                    ( attr = String `name`
                                    , full_name = 'owner.name'
                                    , id = 'owner__name'
                                    , name = 'name'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Adhoc_Group]/Name'
                                    )
                                  ]
                              , full_name = 'owner'
                              , id = 'owner'
                              , name = 'owner'
                              , sig_key = 2
                              , type_name = 'PAP.Adhoc_Group'
                              , ui_name = 'Owner[Adhoc_Group]'
                              , ui_type_name = 'Adhoc_Group'
                              )
                            , Record
                              ( Class = 'Entity'
                              , attr = Entity `owner`
                              , attrs =
                                  [ Record
                                    ( attr = String `name`
                                    , full_name = 'owner.name'
                                    , id = 'owner__name'
                                    , name = 'name'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Association]/Name'
                                    )
                                  ]
                              , full_name = 'owner'
                              , id = 'owner'
                              , name = 'owner'
                              , sig_key = 2
                              , type_name = 'PAP.Association'
                              , ui_name = 'Owner[Association]'
                              , ui_type_name = 'Association'
                              )
                            , Record
                              ( Class = 'Entity'
                              , attr = Entity `owner`
                              , attrs =
                                  [ Record
                                    ( attr = String `name`
                                    , full_name = 'owner.name'
                                    , id = 'owner__name'
                                    , name = 'name'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Company]/Name'
                                    )
                                  , Record
                                    ( attr = String `registered_in`
                                    , full_name = 'owner.registered_in'
                                    , id = 'owner__registered_in'
                                    , name = 'registered_in'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Company]/Registered in'
                                    )
                                  ]
                              , full_name = 'owner'
                              , id = 'owner'
                              , name = 'owner'
                              , sig_key = 2
                              , type_name = 'PAP.Company'
                              , ui_name = 'Owner[Company]'
                              , ui_type_name = 'Company'
                              )
                            , Record
                              ( Class = 'Entity'
                              , attr = Entity `owner`
                              , attrs =
                                  [ Record
                                    ( attr = String `last_name`
                                    , full_name = 'owner.last_name'
                                    , id = 'owner__last_name'
                                    , name = 'last_name'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Person]/Last name'
                                    )
                                  , Record
                                    ( attr = String `first_name`
                                    , full_name = 'owner.first_name'
                                    , id = 'owner__first_name'
                                    , name = 'first_name'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Person]/First name'
                                    )
                                  , Record
                                    ( attr = String `middle_name`
                                    , full_name = 'owner.middle_name'
                                    , id = 'owner__middle_name'
                                    , name = 'middle_name'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Person]/Middle name'
                                    )
                                  , Record
                                    ( attr = String `title`
                                    , full_name = 'owner.title'
                                    , id = 'owner__title'
                                    , name = 'title'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Person]/Academic title'
                                    )
                                  ]
                              , full_name = 'owner'
                              , id = 'owner'
                              , name = 'owner'
                              , sig_key = 2
                              , type_name = 'PAP.Person'
                              , ui_name = 'Owner[Person]'
                              , ui_type_name = 'Person'
                              )
                            ]
                        , default_child = 'PAP.Person'
                        , full_name = 'wireless_interface.my_net_device.my_node.owner'
                        , id = 'wireless_interface__my_net_device__my_node__owner'
                        , name = 'owner'
                        , sig_key = 2
                        , type_name = 'PAP.Subject'
                        , ui_name = 'Wireless interface/My net device/My node/Owner'
                        , ui_type_name = 'Subject'
                        )
                      , Record
                        ( attr = Position `position`
                        , attrs =
                            [ Record
                              ( attr = Angle `lat`
                              , full_name = 'wireless_interface.my_net_device.my_node.position.lat'
                              , id = 'wireless_interface__my_net_device__my_node__position__lat'
                              , name = 'lat'
                              , sig_key = 4
                              , ui_name = 'Wireless interface/My net device/My node/Position/Latitude'
                              )
                            , Record
                              ( attr = Angle `lon`
                              , full_name = 'wireless_interface.my_net_device.my_node.position.lon'
                              , id = 'wireless_interface__my_net_device__my_node__position__lon'
                              , name = 'lon'
                              , sig_key = 4
                              , ui_name = 'Wireless interface/My net device/My node/Position/Longitude'
                              )
                            , Record
                              ( attr = Float `height`
                              , full_name = 'wireless_interface.my_net_device.my_node.position.height'
                              , id = 'wireless_interface__my_net_device__my_node__position__height'
                              , name = 'height'
                              , sig_key = 0
                              , ui_name = 'Wireless interface/My net device/My node/Position/Height'
                              )
                            ]
                        , full_name = 'wireless_interface.my_net_device.my_node.position'
                        , id = 'wireless_interface__my_net_device__my_node__position'
                        , name = 'position'
                        , ui_name = 'Wireless interface/My net device/My node/Position'
                        )
                      , Record
                        ( attr = Boolean `show_in_map`
                        , choices = <Recursion on list...>
                        , full_name = 'wireless_interface.my_net_device.my_node.show_in_map'
                        , id = 'wireless_interface__my_net_device__my_node__show_in_map'
                        , name = 'show_in_map'
                        , sig_key = 1
                        , ui_name = 'Wireless interface/My net device/My node/Show in map'
                        )
                      ]
                  , full_name = 'wireless_interface.my_net_device.my_node'
                  , id = 'wireless_interface__my_net_device__my_node'
                  , name = 'my_node'
                  , sig_key = 2
                  , type_name = 'FFM.Node'
                  , ui_name = 'Wireless interface/My net device/My node'
                  , ui_type_name = 'Node'
                  )
                ]
            , full_name = 'wireless_interface.my_net_device'
            , id = 'wireless_interface__my_net_device'
            , name = 'my_net_device'
            , sig_key = 2
            , type_name = 'FFM.Net_Device'
            , ui_name = 'Wireless interface/My net device'
            , ui_type_name = 'Net_Device'
            )
          ]
      , full_name = 'wireless_interface'
      , id = 'wireless_interface'
      , name = 'wireless_interface'
      , sig_key = 2
      , type_name = 'FFM.Wireless_Interface'
      , ui_name = 'Wireless interface'
      , ui_type_name = 'Wireless_Interface'
      )
    , Record
      ( Class = 'Entity'
      , attr = Role_Ref `virtual_wireless_interface`
      , attrs =
          [ Record
            ( Class = 'Entity'
            , attr = Net_Device `left`
            , attrs =
                [ Record
                  ( Class = 'Entity'
                  , attr = Net_Device_Type `left`
                  , attrs =
                      [ Record
                        ( attr = String `name`
                        , full_name = 'virtual_wireless_interface.left.left.name'
                        , id = 'virtual_wireless_interface__left__left__name'
                        , name = 'name'
                        , sig_key = 3
                        , ui_name = 'Virtual wireless interface/Net device/Net device type/Name'
                        )
                      , Record
                        ( attr = String `model_no`
                        , full_name = 'virtual_wireless_interface.left.left.model_no'
                        , id = 'virtual_wireless_interface__left__left__model_no'
                        , name = 'model_no'
                        , sig_key = 3
                        , ui_name = 'Virtual wireless interface/Net device/Net device type/Model no'
                        )
                      , Record
                        ( attr = String `revision`
                        , full_name = 'virtual_wireless_interface.left.left.revision'
                        , id = 'virtual_wireless_interface__left__left__revision'
                        , name = 'revision'
                        , sig_key = 3
                        , ui_name = 'Virtual wireless interface/Net device/Net device type/Revision'
                        )
                      , Record
                        ( attr = Text `desc`
                        , full_name = 'virtual_wireless_interface.left.left.desc'
                        , id = 'virtual_wireless_interface__left__left__desc'
                        , name = 'desc'
                        , sig_key = 3
                        , ui_name = 'Virtual wireless interface/Net device/Net device type/Description'
                        )
                      ]
                  , full_name = 'virtual_wireless_interface.left.left'
                  , id = 'virtual_wireless_interface__left__left'
                  , name = 'left'
                  , sig_key = 2
                  , type_name = 'FFM.Net_Device_Type'
                  , ui_name = 'Virtual wireless interface/Net device/Net device type'
                  , ui_type_name = 'Net_Device_Type'
                  )
                , Record
                  ( Class = 'Entity'
                  , attr = Entity `node`
                  , attrs =
                      [ Record
                        ( attr = String `name`
                        , full_name = 'virtual_wireless_interface.left.node.name'
                        , id = 'virtual_wireless_interface__left__node__name'
                        , name = 'name'
                        , sig_key = 3
                        , ui_name = 'Virtual wireless interface/Net device/Node/Name'
                        )
                      , Record
                        ( Class = 'Entity'
                        , attr = Entity `manager`
                        , attrs =
                            [ Record
                              ( attr = String `last_name`
                              , full_name = 'virtual_wireless_interface.left.node.manager.last_name'
                              , id = 'virtual_wireless_interface__left__node__manager__last_name'
                              , name = 'last_name'
                              , sig_key = 3
                              , ui_name = 'Virtual wireless interface/Net device/Node/Manager/Last name'
                              )
                            , Record
                              ( attr = String `first_name`
                              , full_name = 'virtual_wireless_interface.left.node.manager.first_name'
                              , id = 'virtual_wireless_interface__left__node__manager__first_name'
                              , name = 'first_name'
                              , sig_key = 3
                              , ui_name = 'Virtual wireless interface/Net device/Node/Manager/First name'
                              )
                            , Record
                              ( attr = String `middle_name`
                              , full_name = 'virtual_wireless_interface.left.node.manager.middle_name'
                              , id = 'virtual_wireless_interface__left__node__manager__middle_name'
                              , name = 'middle_name'
                              , sig_key = 3
                              , ui_name = 'Virtual wireless interface/Net device/Node/Manager/Middle name'
                              )
                            , Record
                              ( attr = String `title`
                              , full_name = 'virtual_wireless_interface.left.node.manager.title'
                              , id = 'virtual_wireless_interface__left__node__manager__title'
                              , name = 'title'
                              , sig_key = 3
                              , ui_name = 'Virtual wireless interface/Net device/Node/Manager/Academic title'
                              )
                            , Record
                              ( attr = Date_Interval `lifetime`
                              , attrs =
                                  [ Record
                                    ( attr = Date `start`
                                    , full_name = 'virtual_wireless_interface.left.node.manager.lifetime.start'
                                    , id = 'virtual_wireless_interface__left__node__manager__lifetime__start'
                                    , name = 'start'
                                    , sig_key = 0
                                    , ui_name = 'Virtual wireless interface/Net device/Node/Manager/Lifetime/Start'
                                    )
                                  , Record
                                    ( attr = Date `finish`
                                    , full_name = 'virtual_wireless_interface.left.node.manager.lifetime.finish'
                                    , id = 'virtual_wireless_interface__left__node__manager__lifetime__finish'
                                    , name = 'finish'
                                    , sig_key = 0
                                    , ui_name = 'Virtual wireless interface/Net device/Node/Manager/Lifetime/Finish'
                                    )
                                  , Record
                                    ( attr = Boolean `alive`
                                    , choices = <Recursion on list...>
                                    , full_name = 'virtual_wireless_interface.left.node.manager.lifetime.alive'
                                    , id = 'virtual_wireless_interface__left__node__manager__lifetime__alive'
                                    , name = 'alive'
                                    , sig_key = 1
                                    , ui_name = 'Virtual wireless interface/Net device/Node/Manager/Lifetime/Alive'
                                    )
                                  ]
                              , full_name = 'virtual_wireless_interface.left.node.manager.lifetime'
                              , id = 'virtual_wireless_interface__left__node__manager__lifetime'
                              , name = 'lifetime'
                              , ui_name = 'Virtual wireless interface/Net device/Node/Manager/Lifetime'
                              )
                            , Record
                              ( attr = Sex `sex`
                              , choices = <Recursion on list...>
                              , full_name = 'virtual_wireless_interface.left.node.manager.sex'
                              , id = 'virtual_wireless_interface__left__node__manager__sex'
                              , name = 'sex'
                              , sig_key = 0
                              , ui_name = 'Virtual wireless interface/Net device/Node/Manager/Sex'
                              )
                            ]
                        , full_name = 'virtual_wireless_interface.left.node.manager'
                        , id = 'virtual_wireless_interface__left__node__manager'
                        , name = 'manager'
                        , sig_key = 2
                        , type_name = 'PAP.Person'
                        , ui_name = 'Virtual wireless interface/Net device/Node/Manager'
                        , ui_type_name = 'Person'
                        )
                      , Record
                        ( Class = 'Entity'
                        , attr = Entity `address`
                        , attrs =
                            [ Record
                              ( attr = String `street`
                              , full_name = 'virtual_wireless_interface.left.node.address.street'
                              , id = 'virtual_wireless_interface__left__node__address__street'
                              , name = 'street'
                              , sig_key = 3
                              , ui_name = 'Virtual wireless interface/Net device/Node/Address/Street'
                              )
                            , Record
                              ( attr = String `zip`
                              , full_name = 'virtual_wireless_interface.left.node.address.zip'
                              , id = 'virtual_wireless_interface__left__node__address__zip'
                              , name = 'zip'
                              , sig_key = 3
                              , ui_name = 'Virtual wireless interface/Net device/Node/Address/Zip code'
                              )
                            , Record
                              ( attr = String `city`
                              , full_name = 'virtual_wireless_interface.left.node.address.city'
                              , id = 'virtual_wireless_interface__left__node__address__city'
                              , name = 'city'
                              , sig_key = 3
                              , ui_name = 'Virtual wireless interface/Net device/Node/Address/City'
                              )
                            , Record
                              ( attr = String `country`
                              , full_name = 'virtual_wireless_interface.left.node.address.country'
                              , id = 'virtual_wireless_interface__left__node__address__country'
                              , name = 'country'
                              , sig_key = 3
                              , ui_name = 'Virtual wireless interface/Net device/Node/Address/Country'
                              )
                            , Record
                              ( attr = String `desc`
                              , full_name = 'virtual_wireless_interface.left.node.address.desc'
                              , id = 'virtual_wireless_interface__left__node__address__desc'
                              , name = 'desc'
                              , sig_key = 3
                              , ui_name = 'Virtual wireless interface/Net device/Node/Address/Description'
                              )
                            , Record
                              ( attr = String `region`
                              , full_name = 'virtual_wireless_interface.left.node.address.region'
                              , id = 'virtual_wireless_interface__left__node__address__region'
                              , name = 'region'
                              , sig_key = 3
                              , ui_name = 'Virtual wireless interface/Net device/Node/Address/Region'
                              )
                            ]
                        , full_name = 'virtual_wireless_interface.left.node.address'
                        , id = 'virtual_wireless_interface__left__node__address'
                        , name = 'address'
                        , sig_key = 2
                        , type_name = 'PAP.Address'
                        , ui_name = 'Virtual wireless interface/Net device/Node/Address'
                        , ui_type_name = 'Address'
                        )
                      , Record
                        ( attr = Text `desc`
                        , full_name = 'virtual_wireless_interface.left.node.desc'
                        , id = 'virtual_wireless_interface__left__node__desc'
                        , name = 'desc'
                        , sig_key = 3
                        , ui_name = 'Virtual wireless interface/Net device/Node/Description'
                        )
                      , Record
                        ( Class = 'Entity'
                        , attr = Entity `owner`
                        , children_np =
                            [ Record
                              ( Class = 'Entity'
                              , attr = Entity `owner`
                              , attrs =
                                  [ Record
                                    ( attr = String `name`
                                    , full_name = 'owner.name'
                                    , id = 'owner__name'
                                    , name = 'name'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Adhoc_Group]/Name'
                                    )
                                  ]
                              , full_name = 'owner'
                              , id = 'owner'
                              , name = 'owner'
                              , sig_key = 2
                              , type_name = 'PAP.Adhoc_Group'
                              , ui_name = 'Owner[Adhoc_Group]'
                              , ui_type_name = 'Adhoc_Group'
                              )
                            , Record
                              ( Class = 'Entity'
                              , attr = Entity `owner`
                              , attrs =
                                  [ Record
                                    ( attr = String `name`
                                    , full_name = 'owner.name'
                                    , id = 'owner__name'
                                    , name = 'name'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Association]/Name'
                                    )
                                  ]
                              , full_name = 'owner'
                              , id = 'owner'
                              , name = 'owner'
                              , sig_key = 2
                              , type_name = 'PAP.Association'
                              , ui_name = 'Owner[Association]'
                              , ui_type_name = 'Association'
                              )
                            , Record
                              ( Class = 'Entity'
                              , attr = Entity `owner`
                              , attrs =
                                  [ Record
                                    ( attr = String `name`
                                    , full_name = 'owner.name'
                                    , id = 'owner__name'
                                    , name = 'name'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Company]/Name'
                                    )
                                  , Record
                                    ( attr = String `registered_in`
                                    , full_name = 'owner.registered_in'
                                    , id = 'owner__registered_in'
                                    , name = 'registered_in'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Company]/Registered in'
                                    )
                                  ]
                              , full_name = 'owner'
                              , id = 'owner'
                              , name = 'owner'
                              , sig_key = 2
                              , type_name = 'PAP.Company'
                              , ui_name = 'Owner[Company]'
                              , ui_type_name = 'Company'
                              )
                            , Record
                              ( Class = 'Entity'
                              , attr = Entity `owner`
                              , attrs =
                                  [ Record
                                    ( attr = String `last_name`
                                    , full_name = 'owner.last_name'
                                    , id = 'owner__last_name'
                                    , name = 'last_name'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Person]/Last name'
                                    )
                                  , Record
                                    ( attr = String `first_name`
                                    , full_name = 'owner.first_name'
                                    , id = 'owner__first_name'
                                    , name = 'first_name'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Person]/First name'
                                    )
                                  , Record
                                    ( attr = String `middle_name`
                                    , full_name = 'owner.middle_name'
                                    , id = 'owner__middle_name'
                                    , name = 'middle_name'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Person]/Middle name'
                                    )
                                  , Record
                                    ( attr = String `title`
                                    , full_name = 'owner.title'
                                    , id = 'owner__title'
                                    , name = 'title'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Person]/Academic title'
                                    )
                                  ]
                              , full_name = 'owner'
                              , id = 'owner'
                              , name = 'owner'
                              , sig_key = 2
                              , type_name = 'PAP.Person'
                              , ui_name = 'Owner[Person]'
                              , ui_type_name = 'Person'
                              )
                            ]
                        , default_child = 'PAP.Person'
                        , full_name = 'virtual_wireless_interface.left.node.owner'
                        , id = 'virtual_wireless_interface__left__node__owner'
                        , name = 'owner'
                        , sig_key = 2
                        , type_name = 'PAP.Subject'
                        , ui_name = 'Virtual wireless interface/Net device/Node/Owner'
                        , ui_type_name = 'Subject'
                        )
                      , Record
                        ( attr = Position `position`
                        , attrs =
                            [ Record
                              ( attr = Angle `lat`
                              , full_name = 'virtual_wireless_interface.left.node.position.lat'
                              , id = 'virtual_wireless_interface__left__node__position__lat'
                              , name = 'lat'
                              , sig_key = 4
                              , ui_name = 'Virtual wireless interface/Net device/Node/Position/Latitude'
                              )
                            , Record
                              ( attr = Angle `lon`
                              , full_name = 'virtual_wireless_interface.left.node.position.lon'
                              , id = 'virtual_wireless_interface__left__node__position__lon'
                              , name = 'lon'
                              , sig_key = 4
                              , ui_name = 'Virtual wireless interface/Net device/Node/Position/Longitude'
                              )
                            , Record
                              ( attr = Float `height`
                              , full_name = 'virtual_wireless_interface.left.node.position.height'
                              , id = 'virtual_wireless_interface__left__node__position__height'
                              , name = 'height'
                              , sig_key = 0
                              , ui_name = 'Virtual wireless interface/Net device/Node/Position/Height'
                              )
                            ]
                        , full_name = 'virtual_wireless_interface.left.node.position'
                        , id = 'virtual_wireless_interface__left__node__position'
                        , name = 'position'
                        , ui_name = 'Virtual wireless interface/Net device/Node/Position'
                        )
                      , Record
                        ( attr = Boolean `show_in_map`
                        , choices = <Recursion on list...>
                        , full_name = 'virtual_wireless_interface.left.node.show_in_map'
                        , id = 'virtual_wireless_interface__left__node__show_in_map'
                        , name = 'show_in_map'
                        , sig_key = 1
                        , ui_name = 'Virtual wireless interface/Net device/Node/Show in map'
                        )
                      ]
                  , full_name = 'virtual_wireless_interface.left.node'
                  , id = 'virtual_wireless_interface__left__node'
                  , name = 'node'
                  , sig_key = 2
                  , type_name = 'FFM.Node'
                  , ui_name = 'Virtual wireless interface/Net device/Node'
                  , ui_type_name = 'Node'
                  )
                , Record
                  ( attr = String `name`
                  , full_name = 'virtual_wireless_interface.left.name'
                  , id = 'virtual_wireless_interface__left__name'
                  , name = 'name'
                  , sig_key = 3
                  , ui_name = 'Virtual wireless interface/Net device/Name'
                  )
                , Record
                  ( attr = Text `desc`
                  , full_name = 'virtual_wireless_interface.left.desc'
                  , id = 'virtual_wireless_interface__left__desc'
                  , name = 'desc'
                  , sig_key = 3
                  , ui_name = 'Virtual wireless interface/Net device/Description'
                  )
                , Record
                  ( Class = 'Entity'
                  , attr = Entity `my_node`
                  , attrs =
                      [ Record
                        ( attr = String `name`
                        , full_name = 'virtual_wireless_interface.left.my_node.name'
                        , id = 'virtual_wireless_interface__left__my_node__name'
                        , name = 'name'
                        , sig_key = 3
                        , ui_name = 'Virtual wireless interface/Net device/My node/Name'
                        )
                      , Record
                        ( Class = 'Entity'
                        , attr = Entity `manager`
                        , attrs =
                            [ Record
                              ( attr = String `last_name`
                              , full_name = 'virtual_wireless_interface.left.my_node.manager.last_name'
                              , id = 'virtual_wireless_interface__left__my_node__manager__last_name'
                              , name = 'last_name'
                              , sig_key = 3
                              , ui_name = 'Virtual wireless interface/Net device/My node/Manager/Last name'
                              )
                            , Record
                              ( attr = String `first_name`
                              , full_name = 'virtual_wireless_interface.left.my_node.manager.first_name'
                              , id = 'virtual_wireless_interface__left__my_node__manager__first_name'
                              , name = 'first_name'
                              , sig_key = 3
                              , ui_name = 'Virtual wireless interface/Net device/My node/Manager/First name'
                              )
                            , Record
                              ( attr = String `middle_name`
                              , full_name = 'virtual_wireless_interface.left.my_node.manager.middle_name'
                              , id = 'virtual_wireless_interface__left__my_node__manager__middle_name'
                              , name = 'middle_name'
                              , sig_key = 3
                              , ui_name = 'Virtual wireless interface/Net device/My node/Manager/Middle name'
                              )
                            , Record
                              ( attr = String `title`
                              , full_name = 'virtual_wireless_interface.left.my_node.manager.title'
                              , id = 'virtual_wireless_interface__left__my_node__manager__title'
                              , name = 'title'
                              , sig_key = 3
                              , ui_name = 'Virtual wireless interface/Net device/My node/Manager/Academic title'
                              )
                            , Record
                              ( attr = Date_Interval `lifetime`
                              , attrs =
                                  [ Record
                                    ( attr = Date `start`
                                    , full_name = 'virtual_wireless_interface.left.my_node.manager.lifetime.start'
                                    , id = 'virtual_wireless_interface__left__my_node__manager__lifetime__start'
                                    , name = 'start'
                                    , sig_key = 0
                                    , ui_name = 'Virtual wireless interface/Net device/My node/Manager/Lifetime/Start'
                                    )
                                  , Record
                                    ( attr = Date `finish`
                                    , full_name = 'virtual_wireless_interface.left.my_node.manager.lifetime.finish'
                                    , id = 'virtual_wireless_interface__left__my_node__manager__lifetime__finish'
                                    , name = 'finish'
                                    , sig_key = 0
                                    , ui_name = 'Virtual wireless interface/Net device/My node/Manager/Lifetime/Finish'
                                    )
                                  , Record
                                    ( attr = Boolean `alive`
                                    , choices = <Recursion on list...>
                                    , full_name = 'virtual_wireless_interface.left.my_node.manager.lifetime.alive'
                                    , id = 'virtual_wireless_interface__left__my_node__manager__lifetime__alive'
                                    , name = 'alive'
                                    , sig_key = 1
                                    , ui_name = 'Virtual wireless interface/Net device/My node/Manager/Lifetime/Alive'
                                    )
                                  ]
                              , full_name = 'virtual_wireless_interface.left.my_node.manager.lifetime'
                              , id = 'virtual_wireless_interface__left__my_node__manager__lifetime'
                              , name = 'lifetime'
                              , ui_name = 'Virtual wireless interface/Net device/My node/Manager/Lifetime'
                              )
                            , Record
                              ( attr = Sex `sex`
                              , choices = <Recursion on list...>
                              , full_name = 'virtual_wireless_interface.left.my_node.manager.sex'
                              , id = 'virtual_wireless_interface__left__my_node__manager__sex'
                              , name = 'sex'
                              , sig_key = 0
                              , ui_name = 'Virtual wireless interface/Net device/My node/Manager/Sex'
                              )
                            ]
                        , full_name = 'virtual_wireless_interface.left.my_node.manager'
                        , id = 'virtual_wireless_interface__left__my_node__manager'
                        , name = 'manager'
                        , sig_key = 2
                        , type_name = 'PAP.Person'
                        , ui_name = 'Virtual wireless interface/Net device/My node/Manager'
                        , ui_type_name = 'Person'
                        )
                      , Record
                        ( Class = 'Entity'
                        , attr = Entity `address`
                        , attrs =
                            [ Record
                              ( attr = String `street`
                              , full_name = 'virtual_wireless_interface.left.my_node.address.street'
                              , id = 'virtual_wireless_interface__left__my_node__address__street'
                              , name = 'street'
                              , sig_key = 3
                              , ui_name = 'Virtual wireless interface/Net device/My node/Address/Street'
                              )
                            , Record
                              ( attr = String `zip`
                              , full_name = 'virtual_wireless_interface.left.my_node.address.zip'
                              , id = 'virtual_wireless_interface__left__my_node__address__zip'
                              , name = 'zip'
                              , sig_key = 3
                              , ui_name = 'Virtual wireless interface/Net device/My node/Address/Zip code'
                              )
                            , Record
                              ( attr = String `city`
                              , full_name = 'virtual_wireless_interface.left.my_node.address.city'
                              , id = 'virtual_wireless_interface__left__my_node__address__city'
                              , name = 'city'
                              , sig_key = 3
                              , ui_name = 'Virtual wireless interface/Net device/My node/Address/City'
                              )
                            , Record
                              ( attr = String `country`
                              , full_name = 'virtual_wireless_interface.left.my_node.address.country'
                              , id = 'virtual_wireless_interface__left__my_node__address__country'
                              , name = 'country'
                              , sig_key = 3
                              , ui_name = 'Virtual wireless interface/Net device/My node/Address/Country'
                              )
                            , Record
                              ( attr = String `desc`
                              , full_name = 'virtual_wireless_interface.left.my_node.address.desc'
                              , id = 'virtual_wireless_interface__left__my_node__address__desc'
                              , name = 'desc'
                              , sig_key = 3
                              , ui_name = 'Virtual wireless interface/Net device/My node/Address/Description'
                              )
                            , Record
                              ( attr = String `region`
                              , full_name = 'virtual_wireless_interface.left.my_node.address.region'
                              , id = 'virtual_wireless_interface__left__my_node__address__region'
                              , name = 'region'
                              , sig_key = 3
                              , ui_name = 'Virtual wireless interface/Net device/My node/Address/Region'
                              )
                            ]
                        , full_name = 'virtual_wireless_interface.left.my_node.address'
                        , id = 'virtual_wireless_interface__left__my_node__address'
                        , name = 'address'
                        , sig_key = 2
                        , type_name = 'PAP.Address'
                        , ui_name = 'Virtual wireless interface/Net device/My node/Address'
                        , ui_type_name = 'Address'
                        )
                      , Record
                        ( attr = Text `desc`
                        , full_name = 'virtual_wireless_interface.left.my_node.desc'
                        , id = 'virtual_wireless_interface__left__my_node__desc'
                        , name = 'desc'
                        , sig_key = 3
                        , ui_name = 'Virtual wireless interface/Net device/My node/Description'
                        )
                      , Record
                        ( Class = 'Entity'
                        , attr = Entity `owner`
                        , children_np =
                            [ Record
                              ( Class = 'Entity'
                              , attr = Entity `owner`
                              , attrs =
                                  [ Record
                                    ( attr = String `name`
                                    , full_name = 'owner.name'
                                    , id = 'owner__name'
                                    , name = 'name'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Adhoc_Group]/Name'
                                    )
                                  ]
                              , full_name = 'owner'
                              , id = 'owner'
                              , name = 'owner'
                              , sig_key = 2
                              , type_name = 'PAP.Adhoc_Group'
                              , ui_name = 'Owner[Adhoc_Group]'
                              , ui_type_name = 'Adhoc_Group'
                              )
                            , Record
                              ( Class = 'Entity'
                              , attr = Entity `owner`
                              , attrs =
                                  [ Record
                                    ( attr = String `name`
                                    , full_name = 'owner.name'
                                    , id = 'owner__name'
                                    , name = 'name'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Association]/Name'
                                    )
                                  ]
                              , full_name = 'owner'
                              , id = 'owner'
                              , name = 'owner'
                              , sig_key = 2
                              , type_name = 'PAP.Association'
                              , ui_name = 'Owner[Association]'
                              , ui_type_name = 'Association'
                              )
                            , Record
                              ( Class = 'Entity'
                              , attr = Entity `owner`
                              , attrs =
                                  [ Record
                                    ( attr = String `name`
                                    , full_name = 'owner.name'
                                    , id = 'owner__name'
                                    , name = 'name'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Company]/Name'
                                    )
                                  , Record
                                    ( attr = String `registered_in`
                                    , full_name = 'owner.registered_in'
                                    , id = 'owner__registered_in'
                                    , name = 'registered_in'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Company]/Registered in'
                                    )
                                  ]
                              , full_name = 'owner'
                              , id = 'owner'
                              , name = 'owner'
                              , sig_key = 2
                              , type_name = 'PAP.Company'
                              , ui_name = 'Owner[Company]'
                              , ui_type_name = 'Company'
                              )
                            , Record
                              ( Class = 'Entity'
                              , attr = Entity `owner`
                              , attrs =
                                  [ Record
                                    ( attr = String `last_name`
                                    , full_name = 'owner.last_name'
                                    , id = 'owner__last_name'
                                    , name = 'last_name'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Person]/Last name'
                                    )
                                  , Record
                                    ( attr = String `first_name`
                                    , full_name = 'owner.first_name'
                                    , id = 'owner__first_name'
                                    , name = 'first_name'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Person]/First name'
                                    )
                                  , Record
                                    ( attr = String `middle_name`
                                    , full_name = 'owner.middle_name'
                                    , id = 'owner__middle_name'
                                    , name = 'middle_name'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Person]/Middle name'
                                    )
                                  , Record
                                    ( attr = String `title`
                                    , full_name = 'owner.title'
                                    , id = 'owner__title'
                                    , name = 'title'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Person]/Academic title'
                                    )
                                  ]
                              , full_name = 'owner'
                              , id = 'owner'
                              , name = 'owner'
                              , sig_key = 2
                              , type_name = 'PAP.Person'
                              , ui_name = 'Owner[Person]'
                              , ui_type_name = 'Person'
                              )
                            ]
                        , default_child = 'PAP.Person'
                        , full_name = 'virtual_wireless_interface.left.my_node.owner'
                        , id = 'virtual_wireless_interface__left__my_node__owner'
                        , name = 'owner'
                        , sig_key = 2
                        , type_name = 'PAP.Subject'
                        , ui_name = 'Virtual wireless interface/Net device/My node/Owner'
                        , ui_type_name = 'Subject'
                        )
                      , Record
                        ( attr = Position `position`
                        , attrs =
                            [ Record
                              ( attr = Angle `lat`
                              , full_name = 'virtual_wireless_interface.left.my_node.position.lat'
                              , id = 'virtual_wireless_interface__left__my_node__position__lat'
                              , name = 'lat'
                              , sig_key = 4
                              , ui_name = 'Virtual wireless interface/Net device/My node/Position/Latitude'
                              )
                            , Record
                              ( attr = Angle `lon`
                              , full_name = 'virtual_wireless_interface.left.my_node.position.lon'
                              , id = 'virtual_wireless_interface__left__my_node__position__lon'
                              , name = 'lon'
                              , sig_key = 4
                              , ui_name = 'Virtual wireless interface/Net device/My node/Position/Longitude'
                              )
                            , Record
                              ( attr = Float `height`
                              , full_name = 'virtual_wireless_interface.left.my_node.position.height'
                              , id = 'virtual_wireless_interface__left__my_node__position__height'
                              , name = 'height'
                              , sig_key = 0
                              , ui_name = 'Virtual wireless interface/Net device/My node/Position/Height'
                              )
                            ]
                        , full_name = 'virtual_wireless_interface.left.my_node.position'
                        , id = 'virtual_wireless_interface__left__my_node__position'
                        , name = 'position'
                        , ui_name = 'Virtual wireless interface/Net device/My node/Position'
                        )
                      , Record
                        ( attr = Boolean `show_in_map`
                        , choices = <Recursion on list...>
                        , full_name = 'virtual_wireless_interface.left.my_node.show_in_map'
                        , id = 'virtual_wireless_interface__left__my_node__show_in_map'
                        , name = 'show_in_map'
                        , sig_key = 1
                        , ui_name = 'Virtual wireless interface/Net device/My node/Show in map'
                        )
                      ]
                  , full_name = 'virtual_wireless_interface.left.my_node'
                  , id = 'virtual_wireless_interface__left__my_node'
                  , name = 'my_node'
                  , sig_key = 2
                  , type_name = 'FFM.Node'
                  , ui_name = 'Virtual wireless interface/Net device/My node'
                  , ui_type_name = 'Node'
                  )
                ]
            , full_name = 'virtual_wireless_interface.left'
            , id = 'virtual_wireless_interface__left'
            , name = 'left'
            , sig_key = 2
            , type_name = 'FFM.Net_Device'
            , ui_name = 'Virtual wireless interface/Net device'
            , ui_type_name = 'Net_Device'
            )
          , Record
            ( Class = 'Entity'
            , attr = Entity `hardware`
            , attrs =
                [ Record
                  ( Class = 'Entity'
                  , attr = Net_Device `left`
                  , attrs =
                      [ Record
                        ( Class = 'Entity'
                        , attr = Net_Device_Type `left`
                        , attrs =
                            [ Record
                              ( attr = String `name`
                              , full_name = 'virtual_wireless_interface.hardware.left.left.name'
                              , id = 'virtual_wireless_interface__hardware__left__left__name'
                              , name = 'name'
                              , sig_key = 3
                              , ui_name = 'Virtual wireless interface/Hardware/Net device/Net device type/Name'
                              )
                            , Record
                              ( attr = String `model_no`
                              , full_name = 'virtual_wireless_interface.hardware.left.left.model_no'
                              , id = 'virtual_wireless_interface__hardware__left__left__model_no'
                              , name = 'model_no'
                              , sig_key = 3
                              , ui_name = 'Virtual wireless interface/Hardware/Net device/Net device type/Model no'
                              )
                            , Record
                              ( attr = String `revision`
                              , full_name = 'virtual_wireless_interface.hardware.left.left.revision'
                              , id = 'virtual_wireless_interface__hardware__left__left__revision'
                              , name = 'revision'
                              , sig_key = 3
                              , ui_name = 'Virtual wireless interface/Hardware/Net device/Net device type/Revision'
                              )
                            , Record
                              ( attr = Text `desc`
                              , full_name = 'virtual_wireless_interface.hardware.left.left.desc'
                              , id = 'virtual_wireless_interface__hardware__left__left__desc'
                              , name = 'desc'
                              , sig_key = 3
                              , ui_name = 'Virtual wireless interface/Hardware/Net device/Net device type/Description'
                              )
                            ]
                        , full_name = 'virtual_wireless_interface.hardware.left.left'
                        , id = 'virtual_wireless_interface__hardware__left__left'
                        , name = 'left'
                        , sig_key = 2
                        , type_name = 'FFM.Net_Device_Type'
                        , ui_name = 'Virtual wireless interface/Hardware/Net device/Net device type'
                        , ui_type_name = 'Net_Device_Type'
                        )
                      , Record
                        ( Class = 'Entity'
                        , attr = Entity `node`
                        , attrs =
                            [ Record
                              ( attr = String `name`
                              , full_name = 'virtual_wireless_interface.hardware.left.node.name'
                              , id = 'virtual_wireless_interface__hardware__left__node__name'
                              , name = 'name'
                              , sig_key = 3
                              , ui_name = 'Virtual wireless interface/Hardware/Net device/Node/Name'
                              )
                            , Record
                              ( Class = 'Entity'
                              , attr = Entity `manager`
                              , attrs =
                                  [ Record
                                    ( attr = String `last_name`
                                    , full_name = 'virtual_wireless_interface.hardware.left.node.manager.last_name'
                                    , id = 'virtual_wireless_interface__hardware__left__node__manager__last_name'
                                    , name = 'last_name'
                                    , sig_key = 3
                                    , ui_name = 'Virtual wireless interface/Hardware/Net device/Node/Manager/Last name'
                                    )
                                  , Record
                                    ( attr = String `first_name`
                                    , full_name = 'virtual_wireless_interface.hardware.left.node.manager.first_name'
                                    , id = 'virtual_wireless_interface__hardware__left__node__manager__first_name'
                                    , name = 'first_name'
                                    , sig_key = 3
                                    , ui_name = 'Virtual wireless interface/Hardware/Net device/Node/Manager/First name'
                                    )
                                  , Record
                                    ( attr = String `middle_name`
                                    , full_name = 'virtual_wireless_interface.hardware.left.node.manager.middle_name'
                                    , id = 'virtual_wireless_interface__hardware__left__node__manager__middle_name'
                                    , name = 'middle_name'
                                    , sig_key = 3
                                    , ui_name = 'Virtual wireless interface/Hardware/Net device/Node/Manager/Middle name'
                                    )
                                  , Record
                                    ( attr = String `title`
                                    , full_name = 'virtual_wireless_interface.hardware.left.node.manager.title'
                                    , id = 'virtual_wireless_interface__hardware__left__node__manager__title'
                                    , name = 'title'
                                    , sig_key = 3
                                    , ui_name = 'Virtual wireless interface/Hardware/Net device/Node/Manager/Academic title'
                                    )
                                  , Record
                                    ( attr = Date_Interval `lifetime`
                                    , attrs =
                                        [ Record
                                          ( attr = Date `start`
                                          , full_name = 'virtual_wireless_interface.hardware.left.node.manager.lifetime.start'
                                          , id = 'virtual_wireless_interface__hardware__left__node__manager__lifetime__start'
                                          , name = 'start'
                                          , sig_key = 0
                                          , ui_name = 'Virtual wireless interface/Hardware/Net device/Node/Manager/Lifetime/Start'
                                          )
                                        , Record
                                          ( attr = Date `finish`
                                          , full_name = 'virtual_wireless_interface.hardware.left.node.manager.lifetime.finish'
                                          , id = 'virtual_wireless_interface__hardware__left__node__manager__lifetime__finish'
                                          , name = 'finish'
                                          , sig_key = 0
                                          , ui_name = 'Virtual wireless interface/Hardware/Net device/Node/Manager/Lifetime/Finish'
                                          )
                                        , Record
                                          ( attr = Boolean `alive`
                                          , choices = <Recursion on list...>
                                          , full_name = 'virtual_wireless_interface.hardware.left.node.manager.lifetime.alive'
                                          , id = 'virtual_wireless_interface__hardware__left__node__manager__lifetime__alive'
                                          , name = 'alive'
                                          , sig_key = 1
                                          , ui_name = 'Virtual wireless interface/Hardware/Net device/Node/Manager/Lifetime/Alive'
                                          )
                                        ]
                                    , full_name = 'virtual_wireless_interface.hardware.left.node.manager.lifetime'
                                    , id = 'virtual_wireless_interface__hardware__left__node__manager__lifetime'
                                    , name = 'lifetime'
                                    , ui_name = 'Virtual wireless interface/Hardware/Net device/Node/Manager/Lifetime'
                                    )
                                  , Record
                                    ( attr = Sex `sex`
                                    , choices = <Recursion on list...>
                                    , full_name = 'virtual_wireless_interface.hardware.left.node.manager.sex'
                                    , id = 'virtual_wireless_interface__hardware__left__node__manager__sex'
                                    , name = 'sex'
                                    , sig_key = 0
                                    , ui_name = 'Virtual wireless interface/Hardware/Net device/Node/Manager/Sex'
                                    )
                                  ]
                              , full_name = 'virtual_wireless_interface.hardware.left.node.manager'
                              , id = 'virtual_wireless_interface__hardware__left__node__manager'
                              , name = 'manager'
                              , sig_key = 2
                              , type_name = 'PAP.Person'
                              , ui_name = 'Virtual wireless interface/Hardware/Net device/Node/Manager'
                              , ui_type_name = 'Person'
                              )
                            , Record
                              ( Class = 'Entity'
                              , attr = Entity `address`
                              , attrs =
                                  [ Record
                                    ( attr = String `street`
                                    , full_name = 'virtual_wireless_interface.hardware.left.node.address.street'
                                    , id = 'virtual_wireless_interface__hardware__left__node__address__street'
                                    , name = 'street'
                                    , sig_key = 3
                                    , ui_name = 'Virtual wireless interface/Hardware/Net device/Node/Address/Street'
                                    )
                                  , Record
                                    ( attr = String `zip`
                                    , full_name = 'virtual_wireless_interface.hardware.left.node.address.zip'
                                    , id = 'virtual_wireless_interface__hardware__left__node__address__zip'
                                    , name = 'zip'
                                    , sig_key = 3
                                    , ui_name = 'Virtual wireless interface/Hardware/Net device/Node/Address/Zip code'
                                    )
                                  , Record
                                    ( attr = String `city`
                                    , full_name = 'virtual_wireless_interface.hardware.left.node.address.city'
                                    , id = 'virtual_wireless_interface__hardware__left__node__address__city'
                                    , name = 'city'
                                    , sig_key = 3
                                    , ui_name = 'Virtual wireless interface/Hardware/Net device/Node/Address/City'
                                    )
                                  , Record
                                    ( attr = String `country`
                                    , full_name = 'virtual_wireless_interface.hardware.left.node.address.country'
                                    , id = 'virtual_wireless_interface__hardware__left__node__address__country'
                                    , name = 'country'
                                    , sig_key = 3
                                    , ui_name = 'Virtual wireless interface/Hardware/Net device/Node/Address/Country'
                                    )
                                  , Record
                                    ( attr = String `desc`
                                    , full_name = 'virtual_wireless_interface.hardware.left.node.address.desc'
                                    , id = 'virtual_wireless_interface__hardware__left__node__address__desc'
                                    , name = 'desc'
                                    , sig_key = 3
                                    , ui_name = 'Virtual wireless interface/Hardware/Net device/Node/Address/Description'
                                    )
                                  , Record
                                    ( attr = String `region`
                                    , full_name = 'virtual_wireless_interface.hardware.left.node.address.region'
                                    , id = 'virtual_wireless_interface__hardware__left__node__address__region'
                                    , name = 'region'
                                    , sig_key = 3
                                    , ui_name = 'Virtual wireless interface/Hardware/Net device/Node/Address/Region'
                                    )
                                  ]
                              , full_name = 'virtual_wireless_interface.hardware.left.node.address'
                              , id = 'virtual_wireless_interface__hardware__left__node__address'
                              , name = 'address'
                              , sig_key = 2
                              , type_name = 'PAP.Address'
                              , ui_name = 'Virtual wireless interface/Hardware/Net device/Node/Address'
                              , ui_type_name = 'Address'
                              )
                            , Record
                              ( attr = Text `desc`
                              , full_name = 'virtual_wireless_interface.hardware.left.node.desc'
                              , id = 'virtual_wireless_interface__hardware__left__node__desc'
                              , name = 'desc'
                              , sig_key = 3
                              , ui_name = 'Virtual wireless interface/Hardware/Net device/Node/Description'
                              )
                            , Record
                              ( Class = 'Entity'
                              , attr = Entity `owner`
                              , children_np =
                                  [ Record
                                    ( Class = 'Entity'
                                    , attr = Entity `owner`
                                    , attrs =
                                        [ Record
                                          ( attr = String `name`
                                          , full_name = 'owner.name'
                                          , id = 'owner__name'
                                          , name = 'name'
                                          , sig_key = 3
                                          , ui_name = 'Owner[Adhoc_Group]/Name'
                                          )
                                        ]
                                    , full_name = 'owner'
                                    , id = 'owner'
                                    , name = 'owner'
                                    , sig_key = 2
                                    , type_name = 'PAP.Adhoc_Group'
                                    , ui_name = 'Owner[Adhoc_Group]'
                                    , ui_type_name = 'Adhoc_Group'
                                    )
                                  , Record
                                    ( Class = 'Entity'
                                    , attr = Entity `owner`
                                    , attrs =
                                        [ Record
                                          ( attr = String `name`
                                          , full_name = 'owner.name'
                                          , id = 'owner__name'
                                          , name = 'name'
                                          , sig_key = 3
                                          , ui_name = 'Owner[Association]/Name'
                                          )
                                        ]
                                    , full_name = 'owner'
                                    , id = 'owner'
                                    , name = 'owner'
                                    , sig_key = 2
                                    , type_name = 'PAP.Association'
                                    , ui_name = 'Owner[Association]'
                                    , ui_type_name = 'Association'
                                    )
                                  , Record
                                    ( Class = 'Entity'
                                    , attr = Entity `owner`
                                    , attrs =
                                        [ Record
                                          ( attr = String `name`
                                          , full_name = 'owner.name'
                                          , id = 'owner__name'
                                          , name = 'name'
                                          , sig_key = 3
                                          , ui_name = 'Owner[Company]/Name'
                                          )
                                        , Record
                                          ( attr = String `registered_in`
                                          , full_name = 'owner.registered_in'
                                          , id = 'owner__registered_in'
                                          , name = 'registered_in'
                                          , sig_key = 3
                                          , ui_name = 'Owner[Company]/Registered in'
                                          )
                                        ]
                                    , full_name = 'owner'
                                    , id = 'owner'
                                    , name = 'owner'
                                    , sig_key = 2
                                    , type_name = 'PAP.Company'
                                    , ui_name = 'Owner[Company]'
                                    , ui_type_name = 'Company'
                                    )
                                  , Record
                                    ( Class = 'Entity'
                                    , attr = Entity `owner`
                                    , attrs =
                                        [ Record
                                          ( attr = String `last_name`
                                          , full_name = 'owner.last_name'
                                          , id = 'owner__last_name'
                                          , name = 'last_name'
                                          , sig_key = 3
                                          , ui_name = 'Owner[Person]/Last name'
                                          )
                                        , Record
                                          ( attr = String `first_name`
                                          , full_name = 'owner.first_name'
                                          , id = 'owner__first_name'
                                          , name = 'first_name'
                                          , sig_key = 3
                                          , ui_name = 'Owner[Person]/First name'
                                          )
                                        , Record
                                          ( attr = String `middle_name`
                                          , full_name = 'owner.middle_name'
                                          , id = 'owner__middle_name'
                                          , name = 'middle_name'
                                          , sig_key = 3
                                          , ui_name = 'Owner[Person]/Middle name'
                                          )
                                        , Record
                                          ( attr = String `title`
                                          , full_name = 'owner.title'
                                          , id = 'owner__title'
                                          , name = 'title'
                                          , sig_key = 3
                                          , ui_name = 'Owner[Person]/Academic title'
                                          )
                                        ]
                                    , full_name = 'owner'
                                    , id = 'owner'
                                    , name = 'owner'
                                    , sig_key = 2
                                    , type_name = 'PAP.Person'
                                    , ui_name = 'Owner[Person]'
                                    , ui_type_name = 'Person'
                                    )
                                  ]
                              , default_child = 'PAP.Person'
                              , full_name = 'virtual_wireless_interface.hardware.left.node.owner'
                              , id = 'virtual_wireless_interface__hardware__left__node__owner'
                              , name = 'owner'
                              , sig_key = 2
                              , type_name = 'PAP.Subject'
                              , ui_name = 'Virtual wireless interface/Hardware/Net device/Node/Owner'
                              , ui_type_name = 'Subject'
                              )
                            , Record
                              ( attr = Position `position`
                              , attrs =
                                  [ Record
                                    ( attr = Angle `lat`
                                    , full_name = 'virtual_wireless_interface.hardware.left.node.position.lat'
                                    , id = 'virtual_wireless_interface__hardware__left__node__position__lat'
                                    , name = 'lat'
                                    , sig_key = 4
                                    , ui_name = 'Virtual wireless interface/Hardware/Net device/Node/Position/Latitude'
                                    )
                                  , Record
                                    ( attr = Angle `lon`
                                    , full_name = 'virtual_wireless_interface.hardware.left.node.position.lon'
                                    , id = 'virtual_wireless_interface__hardware__left__node__position__lon'
                                    , name = 'lon'
                                    , sig_key = 4
                                    , ui_name = 'Virtual wireless interface/Hardware/Net device/Node/Position/Longitude'
                                    )
                                  , Record
                                    ( attr = Float `height`
                                    , full_name = 'virtual_wireless_interface.hardware.left.node.position.height'
                                    , id = 'virtual_wireless_interface__hardware__left__node__position__height'
                                    , name = 'height'
                                    , sig_key = 0
                                    , ui_name = 'Virtual wireless interface/Hardware/Net device/Node/Position/Height'
                                    )
                                  ]
                              , full_name = 'virtual_wireless_interface.hardware.left.node.position'
                              , id = 'virtual_wireless_interface__hardware__left__node__position'
                              , name = 'position'
                              , ui_name = 'Virtual wireless interface/Hardware/Net device/Node/Position'
                              )
                            , Record
                              ( attr = Boolean `show_in_map`
                              , choices = <Recursion on list...>
                              , full_name = 'virtual_wireless_interface.hardware.left.node.show_in_map'
                              , id = 'virtual_wireless_interface__hardware__left__node__show_in_map'
                              , name = 'show_in_map'
                              , sig_key = 1
                              , ui_name = 'Virtual wireless interface/Hardware/Net device/Node/Show in map'
                              )
                            ]
                        , full_name = 'virtual_wireless_interface.hardware.left.node'
                        , id = 'virtual_wireless_interface__hardware__left__node'
                        , name = 'node'
                        , sig_key = 2
                        , type_name = 'FFM.Node'
                        , ui_name = 'Virtual wireless interface/Hardware/Net device/Node'
                        , ui_type_name = 'Node'
                        )
                      , Record
                        ( attr = String `name`
                        , full_name = 'virtual_wireless_interface.hardware.left.name'
                        , id = 'virtual_wireless_interface__hardware__left__name'
                        , name = 'name'
                        , sig_key = 3
                        , ui_name = 'Virtual wireless interface/Hardware/Net device/Name'
                        )
                      , Record
                        ( attr = Text `desc`
                        , full_name = 'virtual_wireless_interface.hardware.left.desc'
                        , id = 'virtual_wireless_interface__hardware__left__desc'
                        , name = 'desc'
                        , sig_key = 3
                        , ui_name = 'Virtual wireless interface/Hardware/Net device/Description'
                        )
                      , Record
                        ( Class = 'Entity'
                        , attr = Entity `my_node`
                        , attrs =
                            [ Record
                              ( attr = String `name`
                              , full_name = 'virtual_wireless_interface.hardware.left.my_node.name'
                              , id = 'virtual_wireless_interface__hardware__left__my_node__name'
                              , name = 'name'
                              , sig_key = 3
                              , ui_name = 'Virtual wireless interface/Hardware/Net device/My node/Name'
                              )
                            , Record
                              ( Class = 'Entity'
                              , attr = Entity `manager`
                              , attrs =
                                  [ Record
                                    ( attr = String `last_name`
                                    , full_name = 'virtual_wireless_interface.hardware.left.my_node.manager.last_name'
                                    , id = 'virtual_wireless_interface__hardware__left__my_node__manager__last_name'
                                    , name = 'last_name'
                                    , sig_key = 3
                                    , ui_name = 'Virtual wireless interface/Hardware/Net device/My node/Manager/Last name'
                                    )
                                  , Record
                                    ( attr = String `first_name`
                                    , full_name = 'virtual_wireless_interface.hardware.left.my_node.manager.first_name'
                                    , id = 'virtual_wireless_interface__hardware__left__my_node__manager__first_name'
                                    , name = 'first_name'
                                    , sig_key = 3
                                    , ui_name = 'Virtual wireless interface/Hardware/Net device/My node/Manager/First name'
                                    )
                                  , Record
                                    ( attr = String `middle_name`
                                    , full_name = 'virtual_wireless_interface.hardware.left.my_node.manager.middle_name'
                                    , id = 'virtual_wireless_interface__hardware__left__my_node__manager__middle_name'
                                    , name = 'middle_name'
                                    , sig_key = 3
                                    , ui_name = 'Virtual wireless interface/Hardware/Net device/My node/Manager/Middle name'
                                    )
                                  , Record
                                    ( attr = String `title`
                                    , full_name = 'virtual_wireless_interface.hardware.left.my_node.manager.title'
                                    , id = 'virtual_wireless_interface__hardware__left__my_node__manager__title'
                                    , name = 'title'
                                    , sig_key = 3
                                    , ui_name = 'Virtual wireless interface/Hardware/Net device/My node/Manager/Academic title'
                                    )
                                  , Record
                                    ( attr = Date_Interval `lifetime`
                                    , attrs =
                                        [ Record
                                          ( attr = Date `start`
                                          , full_name = 'virtual_wireless_interface.hardware.left.my_node.manager.lifetime.start'
                                          , id = 'virtual_wireless_interface__hardware__left__my_node__manager__lifetime__start'
                                          , name = 'start'
                                          , sig_key = 0
                                          , ui_name = 'Virtual wireless interface/Hardware/Net device/My node/Manager/Lifetime/Start'
                                          )
                                        , Record
                                          ( attr = Date `finish`
                                          , full_name = 'virtual_wireless_interface.hardware.left.my_node.manager.lifetime.finish'
                                          , id = 'virtual_wireless_interface__hardware__left__my_node__manager__lifetime__finish'
                                          , name = 'finish'
                                          , sig_key = 0
                                          , ui_name = 'Virtual wireless interface/Hardware/Net device/My node/Manager/Lifetime/Finish'
                                          )
                                        , Record
                                          ( attr = Boolean `alive`
                                          , choices = <Recursion on list...>
                                          , full_name = 'virtual_wireless_interface.hardware.left.my_node.manager.lifetime.alive'
                                          , id = 'virtual_wireless_interface__hardware__left__my_node__manager__lifetime__alive'
                                          , name = 'alive'
                                          , sig_key = 1
                                          , ui_name = 'Virtual wireless interface/Hardware/Net device/My node/Manager/Lifetime/Alive'
                                          )
                                        ]
                                    , full_name = 'virtual_wireless_interface.hardware.left.my_node.manager.lifetime'
                                    , id = 'virtual_wireless_interface__hardware__left__my_node__manager__lifetime'
                                    , name = 'lifetime'
                                    , ui_name = 'Virtual wireless interface/Hardware/Net device/My node/Manager/Lifetime'
                                    )
                                  , Record
                                    ( attr = Sex `sex`
                                    , choices = <Recursion on list...>
                                    , full_name = 'virtual_wireless_interface.hardware.left.my_node.manager.sex'
                                    , id = 'virtual_wireless_interface__hardware__left__my_node__manager__sex'
                                    , name = 'sex'
                                    , sig_key = 0
                                    , ui_name = 'Virtual wireless interface/Hardware/Net device/My node/Manager/Sex'
                                    )
                                  ]
                              , full_name = 'virtual_wireless_interface.hardware.left.my_node.manager'
                              , id = 'virtual_wireless_interface__hardware__left__my_node__manager'
                              , name = 'manager'
                              , sig_key = 2
                              , type_name = 'PAP.Person'
                              , ui_name = 'Virtual wireless interface/Hardware/Net device/My node/Manager'
                              , ui_type_name = 'Person'
                              )
                            , Record
                              ( Class = 'Entity'
                              , attr = Entity `address`
                              , attrs =
                                  [ Record
                                    ( attr = String `street`
                                    , full_name = 'virtual_wireless_interface.hardware.left.my_node.address.street'
                                    , id = 'virtual_wireless_interface__hardware__left__my_node__address__street'
                                    , name = 'street'
                                    , sig_key = 3
                                    , ui_name = 'Virtual wireless interface/Hardware/Net device/My node/Address/Street'
                                    )
                                  , Record
                                    ( attr = String `zip`
                                    , full_name = 'virtual_wireless_interface.hardware.left.my_node.address.zip'
                                    , id = 'virtual_wireless_interface__hardware__left__my_node__address__zip'
                                    , name = 'zip'
                                    , sig_key = 3
                                    , ui_name = 'Virtual wireless interface/Hardware/Net device/My node/Address/Zip code'
                                    )
                                  , Record
                                    ( attr = String `city`
                                    , full_name = 'virtual_wireless_interface.hardware.left.my_node.address.city'
                                    , id = 'virtual_wireless_interface__hardware__left__my_node__address__city'
                                    , name = 'city'
                                    , sig_key = 3
                                    , ui_name = 'Virtual wireless interface/Hardware/Net device/My node/Address/City'
                                    )
                                  , Record
                                    ( attr = String `country`
                                    , full_name = 'virtual_wireless_interface.hardware.left.my_node.address.country'
                                    , id = 'virtual_wireless_interface__hardware__left__my_node__address__country'
                                    , name = 'country'
                                    , sig_key = 3
                                    , ui_name = 'Virtual wireless interface/Hardware/Net device/My node/Address/Country'
                                    )
                                  , Record
                                    ( attr = String `desc`
                                    , full_name = 'virtual_wireless_interface.hardware.left.my_node.address.desc'
                                    , id = 'virtual_wireless_interface__hardware__left__my_node__address__desc'
                                    , name = 'desc'
                                    , sig_key = 3
                                    , ui_name = 'Virtual wireless interface/Hardware/Net device/My node/Address/Description'
                                    )
                                  , Record
                                    ( attr = String `region`
                                    , full_name = 'virtual_wireless_interface.hardware.left.my_node.address.region'
                                    , id = 'virtual_wireless_interface__hardware__left__my_node__address__region'
                                    , name = 'region'
                                    , sig_key = 3
                                    , ui_name = 'Virtual wireless interface/Hardware/Net device/My node/Address/Region'
                                    )
                                  ]
                              , full_name = 'virtual_wireless_interface.hardware.left.my_node.address'
                              , id = 'virtual_wireless_interface__hardware__left__my_node__address'
                              , name = 'address'
                              , sig_key = 2
                              , type_name = 'PAP.Address'
                              , ui_name = 'Virtual wireless interface/Hardware/Net device/My node/Address'
                              , ui_type_name = 'Address'
                              )
                            , Record
                              ( attr = Text `desc`
                              , full_name = 'virtual_wireless_interface.hardware.left.my_node.desc'
                              , id = 'virtual_wireless_interface__hardware__left__my_node__desc'
                              , name = 'desc'
                              , sig_key = 3
                              , ui_name = 'Virtual wireless interface/Hardware/Net device/My node/Description'
                              )
                            , Record
                              ( Class = 'Entity'
                              , attr = Entity `owner`
                              , children_np =
                                  [ Record
                                    ( Class = 'Entity'
                                    , attr = Entity `owner`
                                    , attrs =
                                        [ Record
                                          ( attr = String `name`
                                          , full_name = 'owner.name'
                                          , id = 'owner__name'
                                          , name = 'name'
                                          , sig_key = 3
                                          , ui_name = 'Owner[Adhoc_Group]/Name'
                                          )
                                        ]
                                    , full_name = 'owner'
                                    , id = 'owner'
                                    , name = 'owner'
                                    , sig_key = 2
                                    , type_name = 'PAP.Adhoc_Group'
                                    , ui_name = 'Owner[Adhoc_Group]'
                                    , ui_type_name = 'Adhoc_Group'
                                    )
                                  , Record
                                    ( Class = 'Entity'
                                    , attr = Entity `owner`
                                    , attrs =
                                        [ Record
                                          ( attr = String `name`
                                          , full_name = 'owner.name'
                                          , id = 'owner__name'
                                          , name = 'name'
                                          , sig_key = 3
                                          , ui_name = 'Owner[Association]/Name'
                                          )
                                        ]
                                    , full_name = 'owner'
                                    , id = 'owner'
                                    , name = 'owner'
                                    , sig_key = 2
                                    , type_name = 'PAP.Association'
                                    , ui_name = 'Owner[Association]'
                                    , ui_type_name = 'Association'
                                    )
                                  , Record
                                    ( Class = 'Entity'
                                    , attr = Entity `owner`
                                    , attrs =
                                        [ Record
                                          ( attr = String `name`
                                          , full_name = 'owner.name'
                                          , id = 'owner__name'
                                          , name = 'name'
                                          , sig_key = 3
                                          , ui_name = 'Owner[Company]/Name'
                                          )
                                        , Record
                                          ( attr = String `registered_in`
                                          , full_name = 'owner.registered_in'
                                          , id = 'owner__registered_in'
                                          , name = 'registered_in'
                                          , sig_key = 3
                                          , ui_name = 'Owner[Company]/Registered in'
                                          )
                                        ]
                                    , full_name = 'owner'
                                    , id = 'owner'
                                    , name = 'owner'
                                    , sig_key = 2
                                    , type_name = 'PAP.Company'
                                    , ui_name = 'Owner[Company]'
                                    , ui_type_name = 'Company'
                                    )
                                  , Record
                                    ( Class = 'Entity'
                                    , attr = Entity `owner`
                                    , attrs =
                                        [ Record
                                          ( attr = String `last_name`
                                          , full_name = 'owner.last_name'
                                          , id = 'owner__last_name'
                                          , name = 'last_name'
                                          , sig_key = 3
                                          , ui_name = 'Owner[Person]/Last name'
                                          )
                                        , Record
                                          ( attr = String `first_name`
                                          , full_name = 'owner.first_name'
                                          , id = 'owner__first_name'
                                          , name = 'first_name'
                                          , sig_key = 3
                                          , ui_name = 'Owner[Person]/First name'
                                          )
                                        , Record
                                          ( attr = String `middle_name`
                                          , full_name = 'owner.middle_name'
                                          , id = 'owner__middle_name'
                                          , name = 'middle_name'
                                          , sig_key = 3
                                          , ui_name = 'Owner[Person]/Middle name'
                                          )
                                        , Record
                                          ( attr = String `title`
                                          , full_name = 'owner.title'
                                          , id = 'owner__title'
                                          , name = 'title'
                                          , sig_key = 3
                                          , ui_name = 'Owner[Person]/Academic title'
                                          )
                                        ]
                                    , full_name = 'owner'
                                    , id = 'owner'
                                    , name = 'owner'
                                    , sig_key = 2
                                    , type_name = 'PAP.Person'
                                    , ui_name = 'Owner[Person]'
                                    , ui_type_name = 'Person'
                                    )
                                  ]
                              , default_child = 'PAP.Person'
                              , full_name = 'virtual_wireless_interface.hardware.left.my_node.owner'
                              , id = 'virtual_wireless_interface__hardware__left__my_node__owner'
                              , name = 'owner'
                              , sig_key = 2
                              , type_name = 'PAP.Subject'
                              , ui_name = 'Virtual wireless interface/Hardware/Net device/My node/Owner'
                              , ui_type_name = 'Subject'
                              )
                            , Record
                              ( attr = Position `position`
                              , attrs =
                                  [ Record
                                    ( attr = Angle `lat`
                                    , full_name = 'virtual_wireless_interface.hardware.left.my_node.position.lat'
                                    , id = 'virtual_wireless_interface__hardware__left__my_node__position__lat'
                                    , name = 'lat'
                                    , sig_key = 4
                                    , ui_name = 'Virtual wireless interface/Hardware/Net device/My node/Position/Latitude'
                                    )
                                  , Record
                                    ( attr = Angle `lon`
                                    , full_name = 'virtual_wireless_interface.hardware.left.my_node.position.lon'
                                    , id = 'virtual_wireless_interface__hardware__left__my_node__position__lon'
                                    , name = 'lon'
                                    , sig_key = 4
                                    , ui_name = 'Virtual wireless interface/Hardware/Net device/My node/Position/Longitude'
                                    )
                                  , Record
                                    ( attr = Float `height`
                                    , full_name = 'virtual_wireless_interface.hardware.left.my_node.position.height'
                                    , id = 'virtual_wireless_interface__hardware__left__my_node__position__height'
                                    , name = 'height'
                                    , sig_key = 0
                                    , ui_name = 'Virtual wireless interface/Hardware/Net device/My node/Position/Height'
                                    )
                                  ]
                              , full_name = 'virtual_wireless_interface.hardware.left.my_node.position'
                              , id = 'virtual_wireless_interface__hardware__left__my_node__position'
                              , name = 'position'
                              , ui_name = 'Virtual wireless interface/Hardware/Net device/My node/Position'
                              )
                            , Record
                              ( attr = Boolean `show_in_map`
                              , choices = <Recursion on list...>
                              , full_name = 'virtual_wireless_interface.hardware.left.my_node.show_in_map'
                              , id = 'virtual_wireless_interface__hardware__left__my_node__show_in_map'
                              , name = 'show_in_map'
                              , sig_key = 1
                              , ui_name = 'Virtual wireless interface/Hardware/Net device/My node/Show in map'
                              )
                            ]
                        , full_name = 'virtual_wireless_interface.hardware.left.my_node'
                        , id = 'virtual_wireless_interface__hardware__left__my_node'
                        , name = 'my_node'
                        , sig_key = 2
                        , type_name = 'FFM.Node'
                        , ui_name = 'Virtual wireless interface/Hardware/Net device/My node'
                        , ui_type_name = 'Node'
                        )
                      ]
                  , full_name = 'virtual_wireless_interface.hardware.left'
                  , id = 'virtual_wireless_interface__hardware__left'
                  , name = 'left'
                  , sig_key = 2
                  , type_name = 'FFM.Net_Device'
                  , ui_name = 'Virtual wireless interface/Hardware/Net device'
                  , ui_type_name = 'Net_Device'
                  )
                , Record
                  ( attr = MAC-address `mac_address`
                  , full_name = 'virtual_wireless_interface.hardware.mac_address'
                  , id = 'virtual_wireless_interface__hardware__mac_address'
                  , name = 'mac_address'
                  , sig_key = 3
                  , ui_name = 'Virtual wireless interface/Hardware/Mac address'
                  )
                , Record
                  ( attr = String `name`
                  , full_name = 'virtual_wireless_interface.hardware.name'
                  , id = 'virtual_wireless_interface__hardware__name'
                  , name = 'name'
                  , sig_key = 3
                  , ui_name = 'Virtual wireless interface/Hardware/Name'
                  )
                , Record
                  ( attr = Boolean `is_active`
                  , choices = <Recursion on list...>
                  , full_name = 'virtual_wireless_interface.hardware.is_active'
                  , id = 'virtual_wireless_interface__hardware__is_active'
                  , name = 'is_active'
                  , sig_key = 1
                  , ui_name = 'Virtual wireless interface/Hardware/Is active'
                  )
                , Record
                  ( attr = Text `desc`
                  , full_name = 'virtual_wireless_interface.hardware.desc'
                  , id = 'virtual_wireless_interface__hardware__desc'
                  , name = 'desc'
                  , sig_key = 3
                  , ui_name = 'Virtual wireless interface/Hardware/Description'
                  )
                , Record
                  ( attr = wl-mode `mode`
                  , choices = <Recursion on list...>
                  , full_name = 'virtual_wireless_interface.hardware.mode'
                  , id = 'virtual_wireless_interface__hardware__mode'
                  , name = 'mode'
                  , sig_key = 0
                  , ui_name = 'Virtual wireless interface/Hardware/Mode'
                  )
                , Record
                  ( attr = String `essid`
                  , full_name = 'virtual_wireless_interface.hardware.essid'
                  , id = 'virtual_wireless_interface__hardware__essid'
                  , name = 'essid'
                  , sig_key = 3
                  , ui_name = 'Virtual wireless interface/Hardware/ESSID'
                  )
                , Record
                  ( attr = MAC-address `bssid`
                  , full_name = 'virtual_wireless_interface.hardware.bssid'
                  , id = 'virtual_wireless_interface__hardware__bssid'
                  , name = 'bssid'
                  , sig_key = 3
                  , ui_name = 'Virtual wireless interface/Hardware/BSSID'
                  )
                , Record
                  ( Class = 'Entity'
                  , attr = Entity `standard`
                  , attrs =
                      [ Record
                        ( attr = String `name`
                        , full_name = 'virtual_wireless_interface.hardware.standard.name'
                        , id = 'virtual_wireless_interface__hardware__standard__name'
                        , name = 'name'
                        , sig_key = 3
                        , ui_name = 'Virtual wireless interface/Hardware/Standard/Name'
                        )
                      , Record
                        ( attr = Frequency `bandwidth`
                        , full_name = 'virtual_wireless_interface.hardware.standard.bandwidth'
                        , id = 'virtual_wireless_interface__hardware__standard__bandwidth'
                        , name = 'bandwidth'
                        , sig_key = 4
                        , ui_name = 'Virtual wireless interface/Hardware/Standard/Bandwidth'
                        )
                      ]
                  , full_name = 'virtual_wireless_interface.hardware.standard'
                  , id = 'virtual_wireless_interface__hardware__standard'
                  , name = 'standard'
                  , sig_key = 2
                  , type_name = 'FFM.Wireless_Standard'
                  , ui_name = 'Virtual wireless interface/Hardware/Standard'
                  , ui_type_name = 'Wireless_Standard'
                  )
                , Record
                  ( attr = TX Power `txpower`
                  , full_name = 'virtual_wireless_interface.hardware.txpower'
                  , id = 'virtual_wireless_interface__hardware__txpower'
                  , name = 'txpower'
                  , sig_key = 4
                  , ui_name = 'Virtual wireless interface/Hardware/TX power'
                  )
                , Record
                  ( Class = 'Entity'
                  , attr = Entity `my_node`
                  , attrs =
                      [ Record
                        ( attr = String `name`
                        , full_name = 'virtual_wireless_interface.hardware.my_node.name'
                        , id = 'virtual_wireless_interface__hardware__my_node__name'
                        , name = 'name'
                        , sig_key = 3
                        , ui_name = 'Virtual wireless interface/Hardware/My node/Name'
                        )
                      , Record
                        ( Class = 'Entity'
                        , attr = Entity `manager`
                        , attrs =
                            [ Record
                              ( attr = String `last_name`
                              , full_name = 'virtual_wireless_interface.hardware.my_node.manager.last_name'
                              , id = 'virtual_wireless_interface__hardware__my_node__manager__last_name'
                              , name = 'last_name'
                              , sig_key = 3
                              , ui_name = 'Virtual wireless interface/Hardware/My node/Manager/Last name'
                              )
                            , Record
                              ( attr = String `first_name`
                              , full_name = 'virtual_wireless_interface.hardware.my_node.manager.first_name'
                              , id = 'virtual_wireless_interface__hardware__my_node__manager__first_name'
                              , name = 'first_name'
                              , sig_key = 3
                              , ui_name = 'Virtual wireless interface/Hardware/My node/Manager/First name'
                              )
                            , Record
                              ( attr = String `middle_name`
                              , full_name = 'virtual_wireless_interface.hardware.my_node.manager.middle_name'
                              , id = 'virtual_wireless_interface__hardware__my_node__manager__middle_name'
                              , name = 'middle_name'
                              , sig_key = 3
                              , ui_name = 'Virtual wireless interface/Hardware/My node/Manager/Middle name'
                              )
                            , Record
                              ( attr = String `title`
                              , full_name = 'virtual_wireless_interface.hardware.my_node.manager.title'
                              , id = 'virtual_wireless_interface__hardware__my_node__manager__title'
                              , name = 'title'
                              , sig_key = 3
                              , ui_name = 'Virtual wireless interface/Hardware/My node/Manager/Academic title'
                              )
                            , Record
                              ( attr = Date_Interval `lifetime`
                              , attrs =
                                  [ Record
                                    ( attr = Date `start`
                                    , full_name = 'virtual_wireless_interface.hardware.my_node.manager.lifetime.start'
                                    , id = 'virtual_wireless_interface__hardware__my_node__manager__lifetime__start'
                                    , name = 'start'
                                    , sig_key = 0
                                    , ui_name = 'Virtual wireless interface/Hardware/My node/Manager/Lifetime/Start'
                                    )
                                  , Record
                                    ( attr = Date `finish`
                                    , full_name = 'virtual_wireless_interface.hardware.my_node.manager.lifetime.finish'
                                    , id = 'virtual_wireless_interface__hardware__my_node__manager__lifetime__finish'
                                    , name = 'finish'
                                    , sig_key = 0
                                    , ui_name = 'Virtual wireless interface/Hardware/My node/Manager/Lifetime/Finish'
                                    )
                                  , Record
                                    ( attr = Boolean `alive`
                                    , choices = <Recursion on list...>
                                    , full_name = 'virtual_wireless_interface.hardware.my_node.manager.lifetime.alive'
                                    , id = 'virtual_wireless_interface__hardware__my_node__manager__lifetime__alive'
                                    , name = 'alive'
                                    , sig_key = 1
                                    , ui_name = 'Virtual wireless interface/Hardware/My node/Manager/Lifetime/Alive'
                                    )
                                  ]
                              , full_name = 'virtual_wireless_interface.hardware.my_node.manager.lifetime'
                              , id = 'virtual_wireless_interface__hardware__my_node__manager__lifetime'
                              , name = 'lifetime'
                              , ui_name = 'Virtual wireless interface/Hardware/My node/Manager/Lifetime'
                              )
                            , Record
                              ( attr = Sex `sex`
                              , choices = <Recursion on list...>
                              , full_name = 'virtual_wireless_interface.hardware.my_node.manager.sex'
                              , id = 'virtual_wireless_interface__hardware__my_node__manager__sex'
                              , name = 'sex'
                              , sig_key = 0
                              , ui_name = 'Virtual wireless interface/Hardware/My node/Manager/Sex'
                              )
                            ]
                        , full_name = 'virtual_wireless_interface.hardware.my_node.manager'
                        , id = 'virtual_wireless_interface__hardware__my_node__manager'
                        , name = 'manager'
                        , sig_key = 2
                        , type_name = 'PAP.Person'
                        , ui_name = 'Virtual wireless interface/Hardware/My node/Manager'
                        , ui_type_name = 'Person'
                        )
                      , Record
                        ( Class = 'Entity'
                        , attr = Entity `address`
                        , attrs =
                            [ Record
                              ( attr = String `street`
                              , full_name = 'virtual_wireless_interface.hardware.my_node.address.street'
                              , id = 'virtual_wireless_interface__hardware__my_node__address__street'
                              , name = 'street'
                              , sig_key = 3
                              , ui_name = 'Virtual wireless interface/Hardware/My node/Address/Street'
                              )
                            , Record
                              ( attr = String `zip`
                              , full_name = 'virtual_wireless_interface.hardware.my_node.address.zip'
                              , id = 'virtual_wireless_interface__hardware__my_node__address__zip'
                              , name = 'zip'
                              , sig_key = 3
                              , ui_name = 'Virtual wireless interface/Hardware/My node/Address/Zip code'
                              )
                            , Record
                              ( attr = String `city`
                              , full_name = 'virtual_wireless_interface.hardware.my_node.address.city'
                              , id = 'virtual_wireless_interface__hardware__my_node__address__city'
                              , name = 'city'
                              , sig_key = 3
                              , ui_name = 'Virtual wireless interface/Hardware/My node/Address/City'
                              )
                            , Record
                              ( attr = String `country`
                              , full_name = 'virtual_wireless_interface.hardware.my_node.address.country'
                              , id = 'virtual_wireless_interface__hardware__my_node__address__country'
                              , name = 'country'
                              , sig_key = 3
                              , ui_name = 'Virtual wireless interface/Hardware/My node/Address/Country'
                              )
                            , Record
                              ( attr = String `desc`
                              , full_name = 'virtual_wireless_interface.hardware.my_node.address.desc'
                              , id = 'virtual_wireless_interface__hardware__my_node__address__desc'
                              , name = 'desc'
                              , sig_key = 3
                              , ui_name = 'Virtual wireless interface/Hardware/My node/Address/Description'
                              )
                            , Record
                              ( attr = String `region`
                              , full_name = 'virtual_wireless_interface.hardware.my_node.address.region'
                              , id = 'virtual_wireless_interface__hardware__my_node__address__region'
                              , name = 'region'
                              , sig_key = 3
                              , ui_name = 'Virtual wireless interface/Hardware/My node/Address/Region'
                              )
                            ]
                        , full_name = 'virtual_wireless_interface.hardware.my_node.address'
                        , id = 'virtual_wireless_interface__hardware__my_node__address'
                        , name = 'address'
                        , sig_key = 2
                        , type_name = 'PAP.Address'
                        , ui_name = 'Virtual wireless interface/Hardware/My node/Address'
                        , ui_type_name = 'Address'
                        )
                      , Record
                        ( attr = Text `desc`
                        , full_name = 'virtual_wireless_interface.hardware.my_node.desc'
                        , id = 'virtual_wireless_interface__hardware__my_node__desc'
                        , name = 'desc'
                        , sig_key = 3
                        , ui_name = 'Virtual wireless interface/Hardware/My node/Description'
                        )
                      , Record
                        ( Class = 'Entity'
                        , attr = Entity `owner`
                        , children_np =
                            [ Record
                              ( Class = 'Entity'
                              , attr = Entity `owner`
                              , attrs =
                                  [ Record
                                    ( attr = String `name`
                                    , full_name = 'owner.name'
                                    , id = 'owner__name'
                                    , name = 'name'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Adhoc_Group]/Name'
                                    )
                                  ]
                              , full_name = 'owner'
                              , id = 'owner'
                              , name = 'owner'
                              , sig_key = 2
                              , type_name = 'PAP.Adhoc_Group'
                              , ui_name = 'Owner[Adhoc_Group]'
                              , ui_type_name = 'Adhoc_Group'
                              )
                            , Record
                              ( Class = 'Entity'
                              , attr = Entity `owner`
                              , attrs =
                                  [ Record
                                    ( attr = String `name`
                                    , full_name = 'owner.name'
                                    , id = 'owner__name'
                                    , name = 'name'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Association]/Name'
                                    )
                                  ]
                              , full_name = 'owner'
                              , id = 'owner'
                              , name = 'owner'
                              , sig_key = 2
                              , type_name = 'PAP.Association'
                              , ui_name = 'Owner[Association]'
                              , ui_type_name = 'Association'
                              )
                            , Record
                              ( Class = 'Entity'
                              , attr = Entity `owner`
                              , attrs =
                                  [ Record
                                    ( attr = String `name`
                                    , full_name = 'owner.name'
                                    , id = 'owner__name'
                                    , name = 'name'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Company]/Name'
                                    )
                                  , Record
                                    ( attr = String `registered_in`
                                    , full_name = 'owner.registered_in'
                                    , id = 'owner__registered_in'
                                    , name = 'registered_in'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Company]/Registered in'
                                    )
                                  ]
                              , full_name = 'owner'
                              , id = 'owner'
                              , name = 'owner'
                              , sig_key = 2
                              , type_name = 'PAP.Company'
                              , ui_name = 'Owner[Company]'
                              , ui_type_name = 'Company'
                              )
                            , Record
                              ( Class = 'Entity'
                              , attr = Entity `owner`
                              , attrs =
                                  [ Record
                                    ( attr = String `last_name`
                                    , full_name = 'owner.last_name'
                                    , id = 'owner__last_name'
                                    , name = 'last_name'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Person]/Last name'
                                    )
                                  , Record
                                    ( attr = String `first_name`
                                    , full_name = 'owner.first_name'
                                    , id = 'owner__first_name'
                                    , name = 'first_name'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Person]/First name'
                                    )
                                  , Record
                                    ( attr = String `middle_name`
                                    , full_name = 'owner.middle_name'
                                    , id = 'owner__middle_name'
                                    , name = 'middle_name'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Person]/Middle name'
                                    )
                                  , Record
                                    ( attr = String `title`
                                    , full_name = 'owner.title'
                                    , id = 'owner__title'
                                    , name = 'title'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Person]/Academic title'
                                    )
                                  ]
                              , full_name = 'owner'
                              , id = 'owner'
                              , name = 'owner'
                              , sig_key = 2
                              , type_name = 'PAP.Person'
                              , ui_name = 'Owner[Person]'
                              , ui_type_name = 'Person'
                              )
                            ]
                        , default_child = 'PAP.Person'
                        , full_name = 'virtual_wireless_interface.hardware.my_node.owner'
                        , id = 'virtual_wireless_interface__hardware__my_node__owner'
                        , name = 'owner'
                        , sig_key = 2
                        , type_name = 'PAP.Subject'
                        , ui_name = 'Virtual wireless interface/Hardware/My node/Owner'
                        , ui_type_name = 'Subject'
                        )
                      , Record
                        ( attr = Position `position`
                        , attrs =
                            [ Record
                              ( attr = Angle `lat`
                              , full_name = 'virtual_wireless_interface.hardware.my_node.position.lat'
                              , id = 'virtual_wireless_interface__hardware__my_node__position__lat'
                              , name = 'lat'
                              , sig_key = 4
                              , ui_name = 'Virtual wireless interface/Hardware/My node/Position/Latitude'
                              )
                            , Record
                              ( attr = Angle `lon`
                              , full_name = 'virtual_wireless_interface.hardware.my_node.position.lon'
                              , id = 'virtual_wireless_interface__hardware__my_node__position__lon'
                              , name = 'lon'
                              , sig_key = 4
                              , ui_name = 'Virtual wireless interface/Hardware/My node/Position/Longitude'
                              )
                            , Record
                              ( attr = Float `height`
                              , full_name = 'virtual_wireless_interface.hardware.my_node.position.height'
                              , id = 'virtual_wireless_interface__hardware__my_node__position__height'
                              , name = 'height'
                              , sig_key = 0
                              , ui_name = 'Virtual wireless interface/Hardware/My node/Position/Height'
                              )
                            ]
                        , full_name = 'virtual_wireless_interface.hardware.my_node.position'
                        , id = 'virtual_wireless_interface__hardware__my_node__position'
                        , name = 'position'
                        , ui_name = 'Virtual wireless interface/Hardware/My node/Position'
                        )
                      , Record
                        ( attr = Boolean `show_in_map`
                        , choices = <Recursion on list...>
                        , full_name = 'virtual_wireless_interface.hardware.my_node.show_in_map'
                        , id = 'virtual_wireless_interface__hardware__my_node__show_in_map'
                        , name = 'show_in_map'
                        , sig_key = 1
                        , ui_name = 'Virtual wireless interface/Hardware/My node/Show in map'
                        )
                      ]
                  , full_name = 'virtual_wireless_interface.hardware.my_node'
                  , id = 'virtual_wireless_interface__hardware__my_node'
                  , name = 'my_node'
                  , sig_key = 2
                  , type_name = 'FFM.Node'
                  , ui_name = 'Virtual wireless interface/Hardware/My node'
                  , ui_type_name = 'Node'
                  )
                , Record
                  ( Class = 'Entity'
                  , attr = Entity `my_net_device`
                  , attrs =
                      [ Record
                        ( Class = 'Entity'
                        , attr = Net_Device_Type `left`
                        , attrs =
                            [ Record
                              ( attr = String `name`
                              , full_name = 'virtual_wireless_interface.hardware.my_net_device.left.name'
                              , id = 'virtual_wireless_interface__hardware__my_net_device__left__name'
                              , name = 'name'
                              , sig_key = 3
                              , ui_name = 'Virtual wireless interface/Hardware/My net device/Net device type/Name'
                              )
                            , Record
                              ( attr = String `model_no`
                              , full_name = 'virtual_wireless_interface.hardware.my_net_device.left.model_no'
                              , id = 'virtual_wireless_interface__hardware__my_net_device__left__model_no'
                              , name = 'model_no'
                              , sig_key = 3
                              , ui_name = 'Virtual wireless interface/Hardware/My net device/Net device type/Model no'
                              )
                            , Record
                              ( attr = String `revision`
                              , full_name = 'virtual_wireless_interface.hardware.my_net_device.left.revision'
                              , id = 'virtual_wireless_interface__hardware__my_net_device__left__revision'
                              , name = 'revision'
                              , sig_key = 3
                              , ui_name = 'Virtual wireless interface/Hardware/My net device/Net device type/Revision'
                              )
                            , Record
                              ( attr = Text `desc`
                              , full_name = 'virtual_wireless_interface.hardware.my_net_device.left.desc'
                              , id = 'virtual_wireless_interface__hardware__my_net_device__left__desc'
                              , name = 'desc'
                              , sig_key = 3
                              , ui_name = 'Virtual wireless interface/Hardware/My net device/Net device type/Description'
                              )
                            ]
                        , full_name = 'virtual_wireless_interface.hardware.my_net_device.left'
                        , id = 'virtual_wireless_interface__hardware__my_net_device__left'
                        , name = 'left'
                        , sig_key = 2
                        , type_name = 'FFM.Net_Device_Type'
                        , ui_name = 'Virtual wireless interface/Hardware/My net device/Net device type'
                        , ui_type_name = 'Net_Device_Type'
                        )
                      , Record
                        ( Class = 'Entity'
                        , attr = Entity `node`
                        , attrs =
                            [ Record
                              ( attr = String `name`
                              , full_name = 'virtual_wireless_interface.hardware.my_net_device.node.name'
                              , id = 'virtual_wireless_interface__hardware__my_net_device__node__name'
                              , name = 'name'
                              , sig_key = 3
                              , ui_name = 'Virtual wireless interface/Hardware/My net device/Node/Name'
                              )
                            , Record
                              ( Class = 'Entity'
                              , attr = Entity `manager`
                              , attrs =
                                  [ Record
                                    ( attr = String `last_name`
                                    , full_name = 'virtual_wireless_interface.hardware.my_net_device.node.manager.last_name'
                                    , id = 'virtual_wireless_interface__hardware__my_net_device__node__manager__last_name'
                                    , name = 'last_name'
                                    , sig_key = 3
                                    , ui_name = 'Virtual wireless interface/Hardware/My net device/Node/Manager/Last name'
                                    )
                                  , Record
                                    ( attr = String `first_name`
                                    , full_name = 'virtual_wireless_interface.hardware.my_net_device.node.manager.first_name'
                                    , id = 'virtual_wireless_interface__hardware__my_net_device__node__manager__first_name'
                                    , name = 'first_name'
                                    , sig_key = 3
                                    , ui_name = 'Virtual wireless interface/Hardware/My net device/Node/Manager/First name'
                                    )
                                  , Record
                                    ( attr = String `middle_name`
                                    , full_name = 'virtual_wireless_interface.hardware.my_net_device.node.manager.middle_name'
                                    , id = 'virtual_wireless_interface__hardware__my_net_device__node__manager__middle_name'
                                    , name = 'middle_name'
                                    , sig_key = 3
                                    , ui_name = 'Virtual wireless interface/Hardware/My net device/Node/Manager/Middle name'
                                    )
                                  , Record
                                    ( attr = String `title`
                                    , full_name = 'virtual_wireless_interface.hardware.my_net_device.node.manager.title'
                                    , id = 'virtual_wireless_interface__hardware__my_net_device__node__manager__title'
                                    , name = 'title'
                                    , sig_key = 3
                                    , ui_name = 'Virtual wireless interface/Hardware/My net device/Node/Manager/Academic title'
                                    )
                                  , Record
                                    ( attr = Date_Interval `lifetime`
                                    , attrs =
                                        [ Record
                                          ( attr = Date `start`
                                          , full_name = 'virtual_wireless_interface.hardware.my_net_device.node.manager.lifetime.start'
                                          , id = 'virtual_wireless_interface__hardware__my_net_device__node__manager__lifetime__start'
                                          , name = 'start'
                                          , sig_key = 0
                                          , ui_name = 'Virtual wireless interface/Hardware/My net device/Node/Manager/Lifetime/Start'
                                          )
                                        , Record
                                          ( attr = Date `finish`
                                          , full_name = 'virtual_wireless_interface.hardware.my_net_device.node.manager.lifetime.finish'
                                          , id = 'virtual_wireless_interface__hardware__my_net_device__node__manager__lifetime__finish'
                                          , name = 'finish'
                                          , sig_key = 0
                                          , ui_name = 'Virtual wireless interface/Hardware/My net device/Node/Manager/Lifetime/Finish'
                                          )
                                        , Record
                                          ( attr = Boolean `alive`
                                          , choices = <Recursion on list...>
                                          , full_name = 'virtual_wireless_interface.hardware.my_net_device.node.manager.lifetime.alive'
                                          , id = 'virtual_wireless_interface__hardware__my_net_device__node__manager__lifetime__alive'
                                          , name = 'alive'
                                          , sig_key = 1
                                          , ui_name = 'Virtual wireless interface/Hardware/My net device/Node/Manager/Lifetime/Alive'
                                          )
                                        ]
                                    , full_name = 'virtual_wireless_interface.hardware.my_net_device.node.manager.lifetime'
                                    , id = 'virtual_wireless_interface__hardware__my_net_device__node__manager__lifetime'
                                    , name = 'lifetime'
                                    , ui_name = 'Virtual wireless interface/Hardware/My net device/Node/Manager/Lifetime'
                                    )
                                  , Record
                                    ( attr = Sex `sex`
                                    , choices = <Recursion on list...>
                                    , full_name = 'virtual_wireless_interface.hardware.my_net_device.node.manager.sex'
                                    , id = 'virtual_wireless_interface__hardware__my_net_device__node__manager__sex'
                                    , name = 'sex'
                                    , sig_key = 0
                                    , ui_name = 'Virtual wireless interface/Hardware/My net device/Node/Manager/Sex'
                                    )
                                  ]
                              , full_name = 'virtual_wireless_interface.hardware.my_net_device.node.manager'
                              , id = 'virtual_wireless_interface__hardware__my_net_device__node__manager'
                              , name = 'manager'
                              , sig_key = 2
                              , type_name = 'PAP.Person'
                              , ui_name = 'Virtual wireless interface/Hardware/My net device/Node/Manager'
                              , ui_type_name = 'Person'
                              )
                            , Record
                              ( Class = 'Entity'
                              , attr = Entity `address`
                              , attrs =
                                  [ Record
                                    ( attr = String `street`
                                    , full_name = 'virtual_wireless_interface.hardware.my_net_device.node.address.street'
                                    , id = 'virtual_wireless_interface__hardware__my_net_device__node__address__street'
                                    , name = 'street'
                                    , sig_key = 3
                                    , ui_name = 'Virtual wireless interface/Hardware/My net device/Node/Address/Street'
                                    )
                                  , Record
                                    ( attr = String `zip`
                                    , full_name = 'virtual_wireless_interface.hardware.my_net_device.node.address.zip'
                                    , id = 'virtual_wireless_interface__hardware__my_net_device__node__address__zip'
                                    , name = 'zip'
                                    , sig_key = 3
                                    , ui_name = 'Virtual wireless interface/Hardware/My net device/Node/Address/Zip code'
                                    )
                                  , Record
                                    ( attr = String `city`
                                    , full_name = 'virtual_wireless_interface.hardware.my_net_device.node.address.city'
                                    , id = 'virtual_wireless_interface__hardware__my_net_device__node__address__city'
                                    , name = 'city'
                                    , sig_key = 3
                                    , ui_name = 'Virtual wireless interface/Hardware/My net device/Node/Address/City'
                                    )
                                  , Record
                                    ( attr = String `country`
                                    , full_name = 'virtual_wireless_interface.hardware.my_net_device.node.address.country'
                                    , id = 'virtual_wireless_interface__hardware__my_net_device__node__address__country'
                                    , name = 'country'
                                    , sig_key = 3
                                    , ui_name = 'Virtual wireless interface/Hardware/My net device/Node/Address/Country'
                                    )
                                  , Record
                                    ( attr = String `desc`
                                    , full_name = 'virtual_wireless_interface.hardware.my_net_device.node.address.desc'
                                    , id = 'virtual_wireless_interface__hardware__my_net_device__node__address__desc'
                                    , name = 'desc'
                                    , sig_key = 3
                                    , ui_name = 'Virtual wireless interface/Hardware/My net device/Node/Address/Description'
                                    )
                                  , Record
                                    ( attr = String `region`
                                    , full_name = 'virtual_wireless_interface.hardware.my_net_device.node.address.region'
                                    , id = 'virtual_wireless_interface__hardware__my_net_device__node__address__region'
                                    , name = 'region'
                                    , sig_key = 3
                                    , ui_name = 'Virtual wireless interface/Hardware/My net device/Node/Address/Region'
                                    )
                                  ]
                              , full_name = 'virtual_wireless_interface.hardware.my_net_device.node.address'
                              , id = 'virtual_wireless_interface__hardware__my_net_device__node__address'
                              , name = 'address'
                              , sig_key = 2
                              , type_name = 'PAP.Address'
                              , ui_name = 'Virtual wireless interface/Hardware/My net device/Node/Address'
                              , ui_type_name = 'Address'
                              )
                            , Record
                              ( attr = Text `desc`
                              , full_name = 'virtual_wireless_interface.hardware.my_net_device.node.desc'
                              , id = 'virtual_wireless_interface__hardware__my_net_device__node__desc'
                              , name = 'desc'
                              , sig_key = 3
                              , ui_name = 'Virtual wireless interface/Hardware/My net device/Node/Description'
                              )
                            , Record
                              ( Class = 'Entity'
                              , attr = Entity `owner`
                              , children_np =
                                  [ Record
                                    ( Class = 'Entity'
                                    , attr = Entity `owner`
                                    , attrs =
                                        [ Record
                                          ( attr = String `name`
                                          , full_name = 'owner.name'
                                          , id = 'owner__name'
                                          , name = 'name'
                                          , sig_key = 3
                                          , ui_name = 'Owner[Adhoc_Group]/Name'
                                          )
                                        ]
                                    , full_name = 'owner'
                                    , id = 'owner'
                                    , name = 'owner'
                                    , sig_key = 2
                                    , type_name = 'PAP.Adhoc_Group'
                                    , ui_name = 'Owner[Adhoc_Group]'
                                    , ui_type_name = 'Adhoc_Group'
                                    )
                                  , Record
                                    ( Class = 'Entity'
                                    , attr = Entity `owner`
                                    , attrs =
                                        [ Record
                                          ( attr = String `name`
                                          , full_name = 'owner.name'
                                          , id = 'owner__name'
                                          , name = 'name'
                                          , sig_key = 3
                                          , ui_name = 'Owner[Association]/Name'
                                          )
                                        ]
                                    , full_name = 'owner'
                                    , id = 'owner'
                                    , name = 'owner'
                                    , sig_key = 2
                                    , type_name = 'PAP.Association'
                                    , ui_name = 'Owner[Association]'
                                    , ui_type_name = 'Association'
                                    )
                                  , Record
                                    ( Class = 'Entity'
                                    , attr = Entity `owner`
                                    , attrs =
                                        [ Record
                                          ( attr = String `name`
                                          , full_name = 'owner.name'
                                          , id = 'owner__name'
                                          , name = 'name'
                                          , sig_key = 3
                                          , ui_name = 'Owner[Company]/Name'
                                          )
                                        , Record
                                          ( attr = String `registered_in`
                                          , full_name = 'owner.registered_in'
                                          , id = 'owner__registered_in'
                                          , name = 'registered_in'
                                          , sig_key = 3
                                          , ui_name = 'Owner[Company]/Registered in'
                                          )
                                        ]
                                    , full_name = 'owner'
                                    , id = 'owner'
                                    , name = 'owner'
                                    , sig_key = 2
                                    , type_name = 'PAP.Company'
                                    , ui_name = 'Owner[Company]'
                                    , ui_type_name = 'Company'
                                    )
                                  , Record
                                    ( Class = 'Entity'
                                    , attr = Entity `owner`
                                    , attrs =
                                        [ Record
                                          ( attr = String `last_name`
                                          , full_name = 'owner.last_name'
                                          , id = 'owner__last_name'
                                          , name = 'last_name'
                                          , sig_key = 3
                                          , ui_name = 'Owner[Person]/Last name'
                                          )
                                        , Record
                                          ( attr = String `first_name`
                                          , full_name = 'owner.first_name'
                                          , id = 'owner__first_name'
                                          , name = 'first_name'
                                          , sig_key = 3
                                          , ui_name = 'Owner[Person]/First name'
                                          )
                                        , Record
                                          ( attr = String `middle_name`
                                          , full_name = 'owner.middle_name'
                                          , id = 'owner__middle_name'
                                          , name = 'middle_name'
                                          , sig_key = 3
                                          , ui_name = 'Owner[Person]/Middle name'
                                          )
                                        , Record
                                          ( attr = String `title`
                                          , full_name = 'owner.title'
                                          , id = 'owner__title'
                                          , name = 'title'
                                          , sig_key = 3
                                          , ui_name = 'Owner[Person]/Academic title'
                                          )
                                        ]
                                    , full_name = 'owner'
                                    , id = 'owner'
                                    , name = 'owner'
                                    , sig_key = 2
                                    , type_name = 'PAP.Person'
                                    , ui_name = 'Owner[Person]'
                                    , ui_type_name = 'Person'
                                    )
                                  ]
                              , default_child = 'PAP.Person'
                              , full_name = 'virtual_wireless_interface.hardware.my_net_device.node.owner'
                              , id = 'virtual_wireless_interface__hardware__my_net_device__node__owner'
                              , name = 'owner'
                              , sig_key = 2
                              , type_name = 'PAP.Subject'
                              , ui_name = 'Virtual wireless interface/Hardware/My net device/Node/Owner'
                              , ui_type_name = 'Subject'
                              )
                            , Record
                              ( attr = Position `position`
                              , attrs =
                                  [ Record
                                    ( attr = Angle `lat`
                                    , full_name = 'virtual_wireless_interface.hardware.my_net_device.node.position.lat'
                                    , id = 'virtual_wireless_interface__hardware__my_net_device__node__position__lat'
                                    , name = 'lat'
                                    , sig_key = 4
                                    , ui_name = 'Virtual wireless interface/Hardware/My net device/Node/Position/Latitude'
                                    )
                                  , Record
                                    ( attr = Angle `lon`
                                    , full_name = 'virtual_wireless_interface.hardware.my_net_device.node.position.lon'
                                    , id = 'virtual_wireless_interface__hardware__my_net_device__node__position__lon'
                                    , name = 'lon'
                                    , sig_key = 4
                                    , ui_name = 'Virtual wireless interface/Hardware/My net device/Node/Position/Longitude'
                                    )
                                  , Record
                                    ( attr = Float `height`
                                    , full_name = 'virtual_wireless_interface.hardware.my_net_device.node.position.height'
                                    , id = 'virtual_wireless_interface__hardware__my_net_device__node__position__height'
                                    , name = 'height'
                                    , sig_key = 0
                                    , ui_name = 'Virtual wireless interface/Hardware/My net device/Node/Position/Height'
                                    )
                                  ]
                              , full_name = 'virtual_wireless_interface.hardware.my_net_device.node.position'
                              , id = 'virtual_wireless_interface__hardware__my_net_device__node__position'
                              , name = 'position'
                              , ui_name = 'Virtual wireless interface/Hardware/My net device/Node/Position'
                              )
                            , Record
                              ( attr = Boolean `show_in_map`
                              , choices = <Recursion on list...>
                              , full_name = 'virtual_wireless_interface.hardware.my_net_device.node.show_in_map'
                              , id = 'virtual_wireless_interface__hardware__my_net_device__node__show_in_map'
                              , name = 'show_in_map'
                              , sig_key = 1
                              , ui_name = 'Virtual wireless interface/Hardware/My net device/Node/Show in map'
                              )
                            ]
                        , full_name = 'virtual_wireless_interface.hardware.my_net_device.node'
                        , id = 'virtual_wireless_interface__hardware__my_net_device__node'
                        , name = 'node'
                        , sig_key = 2
                        , type_name = 'FFM.Node'
                        , ui_name = 'Virtual wireless interface/Hardware/My net device/Node'
                        , ui_type_name = 'Node'
                        )
                      , Record
                        ( attr = String `name`
                        , full_name = 'virtual_wireless_interface.hardware.my_net_device.name'
                        , id = 'virtual_wireless_interface__hardware__my_net_device__name'
                        , name = 'name'
                        , sig_key = 3
                        , ui_name = 'Virtual wireless interface/Hardware/My net device/Name'
                        )
                      , Record
                        ( attr = Text `desc`
                        , full_name = 'virtual_wireless_interface.hardware.my_net_device.desc'
                        , id = 'virtual_wireless_interface__hardware__my_net_device__desc'
                        , name = 'desc'
                        , sig_key = 3
                        , ui_name = 'Virtual wireless interface/Hardware/My net device/Description'
                        )
                      , Record
                        ( Class = 'Entity'
                        , attr = Entity `my_node`
                        , attrs =
                            [ Record
                              ( attr = String `name`
                              , full_name = 'virtual_wireless_interface.hardware.my_net_device.my_node.name'
                              , id = 'virtual_wireless_interface__hardware__my_net_device__my_node__name'
                              , name = 'name'
                              , sig_key = 3
                              , ui_name = 'Virtual wireless interface/Hardware/My net device/My node/Name'
                              )
                            , Record
                              ( Class = 'Entity'
                              , attr = Entity `manager`
                              , attrs =
                                  [ Record
                                    ( attr = String `last_name`
                                    , full_name = 'virtual_wireless_interface.hardware.my_net_device.my_node.manager.last_name'
                                    , id = 'virtual_wireless_interface__hardware__my_net_device__my_node__manager__last_name'
                                    , name = 'last_name'
                                    , sig_key = 3
                                    , ui_name = 'Virtual wireless interface/Hardware/My net device/My node/Manager/Last name'
                                    )
                                  , Record
                                    ( attr = String `first_name`
                                    , full_name = 'virtual_wireless_interface.hardware.my_net_device.my_node.manager.first_name'
                                    , id = 'virtual_wireless_interface__hardware__my_net_device__my_node__manager__first_name'
                                    , name = 'first_name'
                                    , sig_key = 3
                                    , ui_name = 'Virtual wireless interface/Hardware/My net device/My node/Manager/First name'
                                    )
                                  , Record
                                    ( attr = String `middle_name`
                                    , full_name = 'virtual_wireless_interface.hardware.my_net_device.my_node.manager.middle_name'
                                    , id = 'virtual_wireless_interface__hardware__my_net_device__my_node__manager__middle_name'
                                    , name = 'middle_name'
                                    , sig_key = 3
                                    , ui_name = 'Virtual wireless interface/Hardware/My net device/My node/Manager/Middle name'
                                    )
                                  , Record
                                    ( attr = String `title`
                                    , full_name = 'virtual_wireless_interface.hardware.my_net_device.my_node.manager.title'
                                    , id = 'virtual_wireless_interface__hardware__my_net_device__my_node__manager__title'
                                    , name = 'title'
                                    , sig_key = 3
                                    , ui_name = 'Virtual wireless interface/Hardware/My net device/My node/Manager/Academic title'
                                    )
                                  , Record
                                    ( attr = Date_Interval `lifetime`
                                    , attrs =
                                        [ Record
                                          ( attr = Date `start`
                                          , full_name = 'virtual_wireless_interface.hardware.my_net_device.my_node.manager.lifetime.start'
                                          , id = 'virtual_wireless_interface__hardware__my_net_device__my_node__manager__lifetime__start'
                                          , name = 'start'
                                          , sig_key = 0
                                          , ui_name = 'Virtual wireless interface/Hardware/My net device/My node/Manager/Lifetime/Start'
                                          )
                                        , Record
                                          ( attr = Date `finish`
                                          , full_name = 'virtual_wireless_interface.hardware.my_net_device.my_node.manager.lifetime.finish'
                                          , id = 'virtual_wireless_interface__hardware__my_net_device__my_node__manager__lifetime__finish'
                                          , name = 'finish'
                                          , sig_key = 0
                                          , ui_name = 'Virtual wireless interface/Hardware/My net device/My node/Manager/Lifetime/Finish'
                                          )
                                        , Record
                                          ( attr = Boolean `alive`
                                          , choices = <Recursion on list...>
                                          , full_name = 'virtual_wireless_interface.hardware.my_net_device.my_node.manager.lifetime.alive'
                                          , id = 'virtual_wireless_interface__hardware__my_net_device__my_node__manager__lifetime__alive'
                                          , name = 'alive'
                                          , sig_key = 1
                                          , ui_name = 'Virtual wireless interface/Hardware/My net device/My node/Manager/Lifetime/Alive'
                                          )
                                        ]
                                    , full_name = 'virtual_wireless_interface.hardware.my_net_device.my_node.manager.lifetime'
                                    , id = 'virtual_wireless_interface__hardware__my_net_device__my_node__manager__lifetime'
                                    , name = 'lifetime'
                                    , ui_name = 'Virtual wireless interface/Hardware/My net device/My node/Manager/Lifetime'
                                    )
                                  , Record
                                    ( attr = Sex `sex`
                                    , choices = <Recursion on list...>
                                    , full_name = 'virtual_wireless_interface.hardware.my_net_device.my_node.manager.sex'
                                    , id = 'virtual_wireless_interface__hardware__my_net_device__my_node__manager__sex'
                                    , name = 'sex'
                                    , sig_key = 0
                                    , ui_name = 'Virtual wireless interface/Hardware/My net device/My node/Manager/Sex'
                                    )
                                  ]
                              , full_name = 'virtual_wireless_interface.hardware.my_net_device.my_node.manager'
                              , id = 'virtual_wireless_interface__hardware__my_net_device__my_node__manager'
                              , name = 'manager'
                              , sig_key = 2
                              , type_name = 'PAP.Person'
                              , ui_name = 'Virtual wireless interface/Hardware/My net device/My node/Manager'
                              , ui_type_name = 'Person'
                              )
                            , Record
                              ( Class = 'Entity'
                              , attr = Entity `address`
                              , attrs =
                                  [ Record
                                    ( attr = String `street`
                                    , full_name = 'virtual_wireless_interface.hardware.my_net_device.my_node.address.street'
                                    , id = 'virtual_wireless_interface__hardware__my_net_device__my_node__address__street'
                                    , name = 'street'
                                    , sig_key = 3
                                    , ui_name = 'Virtual wireless interface/Hardware/My net device/My node/Address/Street'
                                    )
                                  , Record
                                    ( attr = String `zip`
                                    , full_name = 'virtual_wireless_interface.hardware.my_net_device.my_node.address.zip'
                                    , id = 'virtual_wireless_interface__hardware__my_net_device__my_node__address__zip'
                                    , name = 'zip'
                                    , sig_key = 3
                                    , ui_name = 'Virtual wireless interface/Hardware/My net device/My node/Address/Zip code'
                                    )
                                  , Record
                                    ( attr = String `city`
                                    , full_name = 'virtual_wireless_interface.hardware.my_net_device.my_node.address.city'
                                    , id = 'virtual_wireless_interface__hardware__my_net_device__my_node__address__city'
                                    , name = 'city'
                                    , sig_key = 3
                                    , ui_name = 'Virtual wireless interface/Hardware/My net device/My node/Address/City'
                                    )
                                  , Record
                                    ( attr = String `country`
                                    , full_name = 'virtual_wireless_interface.hardware.my_net_device.my_node.address.country'
                                    , id = 'virtual_wireless_interface__hardware__my_net_device__my_node__address__country'
                                    , name = 'country'
                                    , sig_key = 3
                                    , ui_name = 'Virtual wireless interface/Hardware/My net device/My node/Address/Country'
                                    )
                                  , Record
                                    ( attr = String `desc`
                                    , full_name = 'virtual_wireless_interface.hardware.my_net_device.my_node.address.desc'
                                    , id = 'virtual_wireless_interface__hardware__my_net_device__my_node__address__desc'
                                    , name = 'desc'
                                    , sig_key = 3
                                    , ui_name = 'Virtual wireless interface/Hardware/My net device/My node/Address/Description'
                                    )
                                  , Record
                                    ( attr = String `region`
                                    , full_name = 'virtual_wireless_interface.hardware.my_net_device.my_node.address.region'
                                    , id = 'virtual_wireless_interface__hardware__my_net_device__my_node__address__region'
                                    , name = 'region'
                                    , sig_key = 3
                                    , ui_name = 'Virtual wireless interface/Hardware/My net device/My node/Address/Region'
                                    )
                                  ]
                              , full_name = 'virtual_wireless_interface.hardware.my_net_device.my_node.address'
                              , id = 'virtual_wireless_interface__hardware__my_net_device__my_node__address'
                              , name = 'address'
                              , sig_key = 2
                              , type_name = 'PAP.Address'
                              , ui_name = 'Virtual wireless interface/Hardware/My net device/My node/Address'
                              , ui_type_name = 'Address'
                              )
                            , Record
                              ( attr = Text `desc`
                              , full_name = 'virtual_wireless_interface.hardware.my_net_device.my_node.desc'
                              , id = 'virtual_wireless_interface__hardware__my_net_device__my_node__desc'
                              , name = 'desc'
                              , sig_key = 3
                              , ui_name = 'Virtual wireless interface/Hardware/My net device/My node/Description'
                              )
                            , Record
                              ( Class = 'Entity'
                              , attr = Entity `owner`
                              , children_np =
                                  [ Record
                                    ( Class = 'Entity'
                                    , attr = Entity `owner`
                                    , attrs =
                                        [ Record
                                          ( attr = String `name`
                                          , full_name = 'owner.name'
                                          , id = 'owner__name'
                                          , name = 'name'
                                          , sig_key = 3
                                          , ui_name = 'Owner[Adhoc_Group]/Name'
                                          )
                                        ]
                                    , full_name = 'owner'
                                    , id = 'owner'
                                    , name = 'owner'
                                    , sig_key = 2
                                    , type_name = 'PAP.Adhoc_Group'
                                    , ui_name = 'Owner[Adhoc_Group]'
                                    , ui_type_name = 'Adhoc_Group'
                                    )
                                  , Record
                                    ( Class = 'Entity'
                                    , attr = Entity `owner`
                                    , attrs =
                                        [ Record
                                          ( attr = String `name`
                                          , full_name = 'owner.name'
                                          , id = 'owner__name'
                                          , name = 'name'
                                          , sig_key = 3
                                          , ui_name = 'Owner[Association]/Name'
                                          )
                                        ]
                                    , full_name = 'owner'
                                    , id = 'owner'
                                    , name = 'owner'
                                    , sig_key = 2
                                    , type_name = 'PAP.Association'
                                    , ui_name = 'Owner[Association]'
                                    , ui_type_name = 'Association'
                                    )
                                  , Record
                                    ( Class = 'Entity'
                                    , attr = Entity `owner`
                                    , attrs =
                                        [ Record
                                          ( attr = String `name`
                                          , full_name = 'owner.name'
                                          , id = 'owner__name'
                                          , name = 'name'
                                          , sig_key = 3
                                          , ui_name = 'Owner[Company]/Name'
                                          )
                                        , Record
                                          ( attr = String `registered_in`
                                          , full_name = 'owner.registered_in'
                                          , id = 'owner__registered_in'
                                          , name = 'registered_in'
                                          , sig_key = 3
                                          , ui_name = 'Owner[Company]/Registered in'
                                          )
                                        ]
                                    , full_name = 'owner'
                                    , id = 'owner'
                                    , name = 'owner'
                                    , sig_key = 2
                                    , type_name = 'PAP.Company'
                                    , ui_name = 'Owner[Company]'
                                    , ui_type_name = 'Company'
                                    )
                                  , Record
                                    ( Class = 'Entity'
                                    , attr = Entity `owner`
                                    , attrs =
                                        [ Record
                                          ( attr = String `last_name`
                                          , full_name = 'owner.last_name'
                                          , id = 'owner__last_name'
                                          , name = 'last_name'
                                          , sig_key = 3
                                          , ui_name = 'Owner[Person]/Last name'
                                          )
                                        , Record
                                          ( attr = String `first_name`
                                          , full_name = 'owner.first_name'
                                          , id = 'owner__first_name'
                                          , name = 'first_name'
                                          , sig_key = 3
                                          , ui_name = 'Owner[Person]/First name'
                                          )
                                        , Record
                                          ( attr = String `middle_name`
                                          , full_name = 'owner.middle_name'
                                          , id = 'owner__middle_name'
                                          , name = 'middle_name'
                                          , sig_key = 3
                                          , ui_name = 'Owner[Person]/Middle name'
                                          )
                                        , Record
                                          ( attr = String `title`
                                          , full_name = 'owner.title'
                                          , id = 'owner__title'
                                          , name = 'title'
                                          , sig_key = 3
                                          , ui_name = 'Owner[Person]/Academic title'
                                          )
                                        ]
                                    , full_name = 'owner'
                                    , id = 'owner'
                                    , name = 'owner'
                                    , sig_key = 2
                                    , type_name = 'PAP.Person'
                                    , ui_name = 'Owner[Person]'
                                    , ui_type_name = 'Person'
                                    )
                                  ]
                              , default_child = 'PAP.Person'
                              , full_name = 'virtual_wireless_interface.hardware.my_net_device.my_node.owner'
                              , id = 'virtual_wireless_interface__hardware__my_net_device__my_node__owner'
                              , name = 'owner'
                              , sig_key = 2
                              , type_name = 'PAP.Subject'
                              , ui_name = 'Virtual wireless interface/Hardware/My net device/My node/Owner'
                              , ui_type_name = 'Subject'
                              )
                            , Record
                              ( attr = Position `position`
                              , attrs =
                                  [ Record
                                    ( attr = Angle `lat`
                                    , full_name = 'virtual_wireless_interface.hardware.my_net_device.my_node.position.lat'
                                    , id = 'virtual_wireless_interface__hardware__my_net_device__my_node__position__lat'
                                    , name = 'lat'
                                    , sig_key = 4
                                    , ui_name = 'Virtual wireless interface/Hardware/My net device/My node/Position/Latitude'
                                    )
                                  , Record
                                    ( attr = Angle `lon`
                                    , full_name = 'virtual_wireless_interface.hardware.my_net_device.my_node.position.lon'
                                    , id = 'virtual_wireless_interface__hardware__my_net_device__my_node__position__lon'
                                    , name = 'lon'
                                    , sig_key = 4
                                    , ui_name = 'Virtual wireless interface/Hardware/My net device/My node/Position/Longitude'
                                    )
                                  , Record
                                    ( attr = Float `height`
                                    , full_name = 'virtual_wireless_interface.hardware.my_net_device.my_node.position.height'
                                    , id = 'virtual_wireless_interface__hardware__my_net_device__my_node__position__height'
                                    , name = 'height'
                                    , sig_key = 0
                                    , ui_name = 'Virtual wireless interface/Hardware/My net device/My node/Position/Height'
                                    )
                                  ]
                              , full_name = 'virtual_wireless_interface.hardware.my_net_device.my_node.position'
                              , id = 'virtual_wireless_interface__hardware__my_net_device__my_node__position'
                              , name = 'position'
                              , ui_name = 'Virtual wireless interface/Hardware/My net device/My node/Position'
                              )
                            , Record
                              ( attr = Boolean `show_in_map`
                              , choices = <Recursion on list...>
                              , full_name = 'virtual_wireless_interface.hardware.my_net_device.my_node.show_in_map'
                              , id = 'virtual_wireless_interface__hardware__my_net_device__my_node__show_in_map'
                              , name = 'show_in_map'
                              , sig_key = 1
                              , ui_name = 'Virtual wireless interface/Hardware/My net device/My node/Show in map'
                              )
                            ]
                        , full_name = 'virtual_wireless_interface.hardware.my_net_device.my_node'
                        , id = 'virtual_wireless_interface__hardware__my_net_device__my_node'
                        , name = 'my_node'
                        , sig_key = 2
                        , type_name = 'FFM.Node'
                        , ui_name = 'Virtual wireless interface/Hardware/My net device/My node'
                        , ui_type_name = 'Node'
                        )
                      ]
                  , full_name = 'virtual_wireless_interface.hardware.my_net_device'
                  , id = 'virtual_wireless_interface__hardware__my_net_device'
                  , name = 'my_net_device'
                  , sig_key = 2
                  , type_name = 'FFM.Net_Device'
                  , ui_name = 'Virtual wireless interface/Hardware/My net device'
                  , ui_type_name = 'Net_Device'
                  )
                ]
            , full_name = 'virtual_wireless_interface.hardware'
            , id = 'virtual_wireless_interface__hardware'
            , name = 'hardware'
            , sig_key = 2
            , type_name = 'FFM.Wireless_Interface'
            , ui_name = 'Virtual wireless interface/Hardware'
            , ui_type_name = 'Wireless_Interface'
            )
          , Record
            ( attr = MAC-address `mac_address`
            , full_name = 'virtual_wireless_interface.mac_address'
            , id = 'virtual_wireless_interface__mac_address'
            , name = 'mac_address'
            , sig_key = 3
            , ui_name = 'Virtual wireless interface/Mac address'
            )
          , Record
            ( attr = String `name`
            , full_name = 'virtual_wireless_interface.name'
            , id = 'virtual_wireless_interface__name'
            , name = 'name'
            , sig_key = 3
            , ui_name = 'Virtual wireless interface/Name'
            )
          , Record
            ( attr = Boolean `is_active`
            , choices = <Recursion on list...>
            , full_name = 'virtual_wireless_interface.is_active'
            , id = 'virtual_wireless_interface__is_active'
            , name = 'is_active'
            , sig_key = 1
            , ui_name = 'Virtual wireless interface/Is active'
            )
          , Record
            ( attr = Text `desc`
            , full_name = 'virtual_wireless_interface.desc'
            , id = 'virtual_wireless_interface__desc'
            , name = 'desc'
            , sig_key = 3
            , ui_name = 'Virtual wireless interface/Description'
            )
          , Record
            ( attr = wl-mode `mode`
            , choices =
                [
                  ( 'AP'
                  , 'AP'
                  )
                ,
                  ( 'Ad_Hoc'
                  , 'Ad_Hoc'
                  )
                ,
                  ( 'Client'
                  , 'Client'
                  )
                ]
            , full_name = 'virtual_wireless_interface.mode'
            , id = 'virtual_wireless_interface__mode'
            , name = 'mode'
            , sig_key = 0
            , ui_name = 'Virtual wireless interface/Mode'
            )
          , Record
            ( attr = String `essid`
            , full_name = 'virtual_wireless_interface.essid'
            , id = 'virtual_wireless_interface__essid'
            , name = 'essid'
            , sig_key = 3
            , ui_name = 'Virtual wireless interface/ESSID'
            )
          , Record
            ( attr = MAC-address `bssid`
            , full_name = 'virtual_wireless_interface.bssid'
            , id = 'virtual_wireless_interface__bssid'
            , name = 'bssid'
            , sig_key = 3
            , ui_name = 'Virtual wireless interface/BSSID'
            )
          , Record
            ( Class = 'Entity'
            , attr = Entity `my_node`
            , attrs =
                [ Record
                  ( attr = String `name`
                  , full_name = 'virtual_wireless_interface.my_node.name'
                  , id = 'virtual_wireless_interface__my_node__name'
                  , name = 'name'
                  , sig_key = 3
                  , ui_name = 'Virtual wireless interface/My node/Name'
                  )
                , Record
                  ( Class = 'Entity'
                  , attr = Entity `manager`
                  , attrs =
                      [ Record
                        ( attr = String `last_name`
                        , full_name = 'virtual_wireless_interface.my_node.manager.last_name'
                        , id = 'virtual_wireless_interface__my_node__manager__last_name'
                        , name = 'last_name'
                        , sig_key = 3
                        , ui_name = 'Virtual wireless interface/My node/Manager/Last name'
                        )
                      , Record
                        ( attr = String `first_name`
                        , full_name = 'virtual_wireless_interface.my_node.manager.first_name'
                        , id = 'virtual_wireless_interface__my_node__manager__first_name'
                        , name = 'first_name'
                        , sig_key = 3
                        , ui_name = 'Virtual wireless interface/My node/Manager/First name'
                        )
                      , Record
                        ( attr = String `middle_name`
                        , full_name = 'virtual_wireless_interface.my_node.manager.middle_name'
                        , id = 'virtual_wireless_interface__my_node__manager__middle_name'
                        , name = 'middle_name'
                        , sig_key = 3
                        , ui_name = 'Virtual wireless interface/My node/Manager/Middle name'
                        )
                      , Record
                        ( attr = String `title`
                        , full_name = 'virtual_wireless_interface.my_node.manager.title'
                        , id = 'virtual_wireless_interface__my_node__manager__title'
                        , name = 'title'
                        , sig_key = 3
                        , ui_name = 'Virtual wireless interface/My node/Manager/Academic title'
                        )
                      , Record
                        ( attr = Date_Interval `lifetime`
                        , attrs =
                            [ Record
                              ( attr = Date `start`
                              , full_name = 'virtual_wireless_interface.my_node.manager.lifetime.start'
                              , id = 'virtual_wireless_interface__my_node__manager__lifetime__start'
                              , name = 'start'
                              , sig_key = 0
                              , ui_name = 'Virtual wireless interface/My node/Manager/Lifetime/Start'
                              )
                            , Record
                              ( attr = Date `finish`
                              , full_name = 'virtual_wireless_interface.my_node.manager.lifetime.finish'
                              , id = 'virtual_wireless_interface__my_node__manager__lifetime__finish'
                              , name = 'finish'
                              , sig_key = 0
                              , ui_name = 'Virtual wireless interface/My node/Manager/Lifetime/Finish'
                              )
                            , Record
                              ( attr = Boolean `alive`
                              , choices = <Recursion on list...>
                              , full_name = 'virtual_wireless_interface.my_node.manager.lifetime.alive'
                              , id = 'virtual_wireless_interface__my_node__manager__lifetime__alive'
                              , name = 'alive'
                              , sig_key = 1
                              , ui_name = 'Virtual wireless interface/My node/Manager/Lifetime/Alive'
                              )
                            ]
                        , full_name = 'virtual_wireless_interface.my_node.manager.lifetime'
                        , id = 'virtual_wireless_interface__my_node__manager__lifetime'
                        , name = 'lifetime'
                        , ui_name = 'Virtual wireless interface/My node/Manager/Lifetime'
                        )
                      , Record
                        ( attr = Sex `sex`
                        , choices = <Recursion on list...>
                        , full_name = 'virtual_wireless_interface.my_node.manager.sex'
                        , id = 'virtual_wireless_interface__my_node__manager__sex'
                        , name = 'sex'
                        , sig_key = 0
                        , ui_name = 'Virtual wireless interface/My node/Manager/Sex'
                        )
                      ]
                  , full_name = 'virtual_wireless_interface.my_node.manager'
                  , id = 'virtual_wireless_interface__my_node__manager'
                  , name = 'manager'
                  , sig_key = 2
                  , type_name = 'PAP.Person'
                  , ui_name = 'Virtual wireless interface/My node/Manager'
                  , ui_type_name = 'Person'
                  )
                , Record
                  ( Class = 'Entity'
                  , attr = Entity `address`
                  , attrs =
                      [ Record
                        ( attr = String `street`
                        , full_name = 'virtual_wireless_interface.my_node.address.street'
                        , id = 'virtual_wireless_interface__my_node__address__street'
                        , name = 'street'
                        , sig_key = 3
                        , ui_name = 'Virtual wireless interface/My node/Address/Street'
                        )
                      , Record
                        ( attr = String `zip`
                        , full_name = 'virtual_wireless_interface.my_node.address.zip'
                        , id = 'virtual_wireless_interface__my_node__address__zip'
                        , name = 'zip'
                        , sig_key = 3
                        , ui_name = 'Virtual wireless interface/My node/Address/Zip code'
                        )
                      , Record
                        ( attr = String `city`
                        , full_name = 'virtual_wireless_interface.my_node.address.city'
                        , id = 'virtual_wireless_interface__my_node__address__city'
                        , name = 'city'
                        , sig_key = 3
                        , ui_name = 'Virtual wireless interface/My node/Address/City'
                        )
                      , Record
                        ( attr = String `country`
                        , full_name = 'virtual_wireless_interface.my_node.address.country'
                        , id = 'virtual_wireless_interface__my_node__address__country'
                        , name = 'country'
                        , sig_key = 3
                        , ui_name = 'Virtual wireless interface/My node/Address/Country'
                        )
                      , Record
                        ( attr = String `desc`
                        , full_name = 'virtual_wireless_interface.my_node.address.desc'
                        , id = 'virtual_wireless_interface__my_node__address__desc'
                        , name = 'desc'
                        , sig_key = 3
                        , ui_name = 'Virtual wireless interface/My node/Address/Description'
                        )
                      , Record
                        ( attr = String `region`
                        , full_name = 'virtual_wireless_interface.my_node.address.region'
                        , id = 'virtual_wireless_interface__my_node__address__region'
                        , name = 'region'
                        , sig_key = 3
                        , ui_name = 'Virtual wireless interface/My node/Address/Region'
                        )
                      ]
                  , full_name = 'virtual_wireless_interface.my_node.address'
                  , id = 'virtual_wireless_interface__my_node__address'
                  , name = 'address'
                  , sig_key = 2
                  , type_name = 'PAP.Address'
                  , ui_name = 'Virtual wireless interface/My node/Address'
                  , ui_type_name = 'Address'
                  )
                , Record
                  ( attr = Text `desc`
                  , full_name = 'virtual_wireless_interface.my_node.desc'
                  , id = 'virtual_wireless_interface__my_node__desc'
                  , name = 'desc'
                  , sig_key = 3
                  , ui_name = 'Virtual wireless interface/My node/Description'
                  )
                , Record
                  ( Class = 'Entity'
                  , attr = Entity `owner`
                  , children_np =
                      [ Record
                        ( Class = 'Entity'
                        , attr = Entity `owner`
                        , attrs =
                            [ Record
                              ( attr = String `name`
                              , full_name = 'owner.name'
                              , id = 'owner__name'
                              , name = 'name'
                              , sig_key = 3
                              , ui_name = 'Owner[Adhoc_Group]/Name'
                              )
                            ]
                        , full_name = 'owner'
                        , id = 'owner'
                        , name = 'owner'
                        , sig_key = 2
                        , type_name = 'PAP.Adhoc_Group'
                        , ui_name = 'Owner[Adhoc_Group]'
                        , ui_type_name = 'Adhoc_Group'
                        )
                      , Record
                        ( Class = 'Entity'
                        , attr = Entity `owner`
                        , attrs =
                            [ Record
                              ( attr = String `name`
                              , full_name = 'owner.name'
                              , id = 'owner__name'
                              , name = 'name'
                              , sig_key = 3
                              , ui_name = 'Owner[Association]/Name'
                              )
                            ]
                        , full_name = 'owner'
                        , id = 'owner'
                        , name = 'owner'
                        , sig_key = 2
                        , type_name = 'PAP.Association'
                        , ui_name = 'Owner[Association]'
                        , ui_type_name = 'Association'
                        )
                      , Record
                        ( Class = 'Entity'
                        , attr = Entity `owner`
                        , attrs =
                            [ Record
                              ( attr = String `name`
                              , full_name = 'owner.name'
                              , id = 'owner__name'
                              , name = 'name'
                              , sig_key = 3
                              , ui_name = 'Owner[Company]/Name'
                              )
                            , Record
                              ( attr = String `registered_in`
                              , full_name = 'owner.registered_in'
                              , id = 'owner__registered_in'
                              , name = 'registered_in'
                              , sig_key = 3
                              , ui_name = 'Owner[Company]/Registered in'
                              )
                            ]
                        , full_name = 'owner'
                        , id = 'owner'
                        , name = 'owner'
                        , sig_key = 2
                        , type_name = 'PAP.Company'
                        , ui_name = 'Owner[Company]'
                        , ui_type_name = 'Company'
                        )
                      , Record
                        ( Class = 'Entity'
                        , attr = Entity `owner`
                        , attrs =
                            [ Record
                              ( attr = String `last_name`
                              , full_name = 'owner.last_name'
                              , id = 'owner__last_name'
                              , name = 'last_name'
                              , sig_key = 3
                              , ui_name = 'Owner[Person]/Last name'
                              )
                            , Record
                              ( attr = String `first_name`
                              , full_name = 'owner.first_name'
                              , id = 'owner__first_name'
                              , name = 'first_name'
                              , sig_key = 3
                              , ui_name = 'Owner[Person]/First name'
                              )
                            , Record
                              ( attr = String `middle_name`
                              , full_name = 'owner.middle_name'
                              , id = 'owner__middle_name'
                              , name = 'middle_name'
                              , sig_key = 3
                              , ui_name = 'Owner[Person]/Middle name'
                              )
                            , Record
                              ( attr = String `title`
                              , full_name = 'owner.title'
                              , id = 'owner__title'
                              , name = 'title'
                              , sig_key = 3
                              , ui_name = 'Owner[Person]/Academic title'
                              )
                            ]
                        , full_name = 'owner'
                        , id = 'owner'
                        , name = 'owner'
                        , sig_key = 2
                        , type_name = 'PAP.Person'
                        , ui_name = 'Owner[Person]'
                        , ui_type_name = 'Person'
                        )
                      ]
                  , default_child = 'PAP.Person'
                  , full_name = 'virtual_wireless_interface.my_node.owner'
                  , id = 'virtual_wireless_interface__my_node__owner'
                  , name = 'owner'
                  , sig_key = 2
                  , type_name = 'PAP.Subject'
                  , ui_name = 'Virtual wireless interface/My node/Owner'
                  , ui_type_name = 'Subject'
                  )
                , Record
                  ( attr = Position `position`
                  , attrs =
                      [ Record
                        ( attr = Angle `lat`
                        , full_name = 'virtual_wireless_interface.my_node.position.lat'
                        , id = 'virtual_wireless_interface__my_node__position__lat'
                        , name = 'lat'
                        , sig_key = 4
                        , ui_name = 'Virtual wireless interface/My node/Position/Latitude'
                        )
                      , Record
                        ( attr = Angle `lon`
                        , full_name = 'virtual_wireless_interface.my_node.position.lon'
                        , id = 'virtual_wireless_interface__my_node__position__lon'
                        , name = 'lon'
                        , sig_key = 4
                        , ui_name = 'Virtual wireless interface/My node/Position/Longitude'
                        )
                      , Record
                        ( attr = Float `height`
                        , full_name = 'virtual_wireless_interface.my_node.position.height'
                        , id = 'virtual_wireless_interface__my_node__position__height'
                        , name = 'height'
                        , sig_key = 0
                        , ui_name = 'Virtual wireless interface/My node/Position/Height'
                        )
                      ]
                  , full_name = 'virtual_wireless_interface.my_node.position'
                  , id = 'virtual_wireless_interface__my_node__position'
                  , name = 'position'
                  , ui_name = 'Virtual wireless interface/My node/Position'
                  )
                , Record
                  ( attr = Boolean `show_in_map`
                  , choices = <Recursion on list...>
                  , full_name = 'virtual_wireless_interface.my_node.show_in_map'
                  , id = 'virtual_wireless_interface__my_node__show_in_map'
                  , name = 'show_in_map'
                  , sig_key = 1
                  , ui_name = 'Virtual wireless interface/My node/Show in map'
                  )
                ]
            , full_name = 'virtual_wireless_interface.my_node'
            , id = 'virtual_wireless_interface__my_node'
            , name = 'my_node'
            , sig_key = 2
            , type_name = 'FFM.Node'
            , ui_name = 'Virtual wireless interface/My node'
            , ui_type_name = 'Node'
            )
          , Record
            ( Class = 'Entity'
            , attr = Entity `my_net_device`
            , attrs =
                [ Record
                  ( Class = 'Entity'
                  , attr = Net_Device_Type `left`
                  , attrs =
                      [ Record
                        ( attr = String `name`
                        , full_name = 'virtual_wireless_interface.my_net_device.left.name'
                        , id = 'virtual_wireless_interface__my_net_device__left__name'
                        , name = 'name'
                        , sig_key = 3
                        , ui_name = 'Virtual wireless interface/My net device/Net device type/Name'
                        )
                      , Record
                        ( attr = String `model_no`
                        , full_name = 'virtual_wireless_interface.my_net_device.left.model_no'
                        , id = 'virtual_wireless_interface__my_net_device__left__model_no'
                        , name = 'model_no'
                        , sig_key = 3
                        , ui_name = 'Virtual wireless interface/My net device/Net device type/Model no'
                        )
                      , Record
                        ( attr = String `revision`
                        , full_name = 'virtual_wireless_interface.my_net_device.left.revision'
                        , id = 'virtual_wireless_interface__my_net_device__left__revision'
                        , name = 'revision'
                        , sig_key = 3
                        , ui_name = 'Virtual wireless interface/My net device/Net device type/Revision'
                        )
                      , Record
                        ( attr = Text `desc`
                        , full_name = 'virtual_wireless_interface.my_net_device.left.desc'
                        , id = 'virtual_wireless_interface__my_net_device__left__desc'
                        , name = 'desc'
                        , sig_key = 3
                        , ui_name = 'Virtual wireless interface/My net device/Net device type/Description'
                        )
                      ]
                  , full_name = 'virtual_wireless_interface.my_net_device.left'
                  , id = 'virtual_wireless_interface__my_net_device__left'
                  , name = 'left'
                  , sig_key = 2
                  , type_name = 'FFM.Net_Device_Type'
                  , ui_name = 'Virtual wireless interface/My net device/Net device type'
                  , ui_type_name = 'Net_Device_Type'
                  )
                , Record
                  ( Class = 'Entity'
                  , attr = Entity `node`
                  , attrs =
                      [ Record
                        ( attr = String `name`
                        , full_name = 'virtual_wireless_interface.my_net_device.node.name'
                        , id = 'virtual_wireless_interface__my_net_device__node__name'
                        , name = 'name'
                        , sig_key = 3
                        , ui_name = 'Virtual wireless interface/My net device/Node/Name'
                        )
                      , Record
                        ( Class = 'Entity'
                        , attr = Entity `manager`
                        , attrs =
                            [ Record
                              ( attr = String `last_name`
                              , full_name = 'virtual_wireless_interface.my_net_device.node.manager.last_name'
                              , id = 'virtual_wireless_interface__my_net_device__node__manager__last_name'
                              , name = 'last_name'
                              , sig_key = 3
                              , ui_name = 'Virtual wireless interface/My net device/Node/Manager/Last name'
                              )
                            , Record
                              ( attr = String `first_name`
                              , full_name = 'virtual_wireless_interface.my_net_device.node.manager.first_name'
                              , id = 'virtual_wireless_interface__my_net_device__node__manager__first_name'
                              , name = 'first_name'
                              , sig_key = 3
                              , ui_name = 'Virtual wireless interface/My net device/Node/Manager/First name'
                              )
                            , Record
                              ( attr = String `middle_name`
                              , full_name = 'virtual_wireless_interface.my_net_device.node.manager.middle_name'
                              , id = 'virtual_wireless_interface__my_net_device__node__manager__middle_name'
                              , name = 'middle_name'
                              , sig_key = 3
                              , ui_name = 'Virtual wireless interface/My net device/Node/Manager/Middle name'
                              )
                            , Record
                              ( attr = String `title`
                              , full_name = 'virtual_wireless_interface.my_net_device.node.manager.title'
                              , id = 'virtual_wireless_interface__my_net_device__node__manager__title'
                              , name = 'title'
                              , sig_key = 3
                              , ui_name = 'Virtual wireless interface/My net device/Node/Manager/Academic title'
                              )
                            , Record
                              ( attr = Date_Interval `lifetime`
                              , attrs =
                                  [ Record
                                    ( attr = Date `start`
                                    , full_name = 'virtual_wireless_interface.my_net_device.node.manager.lifetime.start'
                                    , id = 'virtual_wireless_interface__my_net_device__node__manager__lifetime__start'
                                    , name = 'start'
                                    , sig_key = 0
                                    , ui_name = 'Virtual wireless interface/My net device/Node/Manager/Lifetime/Start'
                                    )
                                  , Record
                                    ( attr = Date `finish`
                                    , full_name = 'virtual_wireless_interface.my_net_device.node.manager.lifetime.finish'
                                    , id = 'virtual_wireless_interface__my_net_device__node__manager__lifetime__finish'
                                    , name = 'finish'
                                    , sig_key = 0
                                    , ui_name = 'Virtual wireless interface/My net device/Node/Manager/Lifetime/Finish'
                                    )
                                  , Record
                                    ( attr = Boolean `alive`
                                    , choices = <Recursion on list...>
                                    , full_name = 'virtual_wireless_interface.my_net_device.node.manager.lifetime.alive'
                                    , id = 'virtual_wireless_interface__my_net_device__node__manager__lifetime__alive'
                                    , name = 'alive'
                                    , sig_key = 1
                                    , ui_name = 'Virtual wireless interface/My net device/Node/Manager/Lifetime/Alive'
                                    )
                                  ]
                              , full_name = 'virtual_wireless_interface.my_net_device.node.manager.lifetime'
                              , id = 'virtual_wireless_interface__my_net_device__node__manager__lifetime'
                              , name = 'lifetime'
                              , ui_name = 'Virtual wireless interface/My net device/Node/Manager/Lifetime'
                              )
                            , Record
                              ( attr = Sex `sex`
                              , choices = <Recursion on list...>
                              , full_name = 'virtual_wireless_interface.my_net_device.node.manager.sex'
                              , id = 'virtual_wireless_interface__my_net_device__node__manager__sex'
                              , name = 'sex'
                              , sig_key = 0
                              , ui_name = 'Virtual wireless interface/My net device/Node/Manager/Sex'
                              )
                            ]
                        , full_name = 'virtual_wireless_interface.my_net_device.node.manager'
                        , id = 'virtual_wireless_interface__my_net_device__node__manager'
                        , name = 'manager'
                        , sig_key = 2
                        , type_name = 'PAP.Person'
                        , ui_name = 'Virtual wireless interface/My net device/Node/Manager'
                        , ui_type_name = 'Person'
                        )
                      , Record
                        ( Class = 'Entity'
                        , attr = Entity `address`
                        , attrs =
                            [ Record
                              ( attr = String `street`
                              , full_name = 'virtual_wireless_interface.my_net_device.node.address.street'
                              , id = 'virtual_wireless_interface__my_net_device__node__address__street'
                              , name = 'street'
                              , sig_key = 3
                              , ui_name = 'Virtual wireless interface/My net device/Node/Address/Street'
                              )
                            , Record
                              ( attr = String `zip`
                              , full_name = 'virtual_wireless_interface.my_net_device.node.address.zip'
                              , id = 'virtual_wireless_interface__my_net_device__node__address__zip'
                              , name = 'zip'
                              , sig_key = 3
                              , ui_name = 'Virtual wireless interface/My net device/Node/Address/Zip code'
                              )
                            , Record
                              ( attr = String `city`
                              , full_name = 'virtual_wireless_interface.my_net_device.node.address.city'
                              , id = 'virtual_wireless_interface__my_net_device__node__address__city'
                              , name = 'city'
                              , sig_key = 3
                              , ui_name = 'Virtual wireless interface/My net device/Node/Address/City'
                              )
                            , Record
                              ( attr = String `country`
                              , full_name = 'virtual_wireless_interface.my_net_device.node.address.country'
                              , id = 'virtual_wireless_interface__my_net_device__node__address__country'
                              , name = 'country'
                              , sig_key = 3
                              , ui_name = 'Virtual wireless interface/My net device/Node/Address/Country'
                              )
                            , Record
                              ( attr = String `desc`
                              , full_name = 'virtual_wireless_interface.my_net_device.node.address.desc'
                              , id = 'virtual_wireless_interface__my_net_device__node__address__desc'
                              , name = 'desc'
                              , sig_key = 3
                              , ui_name = 'Virtual wireless interface/My net device/Node/Address/Description'
                              )
                            , Record
                              ( attr = String `region`
                              , full_name = 'virtual_wireless_interface.my_net_device.node.address.region'
                              , id = 'virtual_wireless_interface__my_net_device__node__address__region'
                              , name = 'region'
                              , sig_key = 3
                              , ui_name = 'Virtual wireless interface/My net device/Node/Address/Region'
                              )
                            ]
                        , full_name = 'virtual_wireless_interface.my_net_device.node.address'
                        , id = 'virtual_wireless_interface__my_net_device__node__address'
                        , name = 'address'
                        , sig_key = 2
                        , type_name = 'PAP.Address'
                        , ui_name = 'Virtual wireless interface/My net device/Node/Address'
                        , ui_type_name = 'Address'
                        )
                      , Record
                        ( attr = Text `desc`
                        , full_name = 'virtual_wireless_interface.my_net_device.node.desc'
                        , id = 'virtual_wireless_interface__my_net_device__node__desc'
                        , name = 'desc'
                        , sig_key = 3
                        , ui_name = 'Virtual wireless interface/My net device/Node/Description'
                        )
                      , Record
                        ( Class = 'Entity'
                        , attr = Entity `owner`
                        , children_np =
                            [ Record
                              ( Class = 'Entity'
                              , attr = Entity `owner`
                              , attrs =
                                  [ Record
                                    ( attr = String `name`
                                    , full_name = 'owner.name'
                                    , id = 'owner__name'
                                    , name = 'name'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Adhoc_Group]/Name'
                                    )
                                  ]
                              , full_name = 'owner'
                              , id = 'owner'
                              , name = 'owner'
                              , sig_key = 2
                              , type_name = 'PAP.Adhoc_Group'
                              , ui_name = 'Owner[Adhoc_Group]'
                              , ui_type_name = 'Adhoc_Group'
                              )
                            , Record
                              ( Class = 'Entity'
                              , attr = Entity `owner`
                              , attrs =
                                  [ Record
                                    ( attr = String `name`
                                    , full_name = 'owner.name'
                                    , id = 'owner__name'
                                    , name = 'name'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Association]/Name'
                                    )
                                  ]
                              , full_name = 'owner'
                              , id = 'owner'
                              , name = 'owner'
                              , sig_key = 2
                              , type_name = 'PAP.Association'
                              , ui_name = 'Owner[Association]'
                              , ui_type_name = 'Association'
                              )
                            , Record
                              ( Class = 'Entity'
                              , attr = Entity `owner`
                              , attrs =
                                  [ Record
                                    ( attr = String `name`
                                    , full_name = 'owner.name'
                                    , id = 'owner__name'
                                    , name = 'name'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Company]/Name'
                                    )
                                  , Record
                                    ( attr = String `registered_in`
                                    , full_name = 'owner.registered_in'
                                    , id = 'owner__registered_in'
                                    , name = 'registered_in'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Company]/Registered in'
                                    )
                                  ]
                              , full_name = 'owner'
                              , id = 'owner'
                              , name = 'owner'
                              , sig_key = 2
                              , type_name = 'PAP.Company'
                              , ui_name = 'Owner[Company]'
                              , ui_type_name = 'Company'
                              )
                            , Record
                              ( Class = 'Entity'
                              , attr = Entity `owner`
                              , attrs =
                                  [ Record
                                    ( attr = String `last_name`
                                    , full_name = 'owner.last_name'
                                    , id = 'owner__last_name'
                                    , name = 'last_name'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Person]/Last name'
                                    )
                                  , Record
                                    ( attr = String `first_name`
                                    , full_name = 'owner.first_name'
                                    , id = 'owner__first_name'
                                    , name = 'first_name'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Person]/First name'
                                    )
                                  , Record
                                    ( attr = String `middle_name`
                                    , full_name = 'owner.middle_name'
                                    , id = 'owner__middle_name'
                                    , name = 'middle_name'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Person]/Middle name'
                                    )
                                  , Record
                                    ( attr = String `title`
                                    , full_name = 'owner.title'
                                    , id = 'owner__title'
                                    , name = 'title'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Person]/Academic title'
                                    )
                                  ]
                              , full_name = 'owner'
                              , id = 'owner'
                              , name = 'owner'
                              , sig_key = 2
                              , type_name = 'PAP.Person'
                              , ui_name = 'Owner[Person]'
                              , ui_type_name = 'Person'
                              )
                            ]
                        , default_child = 'PAP.Person'
                        , full_name = 'virtual_wireless_interface.my_net_device.node.owner'
                        , id = 'virtual_wireless_interface__my_net_device__node__owner'
                        , name = 'owner'
                        , sig_key = 2
                        , type_name = 'PAP.Subject'
                        , ui_name = 'Virtual wireless interface/My net device/Node/Owner'
                        , ui_type_name = 'Subject'
                        )
                      , Record
                        ( attr = Position `position`
                        , attrs =
                            [ Record
                              ( attr = Angle `lat`
                              , full_name = 'virtual_wireless_interface.my_net_device.node.position.lat'
                              , id = 'virtual_wireless_interface__my_net_device__node__position__lat'
                              , name = 'lat'
                              , sig_key = 4
                              , ui_name = 'Virtual wireless interface/My net device/Node/Position/Latitude'
                              )
                            , Record
                              ( attr = Angle `lon`
                              , full_name = 'virtual_wireless_interface.my_net_device.node.position.lon'
                              , id = 'virtual_wireless_interface__my_net_device__node__position__lon'
                              , name = 'lon'
                              , sig_key = 4
                              , ui_name = 'Virtual wireless interface/My net device/Node/Position/Longitude'
                              )
                            , Record
                              ( attr = Float `height`
                              , full_name = 'virtual_wireless_interface.my_net_device.node.position.height'
                              , id = 'virtual_wireless_interface__my_net_device__node__position__height'
                              , name = 'height'
                              , sig_key = 0
                              , ui_name = 'Virtual wireless interface/My net device/Node/Position/Height'
                              )
                            ]
                        , full_name = 'virtual_wireless_interface.my_net_device.node.position'
                        , id = 'virtual_wireless_interface__my_net_device__node__position'
                        , name = 'position'
                        , ui_name = 'Virtual wireless interface/My net device/Node/Position'
                        )
                      , Record
                        ( attr = Boolean `show_in_map`
                        , choices = <Recursion on list...>
                        , full_name = 'virtual_wireless_interface.my_net_device.node.show_in_map'
                        , id = 'virtual_wireless_interface__my_net_device__node__show_in_map'
                        , name = 'show_in_map'
                        , sig_key = 1
                        , ui_name = 'Virtual wireless interface/My net device/Node/Show in map'
                        )
                      ]
                  , full_name = 'virtual_wireless_interface.my_net_device.node'
                  , id = 'virtual_wireless_interface__my_net_device__node'
                  , name = 'node'
                  , sig_key = 2
                  , type_name = 'FFM.Node'
                  , ui_name = 'Virtual wireless interface/My net device/Node'
                  , ui_type_name = 'Node'
                  )
                , Record
                  ( attr = String `name`
                  , full_name = 'virtual_wireless_interface.my_net_device.name'
                  , id = 'virtual_wireless_interface__my_net_device__name'
                  , name = 'name'
                  , sig_key = 3
                  , ui_name = 'Virtual wireless interface/My net device/Name'
                  )
                , Record
                  ( attr = Text `desc`
                  , full_name = 'virtual_wireless_interface.my_net_device.desc'
                  , id = 'virtual_wireless_interface__my_net_device__desc'
                  , name = 'desc'
                  , sig_key = 3
                  , ui_name = 'Virtual wireless interface/My net device/Description'
                  )
                , Record
                  ( Class = 'Entity'
                  , attr = Entity `my_node`
                  , attrs =
                      [ Record
                        ( attr = String `name`
                        , full_name = 'virtual_wireless_interface.my_net_device.my_node.name'
                        , id = 'virtual_wireless_interface__my_net_device__my_node__name'
                        , name = 'name'
                        , sig_key = 3
                        , ui_name = 'Virtual wireless interface/My net device/My node/Name'
                        )
                      , Record
                        ( Class = 'Entity'
                        , attr = Entity `manager`
                        , attrs =
                            [ Record
                              ( attr = String `last_name`
                              , full_name = 'virtual_wireless_interface.my_net_device.my_node.manager.last_name'
                              , id = 'virtual_wireless_interface__my_net_device__my_node__manager__last_name'
                              , name = 'last_name'
                              , sig_key = 3
                              , ui_name = 'Virtual wireless interface/My net device/My node/Manager/Last name'
                              )
                            , Record
                              ( attr = String `first_name`
                              , full_name = 'virtual_wireless_interface.my_net_device.my_node.manager.first_name'
                              , id = 'virtual_wireless_interface__my_net_device__my_node__manager__first_name'
                              , name = 'first_name'
                              , sig_key = 3
                              , ui_name = 'Virtual wireless interface/My net device/My node/Manager/First name'
                              )
                            , Record
                              ( attr = String `middle_name`
                              , full_name = 'virtual_wireless_interface.my_net_device.my_node.manager.middle_name'
                              , id = 'virtual_wireless_interface__my_net_device__my_node__manager__middle_name'
                              , name = 'middle_name'
                              , sig_key = 3
                              , ui_name = 'Virtual wireless interface/My net device/My node/Manager/Middle name'
                              )
                            , Record
                              ( attr = String `title`
                              , full_name = 'virtual_wireless_interface.my_net_device.my_node.manager.title'
                              , id = 'virtual_wireless_interface__my_net_device__my_node__manager__title'
                              , name = 'title'
                              , sig_key = 3
                              , ui_name = 'Virtual wireless interface/My net device/My node/Manager/Academic title'
                              )
                            , Record
                              ( attr = Date_Interval `lifetime`
                              , attrs =
                                  [ Record
                                    ( attr = Date `start`
                                    , full_name = 'virtual_wireless_interface.my_net_device.my_node.manager.lifetime.start'
                                    , id = 'virtual_wireless_interface__my_net_device__my_node__manager__lifetime__start'
                                    , name = 'start'
                                    , sig_key = 0
                                    , ui_name = 'Virtual wireless interface/My net device/My node/Manager/Lifetime/Start'
                                    )
                                  , Record
                                    ( attr = Date `finish`
                                    , full_name = 'virtual_wireless_interface.my_net_device.my_node.manager.lifetime.finish'
                                    , id = 'virtual_wireless_interface__my_net_device__my_node__manager__lifetime__finish'
                                    , name = 'finish'
                                    , sig_key = 0
                                    , ui_name = 'Virtual wireless interface/My net device/My node/Manager/Lifetime/Finish'
                                    )
                                  , Record
                                    ( attr = Boolean `alive`
                                    , choices = <Recursion on list...>
                                    , full_name = 'virtual_wireless_interface.my_net_device.my_node.manager.lifetime.alive'
                                    , id = 'virtual_wireless_interface__my_net_device__my_node__manager__lifetime__alive'
                                    , name = 'alive'
                                    , sig_key = 1
                                    , ui_name = 'Virtual wireless interface/My net device/My node/Manager/Lifetime/Alive'
                                    )
                                  ]
                              , full_name = 'virtual_wireless_interface.my_net_device.my_node.manager.lifetime'
                              , id = 'virtual_wireless_interface__my_net_device__my_node__manager__lifetime'
                              , name = 'lifetime'
                              , ui_name = 'Virtual wireless interface/My net device/My node/Manager/Lifetime'
                              )
                            , Record
                              ( attr = Sex `sex`
                              , choices = <Recursion on list...>
                              , full_name = 'virtual_wireless_interface.my_net_device.my_node.manager.sex'
                              , id = 'virtual_wireless_interface__my_net_device__my_node__manager__sex'
                              , name = 'sex'
                              , sig_key = 0
                              , ui_name = 'Virtual wireless interface/My net device/My node/Manager/Sex'
                              )
                            ]
                        , full_name = 'virtual_wireless_interface.my_net_device.my_node.manager'
                        , id = 'virtual_wireless_interface__my_net_device__my_node__manager'
                        , name = 'manager'
                        , sig_key = 2
                        , type_name = 'PAP.Person'
                        , ui_name = 'Virtual wireless interface/My net device/My node/Manager'
                        , ui_type_name = 'Person'
                        )
                      , Record
                        ( Class = 'Entity'
                        , attr = Entity `address`
                        , attrs =
                            [ Record
                              ( attr = String `street`
                              , full_name = 'virtual_wireless_interface.my_net_device.my_node.address.street'
                              , id = 'virtual_wireless_interface__my_net_device__my_node__address__street'
                              , name = 'street'
                              , sig_key = 3
                              , ui_name = 'Virtual wireless interface/My net device/My node/Address/Street'
                              )
                            , Record
                              ( attr = String `zip`
                              , full_name = 'virtual_wireless_interface.my_net_device.my_node.address.zip'
                              , id = 'virtual_wireless_interface__my_net_device__my_node__address__zip'
                              , name = 'zip'
                              , sig_key = 3
                              , ui_name = 'Virtual wireless interface/My net device/My node/Address/Zip code'
                              )
                            , Record
                              ( attr = String `city`
                              , full_name = 'virtual_wireless_interface.my_net_device.my_node.address.city'
                              , id = 'virtual_wireless_interface__my_net_device__my_node__address__city'
                              , name = 'city'
                              , sig_key = 3
                              , ui_name = 'Virtual wireless interface/My net device/My node/Address/City'
                              )
                            , Record
                              ( attr = String `country`
                              , full_name = 'virtual_wireless_interface.my_net_device.my_node.address.country'
                              , id = 'virtual_wireless_interface__my_net_device__my_node__address__country'
                              , name = 'country'
                              , sig_key = 3
                              , ui_name = 'Virtual wireless interface/My net device/My node/Address/Country'
                              )
                            , Record
                              ( attr = String `desc`
                              , full_name = 'virtual_wireless_interface.my_net_device.my_node.address.desc'
                              , id = 'virtual_wireless_interface__my_net_device__my_node__address__desc'
                              , name = 'desc'
                              , sig_key = 3
                              , ui_name = 'Virtual wireless interface/My net device/My node/Address/Description'
                              )
                            , Record
                              ( attr = String `region`
                              , full_name = 'virtual_wireless_interface.my_net_device.my_node.address.region'
                              , id = 'virtual_wireless_interface__my_net_device__my_node__address__region'
                              , name = 'region'
                              , sig_key = 3
                              , ui_name = 'Virtual wireless interface/My net device/My node/Address/Region'
                              )
                            ]
                        , full_name = 'virtual_wireless_interface.my_net_device.my_node.address'
                        , id = 'virtual_wireless_interface__my_net_device__my_node__address'
                        , name = 'address'
                        , sig_key = 2
                        , type_name = 'PAP.Address'
                        , ui_name = 'Virtual wireless interface/My net device/My node/Address'
                        , ui_type_name = 'Address'
                        )
                      , Record
                        ( attr = Text `desc`
                        , full_name = 'virtual_wireless_interface.my_net_device.my_node.desc'
                        , id = 'virtual_wireless_interface__my_net_device__my_node__desc'
                        , name = 'desc'
                        , sig_key = 3
                        , ui_name = 'Virtual wireless interface/My net device/My node/Description'
                        )
                      , Record
                        ( Class = 'Entity'
                        , attr = Entity `owner`
                        , children_np =
                            [ Record
                              ( Class = 'Entity'
                              , attr = Entity `owner`
                              , attrs =
                                  [ Record
                                    ( attr = String `name`
                                    , full_name = 'owner.name'
                                    , id = 'owner__name'
                                    , name = 'name'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Adhoc_Group]/Name'
                                    )
                                  ]
                              , full_name = 'owner'
                              , id = 'owner'
                              , name = 'owner'
                              , sig_key = 2
                              , type_name = 'PAP.Adhoc_Group'
                              , ui_name = 'Owner[Adhoc_Group]'
                              , ui_type_name = 'Adhoc_Group'
                              )
                            , Record
                              ( Class = 'Entity'
                              , attr = Entity `owner`
                              , attrs =
                                  [ Record
                                    ( attr = String `name`
                                    , full_name = 'owner.name'
                                    , id = 'owner__name'
                                    , name = 'name'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Association]/Name'
                                    )
                                  ]
                              , full_name = 'owner'
                              , id = 'owner'
                              , name = 'owner'
                              , sig_key = 2
                              , type_name = 'PAP.Association'
                              , ui_name = 'Owner[Association]'
                              , ui_type_name = 'Association'
                              )
                            , Record
                              ( Class = 'Entity'
                              , attr = Entity `owner`
                              , attrs =
                                  [ Record
                                    ( attr = String `name`
                                    , full_name = 'owner.name'
                                    , id = 'owner__name'
                                    , name = 'name'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Company]/Name'
                                    )
                                  , Record
                                    ( attr = String `registered_in`
                                    , full_name = 'owner.registered_in'
                                    , id = 'owner__registered_in'
                                    , name = 'registered_in'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Company]/Registered in'
                                    )
                                  ]
                              , full_name = 'owner'
                              , id = 'owner'
                              , name = 'owner'
                              , sig_key = 2
                              , type_name = 'PAP.Company'
                              , ui_name = 'Owner[Company]'
                              , ui_type_name = 'Company'
                              )
                            , Record
                              ( Class = 'Entity'
                              , attr = Entity `owner`
                              , attrs =
                                  [ Record
                                    ( attr = String `last_name`
                                    , full_name = 'owner.last_name'
                                    , id = 'owner__last_name'
                                    , name = 'last_name'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Person]/Last name'
                                    )
                                  , Record
                                    ( attr = String `first_name`
                                    , full_name = 'owner.first_name'
                                    , id = 'owner__first_name'
                                    , name = 'first_name'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Person]/First name'
                                    )
                                  , Record
                                    ( attr = String `middle_name`
                                    , full_name = 'owner.middle_name'
                                    , id = 'owner__middle_name'
                                    , name = 'middle_name'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Person]/Middle name'
                                    )
                                  , Record
                                    ( attr = String `title`
                                    , full_name = 'owner.title'
                                    , id = 'owner__title'
                                    , name = 'title'
                                    , sig_key = 3
                                    , ui_name = 'Owner[Person]/Academic title'
                                    )
                                  ]
                              , full_name = 'owner'
                              , id = 'owner'
                              , name = 'owner'
                              , sig_key = 2
                              , type_name = 'PAP.Person'
                              , ui_name = 'Owner[Person]'
                              , ui_type_name = 'Person'
                              )
                            ]
                        , default_child = 'PAP.Person'
                        , full_name = 'virtual_wireless_interface.my_net_device.my_node.owner'
                        , id = 'virtual_wireless_interface__my_net_device__my_node__owner'
                        , name = 'owner'
                        , sig_key = 2
                        , type_name = 'PAP.Subject'
                        , ui_name = 'Virtual wireless interface/My net device/My node/Owner'
                        , ui_type_name = 'Subject'
                        )
                      , Record
                        ( attr = Position `position`
                        , attrs =
                            [ Record
                              ( attr = Angle `lat`
                              , full_name = 'virtual_wireless_interface.my_net_device.my_node.position.lat'
                              , id = 'virtual_wireless_interface__my_net_device__my_node__position__lat'
                              , name = 'lat'
                              , sig_key = 4
                              , ui_name = 'Virtual wireless interface/My net device/My node/Position/Latitude'
                              )
                            , Record
                              ( attr = Angle `lon`
                              , full_name = 'virtual_wireless_interface.my_net_device.my_node.position.lon'
                              , id = 'virtual_wireless_interface__my_net_device__my_node__position__lon'
                              , name = 'lon'
                              , sig_key = 4
                              , ui_name = 'Virtual wireless interface/My net device/My node/Position/Longitude'
                              )
                            , Record
                              ( attr = Float `height`
                              , full_name = 'virtual_wireless_interface.my_net_device.my_node.position.height'
                              , id = 'virtual_wireless_interface__my_net_device__my_node__position__height'
                              , name = 'height'
                              , sig_key = 0
                              , ui_name = 'Virtual wireless interface/My net device/My node/Position/Height'
                              )
                            ]
                        , full_name = 'virtual_wireless_interface.my_net_device.my_node.position'
                        , id = 'virtual_wireless_interface__my_net_device__my_node__position'
                        , name = 'position'
                        , ui_name = 'Virtual wireless interface/My net device/My node/Position'
                        )
                      , Record
                        ( attr = Boolean `show_in_map`
                        , choices = <Recursion on list...>
                        , full_name = 'virtual_wireless_interface.my_net_device.my_node.show_in_map'
                        , id = 'virtual_wireless_interface__my_net_device__my_node__show_in_map'
                        , name = 'show_in_map'
                        , sig_key = 1
                        , ui_name = 'Virtual wireless interface/My net device/My node/Show in map'
                        )
                      ]
                  , full_name = 'virtual_wireless_interface.my_net_device.my_node'
                  , id = 'virtual_wireless_interface__my_net_device__my_node'
                  , name = 'my_node'
                  , sig_key = 2
                  , type_name = 'FFM.Node'
                  , ui_name = 'Virtual wireless interface/My net device/My node'
                  , ui_type_name = 'Node'
                  )
                ]
            , full_name = 'virtual_wireless_interface.my_net_device'
            , id = 'virtual_wireless_interface__my_net_device'
            , name = 'my_net_device'
            , sig_key = 2
            , type_name = 'FFM.Net_Device'
            , ui_name = 'Virtual wireless interface/My net device'
            , ui_type_name = 'Net_Device'
            )
          , Record
            ( Class = 'Entity'
            , attr = Entity `standard`
            , attrs =
                [ Record
                  ( attr = String `name`
                  , full_name = 'virtual_wireless_interface.standard.name'
                  , id = 'virtual_wireless_interface__standard__name'
                  , name = 'name'
                  , sig_key = 3
                  , ui_name = 'Virtual wireless interface/Standard/Name'
                  )
                , Record
                  ( attr = Frequency `bandwidth`
                  , full_name = 'virtual_wireless_interface.standard.bandwidth'
                  , id = 'virtual_wireless_interface__standard__bandwidth'
                  , name = 'bandwidth'
                  , sig_key = 4
                  , ui_name = 'Virtual wireless interface/Standard/Bandwidth'
                  )
                ]
            , full_name = 'virtual_wireless_interface.standard'
            , id = 'virtual_wireless_interface__standard'
            , name = 'standard'
            , sig_key = 2
            , type_name = 'FFM.Wireless_Standard'
            , ui_name = 'Virtual wireless interface/Standard'
            , ui_type_name = 'Wireless_Standard'
            )
          , Record
            ( attr = TX Power `txpower`
            , full_name = 'virtual_wireless_interface.txpower'
            , id = 'virtual_wireless_interface__txpower'
            , name = 'txpower'
            , sig_key = 4
            , ui_name = 'Virtual wireless interface/TX power'
            )
          ]
      , full_name = 'virtual_wireless_interface'
      , id = 'virtual_wireless_interface'
      , name = 'virtual_wireless_interface'
      , sig_key = 2
      , type_name = 'FFM.Virtual_Wireless_Interface'
      , ui_name = 'Virtual wireless interface'
      , ui_type_name = 'Virtual_Wireless_Interface'
      )
    ]

    >>> QR  = GTW.RST.TOP.MOM.Query_Restriction
    >>> print (formatted (QR.Filter_Atoms (QR.Filter (FFM.IP4_Network, "owner"))))
    ( Record
      ( AQ = <lifetime.start.AQ [Attr.Type.Querier Date]>
      , attr = Date `start`
      , edit = None
      , full_name = 'lifetime.start'
      , id = 'lifetime__start___AC'
      , name = 'lifetime__start___AC'
      , op = Record
          ( desc = 'Select entities where the attribute is equal to the specified value'
          , label = 'auto-complete'
          )
      , sig_key = 0
      , ui_name = 'Lifetime/Start'
      , value = None
      )
    , Record
      ( AQ = <lifetime.finish.AQ [Attr.Type.Querier Date]>
      , attr = Date `finish`
      , edit = None
      , full_name = 'lifetime.finish'
      , id = 'lifetime__finish___AC'
      , name = 'lifetime__finish___AC'
      , op = Record
          ( desc = 'Select entities where the attribute is equal to the specified value'
          , label = 'auto-complete'
          )
      , sig_key = 0
      , ui_name = 'Lifetime/Finish'
      , value = None
      )
    )

    >>> print (formatted (QR.Filter_Atoms (QR.Filter (FFM.IP4_Network, "parent"))))
    ( Record
      ( AQ = <net_address.AQ [Attr.Type.Querier Ckd]>
      , attr = IP4-network `net_address`
      , edit = None
      , full_name = 'net_address'
      , id = 'net_address___AC'
      , name = 'net_address___AC'
      , op = Record
          ( desc = 'Select entities where the attribute is equal to the specified value'
          , label = 'auto-complete'
          )
      , sig_key = 0
      , ui_name = 'Net address'
      , value = None
      )
    )

    >>> print (formatted (QR.Filter_Atoms (QR.Filter (FFM.Net_Interface_in_IP4_Network, "right"))))
    ( Record
      ( AQ = <net_address.AQ [Attr.Type.Querier Ckd]>
      , attr = IP4-network `net_address`
      , edit = None
      , full_name = 'net_address'
      , id = 'net_address___AC'
      , name = 'net_address___AC'
      , op = Record
          ( desc = 'Select entities where the attribute is equal to the specified value'
          , label = 'auto-complete'
          )
      , sig_key = 0
      , ui_name = 'Net address'
      , value = None
      )
    )

    >>> for aq in FFM.Node.E_Type.AQ.Attrs_Transitive :
    ...     print (aq._ui_name_T)
    Name
    Manager
    Manager/Last name
    Manager/First name
    Manager/Middle name
    Manager/Academic title
    Manager/Lifetime
    Manager/Lifetime/Start
    Manager/Lifetime/Finish
    Manager/Lifetime/Alive
    Manager/Sex
    Address
    Address/Street
    Address/Zip code
    Address/City
    Address/Country
    Address/Description
    Address/Region
    Description
    Owner
    Position
    Position/Latitude
    Position/Longitude
    Position/Height
    Show in map
    Creation
    Creation/C time
    Creation/C user
    Creation/Kind
    Creation/Time
    Creation/User
    Last change
    Last change/C time
    Last change/C user
    Last change/Kind
    Last change/Time
    Last change/User
    Last cid
    Pid
    Type name
    Documents
    Documents/Url
    Documents/Type
    Documents/Description

    >>> for aq in FFM.Net_Interface.E_Type.AQ.Attrs_Transitive :
    ...     print (aq._ui_name_T)
    Device
    Device/Net device type
    Device/Net device type/Name
    Device/Net device type/Model no
    Device/Net device type/Revision
    Device/Net device type/Description
    Device/Node
    Device/Node/Name
    Device/Node/Manager
    Device/Node/Manager/Last name
    Device/Node/Manager/First name
    Device/Node/Manager/Middle name
    Device/Node/Manager/Academic title
    Device/Node/Manager/Lifetime
    Device/Node/Manager/Lifetime/Start
    Device/Node/Manager/Lifetime/Finish
    Device/Node/Manager/Lifetime/Alive
    Device/Node/Manager/Sex
    Device/Node/Address
    Device/Node/Address/Street
    Device/Node/Address/Zip code
    Device/Node/Address/City
    Device/Node/Address/Country
    Device/Node/Address/Description
    Device/Node/Address/Region
    Device/Node/Description
    Device/Node/Owner
    Device/Node/Position
    Device/Node/Position/Latitude
    Device/Node/Position/Longitude
    Device/Node/Position/Height
    Device/Node/Show in map
    Device/Name
    Device/Description
    Device/My node
    Device/My node/Name
    Device/My node/Manager
    Device/My node/Manager/Last name
    Device/My node/Manager/First name
    Device/My node/Manager/Middle name
    Device/My node/Manager/Academic title
    Device/My node/Manager/Lifetime
    Device/My node/Manager/Lifetime/Start
    Device/My node/Manager/Lifetime/Finish
    Device/My node/Manager/Lifetime/Alive
    Device/My node/Manager/Sex
    Device/My node/Address
    Device/My node/Address/Street
    Device/My node/Address/Zip code
    Device/My node/Address/City
    Device/My node/Address/Country
    Device/My node/Address/Description
    Device/My node/Address/Region
    Device/My node/Description
    Device/My node/Owner
    Device/My node/Position
    Device/My node/Position/Latitude
    Device/My node/Position/Longitude
    Device/My node/Position/Height
    Device/My node/Show in map
    Mac address
    Name
    Is active
    Description
    Creation
    Creation/C time
    Creation/C user
    Creation/Kind
    Creation/Time
    Creation/User
    Last change
    Last change/C time
    Last change/C user
    Last change/Kind
    Last change/Time
    Last change/User
    Last cid
    Pid
    Type name
    My node
    My node/Name
    My node/Manager
    My node/Manager/Last name
    My node/Manager/First name
    My node/Manager/Middle name
    My node/Manager/Academic title
    My node/Manager/Lifetime
    My node/Manager/Lifetime/Start
    My node/Manager/Lifetime/Finish
    My node/Manager/Lifetime/Alive
    My node/Manager/Sex
    My node/Address
    My node/Address/Street
    My node/Address/Zip code
    My node/Address/City
    My node/Address/Country
    My node/Address/Description
    My node/Address/Region
    My node/Description
    My node/Owner
    My node/Position
    My node/Position/Latitude
    My node/Position/Longitude
    My node/Position/Height
    My node/Show in map
    My net device
    My net device/Net device type
    My net device/Net device type/Name
    My net device/Net device type/Model no
    My net device/Net device type/Revision
    My net device/Net device type/Description
    My net device/Node
    My net device/Node/Name
    My net device/Node/Manager
    My net device/Node/Manager/Last name
    My net device/Node/Manager/First name
    My net device/Node/Manager/Middle name
    My net device/Node/Manager/Academic title
    My net device/Node/Manager/Lifetime
    My net device/Node/Manager/Lifetime/Start
    My net device/Node/Manager/Lifetime/Finish
    My net device/Node/Manager/Lifetime/Alive
    My net device/Node/Manager/Sex
    My net device/Node/Address
    My net device/Node/Address/Street
    My net device/Node/Address/Zip code
    My net device/Node/Address/City
    My net device/Node/Address/Country
    My net device/Node/Address/Description
    My net device/Node/Address/Region
    My net device/Node/Description
    My net device/Node/Owner
    My net device/Node/Position
    My net device/Node/Position/Latitude
    My net device/Node/Position/Longitude
    My net device/Node/Position/Height
    My net device/Node/Show in map
    My net device/Name
    My net device/Description
    My net device/My node
    My net device/My node/Name
    My net device/My node/Manager
    My net device/My node/Manager/Last name
    My net device/My node/Manager/First name
    My net device/My node/Manager/Middle name
    My net device/My node/Manager/Academic title
    My net device/My node/Manager/Lifetime
    My net device/My node/Manager/Lifetime/Start
    My net device/My node/Manager/Lifetime/Finish
    My net device/My node/Manager/Lifetime/Alive
    My net device/My node/Manager/Sex
    My net device/My node/Address
    My net device/My node/Address/Street
    My net device/My node/Address/Zip code
    My net device/My node/Address/City
    My net device/My node/Address/Country
    My net device/My node/Address/Description
    My net device/My node/Address/Region
    My net device/My node/Description
    My net device/My node/Owner
    My net device/My node/Position
    My net device/My node/Position/Latitude
    My net device/My node/Position/Longitude
    My net device/My node/Position/Height
    My net device/My node/Show in map
    Credentials 1
    Credentials 1/My node
    Credentials 1/My node/Name
    Credentials 1/My node/Manager
    Credentials 1/My node/Manager/Last name
    Credentials 1/My node/Manager/First name
    Credentials 1/My node/Manager/Middle name
    Credentials 1/My node/Manager/Academic title
    Credentials 1/My node/Manager/Lifetime
    Credentials 1/My node/Manager/Lifetime/Start
    Credentials 1/My node/Manager/Lifetime/Finish
    Credentials 1/My node/Manager/Lifetime/Alive
    Credentials 1/My node/Manager/Sex
    Credentials 1/My node/Address
    Credentials 1/My node/Address/Street
    Credentials 1/My node/Address/Zip code
    Credentials 1/My node/Address/City
    Credentials 1/My node/Address/Country
    Credentials 1/My node/Address/Description
    Credentials 1/My node/Address/Region
    Credentials 1/My node/Description
    Credentials 1/My node/Owner
    Credentials 1/My node/Position
    Credentials 1/My node/Position/Latitude
    Credentials 1/My node/Position/Longitude
    Credentials 1/My node/Position/Height
    Credentials 1/My node/Show in map
    Credentials 1/My net device
    Credentials 1/My net device/Net device type
    Credentials 1/My net device/Net device type/Name
    Credentials 1/My net device/Net device type/Model no
    Credentials 1/My net device/Net device type/Revision
    Credentials 1/My net device/Net device type/Description
    Credentials 1/My net device/Node
    Credentials 1/My net device/Node/Name
    Credentials 1/My net device/Node/Manager
    Credentials 1/My net device/Node/Manager/Last name
    Credentials 1/My net device/Node/Manager/First name
    Credentials 1/My net device/Node/Manager/Middle name
    Credentials 1/My net device/Node/Manager/Academic title
    Credentials 1/My net device/Node/Manager/Lifetime
    Credentials 1/My net device/Node/Manager/Lifetime/Start
    Credentials 1/My net device/Node/Manager/Lifetime/Finish
    Credentials 1/My net device/Node/Manager/Lifetime/Alive
    Credentials 1/My net device/Node/Manager/Sex
    Credentials 1/My net device/Node/Address
    Credentials 1/My net device/Node/Address/Street
    Credentials 1/My net device/Node/Address/Zip code
    Credentials 1/My net device/Node/Address/City
    Credentials 1/My net device/Node/Address/Country
    Credentials 1/My net device/Node/Address/Description
    Credentials 1/My net device/Node/Address/Region
    Credentials 1/My net device/Node/Description
    Credentials 1/My net device/Node/Owner
    Credentials 1/My net device/Node/Position
    Credentials 1/My net device/Node/Position/Latitude
    Credentials 1/My net device/Node/Position/Longitude
    Credentials 1/My net device/Node/Position/Height
    Credentials 1/My net device/Node/Show in map
    Credentials 1/My net device/Name
    Credentials 1/My net device/Description
    Credentials 1/My net device/My node
    Ip4 networks
    Ip4 networks/Net address
    Ip4 networks/Description
    Ip4 networks/Owner
    Ip4 networks/Expiration date
    Ip4 networks/Has children
    Ip4 networks/Is free
    Ip4 networks/Parent
    Ip4 networks/Parent/Net address
    Ip4 networks/Parent/Description
    Ip4 networks/Parent/Owner
    Ip4 networks/Parent/Expiration date
    Ip4 networks/Parent/Has children
    Ip4 networks/Parent/Is free
    Ip4 networks/Parent/Parent
    Ip6 networks
    Ip6 networks/Net address
    Ip6 networks/Description
    Ip6 networks/Owner
    Ip6 networks/Expiration date
    Ip6 networks/Has children
    Ip6 networks/Is free
    Ip6 networks/Parent
    Ip6 networks/Parent/Net address
    Ip6 networks/Parent/Description
    Ip6 networks/Parent/Owner
    Ip6 networks/Parent/Expiration date
    Ip6 networks/Parent/Has children
    Ip6 networks/Parent/Is free
    Ip6 networks/Parent/Parent
    Documents
    Documents/Url
    Documents/Type
    Documents/Description

"""

_test_net_fixtures = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...

    >>> FFM = scope.FFM
    >>> PAP = scope.PAP
    >>> net_fixtures (scope)
    >>> scope.commit ()

    >>> show_by_pid (scope.FFM.Node)
    2   : Node                      nogps
    3   : Node                      node2
    38  : Node                      Node-net1
    39  : Node                      Node-net2
    40  : Node                      Node-net3
    41  : Node                      Node-net4

    >>> show_by_pid (scope.FFM.Net_Device)
    28  : Net_Device                Generic, node2, dev
    44  : Net_Device                Generic, Node-net1, n1d1
    45  : Net_Device                Generic, Node-net1, n1d2
    46  : Net_Device                Generic, Node-net2, n2d1
    47  : Net_Device                Generic, Node-net2, n2d2
    48  : Net_Device                Generic, Node-net2, n2d3
    49  : Net_Device                Generic, Node-net3, n3d1
    50  : Net_Device                Generic, Node-net4, n4d1
    51  : Net_Device                Generic, Node-net4, n4d2
    52  : Net_Device                Generic, Node-net4, n4d3
    53  : Net_Device                Generic, Node-net4, n4d4
    54  : Net_Device                Generic, Node-net4, n4d5

    >>> show_query_by_pid (scope.FFM.Belongs_to_Node.query (Q.my_node.name == "nogps"))
    2   : Node                      nogps

    >>> show_query_by_pid (scope.FFM.Belongs_to_Node.query (Q.my_node.name == "node2"))
    3   : Node                      node2
    28  : Net_Device                Generic, node2, dev
    29  : Wired_Interface           Generic, node2, dev, wr
    30  : Wireless_Interface        Generic, node2, dev, wl

    >>> show_query_by_pid (scope.FFM.Belongs_to_Node.query (Q.RAW.my_node.name == "Node-net1"))
    38  : Node                      Node-net1
    44  : Net_Device                Generic, Node-net1, n1d1
    45  : Net_Device                Generic, Node-net1, n1d2

    >>> show_query_by_pid (scope.FFM.Belongs_to_Node.query (Q.RAW.my_node.name == "Node-net2"))
    39  : Node                      Node-net2
    46  : Net_Device                Generic, Node-net2, n2d1
    47  : Net_Device                Generic, Node-net2, n2d2
    48  : Net_Device                Generic, Node-net2, n2d3

    >>> show_query_by_pid (scope.FFM.Belongs_to_Node.query (Q.RAW.my_node.name == "Node-net3"))
    40  : Node                      Node-net3
    49  : Net_Device                Generic, Node-net3, n3d1

    >>> show_query_by_pid (scope.FFM.Belongs_to_Node.query (Q.my_node.name == "node-net4"))
    41  : Node                      Node-net4
    50  : Net_Device                Generic, Node-net4, n4d1
    51  : Net_Device                Generic, Node-net4, n4d2
    52  : Net_Device                Generic, Node-net4, n4d3
    53  : Net_Device                Generic, Node-net4, n4d4
    54  : Net_Device                Generic, Node-net4, n4d5

"""

_test_order_4 = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...

    >>> FFM = scope.FFM
    >>> I4N = FFM.IP4_Network

    >>> PAP = scope.PAP
    >>> ff  = PAP.Association ("Funkfeuer", short_name = "0xFF", raw = True)

    >>> _   = I4N ("10.0.0.16/28")
    >>> _   = I4N ("10.0.0.16/29")
    >>> _   = I4N ("10.0.0.24/29")
    >>> _   = I4N ("10.0.0.24/30")
    >>> _   = I4N ("10.0.0.16/30")
    >>> _   = I4N ("10.0.0.30/32")
    >>> _   = I4N ("10.0.0.32/28")
    >>> _   = I4N ("10.0.0.33/32")
    >>> _   = I4N ("10.0.0.40/29")
    >>> _   = I4N ("10.0.0.40/30")
    >>> _   = I4N ("10.0.0.40/31")
    >>> _   = I4N ("10.0.0.40/32")
    >>> _   = I4N ("10.0.0.128/28")
    >>> _   = I4N ("10.0.0.212/28")
    >>> adr = I4N.net_address.P_Type ("10.0.0.0/32")
    >>> _   = I4N (adr, owner = ff, raw = True)

    >>> scope.commit ()

    >>> ETM = scope.FFM.IP4_Network
    >>> show_networks (scope, ETM)
    10.0.0.0           Funkfeuer                : electric = F, children = F
    10.0.0.16/28                                : electric = F, children = F
    10.0.0.16/29                                : electric = F, children = F
    10.0.0.16/30                                : electric = F, children = F
    10.0.0.24/29                                : electric = F, children = F
    10.0.0.24/30                                : electric = F, children = F
    10.0.0.30                                   : electric = F, children = F
    10.0.0.32/28                                : electric = F, children = F
    10.0.0.33                                   : electric = F, children = F
    10.0.0.40/29                                : electric = F, children = F
    10.0.0.40/30                                : electric = F, children = F
    10.0.0.40/31                                : electric = F, children = F
    10.0.0.40                                   : electric = F, children = F
    10.0.0.128/28                               : electric = F, children = F
    10.0.0.208/28                               : electric = F, children = F

    >>> adr1 = I4N.net_address.P_Type ("192.168.0.112/27")
    >>> adr1
    192.168.0.96/27
    >>> bool (adr1)
    True
    >>> I4N (adr1, owner = ff)
    FFM.IP4_Network ("192.168.0.96/27")

    >>> adr2 = I4N.net_address.P_Type ("192.168.1.96/27")
    >>> adr2
    192.168.1.96/27
    >>> bool (adr2)
    True
    >>> I4N (adr2, owner = ff, raw = True)
    FFM.IP4_Network ("192.168.1.96/27")

"""

_test_order_6 = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...

    >>> FFM = scope.FFM
    >>> I6N = FFM.IP6_Network

    >>> PAP = scope.PAP
    >>> ff  = PAP.Association ("Funkfeuer", short_name = "0xFF", raw = True)

    >>> _   = I6N ("2001:0db8::10/124")
    >>> _   = I6N ("2001:0db8::10/125")
    >>> _   = I6N ("2001:0db8::18/125")
    >>> _   = I6N ("2001:0db8::18/126")
    >>> _   = I6N ("2001:0db8::10/126")
    >>> _   = I6N ("2001:0db8::1E/128")
    >>> _   = I6N ("2001:0db8::20/124")
    >>> _   = I6N ("2001:0db8::21/128")
    >>> _   = I6N ("2001:0db8::28/125")
    >>> _   = I6N ("2001:0db8::28/126")
    >>> _   = I6N ("2001:0db8::28/127")
    >>> _   = I6N ("2001:0db8::28/128")
    >>> _   = I6N ("2001:0db8::80/124")
    >>> _   = I6N ("2001:0db8::D4/124")
    >>> adr = I6N.net_address.P_Type ("2001:0db8::0/128")
    >>> _   = I6N (adr, owner = ff, raw = True)

    >>> scope.commit ()

    >>> ETM = scope.FFM.IP6_Network
    >>> show_networks (scope, ETM)
    2001:db8::         Funkfeuer                : electric = F, children = F
    2001:db8::10/124                            : electric = F, children = F
    2001:db8::10/125                            : electric = F, children = F
    2001:db8::10/126                            : electric = F, children = F
    2001:db8::18/125                            : electric = F, children = F
    2001:db8::18/126                            : electric = F, children = F
    2001:db8::1e                                : electric = F, children = F
    2001:db8::20/124                            : electric = F, children = F
    2001:db8::21                                : electric = F, children = F
    2001:db8::28/125                            : electric = F, children = F
    2001:db8::28/126                            : electric = F, children = F
    2001:db8::28/127                            : electric = F, children = F
    2001:db8::28                                : electric = F, children = F
    2001:db8::80/124                            : electric = F, children = F
    2001:db8::d0/124                            : electric = F, children = F

    >>> adr1 = I6N.net_address.P_Type ("2a02:58::/29")
    >>> adr1
    2a02:58::/29
    >>> bool (adr1)
    True
    >>> I6N  (adr1, owner = ff, raw = True)
    FFM.IP6_Network ("2a02:58::/29")

    >>> adr2 = I6N.net_address.P_Type ("2a02:60::/29")
    >>> adr2
    2a02:60::/29
    >>> bool (adr2)
    True
    >>> I6N  (adr2, owner = ff)
    FFM.IP6_Network ("2a02:60::/29")

"""

_test_std_fixtures = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...

    >>> FFM = scope.FFM
    >>> PAP = scope.PAP
    >>> std_fixtures (scope)
    >>> scope.commit ()

    >>> show_by_pid (scope.FFM.Node)
    2   : Node                      nogps
    3   : Node                      node2

    >>> show_by_pid (scope.FFM.Net_Device)
    28  : Net_Device                Generic, node2, dev

    >>> show_by_pid (scope.FFM.Net_Interface)
    29  : Wired_Interface           Generic, node2, dev, wr
    30  : Wireless_Interface        Generic, node2, dev, wl

    >>> show_by_pid (scope.FFM.Net_Interface_in_IP4_Network)
    31  : Wired_Interface_in_IP4_Network Generic, node2, dev, wr, 192.168.23.1
    32  : Wireless_Interface_in_IP4_Network Generic, node2, dev, wl, 192.168.23.2
    33  : Wired_Interface_in_IP4_Network Generic, node2, dev, wr, 192.168.23.3
    34  : Wireless_Interface_in_IP4_Network Generic, node2, dev, wl, 192.168.23.4

    >>> show_by_pid (scope.FFM.IP4_Network)
    4   : IP4_Network               192.168.23.0/24
    5   : IP4_Network               192.168.23.0/25
    6   : IP4_Network               192.168.23.128/25
    7   : IP4_Network               192.168.23.0/26
    8   : IP4_Network               192.168.23.64/26
    9   : IP4_Network               192.168.23.0/27
    10  : IP4_Network               192.168.23.32/27
    11  : IP4_Network               192.168.23.0/28
    12  : IP4_Network               192.168.23.16/28
    13  : IP4_Network               192.168.23.0/29
    14  : IP4_Network               192.168.23.8/29
    15  : IP4_Network               192.168.23.0/30
    16  : IP4_Network               192.168.23.4/30
    17  : IP4_Network               192.168.23.0/31
    18  : IP4_Network               192.168.23.2/31
    19  : IP4_Network               192.168.23.0
    20  : IP4_Network               192.168.23.1
    21  : IP4_Network               192.168.23.2
    22  : IP4_Network               192.168.23.3
    23  : IP4_Network               192.168.23.4/31
    24  : IP4_Network               192.168.23.6/31
    25  : IP4_Network               192.168.23.4
    26  : IP4_Network               192.168.23.5

    >>> show_query_by_pid (scope.FFM.Belongs_to_Node.query (Q.my_node.name == "nogps"))
    2   : Node                      nogps

    >>> show_query_by_pid (scope.FFM.Belongs_to_Node.query (Q.my_node.name == "node2"))
    3   : Node                      node2
    28  : Net_Device                Generic, node2, dev
    29  : Wired_Interface           Generic, node2, dev, wr
    30  : Wireless_Interface        Generic, node2, dev, wl

"""

_test_debug = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...

    >>> FFM = scope.FFM
    >>> PAP = scope.PAP
    >>> I4N = FFM.IP4_Network
    >>> Adr = I4N.net_address.P_Type

    >>> _   = I4N ("10.0.0.16/28")
    >>> _   = I4N ("10.0.0.16/29")
    >>> _   = I4N ("10.0.0.24/29")
    >>> _   = I4N ("10.0.0.24/30")
    >>> _   = I4N ("10.0.0.16/30")
    >>> _   = I4N ("10.0.0.30/32")
    >>> _   = I4N ("10.0.0.32/28")
    >>> _   = I4N ("10.0.0.33/32")
    >>> _   = I4N ("10.0.0.40/29")
    >>> _   = I4N ("10.0.0.40/30")
    >>> _   = I4N ("10.0.0.40/31")
    >>> _   = I4N ("10.0.0.40/32")
    >>> _   = I4N ("10.0.0.128/28")
    >>> _   = I4N ("10.0.0.212/28")

    >>> mgr = PAP.Person (first_name = 'Ralf', last_name = 'Schlatterbeck', raw = True)
    >>> node1 = FFM.Node (name = "nogps", manager = mgr, raw = True)
    >>> net = FFM.IP4_Network ('192.168.23.0/24', raw = True)
    >>> a1  = net.reserve ('192.168.23.1/32')
    >>> a2  = net.reserve (Adr ('192.168.23.2/32'))
    >>> a3  = net.reserve ('192.168.23.3/32')
    >>> a4  = net.reserve (Adr ('192.168.23.4/32'))
    >>> devtype = FFM.Net_Device_Type.instance_or_new (name = 'Generic', raw = True)
    >>> dev = FFM.Net_Device (left = devtype, node = node1, name = 'dev', raw = True)
    >>> wr  = FFM.Wired_Interface (left = dev, name = 'wr', raw = True)
    >>> wl  = FFM.Wireless_Interface (left = dev, name = 'wl', raw = True)

    >>> ir1 = FFM.Net_Interface_in_IP4_Network (wr, a1, mask_len = 24)
    >>> il1 = FFM.Net_Interface_in_IP4_Network (wl, a2, mask_len = 32)
    >>> ir2 = FFM.Net_Interface_in_IP4_Network (wr, a3, mask_len = 24)
    >>> il2 = FFM.Net_Interface_in_IP4_Network (wl, a4, mask_len = 24)

    >>> il1.right.ETM.query ( (Q.net_address.CONTAINS (il1.right.net_address)) & (Q.electric == False)).attr ("net_address.mask_len").all ()


"""

def show_by_pid (ETM) :
    show_query_by_pid (ETM.query ())
# end def show_by_pid

def show_networks (scope, ETM, * qargs, ** qkw) :
    sk = TFL.Sorted_By ("electric", "-has_children", "net_address")
    pool = qkw.pop ("pool", None)
    if pool is not None :
        qargs += (Q.net_address.IN (pool.net_address), )
    for nw in ETM.query (* qargs, sort_key = sk, ** qkw).distinct () :
        print \
            ( "%-18s %-25s: electric = %1.1s, children = %1.1s"
            % (nw.FO.net_address, nw.FO.owner, nw.electric, nw.has_children)
            )
# end def show_networks

def show_network_count (scope, ETM) :
    print ("%s count: %s" % (ETM.type_name, ETM.count))
# end def show_network_count

def show_query_by_pid (q) :
    for x in q.order_by (Q.pid) :
        print ("%-3s : %-25s %s" % (x.pid, x.type_base_name, x.ui_display))
# end def show_query_by_pid

__test__ = Scaffold.create_test_dict \
  ( dict
      ( test_alloc         = _test_alloc
      , test_partial       = _test_partial
      , test_AQ            = _test_AQ
      , test_net_fixtures  = _test_net_fixtures
      , test_order_4       = _test_order_4
      , test_order_6       = _test_order_6
      , test_std_fixtures  = _test_std_fixtures
      )
  )

X__test__ = Scaffold.create_test_dict \
    ( dict
        ( test_debug     = _test_debug
        )
    )

### __END__ FFM.__test__.IP_Network
