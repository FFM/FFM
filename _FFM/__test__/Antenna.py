# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012 Mag. Christian Tanzer All rights reserved
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
#    FFM.__test__.Nodes
#
# Purpose
#    Test Node and associations
#
# Revision Dates
#     5-Dec-2012 (RS) Creation
#     7-Dec-2012 (RS) Test predicate `band_exists` of `Antenna_Type`
#    ««revision-date»»···
#--

from   __future__ import absolute_import, division, print_function, unicode_literals

from   _FFM.__test__.model      import *
from   datetime                 import datetime

_test_code = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...

    >>> FFM = scope.FFM
    >>> PAP = scope.PAP
    >>> at1 = FFM.Antenna_Type \\
    ...     ( name         = "Yagi1"
    ...     , desc         = "A Yagi"
    ...     , gain         = 17.5
    ...     , polarization = "vertical"
    ...     , raw          = True
    ...     )
    >>> b1 = FFM.Antenna_Band (at1, band = ("2.4 GHz", "3 GHz"), raw = True)
    >>> at2 = FFM.Antenna_Type \\
    ...     ( name         = "Yagi2"
    ...     , desc         = "A Yagi"
    ...     , gain         = 11.5
    ...     , polarization = "horizontal"
    ...     , raw          = True
    ...     )
    >>> b2 = FFM.Antenna_Band (at2, band = ("5 GHz", "6 GHz"), raw = True)
    >>> scope.commit ()

    >>> at3 = FFM.Antenna_Type \\
    ...     ( name         = "Yagi3"
    ...     , desc         = "A Yagi"
    ...     , gain         = 11.5
    ...     , polarization = "horizontal"
    ...     , raw          = True
    ...     )
    >>> scope.commit ()
    Traceback (most recent call last):
      ...
    Invariants: Condition `band_exists` : There must be at least one frequency band for the antenna. (number_of_bands >= 1)
        bands = None
        number_of_bands = 0 << len (bands)

    >>> args = dict (left = at1, azimuth = "180", elevation = 0, raw = True)
    >>> a = FFM.Antenna (name = "1", ** args)
    >>> (a.gain, a.polarization)
    (17.5, 1)
    >>> a = FFM.Antenna (name = "2", gain = 11, ** args)
    >>> (a.gain, a.polarization)
    (11.0, 1)
    >>> a = FFM.Antenna (name = "3", polarization = "horizontal", ** args)
    >>> (a.gain, a.polarization)
    (17.5, 0)
    >>> args = dict (left = at2, azimuth = "90", elevation = 0, raw = True)
    >>> b = FFM.Antenna (name = "4", ** args)
    >>> (b.gain, b.polarization)
    (11.5, 0)
    >>> b = FFM.Antenna (name = "5", polarization = 'left circular', ** args)
    >>> (b.gain, b.polarization)
    (11.5, 2)
    >>> b = FFM.Antenna (name = "6", gain = 22, ** args)
    >>> (b.gain, b.polarization)
    (22.0, 0)

    >>> scope.destroy ()

"""

__test__ = Scaffold.create_test_dict \
  ( dict
      ( main       = _test_code
      )
  )

### __END__ FFM.__test__.Nodes
