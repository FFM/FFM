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
#    FFM.Net_Interface
#
# Purpose
#    Model network interfaces in FFM
#
# Revision Dates
#     6-Mar-2012 (CT) Creation
#    10-May-2012 (CT) Change `mac_address` to `Primary_Optional`, add `name`
#    13-Sep-2012 (RS) Set `is_partial`
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _MOM.import_MOM          import *
from   _FFM                     import FFM

from   _GTW._OMP._NET.Attr_Type import *

import _FFM.Net_Device

_Ancestor_Essence = FFM.Link1

class Net_Interface (_Ancestor_Essence) :
    """Model a network interface of a FFM device"""

    is_partial = True

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        ### Primary attributes

        class left (_Ancestor.left) :
            """Network device the interface is connected to."""

            role_type          = FFM.Net_Device
            role_name          = "device"

        # end class left

        class mac_address (A_MAC_Address) :
            """MAC address of interface."""

            kind               = Attr.Primary_Optional

        # end class mac_address

        class name (A_String) :
            """Name of the node"""

            kind               = Attr.Primary_Optional
            max_length         = 16
            ignore_case        = True
            completer          = Attr.Completer_Spec  (2, Attr.Selector.primary)

        # end class name

        ### Non-primary attributes

        class is_active (A_Boolean) :
            """Indicates if this interface is active."""

            kind               = Attr.Optional

        # end class is_active

    # end class _Attributes

# end class Net_Interface

if __name__ != "__main__" :
    FFM._Export ("*")
### __END__ FFM.Net_Interface
