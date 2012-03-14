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
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _MOM.import_MOM          import *
from   _MOM.import_MOM          import _A_Composite_
from   _FFM                     import FFM

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

__all__ = tuple \
    (  k for (k, v) in globals ().iteritems ()
    if isinstance (v, MOM.Meta.M_Attr_Type)
    )

if __name__ != "__main__" :
    FFM._Export ("*")
### __END__ FFM.Attr_Type
