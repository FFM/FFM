# -*- coding: utf-8 -*-
# Copyright (C) 2013 Mag. Christian Tanzer All rights reserved
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
#    FFM.RST_Api_addons
#
# Purpose
#    Define RESTful resource for FFM-Net_Interface and its descendents
#
# Revision Dates
#    20-May-2013 (CT) Creation
#    ««revision-date»»···
#--

from   __future__ import absolute_import, division, print_function, unicode_literals

from   _FFM                     import FFM
from   _GTW                     import GTW
from   _MOM                     import MOM
from   _TFL                     import TFL

import _FFM.import_FFM

import _GTW._RST._MOM.Role_Bound_Links

from   _MOM.import_MOM          import Q

from   _TFL._Meta.Once_Property import Once_Property
from   _TFL.Decorator           import getattr_safe
from   _TFL.I18N                import _, _T, _Tn

_Ancestor = GTW.RST.MOM.Role_Bound_Links

class RBL_NI (_Ancestor) :
    """RESTful resource for role-bound links of `Net_Interface` to `IP_Network`"""

    class RBL_NI_POST (_Ancestor.POST) :

        _real_name                 = "POST"

        def _apply_attrs (self, resource, request, response, attrs) :
            obj   = resource.obj
            rr    = resource.E_Type.right
            scope = resource.scope
            user  = resource.top.user
            for name in rr.name, rr.role_name :
                if name in attrs :
                    raise ValueError \
                        ("Cannot set %s value to %s" % (name, attrs [name]))
            owner = user.person if user else None
            R_ETM = scope [rr.E_Type]
            pool  = R_ETM.query (is_free = True) ### XXX how to find right pool???
            attrs [rr.name] = pool.allocate (resource.mask_len, owner)
            return self.__super._apply_attrs \
                (resource, request, response, attrs)
        # end def _apply_attrs

    POST = RBL_NI_POST # end class

# end class RBL_NI

class RBL_NI_4 (RBL_NI) :
    """RBL_NI for IP4_Network"""

    mask_len = 32

# end class RBL_NI_4

class RBL_NI_6 (RBL_NI) :
    """RBL_NI for IP6_Network"""

    mask_len = 64 ### XXX ???

# end class RBL_NI_6

FFM.Net_Interface.GTW.rst_mom_rbl_spec = dict \
    ( ip4_network_links = RBL_NI_4
    , ip6_network_links = RBL_NI_6
    )

if __name__ != "__main__" :
    FFM._Export ("*")
### __END__ FFM.RST_Api_addons
