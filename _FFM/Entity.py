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
#    FFM.Entity
#
# Purpose
#    Common base class for essential classes of FFM
#
# Revision Dates
#     6-Mar-2012 (CT) Creation
#    10-May-2012 (CT) Add `An_Entity`, `Id_Entity`, `Object`, `Link1`, `Link2`
#    17-May-2012 (CT) Fix typo (`Common`, not `Command`)
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _MOM.import_MOM        import *
from   _FFM                   import FFM

_Ancestor_Essence = MOM.Entity

class _FFM_Entity_ (_Ancestor_Essence) :
    """Common base class for essential classes of FFM"""

    _real_name = "Entity"
    is_partial = True
    PNS        = FFM

Entity = _FFM_Entity_ # end class

_Ancestor_Essence = MOM.An_Entity

class _FFM_An_Entity_ (Entity, _Ancestor_Essence) :
    """Common base class for essential classes of FFM"""

    _real_name = "An_Entity"
    is_partial = True

An_Entity = _FFM_An_Entity_ # end class

_Ancestor_Essence = MOM.Id_Entity

class _FFM_Id_Entity_ (Entity, _Ancestor_Essence) :
    """Common base class for essential classes of FFM"""

    _real_name = "Id_Entity"
    is_partial = True

Id_Entity = _FFM_Id_Entity_ # end class

_Ancestor_Essence = MOM.Object

class _FFM_Object_ (Entity, _Ancestor_Essence) :
    """Common base class for essential object classes of FFM."""

    _real_name = "Object"
    is_partial = True

Object = _FFM_Object_ # end class

_Ancestor_Essence = MOM.Link1

class _FFM_Link1_ (Entity, _Ancestor_Essence) :
    """Common base class for essential unary link classes of FFM."""

    _real_name = "Link1"
    is_partial = True

Link1 = _FFM_Link1_ # end class

_Ancestor_Essence = MOM.Link2

class _FFM_Link2_ (Entity, _Ancestor_Essence) :
    """Common base class for essential binary link classes of FFM."""

    _real_name = "Link2"
    is_partial = True

Link2 = _FFM_Link2_ # end class

if __name__ != "__main__" :
    FFM._Export ("*")
### __END__ FFM.Entity
