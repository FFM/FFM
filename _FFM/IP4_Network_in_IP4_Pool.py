# -*- coding: utf-8 -*-
# Copyright (C) 2014 Dr. Ralf Schlatterbeck All rights reserved
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
#    FFM.IP4_Network_in_IP4_Pool
#
# Purpose
#    Model IPv4 networks in an IPv4 pool
#
# Revision Dates
#     3-Jul-2014 (RS) Creation
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _MOM.import_MOM        import *
from   _FFM                   import FFM

import _FFM.IP4_Network
import _FFM.IP4_Pool
import _FFM.IP_Network_in_IP_Pool

_Ancestor_Essence = FFM.IP_Network_in_IP_Pool

class IP4_Network_in_IP4_Pool (_Ancestor_Essence) :
    """IPv4 networks in an IPv4 pool."""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        ### Primary attributes

        class left (_Ancestor.left) :
            """IP network."""

            role_type          = FFM.IP4_Network
            link_ref_attr_name = "ip_pool"

        # end class left

        class right (_Ancestor.right) :
            """IP pool."""

            role_type          = FFM.IP4_Pool
            auto_rev_ref       = "ip_pool"
            link_ref_attr_name = "ip_network"

        # end class right

    # end class _Attributes

# end class IP4_Network_in_IP4_Pool

if __name__ != "__main__" :
    FFM._Export ("*")
### __END__ FFM.IP4_Network_in_IP4_Pool
