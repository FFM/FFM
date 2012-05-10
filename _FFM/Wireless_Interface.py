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
#    FFM.Wireless_Interface
#
# Purpose
#    Model a wireless interface of a FFM device
#
# Revision Dates
#    14-Mar-2012 (CT) Creation
#    10-May-2012 (CT) Change `protocol` and `ssid` from `Required` to
#                     `Necessary`
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _MOM.import_MOM        import *
from   _FFM                   import FFM

from   _FFM.Attr_Type         import *
import _FFM.Net_Interface

_Ancestor_Essence = FFM.Net_Interface

class Wireless_Interface (_Ancestor_Essence) :
    """Wireless interface of a FFM device"""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        ### Non-primary attributes

        class protocol (A_Wireless_Protocol) :
            """Protocol used by the wireless interface."""

            example            = "802.11a"
            kind               = Attr.Necessary

        # end class protocol

        ### XXX channels?

        class is_hidden (A_Boolean) :
            """???"""

            kind               = Attr.Optional

        # end class is_hidden

        class power (A_Float) :
            """Transmit power in dBm."""

            kind               = Attr.Optional

        # end class power

        class ssid (A_String) :
            """Network name."""

            example            = "freiesnetz.www.funkfeuer.at"
            kind               = Attr.Necessary
            max_length         = 32
            ui_name            = "SSID"

        # end class ssid

    # end class _Attributes

# end class Wireless_Interface

if __name__ != "__main__" :
    FFM._Export ("*")
### __END__ FFM.Wireless_Interface
