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
#    FFM.Firmware
#
# Purpose
#    Model the firmware of a device
#
# Revision Dates
#    28-Mar-2012 (CT) Creation
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _MOM.import_MOM        import *
from   _FFM                   import FFM

_Ancestor_Essence = MOM.Object

class Firmware_Type (FFM.Entity, _Ancestor_Essence) :
    """Type of firmware usable by some devices."""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class name (A_String) :
            """Name identifying the firmware."""

            kind               = Attr.Primary
            max_length         = 128

        # end class name

        class url (A_Url) :
            """URL for Firmware_Type"""

            kind               = Attr.Primary

        # end class url

    # end class _Attributes

# end class Firmware_Type

_Ancestor_Essence = MOM.Link1

class Firmware (FFM.Entity, _Ancestor_Essence) :
    """Firmware usable by some devices."""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        ### Primary attributes

        class left (_Ancestor.left) :
            """Type of firmware"""

            role_type          = Firmware_Type
            max_links          = 1

        # end class left

        class version (A_String) :
            """Version of the firmware"""

            kind               = Attr.Primary
            max_length         = 16

        # end class version

    # end class _Attributes

# end class Firmware

_Ancestor_Essence = MOM.Link1

class Firmware_Binary (FFM.Entity, _Ancestor_Essence) :
    """Binary for firmware."""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        ### Primary attributes

        class left (_Ancestor.left) :
            """Firmware for which binary was built."""

            role_type          = Firmware

        # end class left

        ### XXX target CPU, size, ...

    # end class _Attributes

# end class Firmware_Binary

if __name__ != "__main__" :
    FFM._Export ("*")
### __END__ FFM.Firmware
