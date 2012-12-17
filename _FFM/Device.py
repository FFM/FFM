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
#    FFM.Device
#
# Purpose
#    Model a device in FFM
#
# Revision Dates
#     6-Mar-2012 (CT) Creation
#     8-Dec-2012 (RS) Add `desc`
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _MOM.import_MOM        import *
from   _FFM                   import FFM
import _FFM.Device_Type

_Ancestor_Essence = FFM.Link1

class Device (_Ancestor_Essence) :
    """Model a device used by a FFM node."""

    is_partial = True

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        ### Primary attributes

        class left (_Ancestor.left) :
            """Type of device"""

            role_type          = FFM.Device_Type
            role_name          = "type"
            ui_allow_new       = False

        # end class left

        class name (A_String) :
            """Name of device"""

            kind               = Attr.Primary_Optional
            max_length         = 40
            ignore_case        = True
            completer          = Attr.Completer_Spec  (2, Attr.Selector.primary)

        # end class name

        ### Non-primary attributes

        class desc (A_Text) :
            """Description of device"""

            kind               = Attr.Optional

        # end class desc

    # end class _Attributes

# end class Device

if __name__ != "__main__" :
    FFM._Export ("*")
### __END__ FFM.Device
