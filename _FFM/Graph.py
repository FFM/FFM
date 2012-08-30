# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.OMP.SRM.
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
#    FFM.Graph
#
# Purpose
#    Graph describing FFM (partial) object model
#
# Revision Dates
#    27-Aug-2012 (RS) Creation
#    30-Aug-2012 (CT) Rearrange graph, add more nodes/links
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _GTW                   import GTW
from   _MOM                   import MOM
from   _FFM                   import FFM
from   _GTW._OMP._PAP         import PAP

import _FFM

from   _MOM._Graph.Spec       import ET
import _MOM._Graph.Entity

from   _TFL._D2               import Cardinal_Direction as CD

def graph (app_type) :
    ### To add::
    # ET.FFM.Ad_Hoc_Mode
    #   ( IS_A   = ET.FFM._Wireless_Mode_, offset = CD.SE)
    # ET.FFM.AP_Mode
    #   ( IS_A   = ET.FFM._Wireless_Mode_, offset = CD.S)
    # ET.FFM.Client_Mode
    #   ( IS_A   = ET.FFM._Wireless_Mode_, offset = CD.SW)
    return MOM.Graph.Spec.Graph \
        ( app_type
        , ET.FFM.Device
            ( E      = ET.FFM.Device_Type
            , E2     = ET.FFM.Device_Type_made_by_Company
                ( E      = ET.PAP.Company)
            , S_W    = ET.FFM.Wireless_Interface_uses_Antenna
                ( S      = ET.FFM.Wireless_Interface
                    ( left = None
                    , W2   = ET.FFM._Wireless_Mode_
                    )
                , N2     = ET.FFM.Antenna
                    ( E2     = ET.FFM.Antenna_Type
                        ( IS_A   = ET.FFM.Device_Type)
                    )
                )
            )
        , ET.FFM.Net_Device
            ( IS_A   = ET.FFM.Device (offset = CD.N)
            , E      = ET.FFM.Net_Device_Type
                ( IS_A   = ET.FFM.Device_Type)
            , S      = ET.FFM.Net_Interface
                ( E      = ET.FFM._Net_Credentials_)
            )
        , ET.FFM.Wireless_Interface
            ( IS_A   = ET.FFM.Net_Interface)
        , ET.FFM.Antenna
            ( IS_A   = ET.FFM.Device)
        )
# end def graph

if __name__ != "__main__" :
    FFM._Export ("*")
### __END__ FFM.Graph
