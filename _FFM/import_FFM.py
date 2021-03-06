# -*- coding: utf-8 -*-
# Copyright (C) 2012-2014 Mag. Christian Tanzer All rights reserved
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
#    FFM.import_FFM
#
# Purpose
#    Import FFM object model
#
# Revision Dates
#     6-Mar-2012 (CT) Creation
#    10-May-2012 (CT) Add `Node_has_Net_Device`, `Wired_Interface`, `Net_Link`
#    20-Aug-2012 (RS) Add `Wireless_Standard`, `Wireless_Channel`
#                    `Regulatory_Domain`, `Regulatory_Permission`,
#                    `Wireless_Interface_uses_Wireless_Channel`
#    30-Aug-2012 (RS) `Person_has_Node` -> `Subject_owns_Node`
#    30-Aug-2012 (RS) Remove `Node_has_Net_Device`
#     6-Sep-2012 (CT) Add `IP6_Network`
#    12-Sep-2012 (CT) Add `Nickname` and `Person_mentors_Person`
#    18-Sep-2012 (RS) remove `Subject_owns_Node` (replace by Id_Entity)
#    21-Sep-2012 (RS) Add `Net_Interface_in_IP6_Network`
#    11-Oct-2012 (RS) Import `Nickname` from `PAP` -- not imported by default
#    12-Oct-2012 (RS) Add `Node_has_Address`
#     9-Nov-2012 (RS) Import `IM_Handle` from `PAP`
#     7-Dec-2012 (RS) Add `Antenna_Band`
#    26-Feb-2013 (CT) Remove `Wired_Link` and `Wireless_Link`
#     4-Mar-2013 (CT) Add `GTW.OMP.PAP.Association`
#    28-Apr-2013 (CT) Add `Person_acts_for_Legal_Entity`
#    27-Mar-2014 (CT) Add `MOM.Document`
#     5-Jun-2014 (RS) Remove `Node_has_Address` (it's already in
#                     `refuse_links` of `Node`)
#    13-Jun-2014 (RS) Remove `Person_acts_for_Legal_Entity`,
#                     add `PAP.Adhoc_Group`, `PAP.Person_in_Group`
#    20-Jun-2014 (RS) Add `IP_Pool`, `IP4_Pool`, `IP6_Pool`
#     1-Jul-2014 (RS) `IP_DNS_Alias` and derivatives
#     3-Jul-2014 (RS) Add `IP_Network_in_IP_Pool`, `IP_Pool_permits_Group`
#                     and descendants
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _MOM.import_MOM        import *
from   _FFM                   import FFM

import _GTW._OMP._PAP.Association
import _GTW._OMP._PAP.IM_Handle
import _GTW._OMP._PAP.Nickname
import _GTW._OMP._PAP.Adhoc_Group
import _GTW._OMP._PAP.Person_in_Group
import _GTW._OMP._PAP.Id_Entity_permits_Group

import _FFM.Antenna
import _FFM.Antenna_Band
import _FFM.Antenna_Type
import _FFM.Device
import _FFM.Device_Type
import _FFM.Firmware
import _FFM.IP4_DNS_Alias
import _FFM.IP4_Network
import _FFM.IP4_Pool
import _FFM.IP6_DNS_Alias
import _FFM.IP6_Network
import _FFM.IP6_Pool
import _FFM.IP_DNS_Alias
import _FFM.IP_Network
import _FFM.IP_Pool
import _FFM.Net_Credentials
import _FFM.Net_Device
import _FFM.Net_Device_Type
import _FFM.Net_Interface
import _FFM.Node
import _FFM.Regulatory_Domain
import _FFM.Regulatory_Permission
import _FFM.Routing_Zone
import _FFM.Wired_Interface
import _FFM.Wireless_Channel
import _FFM.Wireless_Interface
import _FFM.Wireless_Standard

import _FFM.Wireless_Mode
import _FFM.Zone

import _FFM.Device_Type_made_by_Company
import _FFM.IP_Network_in_IP_Pool
import _FFM.IP4_Network_in_IP4_Pool
import _FFM.IP6_Network_in_IP6_Pool
import _FFM.IP_Pool_permits_Group
import _FFM.IP4_Pool_permits_Group
import _FFM.IP6_Pool_permits_Group
import _FFM.Net_Interface_in_IP4_Network
import _FFM.Net_Interface_in_IP6_Network
import _FFM.Net_Interface_in_IP_Network
import _FFM.Net_Link
import _FFM.Person_mentors_Person
import _FFM.Wireless_Interface_uses_Antenna
import _FFM.Wireless_Interface_uses_Wireless_Channel

import _MOM.Document

### __END__ FFM.import_FFM
