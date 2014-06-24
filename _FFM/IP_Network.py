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
#    13-Jun-2014 (RS) Rename `cool_down` to `expiration_date`
#                     Add ui_name for `desc`
#    14-Jun-2014 (RS) Add `node`
#    20-Jun-2014 (RS) Move `node` to `IP_Pool`
#    20-Jun-2014 (RS) Re-add `pool`
#    20-Jun-2014 (RS) Rename `owner_or_cool_down` to `owner_or_expiration`
#    23-Jun-2014 (RS) Implement `free` and `collect_garbage`, some fixes
#                     to pool allocation: need to keep correct pool on split
#    24-Jun-2014 (CT) Fix `ip_pool` query in `min_cooldown_period`
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _MOM.import_MOM          import *
from   _FFM                     import FFM
from   _TFL.pyk                 import pyk

import _FFM.Error

from   _GTW._OMP._NET           import NET
from   _GTW._OMP._PAP           import PAP, Subject

from   datetime                 import datetime

import _GTW._OMP._NET.Attr_Type

_Ancestor_Essence = FFM.Object

class IP_Network (_Ancestor_Essence) :
    """IP Network of FFM"""

    implementation_notes = \
    """
        Strategy of IP-Address reservation
        -----------------------------------

        Method ``allocate`` does *not* specify which ``IP_Network`` to
        get, it just returns the next free one. The method ``reserve``
        gets a specific ``IP_Network`` and succeeds if it is free. Both
        methods are called on a ``IP_Network`` which serves as a pool to
        allocate from.  On success, an allocation returns a new
        ``IP_Network`` object with the owner set to the person reserving
        the network.

        A network which is explicitly allocated (either by creating a
        new ``IP_Network`` from scratch or reserving one as outlined
        above) is a new pool from which new addresses can be allocated
        by calling its ``allocate`` or ``reserve`` method. Of course an
        ``IP_Network`` with the highest netmask (/32 for IPv4 or /128
        for IPv6) can not be used to allocate further addresses from.
        Trying to reserve/allocate from a pool will not find an
        ``IP_Network`` from a sub-pool.

        An ``IP_Network`` can be assigned to a ``Net_Interface`` by
        linking it. When linked it is said to be *in use*.

        After an allocated ``IP_Network`` has been in use for some time,
        it may not be immediately re-allocated. To prevent re-allocation
        for some time, an ``expiration_date`` attribute holds the time
        when the object can be reused.

        Thus ``IP_Network`` objects are free to be allocated if they
        don't have an allocated subnet, are not assigned to a
        ``Net_Interface``, and have an empty ``expiration_date``
        attribute. This is ensured by the ``is_free`` property.

        While allocating, ``IP_Network`` objects are split in two and
        create two successors with a netmask higher by one, each. These
        ``IP_Network`` objects are ``electric`` (as opposed to
        explicitly allocated objects). The two split objects have a
        ``parent`` pointer that holds the parent they were split from.

        The allocation strategy will not allocate explicitly reserved
        subnets of the given ``IP_Network`` nor subnets of an explicitly
        reserved subnet. Explicitly reserved subnets are not
        ``electric`` and can thus be distinguished from implicit
        reservations during reservation/allocation. The pool of a
        reserved/allocated ``IP_Network`` is the next enclosing
        ``IP_Network`` which is not ``electric``.
    """

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
            ui_name            = "Description"

        # end class desc

        class expiration_date (A_Date_Time) :
            """Cool down date after which the IP_Network is free to be
               reallocated.
            """

            kind               = Attr.Internal

        # end class expiration_date

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

        class is_free (A_Boolean) :
            """Indicates whether this `%(type_name)s` can be assigned"""

            kind               = Attr.Query
            query              = Q.NOT \
                (Q.has_children | Q.expiration_date | Q.net_interface_links)

        # end class is_free

        class owner (A_Id_Entity) :
            """Owner of the `%(type_name)s`."""

            kind               = Attr.Optional
            P_Type             = PAP.Subject

        # end class owner

        class parent (A_Id_Entity) :
            """Parent of the `%(type_name)s`."""

            kind               = Attr.Internal

        # end class parent

        class pool (A_Id_Entity) :
            """Pool to which this `%(type_name)s` belongs."""

            kind               = Attr.Optional
            Kind_Mixins        = (Attr.Computed_Set_Mixin, )
            ui_allow_new       = False

            def computed (self, obj) :
                """ Top-level IP_Networks have pool == self """
                if obj :
                    return obj
            # end def computed

        # end class pool

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

        class owner_or_expiration (Pred.Condition) :
            """At most one of `owner` and `expiration_date` can be
               defined at one time.
            """

            kind               = Pred.Region
            assertion          = "not (owner and expiration_date)"
            attr_none          = ("owner", "expiration_date")

        # end class owner_or_expiration

    # end class _Predicates

    def allocate (self, mask_len, owner) :
        # FIXME: Don't allocate if self is electric
        #        We need this when checking permissions on pools
        frm     = self.find_closest_mask   (mask_len)
        net_addr = frm.net_address.subnets (mask_len).next ()
        return self._reserve (self, frm, net_addr, owner)
    # end def allocate

    def collect_garbage (self) :
        """ First update expiration dates: All children of an expired
            Node must have an expiration date <= the parent. In addition
            check the cool_down_period of the pools: If a pool has a
            cool_down_period and now + cool_down_period is smaller than
            the expiration_date, we set the expiration_date to the
            smaller value. Biggest networks first, this recurses to
            smaller ones. A non-existent cool_down_period for one of the
            parent pools doesn't change the result. If we don't find
            *and* cool_down for any of the parent pools, 0 is asumed.

            After this first step, we loop over all now-free nodes with
            an expiration_date < now and free them.
        """
        now = datetime.now ()
        nw = self.ETM.query \
            ( Q.expiration_date
            , Q.net_address.IN (self.net_address)
            , sort_key = TFL.Sorted_By ("net_address.mask_len")
            )
        done = dict ()
        for n in nw :
            if n.net_address not in done :
                n._fix_expiration_date (now, done)

        # get free leaf nodes
        nw = self.ETM.query \
            ( Q.expiration_date != None
            , Q.expiration_date <= now
            , ~ Q.has_children
            , Q.net_address.IN (self.net_address)
            ).all ()
        for n in nw :
            n._collect_garbage (now)
    # end def collect_garbage

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
        if self.is_free and self.net_address.mask_len < mask_len :
            return self
        blocks = self.ETM.query \
            ( Q.is_free
            , Q.owner == self.owner
            , Q.pool == self
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

    def free (self, cool_down_period = None) :
        """ Mark this network as free for reuse, set the expiration date
            according to the pool's settings. If the pool has no
            settings, set expiration date to now.
            We allow override (but only with a *lower* delta) of the
            cool_down_period of the pool.
        """
        if self.pool == self or not self.pool :
            msg = "Cannot free toplevel network %s" % self.net_address
            raise FFM.Error.Cannot_Free_Network (self.net_address, msg)
        now = datetime.now ()
        # check if there are leaf-nodes (without self)
        # which are non-electric and have an owner
        allocated_children = self.ETM.query \
            ( Q.net_address.IN (self.net_address)
            , ~ Q.has_children
            , Q.net_address.mask_len > self.net_address.mask_len
            , Q.owner
            , ~ Q.electric
            ).first ()
        if allocated_children :
            net = self.net_address
            msg = "Cannot free network with allocations: %s" % net
            raise FFM.Error.Cannot_Free_Network (self.net_address, msg)
        cooldown   = self.min_cooldown_period (cool_down_period)
        # If no cool_down_period is found, expire now
        expiration = now
        if cooldown is not None :
            expiration += cooldown
        self.set (expiration_date = expiration, owner = None)
    # end def free

    def min_cooldown_period (self, cool_down_period = None) :
        """ Get minimum cool_down_period of self and all parents.
            Note: We only find parents which have an IP_Pool. If an
            intermediate network doesn't define an IP_Pool or the
            IP_Pool doesn't define the cool_down_period it inherits the
            settings of its parent pool.
            Additionally an initial cool_down_period may be specified.
        """
        cooldown = cool_down_period
        nw = self.ETM.query \
            ( Q.net_address.CONTAINS (self.pool.net_address)
            , Q.ip_pool != None
            , Q.ip_pool.cool_down_period != None
            )
        minpool = None
        for n in nw :
            cd = n.ip_pool.cool_down_period
            if cd is not None :
                if minpool is None or cd < minpool.cool_down_period :
                    minpool = n.ip_pool

        IPP_ETM = self.home_scope [self.ETM.ip_pool.P_Type]
        minpool = IPP_ETM.query \
            ( Q.ip_network.net_address.CONTAINS (self.pool.net_address)
            , Q.cool_down_period != None
            , sort_key = TFL.Sorted_By ("cool_down_period")
            ).first ()

        if minpool is not None :
            if cooldown is None or minpool.cool_down_period < cooldown :
                cooldown = minpool.cool_down_period
        return cooldown
    # end def min_cooldown_period

    def reserve (self, net_addr, owner = None) :
        # FIXME: Don't reserve if self is electric
        #        We need this when checking permissions on pools
        if isinstance (net_addr, pyk.string_types) :
            net_addr = self.E_Type.attr_prop ("net_address").P_Type (net_addr)
        if owner is None :
            owner = self.owner
        frm = self.find_closest_address (net_addr)
        if not (   frm.is_free
               and frm.owner is self.owner
               and not frm.net_interface
               ) :
            msg = \
                ( "Address %s already in use by '%s'"
                % (net_addr, frm.FO.owner)
                )
            raise FFM.Error.Address_Already_Used \
                (net_addr, frm.FO.owner, str (owner.FO), msg)
        return self._reserve (self, frm, net_addr, owner)
    # end def reserve

    def split (self, pool) :
        ETM         = self.ETM
        net_address = self.net_address
        results     = list \
            (ETM ( sn
                 , pool     = pool
                 , owner    = self.owner
                 , parent   = self
                 , electric = True
                 )
            for sn in net_address.subnets (net_address.mask_len + 1)
            )
        return results
    # end def split

    def _collect_garbage (self, now) :
        parent  = self.parent
        if parent is None :
            return
        sibling = self.ETM.query \
            ( Q.parent == self.parent
            , Q.pid != self.pid
            ).first ()
        assert parent.electric or self.pool == parent
        if sibling :
            if  (sibling.has_children or not sibling.electric) :
                self.set \
                    ( owner = self.pool.owner
                    , electric = True
                    , expiration_date = None
                    )
                return
            parent.set (owner = self.parent.pool.owner)
            sibling.destroy ()
        self.destroy ()
        parent._collect_garbage (now)
    # end def _collect_garbage

    def _fix_expiration_date (self, now, done, date = None, cooldown = None) :
        assert self.expiration_date is not None
        done [self.net_address] = 1
        if cooldown is None :
            cooldown = self.min_cooldown_period ()
        elif self.ip_pool and self.ip_pool.cool_down_period is not None :
            if self.ip_pool.cool_down_period < cooldown :
                cooldown = self.ip_pool.cool_down_period
        if date is None or date > self.expiration_date :
            date = self.expiration_date
        if cooldown is not None and now + cooldown < date :
            date = now + cooldown
        if date < self.expiration_date :
            self.set (expiration_date = date)
        for n in self.subnets :
            if not n.electric :
                n._fix_expiration_date (now, done, date, cooldown)
    # end def _fix_expiration_date

    def _reserve (self, pool, frm, net_addr, owner) :
        result = frm
        while result.net_address != net_addr :
            p1, p2 = result.split (frm)
            if net_addr in p1.net_address :
                result, other = p1, p2
            else :
                other, result = p1, p2
            other.set  (pool = pool)
        result.set (pool = pool, owner = owner, electric = False)
        return result
    # end def _reserve

# end class IP_Network

if __name__ != "__main__" :
    FFM._Export ("*")
### __END__ FFM.IP_Network
