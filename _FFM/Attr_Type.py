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
#    FFM.Attr_Type
#
# Purpose
#    Define attribute types for package FFM
#
# Revision Dates
#    14-Mar-2012 (CT) Creation
#    20-Aug-2012 (RS) Add `A_TX_Power`
#    27-Aug-2012 (RS) Add import of `math.log`
#    22-Sep-2012 (RS) Remove `A_Wireless_Protocol`
#    20-Nov-2012 (CT) Fix `A_TX_Power._from_string`, add `_default_unit`
#    05-Dec-2012 (RS) Add `A_Polarization`
#    17-Dec-2012 (CT) Add `A_Wireless_Mode`
#    17-Dec-2012 (RS) Fix unit dBW, use decadic logarithm for dB
#     5-Jun-2013 (CT) Use `is_attr_type`, not home-grown code
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   math                     import log

from   _MOM.import_MOM          import *
from   _MOM.import_MOM          import _A_Unit_, _A_Float_, _A_Named_Value_
from   _FFM                     import FFM
from   _TFL.I18N                import _

import _FFM.Wireless_Mode

class A_Polarization (_A_Named_Value_) :
    """Antenna polarisation"""

    ( horizontal
    , vertical
    , left_circular
    , right_circular
    )            = range (4)

    example      = "vertical"
    typ          = "Antenna Polarization"
    P_Type       = int
    Table        = \
        { "horizontal"     : horizontal
        , "vertical"       : vertical
        , "left circular"  : left_circular
        , "right circular" : right_circular
        }

# end class A_Polarization

class A_TX_Power (_A_Unit_, _A_Float_) :
    """Transmit Power specified in multiples of W or dBW, dBm,
       converted to dBm.
    """

    typ             = _ ("TX Power")
    needs_raw_value = True
    _default_unit   = "dBm"
    _unit_dict      = dict \
        ( mW        = 1
        ,  W        = 1.E3
        , kW        = 1.E6
        , MW        = 1.E9
        , dBm       = 1
        , dBmW      = 1 # alias for dBm, see http://en.wikipedia.org/wiki/DBm
        , dBW       = 1
        )

    def _from_string (self, s, obj, glob, locl) :
        v    = self.__super._from_string (s, obj, glob, locl)
        pat  = self._unit_pattern
        unit = ""
        if pat.search (s) :
            unit = pat.unit
        if unit.startswith ('dB') :
            if unit == 'dBW' :
                v += 30
        else :
            v = log (v) / log (10) * 10.
        return v
    # end def _from_string

# end class A_TX_Power

class A_Wireless_Mode (MOM.Attr._A_Named_Object_) :
    """Wireless mode to use for %(ui_type_name)s"""

    example     = u"Ad_Hoc"
    typ         = "wl-mode"
    Table       = FFM.Wireless_Mode.Table

# end class A_Wireless_Mode

__all__ = tuple (k for (k, v) in globals ().iteritems () if is_attr_type (v))

if __name__ != "__main__" :
    FFM._Export ("*")
### __END__ FFM.Attr_Type
