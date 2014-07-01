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
#    FFM.IP_DNS_Alias
#
# Purpose
#    Model a DNS alias for a Net_Interface_in_IP_Network
#
# Revision Dates
#     1-Jul-2014 (RS) Creation
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _MOM.import_MOM          import *
from   _FFM                     import FFM

from   _GTW._OMP._DNS.Attr_Type import A_DNS_Label

import _FFM.Entity
import _FFM.Net_Interface_in_IP_Network

_Ancestor_Essence = FFM.Link1

class IP_DNS_Alias (_Ancestor_Essence) :
    """DNS alias for IP address"""

    is_partial  = True

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        ### Primary attributes

        class left (_Ancestor.left) :
            """The assigned IP Address"""

            role_name          = 'address'
            role_type          = FFM.Net_Interface_in_IP_Network

        # end class left

        class name (A_DNS_Label) :
            """Name of the alias."""

            kind               = Attr.Primary

        # end class name

    # end class _Attributes

    # For defining uniqueness predicate in descendants
    _unique_name_vars = ("name", )
    _unique_name_dict = dict \
        ( name    = "unique_name"
        , __doc__ = "The name must be unique for this type of address."
        )

# end class IP_DNS_Alias

if __name__ != "__main__" :
    FFM._Export ("*")
### __END__ FFM.IP_DNS_Alias
