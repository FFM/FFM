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
#     4-Mar-2013 (CT) Move error checking to `find_closest_{address,mask}`
#     4-Mar-2013 (CT) Change `find_closest_mask` to use `Q.net_address.IN`,
#                     filter for `self.owner`
#     4-Mar-2013 (CT) Change `reserve` to check for `self.owner`
#     4-Mar-2013 (CT) Don't set `has_children` for `result` of `_reserve`
#     5-Mar-2013 (CT) Fix error condition in `reserve`
#                     (temporarily necessary as long as query attributes
#                     don't work)
#     5-Mar-2013 (CT) Add `electric`, fix predicate `owner_or_cool_down`
#     5-Mar-2013 (CT) Make `owner` argument of `reserve` optional
#    28-Apr-2013 (CT) Add attribute `desc`
#     8-May-2013 (CT) Set `pool.P_Type` to `FFM.IP_Network`
#     7-Aug-2013 (CT) Adapt to major surgery of GTW.OMP.NET.Attr_Type
#    13-Aug-2013 (CT) Adapt to major surgery of GTW.OMP.NET.Attr_Type some more
#     2-Apr-2014 (CT) Fix base class of `net_address`
#     2-Apr-2014 (CT) Change `pool.kind` to internal; pass `pool` in `split`
#     3-Apr-2014 (CT) Change `pool` to `parent`;
#                     change `has_children` to `Attr.Query`
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _MOM.import_MOM          import *
from   _FFM                     import FFM
from   _TFL.pyk                 import pyk

import _FFM.Error

from   _GTW._OMP._NET           import NET
from   _GTW._OMP._PAP           import PAP, Subject

import _GTW._OMP._NET.Attr_Type

_Ancestor_Essence = FFM.Object

class IP_Network (_Ancestor_Essence) :
    """IP Network of FFM"""

    is_partial = True

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        ### Primary attributes

        class net_address (NET._A_CIDR_) :
            """Network address."""

            kind               = Attr.Primary

        # end class net_address

        ### Non-primary attributes

        class desc (A_String) :
            """Description of and remarks about the IP_Network"""

            kind               = Attr.Optional
            max_length         = 80

        # end class desc

        class is_free (A_Boolean) :
            """Indicates whether this `%(type_name)s` can be assigned"""

            kind               = Attr.Query
            query              = Q.NOT \
                (Q.has_children | Q.cool_down | Q.net_interface_links)

        # end class is_free

        class cool_down (A_Date_Time) :
            """Cool down date after which the IP_Network is free to be
               reallocated.
            """

            kind               = Attr.Internal

        # end class cool_down

        class has_children (A_Boolean) :
            """Indicates whether this `%(type_name)s` is split into parts."""

            kind               = Attr.Query
            ### `~ ~ Q.subnets` converts to Boolean in a Python- and
            ### SQL-compatible way
            ### without boolification, using `has_children` as order-by
            ### criterion fails spectacularly because `SAW.QX` then expands
            ### the epk of IP_Network and SQL sucks at comparing NULLS
            query              = ~ ~ Q.subnets

        # end class has_children

        class owner (A_Id_Entity) :
            """Owner of the `%(type_name)s`."""

            kind               = Attr.Optional
            P_Type             = PAP.Subject

        # end class owner

        class parent (A_Id_Entity) :
            """Parent of the `%(type_name)s`."""

            kind               = Attr.Internal

        # end class parent

    # end class _Attributes

    class _Predicates (_Ancestor_Essence._Predicates) :

        _Ancestor = _Ancestor_Essence._Predicates

        class net_address_in_parent (Pred.Condition) :
            """The `net_address` must be contained in the `parent`."""

            kind               = Pred.Object
            assertion          = " and ".join \
                ( ( "net_address in parent.net_address"
                  , "net_address.mask_len == parent.net_address.mask_len + 1"
                  )
                )
            attributes         = \
                ( "net_address", "net_address.mask_len"
                , "parent.net_address", "parent.net_address.mask_len"
                )

        # end class net_address_in_parent

        class owner_or_cool_down (Pred.Condition) :
            """At most one of `owner` and `cool_down` can be defined at one
               time.
            """

            kind               = Pred.Region
            assertion          = "not (owner and cool_down)"
            attr_none          = ("owner", "cool_down")

        # end class owner_or_cool_down

    # end class _Predicates

    def allocate (self, mask_len, owner) :
        pool     = self.find_closest_mask   (mask_len)
        net_addr = pool.net_address.subnets (mask_len).next ()
        return self._reserve (pool, net_addr, owner)
    # end def allocate

    def find_closest_address (self, net_addr) :
        if net_addr in self.net_address :
            blocks = self.ETM.query \
                ( Q.net_address.CONTAINS (net_addr)
                , sort_key = TFL.Sorted_By ("-net_address.mask_len")
                )
            try :
                return TFL.first (blocks)
            except IndexError :
                pass
        msg = \
            ( "Address %s not in the address range [%s] of this %s"
            % (net_addr, self.net_address, self.ui_name)
            )
        raise FFM.Error.Address_not_in_Network \
            (self.net_address, net_addr, msg)
    # end def find_closest_address

    def find_closest_mask (self, mask_len) :
        blocks = self.ETM.query \
            ( Q.is_free
            , Q.owner == self.owner
            , Q.net_address.IN (self.net_address)
            , (  Q.net_address.mask_len <  mask_len)
            | ( (Q.net_address.mask_len == mask_len)
              &  Q.electric
              )
            , sort_key = TFL.Sorted_By ("-net_address.mask_len", "net_address")
            )
        try :
            return TFL.first (blocks)
        except IndexError :
            msg = \
                ( "Address range [%s] of this %s doesn't contain a "
                  "free subrange for mask length %s"
                % (self.net_address, self.ui_name, mask_len)
                )
            raise FFM.Error.No_Free_Address_Range \
                (self.net_address, mask_len, msg)
    # end def find_closest_mask

    def reserve (self, net_addr, owner = None) :
        if isinstance (net_addr, pyk.string_types) :
            net_addr = self.E_Type.attr_prop ("net_address").P_Type (net_addr)
        if owner is None :
            owner = self.owner
        pool = self.find_closest_address (net_addr)
        if not (   pool.is_free
               and pool.owner is self.owner
               and not pool.net_interface
               ) :
            msg = \
                ( "Address %s already in use by '%s'"
                % (net_addr, pool.FO.owner)
                )
            raise FFM.Error.Address_Already_Used \
                (net_addr, pool.FO.owner, str (owner.FO), msg)
        return self._reserve (pool, net_addr, owner)
    # end def reserve

    def split (self, pool) :
        ETM         = self.ETM
        net_address = self.net_address
        results     = list \
            (   ETM (sn, owner = self.owner, parent = self, electric = True)
            for sn in net_address.subnets (net_address.mask_len + 1)
            )
        return results
    # end def split

    def _reserve (self, pool, net_addr, owner) :
        result = pool
        while result.net_address != net_addr :
            p1, p2 = result.split (pool)
            if net_addr in p1.net_address :
                result, other = p1, p2
            else :
                other, result = p1, p2
        result.set (owner = owner, electric = False)
        return result
    # end def _reserve

# end class IP_Network

if __name__ != "__main__" :
    FFM._Export ("*")
### __END__ FFM.IP_Network
