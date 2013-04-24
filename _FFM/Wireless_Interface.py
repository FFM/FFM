# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012-2013 Mag. Christian Tanzer All rights reserved
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
#    20-Aug-2012 (RS) Cleanup, remove `frequency`, use `A_TX_Power`
#    13-Sep-2012 (RS) Remove `protocol`, add `standard`
#    17-Dec-2012 (RS) Add `auto_cache` for `left`
#    17-Dec-2012 (CT) Add attribute `mode`
#    17-Dec-2012 (CT) Set `standard.ui_allow_new` to `False`
#    26-Feb-2013 (CT) Add `Virtual_Wireless_Interface`,
#                     factor and export `_Wireless_Interface_`
#    27-Feb-2013 (CT) Add `Virtual_Wireless_Interface.hardware.sort_skip = True`
#    27-Feb-2013 (CT) Add `Init_Only_Mixin` and `ui_allow_new` to `hardware`
#    24-Apr-2013 (CT) Move `left.auto_cache` to non-partial classes
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _MOM.import_MOM          import *
from   _FFM                     import FFM

from   _GTW._OMP._NET.Attr_Type import *

from   _FFM.Attr_Type           import *
import _FFM.Net_Interface
import _FFM.Wireless_Standard

_Ancestor_Essence = FFM.Net_Interface

class _Wireless_Interface_ (_Ancestor_Essence) :
    """Base class for wireless interfaces"""

    is_partial  = True

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        ### Non-primary attributes

        class mode (A_Wireless_Mode) :

            kind               = Attr.Optional
            raw_default        = "Ad_Hoc"

        # end class mode

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

        class standard (A_Id_Entity) :
            """Wireless standard used by the wireless interface."""

            kind               = Attr.Necessary
            P_Type             = FFM.Wireless_Standard
            ui_allow_new       = False

        # end class standard

        class txpower (A_TX_Power) :
            """Transmit power with unit (units of dBW or W)."""

            kind               = Attr.Optional
            ui_name            = "TX power"

        # end class power

    # end class _Attributes

# end class _Wireless_Interface_

_Ancestor_Essence = _Wireless_Interface_

class Wireless_Interface (_Ancestor_Essence) :
    """Wireless interface of a FFM device"""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class left (_Ancestor.left) :
            """Type of net device"""

            auto_cache         = True

        # end class left

    # end class _Attributes

# end class Wireless_Interface

_Ancestor_Essence = _Wireless_Interface_

class Virtual_Wireless_Interface (_Ancestor_Essence) :
    """Virtual wireless interface of a FFM device"""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class left (_Ancestor.left) :
            """Type of net device"""

            auto_cache         = True

        # end class left

        class hardware (A_Id_Entity) :
            """Hardware interface used by virtual interface."""

            kind               = Attr.Primary
            Kind_Mixins        = (Attr.Init_Only_Mixin, )
            P_Type             = Wireless_Interface
            sort_skip          = True
            ui_allow_new       = False

        # end class hardware

        ### Non-primary attributes

        class standard (_Ancestor.standard) :

            kind               = Attr.Query
            auto_up_depends    = ("hardware", )
            query              = Q.hardware.standard

        # end class standard

        class txpower (_Ancestor.txpower) :

            kind               = Attr.Query
            auto_up_depends    = ("hardware", )
            query              = Q.hardware.txpower

        # end class power

    # end class _Attributes

    class _Predicates (_Ancestor_Essence._Predicates) :

        _Ancestor = _Ancestor_Essence._Predicates

        class valid_left (Pred.Condition) :
            """`left` must be equal to `hardware.left`"""

            kind               = Pred.Object
            assertion          = "left is hardware.left"
            attributes         = ("left", "hardware.left")

        # end class valid_left

    # end class _Predicates

# end class Virtual_Wireless_Interface

if __name__ != "__main__" :
    FFM._Export ("*", "_Wireless_Interface_")
### __END__ FFM.Wireless_Interface
