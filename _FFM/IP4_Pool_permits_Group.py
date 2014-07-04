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
#    FFM.IP4_Pool_permits_Group
#
# Purpose
#    Model permission for IP4_Network reservation from an IP4_Pool
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

import _FFM.IP_Pool_permits_Group

_Ancestor_Essence = FFM.IP_Pool_permits_Group

class IP4_Pool_permits_Group (_Ancestor_Essence) :
    """Permission to reserve IP4_Network from IP4_Pool"""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        ### Primary attributes

        class left (_Ancestor.left) :
            """IP Pool."""

            role_type          = FFM.IP4_Pool

        # end class left

        ### Non-primary attributes

        class user_quota (A_IP4_Quota, _Ancestor.user_quota)   : pass

        class node_quota (A_IP4_Quota, _Ancestor.node_quota)   : pass

        class iface_quota (A_IP4_Quota, _Ancestor.iface_quota) : pass

    # end class _Attributes

# end class IP4_Pool_permits_Group

if __name__ != "__main__" :
    FFM._Export ("*")
### __END__ FFM.IP4_Pool_permits_Group
