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
#    27-Feb-2013 (CT) Remove `free.auto_up_depends`
#    27-Feb-2013 (CT) Add allocation methods, attribute `has_children`
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _MOM.import_MOM          import *
from   _FFM                     import FFM

import _FFM.Error

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

        class is_free (A_Boolean) :
            """Indicates whether this `%(type_name)s` can be assigned"""

            kind               = Attr.Query
            query              = \
                ( (Q.has_children  == False)
                &  (Q.cool_down     == None)
                #& (Q.net_interface == None) ### XXX
                )

        # end class is_free

        class cool_down (A_Date_Time) :
            """Cool down date after which the IP_Network is free to be
               reallocated.
            """

            kind               = Attr.Internal

        # end class cool_down

        class has_children (A_Boolean) :
            """Indicates whether this `%(type_name)s` is split into parts."""

            ### XXX should be Attr.Query if it only worked
            kind               = Attr.Internal
            default            = False

        # end class has_children

        class owner (A_Id_Entity) :
            """Owner of the `%(type_name)s`."""

            kind               = Attr.Optional
            P_Type             = PAP.Subject

        # end class owner

        class pool (A_Id_Entity) :
            """Pool the `%(type_name)s` belongs to."""

            kind               = Attr.Optional

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

    def allocate (self, mask_len, owner) :
        pool = self.find_closest_mask (mask_len)
        if pool is None :
            msg = \
                ( "Address range [%s] of this %s doesn't contain a "
                  "free subrange for mask length %s"
                % (self.net_address, self.ui_name, mask_len)
                )
            raise FFM.Error.No_Free_Address_Range \
                (self.net_address, mask_len, msg)
        result = pool
        ETM    = self.ETM
        E_Type = self.E_Type
        E_Type.net_address.P_Type (pool)
        net_addr = E_Type.net_address.P_Type \
            (pool.net_address.address.subnets (mask_len).next ())
        return self._reserve (pool, net_addr, owner)
    # end def allocate

    def find_closest_address (self, net_addr) :
        if net_addr in self.net_address :
            result = self.ETM.query \
                ( Q.net_address.CONTAINS (net_addr)
                , sort_key = TFL.Sorted_By ("-net_address.mask_len")
                ).first ()
            return result
    # end def find_closest_address

    def find_closest_mask (self, mask_len) :
        blocks = self.ETM.query \
            ( ### XXX factor `is_free` once query attributes work properly
              (Q.has_children  == False)
            & (Q.cool_down     == None)
            & (Q.net_address.mask_len <= mask_len)
            & (Q.net_address.CONTAINS (self.net_address))
            , sort_key = TFL.Sorted_By ("-net_address.mask_len")
            )
        for b in blocks :
            if b.net_interface is None :
                return b
    # end def find_closest_mask

    def reserve (self, net_addr, owner) :
        pool = self.find_closest_address (net_addr)
        if pool is None :
            msg = \
                ( "Address %s not in the address range [%s] of this %s"
                % (net_addr, self.net_address, self.ui_name)
                )
            raise FFM.Error.Address_not_in_Network \
                (self.net_address, net_addr, msg)
        if not pool.is_free :
            msg = \
                ( "Address %s already in use by '%s'"
                % (net_addr, pool.FO.owner)
                )
            raise FFM.Error.Address_Already_Used \
                (net_addr, pool.FO.owner, str (owner.FO), msg)
        return self._reserve (pool, net_addr, owner)
    # end def reserve

    def split (self) :
        ETM         = self.ETM
        E_Type      = self.E_Type
        net_address = self.net_address
        results     = []
        for sn in net_address.address.subnets (net_address.mask_len + 1) :
            sn_addr = E_Type.net_address.P_Type (sn)
            results.append (ETM (sn_addr, owner = self.owner))
        self.has_children = True
        return results
    # end def split

    def _reserve (self, pool, net_addr, owner) :
        result = pool
        while result.net_address != net_addr :
            p1, p2 = result.split ()
            if net_addr in p1.net_address :
                result, other = p1, p2
            else :
                other, result = p1, p2
        result.set (owner = owner, has_children = True)
        return result
    # end def _reserve

# end class IP_Network

if __name__ != "__main__" :
    FFM._Export ("*")
### __END__ FFM.IP_Network
