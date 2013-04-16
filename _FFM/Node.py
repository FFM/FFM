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
#    FFM.Node
#
# Purpose
#    Model a node of FFM
#
# Revision Dates
#     6-Mar-2012 (CT) Creation
#    19-Jul-2012 (RS) Add `position`
#    20-Jul-2012 (RS) `Node` no longer inherits from `PAP.Subject`
#    18-Sep-2012 (RS) Add `owner` and `manager`
#    22-Sep-2012 (RS) make `name` `A_DNS_Label`
#    11-Oct-2012 (RS) `map_p` -> `show_in_map`
#    12-Oct-2012 (RS) Make `Node` a `PAP.Subject` again.
#    16-Oct-2012 (CT) Correct `refuse_links`
#     6-Dec-2012 (RS) Add `belongs_to_node`
#    13-Dec-2012 (CT) Set `owner.P_Type` to `PAP.Person`
#    13-Dec-2012 (CT) Set `owner.ui_allow_new` to `False`
#    14-Dec-2012 (CT) Return `obj`, not `self`, from `belongs_to_node.computed`
#    17-Dec-2012 (CT) Set `manager.ui_allow_new` to `False`
#     4-Apr-2013 (CT) Change `owner.P_Type` back to `PAP.Subject`
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _MOM.import_MOM          import *
from   _MOM._Attr.Position      import A_Position
from   _FFM                     import FFM
from   _GTW._OMP._PAP           import PAP, Person, Subject
from   _GTW._OMP._DNS.Attr_Type import A_DNS_Label

import _FFM.Entity

_Ancestor_Essence = PAP.Subject

class Node (FFM.Entity, _Ancestor_Essence) :
    """Model a node of FFM"""

    refuse_links = set \
        (( "GTW.OMP.PAP.Node_has_Phone"
         , "GTW.OMP.PAP.Node_has_Email"
         , "GTW.OMP.PAP.Subject_has_Phone"
         , "GTW.OMP.PAP.Subject_has_Email"
        ))

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor    = _Ancestor_Essence._Attributes

        class name (A_DNS_Label) :
            """Name of the node"""

            kind               = Attr.Primary
            completer          = Attr.Completer_Spec  (2, Attr.Selector.primary)

        # end class name

        class belongs_to_node (A_Id_Entity) :
            """Node to which this entity belongs."""

            kind               = Attr.Computed

            def computed (self, obj) :
                return obj
            # end def computed

        # end class belongs_to_node

        class manager (A_Id_Entity) :
            """Manager of the node"""

            kind               = Attr.Required
            P_Type             = PAP.Person
            ui_allow_new       = False

        # end class manager

        class owner (A_Id_Entity) :
            """Owner of the node, defaults to manager"""

            kind               = Attr.Optional
            Kind_Mixins        = (Attr.Computed_Mixin, )
            P_Type             = PAP.Subject
            ui_allow_new       = False

            def computed (self, obj) :
                if obj :
                    return obj.manager
            # end def computed

        # end class owner

        class position (A_Position) :
            """GPS position and optional height of the node"""

            kind               = Attr.Optional

        # end class position

        class show_in_map (A_Boolean) :
            """Show in map."""

            kind               = Attr.Optional
            default            = True

        # end class show_in_map

    # end class _Attributes

# end class Node

Node._Attributes.belongs_to_node.P_Type = Node

if __name__ != "__main__" :
    FFM._Export ("*")
### __END__ FFM.Node
