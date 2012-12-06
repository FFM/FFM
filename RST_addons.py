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

class User_Nodes (GTW.RST.TOP.MOM.Admin.E_Type) :
    """Directory displaying the node instances belonging to the current user."""

    dir_template_name     = "user_nodes_admin"
    user                  = None

    @property
    @getattr_safe
    def head_line (self) :
        u = self.user
        if u and u.person :
            u = u.person
        if u :
            u = u.FO
        return "%s owned/managed by %s" % \
            (_T (self.ETM.E_Type.ui_name), u)
    # end def head_line

    def query (self, sort_key = None) :
        result = self.__super.query (sort_key = sort_key)
        if self.user is not None :
            person = self.user.person
            if person is not None :
                qf = (Q.owner == person) | (Q.manager == person)
                result = result.filter (qf)
        return result
    # end def query

# end class User_Nodes

### __END__ RST_addons
