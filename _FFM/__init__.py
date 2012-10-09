# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package FFM.
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
#    FFM.__init__
#
# Purpose
#    Package defining the common node model for Funkfeuer...
#
# Revision Dates
#     6-Mar-2012 (CT) Creation
#     9-Oct-2012 (CT) Add `_desc_`
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from _TFL.Package_Namespace import Package_Namespace

_desc_ = """
Object model defining the common node model for Funkfeuer.
"""

FFM = Package_Namespace ()

del Package_Namespace

### __END__ FFM.__init__
