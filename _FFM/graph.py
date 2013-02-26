# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012-2013 Mag. Christian Tanzer All rights reserved
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
#    FFM.graph
#
# Purpose
#    Graph describing FFM (partial) object model
#
# Revision Dates
#    27-Aug-2012 (RS) Creation
#    30-Aug-2012 (CT) Rearrange graph, add more nodes/links
#    31-Aug-2012 (CT) Adapt to MOM.Graph.Spec API change
#     6-Sep-2012 (CT) Add lots more nodes/links, rearrange graph
#    18-Sep-2012 (RS) Put `Node` and `Subject` and descendants in the middle
#                     for new Id_Entities of `Node`, fixes tanzer constraint
#    19-Sep-2012 (CT) Disentangle links, remove whitespace
#    24-Sep-2012 (CT) Add `Command`
#    18-Oct-2012 (RS) Add `Wired_Interface` and associations
#    18-Oct-2012 (RS) Add `Node` `IS_A` `Subject`
#    22-Nov-2012 (CT) Add `Role.left` to `Wireless_Channel`
#    22-Nov-2012 (RS) Move `Net_Interface_in_IP_Network.right` to South
#     8-Dec-2012 (RS) Add `Antenna_Band`
#    17-Dec-2012 (CT) Remove `Wireless_Mode`
#    17-Dec-2012 (RS) Skip explicit links from children of `Net_Interface`
#    26-Feb-2013 (CT) Remove `Wired_Link` and `Wireless_Link`
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _GTW                   import GTW
from   _MOM                   import MOM
from   _FFM                   import FFM
from   _GTW._OMP._PAP         import PAP

from   _MOM._Graph.Spec       import Attr, Child, ET, IS_A, Role, Skip

import _MOM._Graph.Command
import _MOM._Graph.Entity

from   _TFL                   import sos
from   _TFL._D2               import Cardinal_Direction as CD
from   _TFL.I18N              import _, _T

def graph (app_type) :
    return MOM.Graph.Spec.Graph \
        ( app_type
        , ET.FFM.Device
            ( Role.left
                ( ET.FFM.Device_Type_made_by_Company
                    ( Role.right
                        ( IS_A.PAP.Subject
                            ( Child.PAP.Person (offset = CD.N)
                            , offset = CD.W
                            )
                        , offset = CD.S
                        )
                    , offset = CD.W
                    )
                , offset       = CD.E * 4
                , guide_offset = 1.0
                , source_side  = "N"
                , target_side  = "N"
                )
            , Child.FFM.Antenna
                ( Role.left
                    ( IS_A.FFM.Device_Type
                    , ET.FFM.Antenna_Band (offset = CD.E)
                    , offset = CD.E * 4
                    )
                , offset = CD.N
                )
            , Child.FFM.Net_Device
                ( Role.left
                    ( IS_A.FFM.Device_Type
                    , guide_offset = 0.5
                    , offset       = CD.E * 3
                    , source_side  = "S"
                    , target_side  = "S"
                    )
                , Attr.node
                    ( Attr.manager (source_side = "N", target_side = "N")
                    , Attr.owner
                        ( guide_offset = 0.75
                        , source_side  = "E"
                        , target_side  = "W"
                        )
                    , IS_A.PAP.Subject (source_side = "E", target_side = "W")
                    , offset = CD.N
                    )
                , ET.FFM.Net_Interface (offset = CD.S + CD.E * 2)
                , offset = CD.E + CD.S
                )
            )
        , ET.FFM.Net_Interface
            ( Role.left (guide_offset = 1.0)
            , ET.FFM.Net_Link (offset = CD.S)
            , ET.FFM._Net_Credentials_
                ( Role.left (guide_offset = 1.0)
                , offset = CD.N + CD.E * 2
                )
            , ET.FFM.Net_Interface_in_IP_Network
                ( Role.right
                    ( Child.FFM.IP4_Network (offset = CD.SW)
                    , Child.FFM.IP6_Network (offset = CD.S)
                    , offset = CD.S
                    )
                , Role.left
                    ( source_side  = "N"
                    , target_side  = "N"
                    , guide_offset = 0.5
                    )
                , offset = CD.E * 2
                )
            , Child.FFM.Wireless_Interface
                ( Skip.left
                , ET.FFM.Wireless_Interface_uses_Antenna
                    ( Role.left
                        ( guide_offset = 1.5
                        )
                    , Role.right
                        ( anchor      = False
                        , source_side = "W"
                        , target_side = "W"
                        )
                    , offset = CD.N + CD.W * 2
                    )
                , ET.FFM.Wireless_Interface_uses_Wireless_Channel
                    ( Role.right
                        ( Role.left
                            ( offset = CD.S
                            )
                        , offset = CD.W
                        )
                    , offset = CD.W
                    )
                , offset = CD.W
                )
            , Child.FFM.Wired_Interface
                ( Skip.left
                , offset = CD.E
                )
            )
        , desc  = _T ("Graph displaying Funkfeuer object model")
        , title = _T ("FFM graph")
        )
# end def graph

class Command (MOM.Graph.Command) :

    PNS                   = FFM

    @property
    def PNS_Aliases (self) :
        return dict \
            ( Auth        = GTW.OMP.Auth
            , PAP         = GTW.OMP.PAP
            )
    # end def PNS_Aliases

    _defaults             = dict \
        ( name            = "nodedb"
        )

    def _app_dir_default (self) :
        return sos.path.normpath (sos.path.join (self.app_dir, "..", "doc"))
    # end def _app_dir_default

# end class Command

if __name__ != "__main__" :
    FFM._Export ("*")
else :
    import _GTW._OMP._PAP.import_PAP
    import _GTW._OMP._Auth.import_Auth
    import _FFM.import_FFM
    Command () ()
### __END__ FFM.graph
