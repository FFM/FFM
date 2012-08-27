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
#    FFM.Regulatory_Permission
#
# Purpose
#    Model a regulatory transmit permission
#
# Revision Dates
#    20-Aug-2012 (RS) Creation
#    27-Aug-2012 (RS) Fix `bandwidth`
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _MOM.import_MOM            import *
from   _MOM._Attr.Number_Interval import *
from   _FFM                       import FFM
from   _FFM.Attr_Type             import A_TX_Power

import _FFM.Entity

_Ancestor_Essence = FFM.Link1

class Regulatory_Permission (_Ancestor_Essence) :
    """Regulatory transmit permission"""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class left (A_String) :
            """The regulatory domain that gives this permission."""

            kind               = Attr.Primary
            role_name          = 'domain'

        # end class left

        class band (A_Frequency_Interval) :
            """Frequency range for which transmission is allowed."""

            kind               = Attr.Primary

        # end class band

        class bandwidth (A_Frequency) :
            """Maximum allowed bandwidth."""

            kind               = Attr.Necessary
            example            = "20 MHz"

        # end class bandwidth

        class gain (A_Float) :
            """Maximum allowed antenna gain in dB."""

            kind               = Attr.Optional
            example            = "6"

        # end class gain

        class eirp (A_TX_Power) :
            """Maximum allowed TX power in dBm, dBW or units of W."""

            kind               = Attr.Optional
            example            = "20 dBm"

        # end class gain

        class need_DFS (A_Boolean) :
            """Band needs dynamic frequency selection."""

            kind               = Attr.Necessary
            default            = False

        # end class need_DFS

        class indoor_only (A_Boolean) :
            """Only indoor TX allowed."""

            kind               = Attr.Necessary
            default            = False

        # end class indoor_only

    # end class _Attributes

# end class Regulatory_Permission

if __name__ != "__main__" :
    FFM._Export ("*")
### __END__ FFM.Regulatory_Permission
