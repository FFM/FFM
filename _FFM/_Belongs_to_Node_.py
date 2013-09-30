# -*- coding: iso-8859-15 -*-
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
#    FFM._Belongs_to_Node_
#
# Purpose
#    Mixin for computed `belongs_to_node` attribute
#
# Revision Dates
#     6-Dec-2012 (CT) Creation
#    14-Dec-2012 (CT) Change `belongs_to_node.kind` to `Attr.Query`
#    17-Dec-2012 (CT) Set `belongs_to_node.hidden` to `True`
#    26-Jan-2013 (CT) Define `belongs_to_node.query`, not `.query_fct`
#    25-Feb-2013 (CT) Add `belongs_to_node.query_preconditions`
#    26-Feb-2013 (CT) Disable `belongs_to_node`
#    14-Aug-2013 (CT) Re-enable `belongs_to_node`
#    14-Aug-2013 (CT) Add `is_partial = True`,
#                     derive from `FFM.Id_Entity`, not `FFM.Entity`
#     4-Sep-2013 (CT) Derive from `FFM.Link`, not `FFM.Id_Entity`
#    30-Sep-2013 (CT) Split into partial `_Belongs_to_Node_`, non-partial
#                     `_Belongs_to_Node__Left_`
#    ««revision-date»»···
#--

from   __future__ import absolute_import, division, print_function, unicode_literals

from   _MOM.import_MOM          import *
from   _FFM                     import FFM
import _FFM.Entity

_Ancestor_Essence = FFM.Id_Entity

class _Belongs_to_Node_ (_Ancestor_Essence) :
    """Mixin for computed `belongs_to_node` attribute"""

    is_partial = True

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class belongs_to_node (A_Id_Entity) :
            """Node this %(ui_type_name)s belongs to."""

            kind                = Attr.Query
            hidden              = True
            P_Type              = "FFM.Node"
            is_partial          = True ### `query` is defined by descendents

        # end class belongs_to_node

    # end class _Attributes

# end class _Belongs_to_Node_

_Ancestor_Essence = FFM.Link
_Mixin            = _Belongs_to_Node_

class _Belongs_to_Node__Left_ (_Mixin, _Ancestor_Essence) :
    """Mixin for computed `belongs_to_node` attribute"""

    is_partial = True

    class _Attributes (_Mixin._Attributes, _Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class belongs_to_node (_Mixin._Attributes.belongs_to_node) :

            query               = Q.left.belongs_to_node
            query_preconditions = (Q.left, )
            is_partial          = False

        # end class belongs_to_node

    # end class _Attributes

# end class _Belongs_to_Node__Left_

if __name__ != "__main__" :
    FFM._Export ("_Belongs_to_Node_", "_Belongs_to_Node__Left_")
### __END__ FFM._Belongs_to_Node_
