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
#    FFM.IP_Pool_permits_Group
#
# Purpose
#    Model permission for IP_Network reservation from an IP_Pool
#
# Revision Dates
#     3-Jul-2014 (RS) Creation
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _MOM.import_MOM        import *
from   _FFM                   import FFM
from   _GTW._OMP._PAP         import PAP

from   _FFM.Attr_Type         import *

import _FFM.IP_Network
import _GTW._OMP._PAP.Id_Entity_permits_Group

_Ancestor_Essence = PAP.Id_Entity_permits_Group

class IP_Pool_permits_Group (_Ancestor_Essence) :
    """Permission to reserve IP_Network from IP_Pool"""

    is_partial  = True

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        ### Primary attributes

        class left (_Ancestor.left) :
            """IP Pool."""

            role_type          = FFM.IP_Pool

        # end class left

        ### Non-primary attributes

        class user_quota (_A_IP_Quota_) :
            """Quota of IP allocations from this IP pool per user."""

            kind = Attr.Optional

        # end class user_quota

        class node_quota (_A_IP_Quota_) :
            """Quota of IP allocations from this IP pool per node."""

            kind = Attr.Optional

        # end class user_quota

        class iface_quota (_A_IP_Quota_) :
            """Quota of IP allocations from this IP pool for a single
               network interface.
            """

            kind = Attr.Optional

        # end class iface_quota

    # end class _Attributes

# end class IP_Pool_permits_Group

if __name__ != "__main__" :
    FFM._Export ("*")
### __END__ FFM.IP_Pool_permits_Group
