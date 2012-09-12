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
#    FFM.Nickname
#
# Purpose
#    Model nickname of a person in FFM.
#
# Revision Dates
#    12-Sep-2012 (RS) Creation
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _MOM.import_MOM        import *
from   _FFM                   import FFM
from   _GTW._OMP._PAP         import PAP

import _GTW._OMP._PAP.Person
import _FFM.Entity

_Ancestor_Essence = FFM.Link1

class Nickname (_Ancestor_Essence) :
    """Nickname of a person in FFM"""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        ### Primary attributes

        class left (_Ancestor.left) :
            """The Person to which the nickname belongs."""

            role_type          = PAP.Person
            role_name          = "person"
            auto_cache         = "nicknames"

        # end class left

        class name (A_String) :
            """The nickname."""

            kind               = Attr.Primary

        # end class left

    # end class _Attributes

# end class Nickname

if __name__ != "__main__" :
    FFM._Export ("*")
### __END__ FFM.Nickname
