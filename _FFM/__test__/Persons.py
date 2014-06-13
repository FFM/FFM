# -*- coding: utf-8 -*-
# Copyright (C) 2012-2014 Mag. Christian Tanzer All rights reserved
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
#    FFM.__test__.Persons
#
# Purpose
#    Test Person and associations
#
# Revision Dates
#    19-Sep-2012 (RS) Creation
#    11-Oct-2012 (RS) Fix missing `raw` parameter
#    11-Oct-2012 (RS) `Nickname` test
#    14-Jun-2014 (RS) `PAP.Adhoc_Group`, `PAP.Person_in_Group`
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
    >>> p1  = PAP.Person \\
    ...     (first_name = 'Ralf', last_name = 'Schlatterbeck', raw = True)
    >>> p2  = PAP.Person \\
    ...     (first_name = 'Hans', last_name = 'Schlatterbeck', raw = True)
    >>> pmp = FFM.Person_mentors_Person (p1, p2)
    >>> nic = PAP.Nickname ('runtux', raw = True)
    >>> phn = PAP.Person_has_Nickname (p1, nic)
    >>> c1  = PAP.Company ("Open Source Consulting")
    >>> pg1 = PAP.Person_in_Group (p1, c1)

    >>> g   = PAP.Adhoc_Group ("New Adhoc Group")
    >>> pg2 = PAP.Person_in_Group (p1, g)


"""

__test__ = Scaffold.create_test_dict \
  ( dict
      ( main       = _test_code
      )
  )

### __END__ FFM.__test__.Nodes
