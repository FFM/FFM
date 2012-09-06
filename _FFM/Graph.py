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
#    31-Aug-2012 (CT) Adapt to MOM.Graph.Spec API change
#     6-Sep-2012 (CT) Add lots more nodes/links, rearrange graph
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _GTW                   import GTW
from   _MOM                   import MOM
from   _FFM                   import FFM
from   _GTW._OMP._PAP         import PAP

import _FFM

from   _MOM._Graph.Spec       import Attr, Child, ET, IS_A, Role, Skip
import _MOM._Graph.Entity

from   _TFL._D2               import Cardinal_Direction as CD

def graph (app_type) :
    return MOM.Graph.Spec.Graph \
        ( app_type
        , ET.FFM.Device
            ( Role.left
                ( ET.FFM.Device_Type_made_by_Company
                    ( Role.right (offset = CD.N)
                    , offset = CD.E
                    )
                , offset = CD.E
                )
            , ET.FFM.Wireless_Interface_uses_Antenna
                ( Role.left
                    ( ET.FFM._Wireless_Mode_
                        ( Child.FFM.Ad_Hoc_Mode
                            ( offset = CD.SW
                            )
                        , Child.FFM.AP_Mode
                            ( offset = CD.S
                            )
                        , Child.FFM.Client_Mode
                            ( offset = CD.SE
                            )
                        , offset = CD.SW
                        )
                    , ET.FFM.Wireless_Interface_uses_Wireless_Channel
                        ( Role.right (offset = CD.W)
                        , offset  = CD.W
                        )
                    , offset      = CD.SE
                    )
                , Role.right
                    ( ET.FFM.Antenna_Type
                        ( IS_A.FFM.Device_Type
                        , offset = CD.E * 3
                        )
                    , offset = CD.N * 3
                    )
                , offset = CD.S + CD.W * 2
                )
            )
        , ET.FFM.Net_Device
            ( IS_A.FFM.Device (offset = CD.N)
            , Attr.node
                ( ET.FFM.Subject_owns_Node
                    ( Role.left
                        ( Child.PAP.Company
                        , offset = CD.N
                        )
                    , offset = CD.N
                    )
                , offset = CD.W
                )
            , Role.left
                ( IS_A.FFM.Device_Type
                , offset = CD.E
                )
            , ET.FFM.Net_Interface
                ( ET.FFM._Net_Credentials_ (offset = CD.SE)
                , ET.FFM.Net_Interface_in_IP_Network
                    ( Role.right
                        ( Child.FFM.IP4_Network (offset = CD.S)
                        , Child.FFM.IP6_Network (offset = CD.N)
                        , offset = CD.E
                        )
                    , offset = CD.E
                    )
                , ET.FFM.Net_Link
                    ( Child.FFM.Wireless_Link
                        ( offset = CD.W
                        )
                    , offset = CD.S
                    )
                , offset = CD.S
                )
            )
        , ET.FFM.Wireless_Interface
            ( IS_A.FFM.Net_Interface
            , Skip.left
            )
        , ET.FFM.Antenna
            ( IS_A.FFM.Device (source_side = "E")
            )
        )
# end def graph

if __name__ != "__main__" :
    FFM._Export ("*")
### __END__ FFM.Graph
