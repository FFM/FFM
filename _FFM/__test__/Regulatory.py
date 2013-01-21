# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012-2013 Mag. Christian Tanzer All rights reserved
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
#    FFM.__test__.Regulatory
#
# Purpose
#    Test Regulatory data structures from fixtures
#    Also test dB conversion and queries
#
# Revision Dates
#    17-Dec-2012 (RS) Creation
#    ««revision-date»»···
#--

from   __future__ import absolute_import, division, print_function, unicode_literals

from   _FFM.__test__.model      import *
from   _FFM.fixtures            import create as fixtures

_test_code = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...
    >>> fixtures (scope)

    >>> FFM = scope.FFM
    >>> FFM.Regulatory_Permission.E_Type.eirp.attr._default_unit
    u'dBm'
    >>> FFM.Regulatory_Permission.query (Q.RAW.band.lower > '28 MHz').count ()
    3
    >>> FFM.Regulatory_Permission.query (Q.RAW.band.lower < '28 MHz').count ()
    1
    >>> FFM.Regulatory_Permission.query (Q.eirp <= 25).count ()
    3
    >>> FFM.Regulatory_Permission.query (Q.eirp >= 26.5).count ()
    1
    >>> FFM.Regulatory_Permission.query (Q.eirp > 27.5).count ()
    0

    #>>> FFM.Regulatory_Permission.query (Q.eirp <= '110 mW').count ()
    #3
    #>>> FFM.Regulatory_Permission.query (Q.eirp <= '21 dBm').count ()
    #3
    #>>> FFM.Regulatory_Permission.query (Q.eirp <= '21 dBmW').count ()
    #3
    #>>> FFM.Regulatory_Permission.query (Q.eirp <= '21 xyzzy').count ()
    #3

    #>>> FFM.Regulatory_Permission.query (Q.RAW.eirp <= '110 mW').count ()
    #3
    #>>> FFM.Regulatory_Permission.query (Q.RAW.eirp > '0.11 W').count ()
    #1
    #>>> FFM.Regulatory_Permission.query (Q.RAW.eirp > '110 mW').count ()
    #1

    >>> FFM.Wireless_Channel.query (Q.RAW.frequency > "5.7 GHz").count ()
    58
    >>> FFM.Wireless_Channel.query (Q.RAW.frequency < "5.7 GHz").count ()
    28

    >>> dom   = FFM.Regulatory_Domain.instance (countrycode = "AT", raw = True)
    >>> band1 = dict (lower = "1 THz", upper = "2 THz")
    >>> rp1   = FFM.Regulatory_Permission \\
    ...    (dom, band1, bandwidth = "40MHz", eirp = "100mW", raw = True)
    >>> round (rp1.eirp, 2)
    20.0
    >>> rp1.raw_attr ('eirp')
    u'100mW'
    >>> band2 = dict (lower = "2 THz", upper = "3 THz")
    >>> rp2    = FFM.Regulatory_Permission \\
    ...    (dom, band2, bandwidth = "40MHz", eirp = "1W", raw = True)
    >>> round (rp2.eirp, 2)
    30.0
    >>> rp2.raw_attr ('eirp')
    u'1W'
    >>> band3 = dict (lower = "3 THz", upper = "4 THz")
    >>> rp3    = FFM.Regulatory_Permission \\
    ...    (dom, band3, bandwidth = "40MHz", eirp = "10dBmW", raw = True)
    >>> round (rp3.eirp, 2)
    10.0
    >>> rp3.raw_attr ('eirp')
    u'10dBmW'
    >>> band4 = dict (lower = "4 THz", upper = "5 THz")
    >>> rp4    = FFM.Regulatory_Permission \\
    ...    (dom, band4, bandwidth = "40MHz", eirp = "10dBW", raw = True)
    >>> round (rp4.eirp, 2)
    40.0
    >>> rp4.raw_attr ('eirp')
    u'10dBW'

"""

__test__ = Scaffold.create_test_dict \
  ( dict
      ( main       = _test_code
      )
  )

### __END__ FFM.__test__.Regulatory
