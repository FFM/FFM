# -*- coding: utf-8 -*-
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
#    FFM.Routing_Zone
#
# Purpose
#    Model the routing of a zone of FFM
#
# Revision Dates
#     6-Mar-2012 (CT) Creation
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _MOM.import_MOM        import *
from   _FFM                   import FFM
import _FFM.Zone

_Ancestor_Essence = FFM.Link1

class Routing_Zone (_Ancestor_Essence) :
    """Model the routing of a zone of FFM."""

    is_partial = True

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        ### Primary attributes

        class left (_Ancestor.left) :
            """The zone that's routed for."""

            role_type          = FFM.Zone
            ui_allow_new       = True

        # end class left

    # end class _Attributes

# end class Routing_Zone

_Ancestor_Essence = Routing_Zone

class Routing_Zone_OLSR (_Ancestor_Essence) :
    """Routing zone using the OLSR routing protocol."""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        ### XXX define the attributes necessary to parameterize the routing
        ### for `zone`

    # end class _Attributes

# end class Routing_Zone_OLSR

if __name__ != "__main__" :
    FFM._Export ("*")
### __END__ FFM.Routing_Zone
