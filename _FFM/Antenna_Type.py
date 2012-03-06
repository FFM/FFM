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
#    FFM.Antenna_Type
#
# Purpose
#    Model the type of antennas in FFM
#
# Revision Dates
#     6-Mar-2012 (CT) Creation
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _MOM.import_MOM           import *
from   _MOM._Attr.Float_Interval import *
from   _FFM                      import FFM
import _FFM.Device_Type

_Ancestor_Essence = FFM.Device_Type

class Antenna_Type (_Ancestor_Essence) :
    """Model the type of antennas in FFM."""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class gain (A_Float) :
            """Describes how well the antenna converts input power into radio
               waves headed in a specified direction (in dBi).
            """

            kind               = Attr.Required

        # end class gain

        class freqency (A_Float_Interval) :
            """Frequency range the antenna supports."""

            kind               = Attr.Required

        # end class freqency

    # end class _Attributes

# end class Antenna_Type

if __name__ != "__main__" :
    FFM._Export ("*")
### __END__ FFM.Antenna_Type
