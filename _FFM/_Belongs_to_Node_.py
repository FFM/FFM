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
#    FFM._Belongs_to_Node_
#
# Purpose
#    Mixin for computed `belongs_to_node` attribute
#
# Revision Dates
#     6-Dec-2012 (CT) Creation
#    ««revision-date»»···
#--

from   __future__ import absolute_import, division, print_function, unicode_literals

from   _MOM.import_MOM          import *
from   _FFM                     import FFM
import _FFM.Entity
import _FFM.Node


_Ancestor_Essence = FFM.Entity

class _Belongs_to_Node_ (_Ancestor_Essence) :
    """Mixin for computed `belongs_to_node` attribute"""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class belongs_to_node (A_Id_Entity) :
            """Node this %(ui_name)s belongs to."""

            kind               = Attr.Computed
            P_Type             = FFM.Node

            def computed (self, obj) :
                return obj.left.belongs_to_node
            # end def computed

        # end class belongs_to_node

    # end class _Attributes

# end class _Belongs_to_Node_

if __name__ != "__main__" :
    FFM._Export ("_Belongs_to_Node_")
### __END__ FFM._Belongs_to_Node_
