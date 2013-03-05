# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012-2013 Dr. Ralf Schlatterbeck All rights reserved
# Reichergasse 131, A--3411 Weidling, Austria. rsc@runtux.com
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
#    FFM.Net_Interface_in_IP_Network
#
# Purpose
#    Model a Net interface in an IP network
#
# Revision Dates
#    18-May-2012 (RS) Creation
#    23-May-2012 (RS) Use `_A_IP_Address_` for `ip_address`
#    20-Sep-2012 (RS) Add `auto_cache_np`, `auto_derive_np` to `left`
#                     remove `auto_cache` from `right`
#     5-Mar-2013 (CT) Set `right.max_links = 1`
#     5-Mar-2013 (CT) Replace `ip_address` by `mask_len`
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _MOM.import_MOM          import *
from   _FFM                     import FFM

from   _FFM.Attr_Type           import *
from   _GTW._OMP._NET.Attr_Type import *

import _FFM.Net_Interface
import _FFM.IP_Network

_Ancestor_Essence = FFM.Link2

class Net_Interface_in_IP_Network (_Ancestor_Essence) :
    """Net interface in IP network"""

    is_partial = True

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        ### Primary attributes

        class left (_Ancestor.left) :
            """Network interface."""

            role_type          = FFM.Net_Interface
            auto_cache         = True
            auto_derive_np     = True
            auto_cache_np      = True

        # end class left

        class right (_Ancestor.right) :
            """IP Network."""

            role_type          = FFM.IP_Network
            max_links          = 1

        # end class right

        ### Non-primary attributes

        class mask_len (A_Int) :
            """Network mask used for this IP Network."""

            kind               = Attr.Required

        # end class mask_len

    # end class _Attributes

    class _Predicates (_Ancestor_Essence._Predicates) :

        _Ancestor = _Ancestor_Essence._Predicates

        class valid_mask_len (Pred.Condition) :
            """The `mask_len` must match the one of `right` or of any
               network containing `right`.
            """

            kind               = Pred.Object
            assertion          = "mask_len in possible_mask_lens"
            attributes         = ("mask_len", "right.net_address")
            bindings           = dict \
                ( possible_mask_lens =
                    """sorted """
                      """( right.ETM.query """
                            """( (Q.net_address.CONTAINS (right.net_address))"""
                            """& (Q.electric == False)"""
                            """).attr ("net_address.mask_len")"""
                      """)"""
                )

        # end class valid_mask_len

    # end class _Predicates

# end class Net_Interface_in_IP_Network

if __name__ != "__main__" :
    FFM._Export ("*")
### __END__ FFM.Net_Interface_in_IP_Network
