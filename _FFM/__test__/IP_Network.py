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

    >>> ff  = PAP.Association ("Funkfeuer", short_name = "0xFF", raw = True)
    >>> mg  = PAP.Person ("Glueck", "Martin", raw = True)
    >>> ak  = PAP.Person ("Kaplan", "Aaron", raw = True)
    >>> rs  = PAP.Person ("Schlatterbeck", "Ralf", raw = True)
    >>> ct  = PAP.Person ("Tanzer", "Christian", raw = True)
    >>> osc = PAP.Company ("Open Source Consulting", raw = True)

    >>> show_networks (FFM.IP4_Network)

    >>> ff_pool  = FFM.IP4_Network (('10.0.0.0/8', ), owner = ff, raw = True)
    >>> show_networks (FFM.IP4_Network)
    10.0.0.0/8         Funkfeuer                 False

    >>> print ("FFM.IP4_Network count:", FFM.IP4_Network.count)
    FFM.IP4_Network count: 1

    >>> osc_pool = ff_pool.allocate (16, osc)
    >>> show_networks (FFM.IP4_Network)
    10.0.0.0/8         Funkfeuer                 True
    10.0.0.0/9         Funkfeuer                 True
    10.0.0.0/10        Funkfeuer                 True
    10.0.0.0/11        Funkfeuer                 True
    10.0.0.0/12        Funkfeuer                 True
    10.0.0.0/13        Funkfeuer                 True
    10.0.0.0/14        Funkfeuer                 True
    10.0.0.0/15        Funkfeuer                 True
    10.128.0.0/9       Funkfeuer                 False
    10.64.0.0/10       Funkfeuer                 False
    10.32.0.0/11       Funkfeuer                 False
    10.16.0.0/12       Funkfeuer                 False
    10.8.0.0/13        Funkfeuer                 False
    10.4.0.0/14        Funkfeuer                 False
    10.2.0.0/15        Funkfeuer                 False
    10.0.0.0/16        Open Source Consulting    False
    10.1.0.0/16        Funkfeuer                 False

    >>> print ("FFM.IP4_Network count:", FFM.IP4_Network.count)
    FFM.IP4_Network count: 17

    >>> rs_pool = osc_pool.allocate (28, rs)
    >>> show_networks (FFM.IP4_Network, Q.net_address.IN (osc_pool.net_address))
    10.0.0.0/16        Open Source Consulting    True
    10.0.0.0/17        Open Source Consulting    True
    10.0.0.0/18        Open Source Consulting    True
    10.0.0.0/19        Open Source Consulting    True
    10.0.0.0/20        Open Source Consulting    True
    10.0.0.0/21        Open Source Consulting    True
    10.0.0.0/22        Open Source Consulting    True
    10.0.0.0/23        Open Source Consulting    True
    10.0.0.0/24        Open Source Consulting    True
    10.0.0.0/25        Open Source Consulting    True
    10.0.0.0/26        Open Source Consulting    True
    10.0.0.0/27        Open Source Consulting    True
    10.0.128.0/17      Open Source Consulting    False
    10.0.64.0/18       Open Source Consulting    False
    10.0.32.0/19       Open Source Consulting    False
    10.0.16.0/20       Open Source Consulting    False
    10.0.8.0/21        Open Source Consulting    False
    10.0.4.0/22        Open Source Consulting    False
    10.0.2.0/23        Open Source Consulting    False
    10.0.1.0/24        Open Source Consulting    False
    10.0.0.128/25      Open Source Consulting    False
    10.0.0.64/26       Open Source Consulting    False
    10.0.0.32/27       Open Source Consulting    False
    10.0.0.0/28        Schlatterbeck Ralf        False
    10.0.0.16/28       Open Source Consulting    False

    >>> show_networks (FFM.IP4_Network, Q.net_address.IN (rs_pool.net_address))
    10.0.0.0/28        Schlatterbeck Ralf        False

    >>> print ("FFM.IP4_Network count:", FFM.IP4_Network.count)
    FFM.IP4_Network count: 41

    >>> ct_pool = rs_pool.allocate (30, ct)
    >>> show_networks (FFM.IP4_Network, Q.net_address.IN (rs_pool.net_address))
    10.0.0.0/28        Schlatterbeck Ralf        True
    10.0.0.0/29        Schlatterbeck Ralf        True
    10.0.0.8/29        Schlatterbeck Ralf        False
    10.0.0.0/30        Tanzer Christian          False
    10.0.0.4/30        Schlatterbeck Ralf        False

    >>> ak_pool = rs_pool.allocate (28, ak)
    Traceback (most recent call last):
      ...
    No_Free_Address_Range: Address range [("10.0.0.0/28", )] of this IP4_Network doesn't contain a free subrange for mask length 28

    >>> ak_pool = rs_pool.allocate (30, ak)
    >>> show_networks (FFM.IP4_Network, Q.net_address.IN (rs_pool.net_address))
    10.0.0.0/28        Schlatterbeck Ralf        True
    10.0.0.0/29        Schlatterbeck Ralf        True
    10.0.0.8/29        Schlatterbeck Ralf        False
    10.0.0.0/30        Tanzer Christian          False
    10.0.0.4/30        Kaplan Aaron              False

    >>> print ("FFM.IP4_Network count:", FFM.IP4_Network.count)
    FFM.IP4_Network count: 45

    >>> mg_pool = rs_pool.allocate (29, mg)
    >>> show_networks (FFM.IP4_Network, Q.net_address.IN (rs_pool.net_address))
    10.0.0.0/28        Schlatterbeck Ralf        True
    10.0.0.0/29        Schlatterbeck Ralf        True
    10.0.0.8/29        Glueck Martin             False
    10.0.0.0/30        Tanzer Christian          False
    10.0.0.4/30        Kaplan Aaron              False

    >>> xx_pool = rs_pool.allocate (30, mg)
    Traceback (most recent call last):
      ...
    No_Free_Address_Range: Address range [("10.0.0.0/28", )] of this IP4_Network doesn't contain a free subrange for mask length 30

    >>> print ("FFM.IP4_Network count:", FFM.IP4_Network.count)
    FFM.IP4_Network count: 45

"""

def show_networks (ETM, * qargs, ** qkw) :
    sk = TFL.Sorted_By \
        ("-has_children", "net_address.address.mask", "net_address.address.ip")
    for nw in ETM.query (* qargs, sort_key = sk, ** qkw) :
        print \
            ( "%-18s %-25s %s"
            % (nw.FO.net_address, nw.FO.owner, nw.has_children)
            )
# end def show_networks

__test__ = Scaffold.create_test_dict \
  ( dict
      ( main       = _test_code
      )
  )

### __END__ FFM.__test__.IP_Network
