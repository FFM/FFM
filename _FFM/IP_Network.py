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
#    FFM.IP_Network
#
# Purpose
#    Model network interfaces in FFM
#
# Revision Dates
#    18-May-2012 (RS) Creation
#    22-May-2012 (RS) Add `net_mask`
#    23-May-2012 (RS) Use `_A_IP_Address_` for `net_address`
#    13-Aug-2012 (RS) Make `IP_Network.net_address` descendant of
#                     `_A_Composite_IP_Address_`, remove `net_mask`,
#                     set is_partial
#    26-Jan-2013 (CT) Add `pool`, `owner`, `free`, and `cool_down`
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _MOM.import_MOM          import *
from   _FFM                     import FFM

from   _GTW._OMP._NET.Attr_Type import *
from   _GTW._OMP._PAP           import PAP, Subject

_Ancestor_Essence = FFM.Object

class IP_Network (_Ancestor_Essence) :
    """IP Network of FFM"""

    is_partial = True

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        ### Primary attributes

        class net_address (_A_Composite_IP_Address_) :
            """Network address."""

            kind               = Attr.Primary

        # end class net_address

        ### Non-primary attributes

        class free (A_Boolean) :
            """Indicates whether this `%(type_name)s` can be assigned"""

            kind               = Attr.Query
            auto_up_depends    = ("cool_down", "owner")
            query              = (Q.owner == None) & (Q.cool_down == None)

        # end class free

        class cool_down (A_Date_Time) :
            """Cool down date after which the IP_Network is free to be
               reallocated.
            """

            kind               = Attr.Internal

        # end class cool_down

        class owner (A_Id_Entity) :
            """Owner of the `%(type_name)s`."""

            kind               = Attr.Optional
            P_Type             = PAP.Subject

        # end class owner

        class pool (A_Id_Entity) :
            """Pool the `%(type_name)s` belongs to."""

            kind               = Attr.Optional

            check              = \
                ( "(pool is None) or isinstance (self, pool.E_Type)"
                ,
                )

        # end class pool

    # end class _Attributes

    class _Predicates (_Ancestor_Essence._Predicates) :

        _Ancestor = _Ancestor_Essence._Predicates

        class net_address_in_pool (Pred.Condition) :
            """The `net_address` must be contained in the `pool`."""

            kind               = Pred.Object
            assertion          = "net_address in pool.net_address"
            attributes         = ("net_address", "pool.net_address")

        # end class net_address_in_pool

        class owner_or_cool_down (Pred.Region) :
            """At most one of `owner` and `cool_down` can be defined at one
               time.
            """

            kind               = Pred.Object
            assertion          = "not (owner and cool_down)"
            attr_none          = ("owner", "cool_down")

        # end class owner_or_cool_down

    # end class _Predicates

# end class IP_Network

#IP_Network._Attributes.pool.P_Type = IP_Network

if __name__ != "__main__" :
    FFM._Export ("*")
### __END__ FFM.IP_Network
