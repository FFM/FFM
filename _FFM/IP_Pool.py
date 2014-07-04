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
#    FFM.IP_Pool
#
# Purpose
#    Model Attributes of an IP network pool
#
# Revision Dates
#    20-Jun-2014 (RS) Creation
#    23-Jun-2014 (RS) Add `cool_down_period`, rename `left.link_ref_attr_name`
#     3-Jul-2014 (RS) `IP_Pool` no longer `Link1`, rename
#                     `_A_IP_Netmask_Interval_`
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _MOM.import_MOM            import *
from   _FFM                       import FFM
from   _FFM.Attr_Type             import _A_IP_Netmask_Interval_

from   _MOM._Attr.Date_Time_Delta import A_Date_Time_Delta

import _FFM.IP_Network

_Ancestor_Essence = FFM.Object

class IP_Pool (_Ancestor_Essence) :
    """Attributes of an IP network pool."""

    is_partial  = True

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        ### Primary attributes

        class name (A_String) :
            """Name of IP_Pool"""

            kind               = Attr.Primary
            max_length         = 40
            ignore_case        = True

        # end class left

        ### Non-primary attributes

        class cool_down_period (A_Date_Time_Delta) :
            """Cool down period for this %(type_name)s."""

            kind               = Attr.Optional

        # end class cool_down_period

        class netmask_interval (_A_IP_Netmask_Interval_) :
            """Limit netmasks to allocate from this %(type_name)s."""

            kind               = Attr.Optional

        # end class netmask_interval

        class node (A_Id_Entity) :
            """Node for which this `%(type_name)s` is reserved."""

            kind               = Attr.Optional
            P_Type             = FFM.Node
            ui_allow_new       = False

         # end class node

    # end class _Attributes

# end class IP_Pool

if __name__ != "__main__" :
    FFM._Export ("*")
### __END__ FFM.IP_Pool
