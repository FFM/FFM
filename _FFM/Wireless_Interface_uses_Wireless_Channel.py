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
#    FFM.Wireless_Interface_uses_Wireless_Channel
#
# Purpose
#    Model the channel used by a wireless interface
#
# Revision Dates
#    20-Aug-2012 (RS) Creation
#     6-Dec-2012 (RS) Add `belongs_to_node`
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _MOM.import_MOM        import *
from   _FFM                   import FFM

from   _FFM.Attr_Type         import *
import _FFM.Wireless_Channel
import _FFM.Wireless_Interface
import _FFM._Belongs_to_Node_

_Ancestor_Essence = FFM.Link2
_Mixin = FFM._Belongs_to_Node_

class Wireless_Interface_uses_Wireless_Channel (_Mixin, _Ancestor_Essence) :
    """Wireless channel used by a wireless interface"""

    class _Attributes (_Mixin._Attributes, _Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        ### Primary attributes

        class left (_Ancestor.left) :
            """Wireless interface."""

            role_type          = FFM.Wireless_Interface
            auto_cache         = True
            role_name          = "interface"

        # end class left

        class right (_Ancestor.right) :
            """Wireless channel."""

            role_type          = FFM.Wireless_Channel
            auto_cache         = True
            role_name          = "channel"

        # end class right

        ### Non-primary attributes

    # end class _Attributes

# end class Wireless_Interface_uses_Wireless_Channel

if __name__ != "__main__" :
    FFM._Export ("*")
### __END__ FFM.Wireless_Interface_uses_Wireless_Channel
