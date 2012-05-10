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
#    FFM.Wireless_Mode
#
# Purpose
#    Model the mode a wireless device operates in
#
# Revision Dates
#    14-Mar-2012 (CT) Creation
#    10-May-2012 (CT) Add `is_linkable`
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _MOM.import_MOM        import *
from   _FFM                   import FFM
import _FFM.Entity

_Ancestor_Essence = FFM.Link1

class _Wireless_Mode_ (_Ancestor_Essence) :
    """Model the mode a wireless device operates in."""

    is_partial = True

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        ### Primary attributes

        class left (_Ancestor.left) :
            """The wireless device operating in this mode."""

            role_type          = FFM.Wireless_Interface
            role_name          = "interface"
            auto_cache         = "mode"

        # end class left

        ### *** BEWARE ***
        ### To ensure that a `Wireless_Interface` has only one `mode`, no
        ### other essential primary key attributes must be defined here or by
        ### derived classes

    # end class _Attributes

# end class _Wireless_Mode_

_Ancestor_Essence = _Wireless_Mode_

class Ad_Hoc_Mode (_Ancestor_Essence) :
    """Model the mode `ad hoc`."""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

    # end class _Attributes

    def is_linkable (self, other) :
        return isinstance (other, self.home_scope.FFM.Ad_Hoc_Mode.E_Type)
    # end def is_linkable

# end class Ad_Hoc_Mode

class AP_Mode (_Ancestor_Essence) :
    """Model the mode `access point`."""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        ### XXX

    # end class _Attributes

    def is_linkable (self, other) :
        return isinstance (other, self.home_scope.FFM.Client_Mode.E_Type)
    # end def is_linkable

# end class AP_Mode

class Client_Mode (_Ancestor_Essence) :
    """Model the mode `client`."""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

    # end class _Attributes

    def is_linkable (self, other) :
        return isinstance (other, self.home_scope.FFM.AP_Mode.E_Type)
    # end def is_linkable

# end class Client_Mode

if __name__ != "__main__" :
    FFM._Export ("*")
### __END__ FFM.Wireless_Mode
