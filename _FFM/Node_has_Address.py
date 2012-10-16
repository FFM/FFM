# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package FFM.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# ****************************************************************************
#
#++
# Name
#    GTW.OMP.PAP.Node_has_Address
#
# Purpose
#    Model the link between a Node and an Address:
#    allow only one Address per Node
#
# Revision Dates
#    12-Oct-2012 (RS) Creation
#    ««revision-date»»···
#--

from   __future__            import unicode_literals

from   _MOM.import_MOM        import *
from   _GTW                   import GTW
from   _FFM                   import FFM
from   _GTW._OMP._PAP         import PAP
from   _TFL.I18N              import _

from   _GTW._OMP._PAP.Subject_has_Property   import Subject_has_Property
from   _GTW._OMP._PAP.Address                import Address
from   _FFM                                  import Node

_Ancestor_Essence = Subject_has_Property

class Node_has_Address (_Ancestor_Essence) :
    """Link a Node to an address"""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class left (_Ancestor.left) :

            role_type       = FFM.Node
            max_links       = 1

        # end class left

        class right (_Ancestor.right) :
            """Address of %(left.role_name)s"""

            role_type = PAP.Address

        # end class right

    # end class _Attributes

# end class Node_has_Address

if __name__ != "__main__" :
    GTW.OMP.PAP._Export ("*")
### __END__ FFM.Node_has_Address
