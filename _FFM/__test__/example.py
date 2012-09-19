# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package FFM.__test__.
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
#    FFM.__test__.example
#
# Purpose
#    Example how to use test scaffolding for FFM
#
# Revision Dates
#    18-Sep-2012 (CT) Creation
#    18-Sep-2012 (CT) Import from `_FFM.__test__`, not `_GTW.__test__`
#    ««revision-date»»···
#--

from   __future__ import absolute_import, division, print_function, unicode_literals

from   _FFM.__test__.model      import *

_test_code = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...

    >>> for T in scope.T_Extension :
    ...     if hasattr (T, "refuse_links") :
    ...         print (T.type_name, sorted (T.refuse_links))
    MOM.Id_Entity []
    MOM.Link []
    MOM.Link1 []
    MOM._MOM_Link_n_ []
    MOM.Link2 []
    MOM.Link2_Ordered []
    MOM.Link3 []
    MOM.Object []
    MOM.Named_Object []
    FFM.Link1 []
    FFM.Link2 []
    FFM.Link2_Ordered []
    FFM.Link3 []
    FFM.Object []
    FFM.Id_Entity []
    FFM.Named_Object []
    FFM.Device_Type []
    FFM.Antenna_Type []
    FFM.Device []
    FFM.Antenna []
    FFM.Firmware_Type []
    FFM.Firmware_Version []
    FFM.Firmware_Bin []
    FFM.Firmware_Binary []
    FFM.Firmware_Bundle []
    FFM.Firmware_Binary_in_Firmware_Bundle []
    FFM.IP_Network []
    FFM.IP4_Network []
    FFM.IP6_Network []
    FFM.Net_Device_Type []
    FFM.Node []
    FFM.Net_Device []
    FFM.Net_Interface []
    FFM._Net_Credentials_ []
    FFM.WPA_Credentials []
    PAP.Link1 []
    PAP.Link2 []
    PAP.Link2_Ordered []
    PAP.Link3 []
    PAP.Object []
    PAP.Id_Entity []
    PAP.Named_Object []
    PAP.Subject []
    PAP.Person []
    FFM.Nickname []
    FFM.Regulatory_Domain []
    FFM.Regulatory_Permission []
    FFM.Zone []
    FFM.Routing_Zone []
    FFM.Routing_Zone_OLSR []
    FFM.Wired_Interface []
    FFM.Wireless_Channel []
    FFM.Wireless_Standard []
    FFM.Wireless_Interface []
    FFM._Wireless_Mode_ []
    FFM.Ad_Hoc_Mode []
    FFM.AP_Mode []
    FFM.Client_Mode []
    PAP.Company []
    FFM.Device_Type_made_by_Company []
    FFM.Net_Interface_in_IP_Network []
    FFM.Net_Interface_in_IP4_Network []
    FFM.Net_Link []
    FFM.Person_mentors_Person []
    FFM.Subject_owns_Node []
    FFM.Wired_Link []
    FFM.Wireless_Interface_uses_Antenna []
    FFM.Wireless_Interface_uses_Wireless_Channel []
    FFM.Wireless_Link []
    Auth.Link1 []
    Auth.Link2 []
    Auth.Link2_Ordered []
    Auth.Link3 []
    Auth.Object []
    Auth.Id_Entity []
    Auth.Named_Object []
    Auth.Account []
    Auth.Account_Anonymous [u'GTW.OMP.Auth.Account_in_Group']
    Auth.Account_P []
    Auth.Group []
    Auth.Account_in_Group []
    Auth._Account_Action_ []
    Auth.Account_Activation []
    Auth.Account_Password_Change_Required []
    Auth._Account_Token_Action_ []
    Auth.Account_EMail_Verification []
    Auth.Account_Password_Reset []
    PAP.Address []
    PAP.Email []
    PAP.Phone []
    PAP.Subject_has_Property []
    PAP.Subject_has_Address []
    PAP.Company_has_Address []
    PAP.Subject_has_Email []
    PAP.Company_has_Email []
    PAP.Subject_has_Phone []
    PAP.Company_has_Phone []
    PAP.Entity_created_by_Person [u'GTW.OMP.PAP.Entity_created_by_Person', u'PAP.Entity_created_by_Person']
    PAP.Person_has_Address []
    PAP.Person_has_Email []
    PAP.Person_has_Phone []

    >>> scope.destroy ()

"""

__test__ = Scaffold.create_test_dict \
  ( dict
      ( main       = _test_code
      )
  )

### __END__ FFM.__test__.example
