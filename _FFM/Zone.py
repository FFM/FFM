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
#    FFM.Zone
#
# Purpose
#    Model a routing zone of FFM
#
# Revision Dates
#     6-Mar-2012 (CT) Creation
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _MOM.import_MOM        import *
from   _FFM                   import FFM
import _FFM.Entity

_Ancestor_Essence = MOM.Object

class Zone (FFM.Entity, _Ancestor_Essence) :
    """Model a routing zone of FFM."""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class name (A_String) :
            """Name of the zone"""

            kind               = Attr.Primary
            max_length         = 64
            ignore_case        = True
            completer          = Attr.Completer_Spec  (2, Attr.Selector.primary)

        # end class name

    # end class _Attributes

# end class Zone

if __name__ != "__main__" :
    FFM._Export ("*")
### __END__ FFM.Zone
