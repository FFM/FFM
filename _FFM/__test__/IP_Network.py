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
#     7-Mar-2013 (RS) Test for previously failing `CONTAINS` query
#    19-Mar-2013 (CT) Add test case `test_AQ`
#    22-Mar-2013 (CT) Add test for `Query_Restriction`
#    28-Mar-2013 (CT) Add `AQ.Attrs_Transitive...ui_name`, `.pool.pool.pool...`
#    11-Apr-2013 (CT) Adapt to changes in `MOM.Attr.Querier`
#    28-Apr-2013 (CT) Adapt to addition of `IP_Network.desc`
#     7-Aug-2013 (CT) Adapt to major surgery of GTW.OMP.NET.Attr_Type
#    13-Aug-2013 (CT) Add `test_order`, adapt other tests to change in order
#    22-Aug-2013 (CT) Add tests for I4N and I6N calls with wrong `raw` value
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
    <pool.AQ [Attr.Type.Querier Id_Entity]>
    <last_cid.AQ [Attr.Type.Querier Ckd]>
    <pid.AQ [Attr.Type.Querier Ckd]>
    <type_name.AQ [Attr.Type.Querier String]>
    <is_free.AQ [Attr.Type.Querier Boolean]>
    <cool_down.AQ [Attr.Type.Querier Ckd]>
    <has_children.AQ [Attr.Type.Querier Boolean]>

    >>> for aq in AQ.Attrs_Transitive :
    ...     print (aq, aq.E_Type.type_name if aq.E_Type else "-"*5)
    <net_address.AQ [Attr.Type.Querier Ckd]> -----
    <desc.AQ [Attr.Type.Querier String]> -----
    <owner.AQ [Attr.Type.Querier Id_Entity]> PAP.Subject
    <pool.AQ [Attr.Type.Querier Id_Entity]> FFM.IP4_Network
    <pool.net_address.AQ [Attr.Type.Querier Ckd]> -----
    <pool.desc.AQ [Attr.Type.Querier String]> -----
    <pool.owner.AQ [Attr.Type.Querier Id_Entity]> PAP.Subject
    <pool.pool.AQ [Attr.Type.Querier Id_Entity]> FFM.IP4_Network
    <pool.last_cid.AQ [Attr.Type.Querier Ckd]> -----
    <pool.pid.AQ [Attr.Type.Querier Ckd]> -----
    <pool.type_name.AQ [Attr.Type.Querier String]> -----
    <pool.is_free.AQ [Attr.Type.Querier Boolean]> -----
    <pool.cool_down.AQ [Attr.Type.Querier Ckd]> -----
    <pool.has_children.AQ [Attr.Type.Querier Boolean]> -----
    <last_cid.AQ [Attr.Type.Querier Ckd]> -----
    <pid.AQ [Attr.Type.Querier Ckd]> -----
    <type_name.AQ [Attr.Type.Querier String]> -----
    <is_free.AQ [Attr.Type.Querier Boolean]> -----
    <cool_down.AQ [Attr.Type.Querier Ckd]> -----
    <has_children.AQ [Attr.Type.Querier Boolean]> -----

    >>> for aq in AQ.Attrs_Transitive :
    ...     str (aq._ui_name_T)
    'Net address'
    'Desc'
    'Owner'
    'Pool'
    'Pool/Net address'
    'Pool/Desc'
    'Pool/Owner'
    'Pool/Pool'
    'Pool/Last cid'
    'Pool/Pid'
    'Pool/Type name'
    'Pool/Is free'
    'Pool/Cool down'
    'Pool/Has children'
    'Last cid'
    'Pid'
    'Type name'
    'Is free'
    'Cool down'
    'Has children'

    >>> AQ.pool.pool.pool.owner
    <pool.pool.pool.owner.AQ [Attr.Type.Querier Id_Entity]>

    >>> for aq in AQ.Atoms :
    ...     print (aq)
    <net_address.AQ [Attr.Type.Querier Ckd]>
    <desc.AQ [Attr.Type.Querier String]>
    <pool.net_address.AQ [Attr.Type.Querier Ckd]>
    <pool.desc.AQ [Attr.Type.Querier String]>
    <pool.last_cid.AQ [Attr.Type.Querier Ckd]>
    <pool.pid.AQ [Attr.Type.Querier Ckd]>
    <pool.type_name.AQ [Attr.Type.Querier String]>
    <pool.is_free.AQ [Attr.Type.Querier Boolean]>
    <pool.cool_down.AQ [Attr.Type.Querier Ckd]>
    <pool.has_children.AQ [Attr.Type.Querier Boolean]>
    <last_cid.AQ [Attr.Type.Querier Ckd]>
    <pid.AQ [Attr.Type.Querier Ckd]>
    <type_name.AQ [Attr.Type.Querier String]>
    <is_free.AQ [Attr.Type.Querier Boolean]>
    <cool_down.AQ [Attr.Type.Querier Ckd]>
    <has_children.AQ [Attr.Type.Querier Boolean]>

    >>> print (formatted (AQ.As_Json_Cargo))
    { 'filters' :
        [ { 'name' : 'net_address'
          , 'sig_key' : 0
          , 'ui_name' : 'Net address'
          }
        , { 'name' : 'desc'
          , 'sig_key' : 3
          , 'ui_name' : 'Desc'
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
                , 'type_name' : 'FFM.Node'
                , 'ui_name' : 'Owner'
                , 'ui_type_name' : 'Node'
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
              [ { 'name' : 'net_address'
                , 'sig_key' : 0
                , 'ui_name' : 'Net address'
                }
              , { 'name' : 'desc'
                , 'sig_key' : 3
                , 'ui_name' : 'Desc'
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
                      , 'type_name' : 'FFM.Node'
                      , 'ui_name' : 'Owner'
                      , 'ui_type_name' : 'Node'
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
                , 'name' : 'pool'
                , 'sig_key' : 2
                , 'ui_name' : 'Pool'
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
              , { 'name' : 'is_free'
                , 'sig_key' : 1
                , 'ui_name' : 'Is free'
                }
              , { 'name' : 'cool_down'
                , 'sig_key' : 0
                , 'ui_name' : 'Cool down'
                }
              , { 'name' : 'has_children'
                , 'sig_key' : 1
                , 'ui_name' : 'Has children'
                }
              ]
          , 'name' : 'pool'
          , 'sig_key' : 2
          , 'ui_name' : 'Pool'
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
        , { 'name' : 'is_free'
          , 'sig_key' : 1
          , 'ui_name' : 'Is free'
          }
        , { 'name' : 'cool_down'
          , 'sig_key' : 0
          , 'ui_name' : 'Cool down'
          }
        , { 'name' : 'has_children'
          , 'sig_key' : 1
          , 'ui_name' : 'Has children'
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
      , ui_name = 'Desc'
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
                  , ui_name = 'Owner[Node]/Name'
                  )
                ]
            , full_name = 'owner'
            , id = 'owner'
            , name = 'owner'
            , sig_key = 2
            , type_name = 'FFM.Node'
            , ui_name = 'Owner[Node]'
            , ui_type_name = 'Node'
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
      , attr = Entity `pool`
      , attrs =
          [ Record
            ( attr = IP4-network `net_address`
            , full_name = 'pool.net_address'
            , id = 'pool__net_address'
            , name = 'net_address'
            , sig_key = 0
            , ui_name = 'Pool/Net address'
            )
          , Record
            ( attr = String `desc`
            , full_name = 'pool.desc'
            , id = 'pool__desc'
            , name = 'desc'
            , sig_key = 3
            , ui_name = 'Pool/Desc'
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
                        , ui_name = 'Owner[Node]/Name'
                        )
                      ]
                  , full_name = 'owner'
                  , id = 'owner'
                  , name = 'owner'
                  , sig_key = 2
                  , type_name = 'FFM.Node'
                  , ui_name = 'Owner[Node]'
                  , ui_type_name = 'Node'
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
            , full_name = 'pool.owner'
            , id = 'pool__owner'
            , name = 'owner'
            , sig_key = 2
            , type_name = 'PAP.Subject'
            , ui_name = 'Pool/Owner'
            , ui_type_name = 'Subject'
            )
          , Record
            ( Class = 'Entity'
            , attr = Entity `pool`
            , full_name = 'pool.pool'
            , id = 'pool__pool'
            , name = 'pool'
            , sig_key = 2
            , type_name = 'FFM.IP4_Network'
            , ui_name = 'Pool/Pool'
            , ui_type_name = 'IP4_Network'
            )
          , Record
            ( attr = Int `last_cid`
            , full_name = 'pool.last_cid'
            , id = 'pool__last_cid'
            , name = 'last_cid'
            , sig_key = 0
            , ui_name = 'Pool/Last cid'
            )
          , Record
            ( attr = Surrogate `pid`
            , full_name = 'pool.pid'
            , id = 'pool__pid'
            , name = 'pid'
            , sig_key = 0
            , ui_name = 'Pool/Pid'
            )
          , Record
            ( attr = String `type_name`
            , full_name = 'pool.type_name'
            , id = 'pool__type_name'
            , name = 'type_name'
            , sig_key = 3
            , ui_name = 'Pool/Type name'
            )
          , Record
            ( attr = Boolean `is_free`
            , choices =
                [ 'no'
                , 'yes'
                ]
            , full_name = 'pool.is_free'
            , id = 'pool__is_free'
            , name = 'is_free'
            , sig_key = 1
            , ui_name = 'Pool/Is free'
            )
          , Record
            ( attr = Date-Time `cool_down`
            , full_name = 'pool.cool_down'
            , id = 'pool__cool_down'
            , name = 'cool_down'
            , sig_key = 0
            , ui_name = 'Pool/Cool down'
            )
          , Record
            ( attr = Boolean `has_children`
            , choices =
                [ 'no'
                , 'yes'
                ]
            , full_name = 'pool.has_children'
            , id = 'pool__has_children'
            , name = 'has_children'
            , sig_key = 1
            , ui_name = 'Pool/Has children'
            )
          ]
      , full_name = 'pool'
      , id = 'pool'
      , name = 'pool'
      , sig_key = 2
      , type_name = 'FFM.IP4_Network'
      , ui_name = 'Pool'
      , ui_type_name = 'IP4_Network'
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
      ( attr = Boolean `is_free`
      , choices = <Recursion on list...>
      , full_name = 'is_free'
      , id = 'is_free'
      , name = 'is_free'
      , sig_key = 1
      , ui_name = 'Is free'
      )
    , Record
      ( attr = Date-Time `cool_down`
      , full_name = 'cool_down'
      , id = 'cool_down'
      , name = 'cool_down'
      , sig_key = 0
      , ui_name = 'Cool down'
      )
    , Record
      ( attr = Boolean `has_children`
      , choices = <Recursion on list...>
      , full_name = 'has_children'
      , id = 'has_children'
      , name = 'has_children'
      , sig_key = 1
      , ui_name = 'Has children'
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
    , Record
      ( AQ = <last_cid.AQ [Attr.Type.Querier Ckd]>
      , attr = Int `last_cid`
      , edit = None
      , full_name = 'last_cid'
      , id = 'last_cid___AC'
      , name = 'last_cid___AC'
      , op = Record
          ( desc = 'Select entities where the attribute is equal to the specified value'
          , label = 'auto-complete'
          )
      , sig_key = 0
      , ui_name = 'Last cid'
      , value = None
      )
    , Record
      ( AQ = <pid.AQ [Attr.Type.Querier Ckd]>
      , attr = Surrogate `pid`
      , edit = None
      , full_name = 'pid'
      , id = 'pid___AC'
      , name = 'pid___AC'
      , op = Record
          ( desc = 'Select entities where the attribute is equal to the specified value'
          , label = 'auto-complete'
          )
      , sig_key = 0
      , ui_name = 'Pid'
      , value = None
      )
    , Record
      ( AQ = <type_name.AQ [Attr.Type.Querier String]>
      , attr = String `type_name`
      , edit = None
      , full_name = 'type_name'
      , id = 'type_name___AC'
      , name = 'type_name___AC'
      , op = Record
          ( desc = 'Select entities where the attribute value starts with the specified value'
          , label = 'auto-complete'
          )
      , sig_key = 3
      , ui_name = 'Type name'
      , value = None
      )
    )

    >>> print (formatted (QR.Filter_Atoms (QR.Filter (FFM.IP4_Network, "pool"))))
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
    Manager/Salutation
    Manager/Sex
    Manager/Last cid
    Manager/Pid
    Manager/Type name
    Lifetime
    Lifetime/Start
    Lifetime/Finish
    Lifetime/Alive
    Address
    Address/Street
    Address/Zip code
    Address/City
    Address/Country
    Address/Description
    Address/Region
    Address/Last cid
    Address/Pid
    Address/Type name
    Owner
    Position
    Position/Latitude
    Position/Longitude
    Position/Height
    Show in map
    Last cid
    Pid
    Type name

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
    for x in ETM.query ().order_by (Q.pid) :
        print ("%-3s : %-25s %s" % (x.pid, x.type_base_name, x.ui_display))
# end def show_by_pid

def show_networks (scope, ETM, * qargs, ** qkw) :
    sk = TFL.Sorted_By ("electric", "-has_children", "net_address")
    pool = qkw.pop ("pool", None)
    if pool is not None :
        qargs += (Q.net_address.IN (pool.net_address), )
    for nw in ETM.query (* qargs, sort_key = sk, ** qkw) :
        print \
            ( "%-18s %-25s: electric = %1.1s, children = %1.1s"
            % (nw.FO.net_address, nw.FO.owner, nw.electric, nw.has_children)
            )
# end def show_networks

def show_network_count (scope, ETM) :
    print ("%s count: %s" % (ETM.type_name, ETM.count))
# end def show_network_count

__test__ = Scaffold.create_test_dict \
  ( dict
      ( test_alloc         = _test_alloc
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
