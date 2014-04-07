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
#    FFM.Regulatory_Domain
#
# Purpose
#    Model a wireless regulatory domain
#
# Revision Dates
#    20-Aug-2012 (RS) Creation
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _MOM.import_MOM        import *
from   _FFM                   import FFM

import _FFM.Entity

_Ancestor_Essence = FFM.Object

class Regulatory_Domain (_Ancestor_Essence) :
    """Wireless Regulatory Domain"""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class countrycode (A_String) :
            """Two-letter country-code"""

            kind               = Attr.Primary
            max_length         = 2
            ignore_case        = True

        # end class countrycode

    # end class _Attributes

# end class Regulatory_Domain

if __name__ != "__main__" :
    FFM._Export ("*")
### __END__ FFM.Regulatory_Domain
