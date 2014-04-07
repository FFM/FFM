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
#    FFM.Net_Link
#
# Purpose
#    Model a link between two network interfaces
#
# Revision Dates
#    10-May-2012 (CT) Creation
#    18-May-2012 (CT) Change `not_inverse` to use `count`, not `one`
#    19-Sep-2012 (CT) Use `force_role_name`, not `role_name`
#    26-Feb-2013 (CT) Remove `is_partial = True`,
#                     i.e., allow links between different `Net_Interface`
#    20-May-2013 (CT) Add `link_ref_suffix` to `left` and `right`
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _MOM.import_MOM          import *
from   _FFM                     import FFM

import _FFM.Net_Interface

_Ancestor_Essence = FFM.Link2

class Net_Link (_Ancestor_Essence) :
    """Link between two network interfaces."""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        ### Primary attributes

        class left (_Ancestor.left) :
            """Left network interface"""

            role_type          = FFM.Net_Interface
            force_role_name    = "left"
            link_ref_suffix    = "_net_link"

        # end class left

        class right (_Ancestor.right) :
            """Right network interface"""

            role_type          = FFM.Net_Interface
            force_role_name    = "right"
            link_ref_suffix    = "_net_link"

        # end class right

        ### Non-primary attributes

    # end class _Attributes

    class _Predicates (_Ancestor_Essence._Predicates) :

        _Ancestor = _Ancestor_Essence._Predicates

        class left_not_right (Pred.Condition) :
            """`left` and `right` must be different objects!"""

            kind               = Pred.Object
            assertion          = "left != right"
            attributes         = ("left", "right")

        # end class left_not_right

        class not_inverse (Pred.Condition) :
            """There must not be a second link with `left` and `right`
               swapped.
            """

            kind               = Pred.Region
            assertion          = "inverse_count == 0"
            attributes         = ("left", "right")
            bindings           = dict \
                ( inverse_count  =
                    "this.ETM.query (left = right, right = left).count ()"
                )

        # end class not_inverse

    # end class _Predicates

# end class Net_Link

if __name__ != "__main__" :
    FFM._Export ("*")
### __END__ FFM.Net_Link
