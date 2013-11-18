# -*- coding: utf-8 -*-
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
#    FFM.Person_mentors_Person
#
# Purpose
#    Model mentor relationship between persons
#
# Revision Dates
#    12-Sep-2012 (RS) Creation
#    13-Sep-2012 (RS) Mentored person is `apprentice`
#    19-Sep-2012 (CT) Derive `right` from `_Ancestor.right`, not `.left`
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _MOM.import_MOM        import *
from   _FFM                   import FFM
from   _GTW._OMP._PAP         import PAP

import _GTW._OMP._PAP.Person
import _FFM.Entity

_Ancestor_Essence = FFM.Link2

class Person_mentors_Person (_Ancestor_Essence) :
    """Person is the mentor of another person."""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        ### Primary attributes

        class left (_Ancestor.left) :
            """The Person mentoring another person."""

            role_type          = PAP.Person
            role_name          = "mentor"

        # end class left

        class right (_Ancestor.right) :
            """The Person being mentored."""

            role_type          = PAP.Person
            role_name          = "apprentice"

        # end class right

    # end class _Attributes

# end class Person_mentors_Person

if __name__ != "__main__" :
    FFM._Export ("*")
### __END__ FFM.Person_mentors_Person
