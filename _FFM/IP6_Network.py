# -*- coding: utf-8 -*-
# Copyright (C) 2012-2014 Dr. Ralf Schlatterbeck All rights reserved
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
#    FFM.IP6_Network
#
# Purpose
#    Model IP6 Network of FFM
#
# Revision Dates
#    22-May-2012 (RS) Creation
#    27-Feb-2013 (CT) Add `pool`
#     7-Aug-2013 (CT) Adapt to major surgery of GTW.OMP.NET.Attr_Type
#     2-Apr-2014 (CT) Fix bases of `net_address`
#     2-Apr-2014 (CT) Add `pool.rev_ref_attr_name`
#     3-Apr-2014 (CT) Change `pool` to `parent`
#    20-Jun-2014 (RS) Re-add `pool`
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _MOM.import_MOM          import *
from   _FFM                     import FFM

from   _FFM.Attr_Type           import *
from   _GTW._OMP._NET           import NET

import _FFM.IP_Network

import _GTW._OMP._NET.Attr_Type

_Ancestor_Essence = FFM.IP_Network

class IP6_Network (_Ancestor_Essence) :
    """IPv6 Network of FFM"""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        ### Primary attributes

        class net_address (NET.A_IP6_Network, _Ancestor.net_address) :
            """IPv6 Network address."""

        # end class net_address

        ### Non-primary attributes

        class parent (_Ancestor.parent) :
            """Parent of the `%(type_name)s`."""

            P_Type             = "FFM.IP6_Network"
            rev_ref_attr_name  = "subnets"

        # end class parent

        class pool (_Ancestor.pool) :
            """Pool to which this `%(type_name)s` belongs."""

            P_Type             = "FFM.IP6_Network"

        # end class pool

    # end class _Attributes

# end class IP6_Network

if __name__ != "__main__" :
    FFM._Export ("*")
### __END__ FFM.IP6_Network
