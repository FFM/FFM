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
#    17-Aug-2012 (AK) `SSID` -> `ESSID`, add `BSSID`, `power` -> `tx_power`
#                     add `frequency`
#    20-Aug-2012 (RS) cleanup, remove `frequency`, use `A_TX_Power`
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _MOM.import_MOM          import *
from   _FFM                     import FFM

from   _GTW._OMP._NET.Attr_Type import *

from   _FFM.Attr_Type           import *
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

        class txpower (A_TX_Power) :
            """Transmit power with unit (units of dBW or W)."""

            kind               = Attr.Optional
            ui_name            = "TX power"

        # end class power

        class essid (A_String) :
            """Network name."""

            example            = "freiesnetz.www.funkfeuer.at"
            kind               = Attr.Optional
            max_length         = 32
            ui_name            = "ESSID"

        # end class essid

        class bssid (A_MAC_Address) :
            """Cell name."""

            kind               = Attr.Optional
            ui_name            = "BSSID"
            example            = "de:ad:be:ef:00:01"

        # end class bssid

        ### MAC parameters
        class is_hidden (A_Boolean) :
            """???"""

            kind               = Attr.Optional

        # end class is_hidden

    # end class _Attributes

# end class Wireless_Interface

if __name__ != "__main__" :
    FFM._Export ("*")
### __END__ FFM.Wireless_Interface
