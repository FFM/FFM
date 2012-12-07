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

import _JNJ.Templateer

from   _MOM.import_MOM          import Q

from   _TFL.Decorator           import getattr_safe
from   _TFL.I18N                import _, _T, _Tn

JNJ.Template ("user_nodes_admin", "html/user_nodes_admin.jnj")

_Ancestor = GTW.RST.TOP.MOM.Admin.E_Type

class _User_Node_Changer_ (_Ancestor.Changer) :

    _real_name = "Changer"

    def allow_method (self, method, user) :
        return self.user_has_permission (user)
    # end def allow_method

    def user_has_permission (self, user) :
        person = user.person if user else None
        if self.obj and person is not None :
            return ((Q.owner == person) | (Q.manager == person)) (self.obj)
    # end def user_has_permission

Changer = _User_Node_Changer_ # end class

class User_Nodes (_Ancestor) :
    """Directory displaying the node instances belonging to the current user."""

    Changer               = Changer
    dir_template_name     = "user_nodes_admin"
    dont_et_map           = True
    skip_etag             = True

    _entry_type_map       = dict \
        ( _Ancestor._entry_type_map
        , ** {Changer.name : Changer}
        )

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

    @property
    @getattr_safe
    def head_line (self) :
        result = self.__super.head_line
        u = self.top.user
        if u and u.person :
            u = u.person
        if u :
            u = u.FO
            result = "%s: owned/managed by %s" % (result, u)
        return result
    # end def head_line

    @property
    @getattr_safe
    def query_filters_d (self) :
        user   = self.top.user
        person = user.person if user else None
        if person is not None :
            result = (Q.owner == person) | (Q.manager == person)
        else :
            result = (Q.pid == 0) ### don't show any entries
        return (result, ) + self.__super.query_filters_d
    # end def query_filters_d

    @property
    @getattr_safe
    def _change_info_key (self) :
        user = self.top.user
        pid  = user.pid if user else None
        return self.__super._change_info_key, pid
    # end def _change_info_key

# end class User_Nodes

### __END__ RST_addons
