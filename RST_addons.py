# -*- coding: utf-8 -*-
# Copyright (C) 2012-2014 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
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
#    RST_addons
#
# Purpose
#    Addons for GTW.RST...
#
# Revision Dates
#     6-Dec-2012 (CT) Creation
#     7-Dec-2012 (CT) Continue creation
#    14-Dec-2012 (CT) Factor `Is_Owner_or_Manager`, set `child_permission_map`
#    14-Dec-2012 (CT) Factor `GTW.RST.TOP.MOM.Admin_Restricted`
#    14-Dec-2012 (CT) Factor `User_Entity`
#    17-Dec-2012 (CT) Add `User_Node_Dependent` and descendents
#    24-Apr-2013 (CT) Fix `Is_Owner_or_Manager.predicate`
#    25-Apr-2013 (CT) Add `eligible_objects`, `child_postconditions_map`,
#                     `_pre_commit_entity_check`
#    25-Apr-2013 (CT) Add `eligible_object_restriction`
#    28-Apr-2013 (CT) DRY `User_Node.form_parameters`
#    28-Apr-2013 (CT) Add `Login_has_Person`
#    30-Apr-2013 (CT) Add `Node_Manager_Error`, `_pre_commit_node_check`
#    30-Apr-2013 (CT) Remove `prefilled` from `User_Node.form_parameters` for
#                     `manager`
#     7-Oct-2013 (CT) Simplify `Is_Owner_or_Manager.predicate`
#                     * `belongs_to_node` works now
#                     * remove redefinitions of `query_filters_restricted`
#     7-Oct-2013 (CT) Add `User_Antenna`
#    14-Apr-2014 (CT) Rename `belongs_to_node` to `my_node`
#    ««revision-date»»···
#--

from   __future__ import absolute_import, division, print_function, unicode_literals

from   _FFM                     import FFM
from   _GTW                     import GTW
from   _JNJ                     import JNJ
from   _MOM                     import MOM
from   _TFL                     import TFL

import _FFM.import_FFM

import _GTW._RST._TOP.import_TOP
import _GTW._RST._TOP._MOM.import_MOM

import _GTW._RST._TOP._MOM.Admin
import _GTW._RST._TOP._MOM.Admin_Restricted

from   _MOM.import_MOM          import Q

from   _TFL._Meta.Once_Property import Once_Property
from   _TFL.Decorator           import getattr_safe, Add_New_Method
from   _TFL.I18N                import _, _T, _Tn

class Node_Manager_Error (MOM.Error._Invariant_, TypeError) :
    """You are not allowed to change owner or manager unless after the change
       you are still either owner or manager
    """

    class inv :
        name       = "Node_Manager_Error"

    def __init__ (self, obj, changed, user) :
        self.__super.__init__ (obj)
        self.obj          = obj
        self.changed      = tuple \
            ((c, getattr (obj.E_Type, c).ui_name_T) for c in changed)
        self.user         = user
        self.attributes   = ("manager", "owner")
        self.values = vs  = tuple \
            (  (v.ui_display if v is not None else v)
            for v in (getattr (obj, k) for k in self.attributes)
            )
        self.args         = (obj, changed, vs, user)
    # end def __init__

    @Once_Property
    def as_unicode (self) :
        bindings = dict (self.bindings)
        result = \
            ( _T( "You are not allowed to change %s unless afterwards "
                  "you [%s] are still either manager or owner"
                )
            % ( _T (" and ").join
                  ( "'%s' %s '%s'"
                  % (d, _T ("to"), bindings [k]) for k, d in self.changed
                  )
              , self.user
              )
            )
        return result
    # end def as_unicode

    @Once_Property
    def bindings (self) :
        return zip (self.attributes, self.values)
    # end def bindings

    @Once_Property
    def head (self) :
        return unicode (self)
    # end def head

# end class Node_Manager_Error

class Is_Owner_or_Manager (GTW.RST._Permission_) :
    """Permission if user is the owner or manager of the object"""

    def predicate (self, user, page, * args, ** kw) :
        if user :
            obj = getattr (page, "obj", None)
            if obj is not None :
                try :
                    qf = page.query_filters_restricted ()
                except AttributeError :
                    pass
                else :
                    if qf is not None :
                        return qf (obj)
    # end def predicate

# end class Is_Owner_or_Manager

class Login_has_Person (GTW.RST._Permission_) :
    """Permission if user has an associated person"""

    def predicate (self, user, page, * args, ** kw) :
        if user :
            return user.person is not None
    # end def predicate

# end class Login_has_Person

@Add_New_Method (FFM.Net_Device, FFM.Wired_Interface, FFM.Wireless_Interface)
def _FFM_User_Entity_PRC (self, resource, request, response, attribute_changes) :
    for eia in self.id_entity_attr :
        if eia.name in attribute_changes or eia.is_primary :
            ET = eia.E_Type
            eligible = resource.eligible_objects (ET.type_name)
            if eligible is not None :
                ent = getattr (self, eia.name)
                if ent not in eligible :
                    err = MOM.Error.Permission (self, eia, ent, eligible)
                    self.add_error (err)
                    raise err
# end def _FFM_User_Entity_PRC

_pre_commit_entity_check = GTW.RST.MOM.Pre_Commit_Entity_Check \
    ("_FFM_User_Entity_PRC")

@Add_New_Method (FFM.Node)
def _FFM_Node_PRC (self, resource, request, response, attribute_changes) :
    changed = tuple (k for k in ("manager", "owner") if k in attribute_changes)
    if changed :
        user = resource.user_restriction
        if not (self.manager is user or self.owner is user) :
            err = Node_Manager_Error (self, changed, user.ui_display)
            self.add_error (err)
            raise err
# end def _FFM_Node_PRC

_pre_commit_node_check = GTW.RST.MOM.Pre_Commit_Entity_Check \
    ("_FFM_Node_PRC")

_Ancestor = GTW.RST.TOP.MOM.Admin_Restricted.E_Type

class User_Entity (_Ancestor) :
    """Directory displaying instances of one E_Type belonging to the current user."""

    child_permission_map      = dict \
        ( change              = Is_Owner_or_Manager
        , delete              = Is_Owner_or_Manager
        )
    child_postconditions_map  = dict \
        ( create              = (_pre_commit_entity_check, )
        , change              = (_pre_commit_entity_check, )
        )
    et_map_name               = "admin_noom"
    restriction_desc          = _ ("owned/managed by")

    def __init__ (self, ** kw) :
        app_type = self.top.App_Type
        ET_Map   = self.top.ET_Map
        ETM      = kw.pop ("ETM", None) or self._ETM
        pns, etm = ETM.split (".")
        PNS      = app_type.PNS_Map [pns]
        Nav      = getattr (getattr (PNS, "Nav", None), "Admin", None)
        xkw      = dict (getattr (Nav, etm, {}), ETM = ETM, ** kw)
        self.__super.__init__ (** xkw)
    # end def __init__

    @property
    @getattr_safe
    def user_restriction (self) :
        user = self.top.user
        return user.person if user else None
    # end def user_restriction

    def eligible_objects (self, type_name) :
        etn = getattr (type_name, "type_name", type_name)
        adm = getattr (self.ET_Map.get (etn), self.et_map_name, None)
        if adm is not None :
            return adm.objects
    # end def eligible_objects

    def eligible_object_restriction (self, type_name) :
        etn = getattr (type_name, "type_name", type_name)
        adm = getattr (self.ET_Map.get (etn), self.et_map_name, None)
        if adm is not None :
            return adm.query_filters_restricted ()
    # end def eligible_object_restriction

    def query_filters_restricted (self) :
        person = self.user_restriction
        if person is not None :
            return \
                ( (Q.my_node.owner   == person)
                | (Q.my_node.manager == person)
                )
    # end def query_filters_restricted

# end class User_Entity

class User_Node (User_Entity) :
    """Directory displaying the node instances belonging to the current user."""

    _ETM                  = "FFM.Node"

    child_postconditions_map  = dict \
        ( User_Entity.child_postconditions_map
        , change = (_pre_commit_node_check, _pre_commit_entity_check)
        )

    @property
    @getattr_safe
    def form_parameters (self) :
        result = self.__super.form_parameters
        u = self.user_restriction
        if u is not None :
            result.setdefault ("form_kw", {}).update \
                (manager = dict (init = u))
        return result
    # end def form_parameters

# end class User_Node

class User_Node_Dependent (User_Entity) :
    """Temporary until query attributes with chained Q expressions work"""

    ET_depends            = "FFM.Node" ### E_Type we depend on

    @Once_Property
    @getattr_safe
    def change_query_filters (self) :
        result = self.__super.change_query_filters [0]
        ETd    = getattr \
            (self.top.ET_Map [self.ET_depends], self.et_map_name, None)
        if ETd is not None :
            result = result | ETd.change_query_filters [0]
        return (result, )
    # end def change_query_filters

# end class User_Node_Dependent

class User_Antenna (User_Node_Dependent) :

    ET_depends            = "FFM.Wireless_Interface_uses_Antenna"
    _ETM                  = "FFM.Antenna"

# end class User_Antenna

class User_Net_Device (User_Node_Dependent) :

    _ETM                  = "FFM.Net_Device"

    @property
    @getattr_safe
    def form_parameters (self) :
        result = self.__super.form_parameters
        u = self.top.user
        if u and u.person :
            u = u.person
            if u :
                result.setdefault ("form_kw", {}).update \
                    ( node = dict
                        ( manager = dict
                            ( prefilled   = True
                            , init        = u
                            )
                        )
                    )
        return result
    # end def form_parameters

# end class User_Net_Device

class User_Wired_Interface (User_Node_Dependent) :

    ET_depends            = "FFM.Net_Device"
    _ETM                  = "FFM.Wired_Interface"

# end class User_Wired_Interface

class User_Wireless_Interface (User_Node_Dependent) :

    ET_depends            = "FFM.Net_Device"
    _ETM                  = "FFM.Wireless_Interface"

# end class User_Wireless_Interface

class User_Wireless_Interface_uses_Antenna (User_Node_Dependent) :

    ET_depends            = "FFM.Wireless_Interface"
    _ETM                  = "FFM.Wireless_Interface_uses_Antenna"

# end class User_Wireless_Interface_uses_Antenna

class User_Wireless_Interface_uses_Wireless_Channel (User_Node_Dependent) :

    ET_depends            = "FFM.Wireless_Interface"
    _ETM                  = "FFM.Wireless_Interface_uses_Wireless_Channel"

# end class User_Wireless_Interface_uses_Wireless_Channel

### __END__ RST_addons
