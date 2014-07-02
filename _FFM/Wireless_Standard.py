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
#    FFM.Wireless_Standard
#
# Purpose
#    Model a wireless standard
#
# Revision Dates
#    20-Aug-2012 (RS) Creation
#    17-Dec-2012 (CT) Change `name.completer.treshold` to `0` (was `2`)
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _MOM.import_MOM        import *
from   _FFM                   import FFM

_Ancestor_Essence = FFM.Object

class Wireless_Standard (_Ancestor_Essence) :
    """Wireless standard"""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class name (A_String) :
            """Name of the standard"""

            kind               = Attr.Primary
            max_length         = 20
            ignore_case        = True
            completer          = Attr.Completer_Spec  (0, Attr.Selector.primary)

        # end class name

        class bandwidth (A_Frequency) :
            """Bandwidth of a channel"""

            kind               = Attr.Necessary

        # end class bandwidth

    # end class _Attributes

# end class Wireless_Standard

if __name__ != "__main__" :
    FFM._Export ("*")
### __END__ FFM.Wireless_Standard
