# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012 Mag. Christian Tanzer All rights reserved
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
#    14-Dec-2012 (CT) Factor `User_Entities`
#    ««revision-date»»···
#--

from   __future__ import absolute_import, division, print_function, unicode_literals

from   _FFM                     import FFM
from   _GTW                     import GTW
from   _JNJ                     import JNJ
from   _MOM                     import MOM
from   _TFL                     import TFL

import _GTW._RST._TOP.import_TOP
import _GTW._RST._TOP._MOM.import_MOM

import _GTW._RST._TOP._MOM.Admin
import _GTW._RST._TOP._MOM.Admin_Restricted

from   _MOM.import_MOM          import Q

from   _TFL.Decorator           import getattr_safe
from   _TFL.I18N                import _, _T, _Tn

class Is_Owner_or_Manager (GTW.RST._Permission_) :
    """Permission if user is the owner or manager of the object"""

    def predicate (self, user, page, * args, ** kw) :
        if user :
            try :
                qf = page.query_filters_restricted ()
            except AttributeError :
                pass
            else :
                if qf is not None :
                    obj  = getattr (page, "obj", None)
                    node = getattr (obj, "belongs_to_node", None)
                    if node is not None :
                        return qf (node)
    # end def predicate

# end class Is_Owner_or_Manager

_Ancestor = GTW.RST.TOP.MOM.Admin_Restricted.E_Type

class User_Entities (_Ancestor) :
    """Directory displaying instances of one E_Type belonging to the current user."""

    child_permission_map  = dict \
        ( change          = Is_Owner_or_Manager
        , delete          = Is_Owner_or_Manager
        )
    restriction_desc      = _ ("owned/managed by")

    @property
    @getattr_safe
    def user_restriction (self) :
        user = self.top.user
        return user.person if user else None
    # end def user_restriction

    def query_filters_restricted (self) :
        person = self.user_restriction
        if person is not None :
            return \
                ( (Q.belongs_to_node.owner   == person)
                | (Q.belongs_to_node.manager == person)
                )
    # end def query_filters_restricted

# end class User_Entities

class User_Nodes (User_Entities) :
    """Directory displaying the node instances belonging to the current user."""

    @property
    @getattr_safe
    def form_parameters (self) :
        result = self.__super.form_parameters
        u = self.top.user
        if u and u.person :
            u = u.person
            if u :
                result.setdefault ("form_kw", {}).update \
                    ( manager = dict
                        ( prefilled   = True
                        , init        = u
                        )
                    )
        return result
    # end def form_parameters

    def query_filters_restricted (self) :
        person = self.user_restriction
        if person is not None :
            return (Q.owner == person) | (Q.manager == person)
    # end def query_filters_restricted

# end class User_Nodes

### __END__ RST_addons
