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
#    FFM.Wireless_Link
#
# Purpose
#    Model a link between two wireless interfaces
#
# Revision Dates
#    10-May-2012 (CT) Creation
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _MOM.import_MOM          import *
from   _FFM                     import FFM

import _FFM.Net_Link
import _FFM.Wireless_Interface

_Ancestor_Essence = FFM.Net_Link

class Wireless_Link (_Ancestor_Essence) :
    """Link between two wireless network interfaces."""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        ### Primary attributes

        class left (_Ancestor.left) :

            role_type          = FFM.Wireless_Interface

        # end class left

        class right (_Ancestor.right) :

            role_type          = FFM.Wireless_Interface

        # end class right

        ### Non-primary attributes

    # end class _Attributes

    class _Predicates (_Ancestor_Essence._Predicates) :

        _Ancestor = _Ancestor_Essence._Predicates

        class valid_modes (Pred.Condition) :
            """`left.mode` and `right.mode` must be linkable to each other."""

            kind               = Pred.Object
            assertion          = "left.mode.is_linkable (right.mode)"
            attributes         = ("left.mode", "right.mode")

        # end class valid_modes

    # end class _Predicates

# end class Wireless_Link

if __name__ != "__main__" :
    FFM._Export ("*")
### __END__ FFM.Wireless_Link
