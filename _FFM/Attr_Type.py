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
#    FFM.Attr_Type
#
# Purpose
#    Define attribute types for package FFM
#
# Revision Dates
#    14-Mar-2012 (CT) Creation
#    20-Aug-2012 (RS) Add `A_TX_Power`
#    27-Aug-2012 (RS) Add import of `math.log`
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   math                     import log

from   _MOM.import_MOM          import *
from   _MOM.import_MOM          import _A_Composite_, _A_Named_Value_
from   _MOM.import_MOM          import _A_Unit_, _A_Float_
from   _FFM                     import FFM
from   _TFL.I18N                import _

class A_Wireless_Protocol (_A_Named_Value_) :
    """An attribute selecting a specific wireless protocol."""

    ( WLP_802_11_a
    , WLP_802_11_b
    , WLP_802_11_g
    , WLP_802_11_n
    )            = range (4)

    example      = "802.11a"
    typ          = "WL-Protocol"
    P_Type       = int
    Table        = \
        { "802.11a" : WLP_802_11_a
        , "802.11b" : WLP_802_11_b
        , "802.11g" : WLP_802_11_g
        , "802.11n" : WLP_802_11_n
        }

# end class A_Wireless_Protocol

class A_TX_Power (_A_Unit_, _A_Float_) :
    """Transmit Power specified in units of W or dBW, dBm,
       converted to dBm.
    """

    typ             = _ ("TX Power")
    needs_raw_value = True
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
        v = self.__super._from_string (s, obj, glob, locl)
        if s.startswith ('dB') :
            if s == 'dbW' :
                v += 30
        else :
            v = log (v) * 10.
        return v
    # end def _from_string

# end class A_TX_Power

__all__ = tuple \
    (  k for (k, v) in globals ().iteritems ()
    if isinstance (v, MOM.Meta.M_Attr_Type)
    )

if __name__ != "__main__" :
    FFM._Export ("*")
### __END__ FFM.Attr_Type
