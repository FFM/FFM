# -*- coding: utf-8 -*-
# Copyright (C) 2012-2013 Mag. Christian Tanzer All rights reserved
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
#    18-Jun-2012 (CT) Add missing `is_partial` to `Firmware_Bin`
#    15-May-2013 (CT) Rename `auto_cache` to `auto_rev_ref`
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _MOM.import_MOM        import *
from   _FFM                   import FFM

_Ancestor_Essence = FFM.Object

class Firmware_Type (_Ancestor_Essence) :
    """Type of firmware usable by some devices."""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class name (A_String) :
            """Name identifying the firmware type."""

            kind               = Attr.Primary
            max_length         = 128

        # end class name

        class url (A_Url_X) :
            """URL for Firmware_Type"""

            kind               = Attr.Primary

        # end class url

    # end class _Attributes

# end class Firmware_Type

_Ancestor_Essence = FFM.Link1

class Firmware_Version (_Ancestor_Essence) :
    """Firmware version usable by some devices."""

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

# end class Firmware_Version

_Ancestor_Essence = FFM.Id_Entity

class Firmware_Bin (_Ancestor_Essence) :
    """Base class for Firmware_Binary and Firmware_Bundle."""

    is_partial = True

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

    # end class _Attributes

# end class Firmware_Bin

_Ancestor_Essence = FFM.Link1

class Firmware_Binary (Firmware_Bin, _Ancestor_Essence) :
    """Binary for firmware."""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        ### Primary attributes

        class left (_Ancestor.left) :
            """Firmware for which binary was built."""

            role_type          = Firmware_Version

        # end class left

        ### XXX target CPU, size, ...

        class binaries (A_Blob) :
            """List of binaries containing firmware."""

            kind               = Attr.Computed

            def computed (self, obj) :
                return (obj, )
            # end def computed

        # end class binaries

    # end class _Attributes

# end class Firmware_Binary

_Ancestor_Essence = FFM.Object

class Firmware_Bundle (Firmware_Bin, _Ancestor_Essence) :
    """A bundle of binaries for firmware."""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class name (A_String) :
            """Name identifying the firmware bundle."""

            kind               = Attr.Primary
            max_length         = 128

        # end class name

        class version (A_String) :
            """Version of the firmware bundle."""

            kind               = Attr.Primary
            max_length         = 16

        # end class version

    # end class _Attributes

# end class Firmware_Bundle

_Ancestor_Essence = FFM.Link2

class Firmware_Binary_in_Firmware_Bundle (_Ancestor_Essence) :
    """Link Firmware_Binary to Firmware_Bundle."""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        ### Primary attributes

        class left (_Ancestor.left) :
            """Binary."""

            role_type          = Firmware_Binary
            auto_rev_ref       = "binary"

        # end class left

        class right (_Ancestor.right) :
            """Bundle."""

            role_type          = Firmware_Bundle

        # end class right

    # end class _Attributes

# end class Firmware_Binary_in_Firmware_Bundle

if __name__ != "__main__" :
    FFM._Export ("*")
### __END__ FFM.Firmware
