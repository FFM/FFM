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
#    FFM.Net_Interface_in_IP4_Network
#
# Purpose
#    Model a Net interface in an IPv4 network
#
# Revision Dates
#    18-May-2012 (RS) Creation
#    21-Sep-2012 (RS) set `is_partial`
#     5-Mar-2013 (CT) Remove redefinition of `ip_address` (gone from parent)
#    15-May-2013 (CT) Rename `auto_cache` to `auto_rev_ref`
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _MOM.import_MOM          import *
from   _FFM                     import FFM

from   _FFM.Attr_Type           import *
import _FFM.Net_Interface_in_IP_Network

_Ancestor_Essence = FFM.Net_Interface_in_IP_Network

class Net_Interface_in_IP4_Network (_Ancestor_Essence) :
    """Net interface in IPv4 network"""

    is_partial = True

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        ### Primary attributes

        class right (_Ancestor.right) :
            """IP Network."""

            role_type          = FFM.IP4_Network
            auto_rev_ref       = True

        # end class right

        ### Non-primary attributes

    # end class _Attributes

# end class Net_Interface_in_IP4_Network

if __name__ != "__main__" :
    FFM._Export ("*")
### __END__ FFM.Net_Interface_in_IP4_Network
