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
    return MOM.Graph.Spec.Graph \
        ( app_type
        , ET.FFM.Net_Device
            ( N      = ET.FFM.Device          (E = ET.FFM.Device_Type)
            , E      = ET.FFM.Net_Device_Type ()
            #, S      = ET.FFM.Net_Interface   (E = ET.FFM.Net_Credentials)
            )
        , ET.FFM.Antenna
            ( S      = ET.FFM.Device          ()
            , E      = ET.FFM.Antenna_Type    ()
            )
#        , ET.FFM.Device_Type_made_by_Company
#            ( E      = ET.PAP.Company         ()
#            , W      = ET.FFM.Device_Type     ()
#            )
        )
# end def graph

if __name__ != "__main__" :
    FFM._Export ("*")
### __END__ FFM.Graph
