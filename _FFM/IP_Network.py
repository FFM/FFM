# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012 Dr. Ralf Schlatterbeck All rights reserved
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
#    FFM.IP_Network
#
# Purpose
#    Model network interfaces in FFM
#
# Revision Dates
#    18-May-2012 (RS) Creation
#    22-May-2012 (RS) Add `net_mask`
#    23-May-2012 (RS) Use `_A_IP_Address_` for `net_address`
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _MOM.import_MOM          import *
from   _FFM                     import FFM

from   _GTW._OMP._NET.Attr_Type import *

_Ancestor_Essence = FFM.Object

class IP_Network (_Ancestor_Essence) :
    """IP Network of FFM"""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        ### Primary attributes

        class net_address (_A_IP_Address_) :
            """Network address."""

            kind               = Attr.Primary

        # end class net_address

        ### Non-primary attributes

        class net_mask (A_Int) :
            """Network mask."""

            kind               = Attr.Internal
            auto_up_depends    = ("net_address",)
            min_value          = 0
            max_value          = 128

            def computed (self, obj) :
                if obj and '/' in obj.net_address :
                    return int (obj.net_address.split ('/') [-1])
                return self.max_value
            # end def computed

        # end class net_mask

    # end class _Attributes

# end class IP_Network

if __name__ != "__main__" :
    FFM._Export ("*")
### __END__ FFM.IP_Network
