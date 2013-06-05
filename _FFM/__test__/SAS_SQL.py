# -*- coding: iso-8859-15 -*-
# Copyright (C) 2013 Mag. Christian Tanzer All rights reserved
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
#    FFM.__test__.SAS_SQL
#
# Purpose
#    Test SQL definitions of SAS
#
# Revision Dates
#    30-May-2013 (CT) Creation
#    ««revision-date»»···
#--

from   __future__                 import print_function
from   __future__                 import unicode_literals

from   _FFM                       import FFM
from   _GTW.__test__.SAS_SQL      import *
from   _MOM.inspect               import children_trans_iter

import _FFM.import_FFM
import _GTW._OMP._Auth.import_Auth
import _GTW._OMP._PAP.import_PAP

_test_select = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...

    >>> show_select (scope)
    Auth.Account_in_Group
        SELECT "Auth__Account_in_Group".electric,
               "Auth__Account_in_Group".last_cid,
               "Auth__Account_in_Group".left_pid,
               "Auth__Account_in_Group".pid,
               "Auth__Account_in_Group".right_pid,
               "Auth__Account_in_Group".type_name,
               "Auth__Account_in_Group".x_locked
        FROM "Auth__Account_in_Group"
    Auth.Certificate
        SELECT "Auth__Certificate"."desc",
               "Auth__Certificate".__validity_finish,
               "Auth__Certificate".__validity_start,
               "Auth__Certificate".electric,
               "Auth__Certificate".email,
               "Auth__Certificate".last_cid,
               "Auth__Certificate".pem,
               "Auth__Certificate".pid,
               "Auth__Certificate".revocation_date,
               "Auth__Certificate".type_name,
               "Auth__Certificate".x_locked
        FROM "Auth__Certificate"
    Auth.Group
        SELECT "Auth__Group"."desc",
               "Auth__Group".electric,
               "Auth__Group".last_cid,
               "Auth__Group".name,
               "Auth__Group".pid,
               "Auth__Group".type_name,
               "Auth__Group".x_locked
        FROM "Auth__Group"
    Auth._Account_
        SELECT "Auth___Account_".electric,
               "Auth___Account_".enabled,
               "Auth___Account_".last_cid,
               "Auth___Account_".name,
               "Auth___Account_".pid,
               "Auth___Account_".superuser,
               "Auth___Account_".suspended,
               "Auth___Account_".type_name,
               "Auth___Account_".x_locked
        FROM "Auth___Account_"
    Auth.Account Auth._Account_
        SELECT "Auth__Account"."Auth___Account__pid",
               "Auth__Account".password,
               "Auth__Account".ph_name
        FROM "Auth__Account"
    EVT.Event
        SELECT "EVT__Event".__date_finish,
               "EVT__Event".__date_start,
               "EVT__Event".__time_finish,
               "EVT__Event".__time_start,
               "EVT__Event".calendar_pid,
               "EVT__Event".detail,
               "EVT__Event".electric,
               "EVT__Event".last_cid,
               "EVT__Event".left_pid,
               "EVT__Event".pid,
               "EVT__Event".short_title,
               "EVT__Event".type_name,
               "EVT__Event".x_locked
        FROM "EVT__Event"
    EVT.Event_occurs
        SELECT "EVT__Event_occurs".__time_finish,
               "EVT__Event_occurs".__time_start,
               "EVT__Event_occurs".date,
               "EVT__Event_occurs".last_cid,
               "EVT__Event_occurs".left_pid,
               "EVT__Event_occurs".pid,
               "EVT__Event_occurs".type_name,
               "EVT__Event_occurs".x_locked
        FROM "EVT__Event_occurs"
    EVT.Recurrence_Rule
        SELECT "EVT__Recurrence_Rule"."desc",
               "EVT__Recurrence_Rule".count,
               "EVT__Recurrence_Rule".easter_offset,
               "EVT__Recurrence_Rule".electric,
               "EVT__Recurrence_Rule".finish,
               "EVT__Recurrence_Rule".is_exception,
               "EVT__Recurrence_Rule".last_cid,
               "EVT__Recurrence_Rule".left_pid,
               "EVT__Recurrence_Rule".month,
               "EVT__Recurrence_Rule".month_day,
               "EVT__Recurrence_Rule".period,
               "EVT__Recurrence_Rule".pid,
               "EVT__Recurrence_Rule".restrict_pos,
               "EVT__Recurrence_Rule".start,
               "EVT__Recurrence_Rule".type_name,
               "EVT__Recurrence_Rule".unit,
               "EVT__Recurrence_Rule".week,
               "EVT__Recurrence_Rule".week_day,
               "EVT__Recurrence_Rule".x_locked,
               "EVT__Recurrence_Rule".year_day
        FROM "EVT__Recurrence_Rule"
    EVT.Recurrence_Spec
        SELECT "EVT__Recurrence_Spec".date_exceptions,
               "EVT__Recurrence_Spec".dates,
               "EVT__Recurrence_Spec".electric,
               "EVT__Recurrence_Spec".last_cid,
               "EVT__Recurrence_Spec".left_pid,
               "EVT__Recurrence_Spec".pid,
               "EVT__Recurrence_Spec".type_name,
               "EVT__Recurrence_Spec".x_locked
        FROM "EVT__Recurrence_Spec"
    EVT.Calendar
        SELECT "EVT__Calendar"."desc",
               "EVT__Calendar".electric,
               "EVT__Calendar".last_cid,
               "EVT__Calendar".name,
               "EVT__Calendar".pid,
               "EVT__Calendar".type_name,
               "EVT__Calendar".x_locked
        FROM "EVT__Calendar"
    FFM.Firmware_Binary
        SELECT "FFM__Firmware_Binary".electric,
               "FFM__Firmware_Binary".last_cid,
               "FFM__Firmware_Binary".left_pid,
               "FFM__Firmware_Binary".pid,
               "FFM__Firmware_Binary".type_name,
               "FFM__Firmware_Binary".x_locked
        FROM "FFM__Firmware_Binary"
    FFM.Firmware_Bundle
        SELECT "FFM__Firmware_Bundle".electric,
               "FFM__Firmware_Bundle".last_cid,
               "FFM__Firmware_Bundle".name,
               "FFM__Firmware_Bundle".pid,
               "FFM__Firmware_Bundle".type_name,
               "FFM__Firmware_Bundle".version,
               "FFM__Firmware_Bundle".x_locked
        FROM "FFM__Firmware_Bundle"
    FFM.Antenna_Band
        SELECT "FFM__Antenna_Band".__band___raw_lower,
               "FFM__Antenna_Band".__band___raw_upper,
               "FFM__Antenna_Band".__band_lower,
               "FFM__Antenna_Band".__band_upper,
               "FFM__Antenna_Band".electric,
               "FFM__Antenna_Band".last_cid,
               "FFM__Antenna_Band".left_pid,
               "FFM__Antenna_Band".pid,
               "FFM__Antenna_Band".type_name,
               "FFM__Antenna_Band".x_locked
        FROM "FFM__Antenna_Band"
    FFM.Antenna
        SELECT "FFM__Antenna"."desc",
               "FFM__Antenna".__raw_azimuth,
               "FFM__Antenna".__raw_name,
               "FFM__Antenna".azimuth,
               "FFM__Antenna".electric,
               "FFM__Antenna".elevation,
               "FFM__Antenna".gain,
               "FFM__Antenna".last_cid,
               "FFM__Antenna".left_pid,
               "FFM__Antenna".name,
               "FFM__Antenna".pid,
               "FFM__Antenna".polarization,
               "FFM__Antenna".type_name,
               "FFM__Antenna".x_locked
        FROM "FFM__Antenna"
    FFM.Net_Device
        SELECT "FFM__Net_Device"."desc",
               "FFM__Net_Device".__raw_name,
               "FFM__Net_Device".electric,
               "FFM__Net_Device".last_cid,
               "FFM__Net_Device".left_pid,
               "FFM__Net_Device".name,
               "FFM__Net_Device".node_pid,
               "FFM__Net_Device".pid,
               "FFM__Net_Device".type_name,
               "FFM__Net_Device".x_locked
        FROM "FFM__Net_Device"
    FFM.Firmware_Version
        SELECT "FFM__Firmware_Version".electric,
               "FFM__Firmware_Version".last_cid,
               "FFM__Firmware_Version".left_pid,
               "FFM__Firmware_Version".pid,
               "FFM__Firmware_Version".type_name,
               "FFM__Firmware_Version".version,
               "FFM__Firmware_Version".x_locked
        FROM "FFM__Firmware_Version"
    FFM.Net_Interface
        SELECT "FFM__Net_Interface"."desc",
               "FFM__Net_Interface".__raw_name,
               "FFM__Net_Interface".electric,
               "FFM__Net_Interface".is_active,
               "FFM__Net_Interface".last_cid,
               "FFM__Net_Interface".left_pid,
               "FFM__Net_Interface".mac_address,
               "FFM__Net_Interface".name,
               "FFM__Net_Interface".pid,
               "FFM__Net_Interface".type_name,
               "FFM__Net_Interface".x_locked
        FROM "FFM__Net_Interface"
    FFM.Wired_Interface FFM.Net_Interface
        SELECT "FFM__Wired_Interface"."FFM__Net_Interface_pid"
        FROM "FFM__Wired_Interface"
    FFM._Wireless_Interface_ FFM.Net_Interface
        SELECT "FFM___Wireless_Interface_"."FFM__Net_Interface_pid",
               "FFM___Wireless_Interface_".__raw_txpower,
               "FFM___Wireless_Interface_".bssid,
               "FFM___Wireless_Interface_".essid,
               "FFM___Wireless_Interface_".mode,
               "FFM___Wireless_Interface_".standard_pid,
               "FFM___Wireless_Interface_".txpower
        FROM "FFM___Wireless_Interface_"
    FFM.Virtual_Wireless_Interface FFM.Net_Interface
        SELECT "FFM__Virtual_Wireless_Interface"."FFM___Wireless_Interface__pid",
               "FFM__Virtual_Wireless_Interface".hardware_pid
        FROM "FFM__Virtual_Wireless_Interface"
    FFM.Wireless_Interface FFM.Net_Interface
        SELECT "FFM__Wireless_Interface"."FFM___Wireless_Interface__pid"
        FROM "FFM__Wireless_Interface"
    FFM.Regulatory_Permission
        SELECT "FFM__Regulatory_Permission"."need_DFS",
               "FFM__Regulatory_Permission".__band___raw_lower,
               "FFM__Regulatory_Permission".__band___raw_upper,
               "FFM__Regulatory_Permission".__band_lower,
               "FFM__Regulatory_Permission".__band_upper,
               "FFM__Regulatory_Permission".__raw_bandwidth,
               "FFM__Regulatory_Permission".__raw_eirp,
               "FFM__Regulatory_Permission".bandwidth,
               "FFM__Regulatory_Permission".eirp,
               "FFM__Regulatory_Permission".electric,
               "FFM__Regulatory_Permission".gain,
               "FFM__Regulatory_Permission".indoor_only,
               "FFM__Regulatory_Permission".last_cid,
               "FFM__Regulatory_Permission".left_pid,
               "FFM__Regulatory_Permission".pid,
               "FFM__Regulatory_Permission".type_name,
               "FFM__Regulatory_Permission".x_locked
        FROM "FFM__Regulatory_Permission"
    FFM.Routing_Zone_OLSR
        SELECT "FFM__Routing_Zone_OLSR".electric,
               "FFM__Routing_Zone_OLSR".last_cid,
               "FFM__Routing_Zone_OLSR".left_pid,
               "FFM__Routing_Zone_OLSR".pid,
               "FFM__Routing_Zone_OLSR".type_name,
               "FFM__Routing_Zone_OLSR".x_locked
        FROM "FFM__Routing_Zone_OLSR"
    FFM.Wireless_Channel
        SELECT "FFM__Wireless_Channel".__raw_frequency,
               "FFM__Wireless_Channel".electric,
               "FFM__Wireless_Channel".frequency,
               "FFM__Wireless_Channel".last_cid,
               "FFM__Wireless_Channel".left_pid,
               "FFM__Wireless_Channel".number,
               "FFM__Wireless_Channel".pid,
               "FFM__Wireless_Channel".type_name,
               "FFM__Wireless_Channel".x_locked
        FROM "FFM__Wireless_Channel"
    FFM.WPA_Credentials
        SELECT "FFM__WPA_Credentials".electric,
               "FFM__WPA_Credentials".key,
               "FFM__WPA_Credentials".last_cid,
               "FFM__WPA_Credentials".left_pid,
               "FFM__WPA_Credentials".pid,
               "FFM__WPA_Credentials".type_name,
               "FFM__WPA_Credentials".x_locked
        FROM "FFM__WPA_Credentials"
    FFM.Device_Type_made_by_Company
        SELECT "FFM__Device_Type_made_by_Company".electric,
               "FFM__Device_Type_made_by_Company".last_cid,
               "FFM__Device_Type_made_by_Company".left_pid,
               "FFM__Device_Type_made_by_Company".pid,
               "FFM__Device_Type_made_by_Company".right_pid,
               "FFM__Device_Type_made_by_Company".type_name,
               "FFM__Device_Type_made_by_Company".x_locked
        FROM "FFM__Device_Type_made_by_Company"
    FFM.Firmware_Binary_in_Firmware_Bundle
        SELECT "FFM__Firmware_Binary_in_Firmware_Bundle".electric,
               "FFM__Firmware_Binary_in_Firmware_Bundle".last_cid,
               "FFM__Firmware_Binary_in_Firmware_Bundle".left_pid,
               "FFM__Firmware_Binary_in_Firmware_Bundle".pid,
               "FFM__Firmware_Binary_in_Firmware_Bundle".right_pid,
               "FFM__Firmware_Binary_in_Firmware_Bundle".type_name,
               "FFM__Firmware_Binary_in_Firmware_Bundle".x_locked
        FROM "FFM__Firmware_Binary_in_Firmware_Bundle"
    FFM.Virtual_Wireless_Interface_in_IP4_Network
        SELECT "FFM__Virtual_Wireless_Interface_in_IP4_Network".electric,
               "FFM__Virtual_Wireless_Interface_in_IP4_Network".last_cid,
               "FFM__Virtual_Wireless_Interface_in_IP4_Network".left_pid,
               "FFM__Virtual_Wireless_Interface_in_IP4_Network".mask_len,
               "FFM__Virtual_Wireless_Interface_in_IP4_Network".pid,
               "FFM__Virtual_Wireless_Interface_in_IP4_Network".right_pid,
               "FFM__Virtual_Wireless_Interface_in_IP4_Network".type_name,
               "FFM__Virtual_Wireless_Interface_in_IP4_Network".x_locked
        FROM "FFM__Virtual_Wireless_Interface_in_IP4_Network"
    FFM.Wired_Interface_in_IP4_Network
        SELECT "FFM__Wired_Interface_in_IP4_Network".electric,
               "FFM__Wired_Interface_in_IP4_Network".last_cid,
               "FFM__Wired_Interface_in_IP4_Network".left_pid,
               "FFM__Wired_Interface_in_IP4_Network".mask_len,
               "FFM__Wired_Interface_in_IP4_Network".pid,
               "FFM__Wired_Interface_in_IP4_Network".right_pid,
               "FFM__Wired_Interface_in_IP4_Network".type_name,
               "FFM__Wired_Interface_in_IP4_Network".x_locked
        FROM "FFM__Wired_Interface_in_IP4_Network"
    FFM.Wireless_Interface_in_IP4_Network
        SELECT "FFM__Wireless_Interface_in_IP4_Network".electric,
               "FFM__Wireless_Interface_in_IP4_Network".last_cid,
               "FFM__Wireless_Interface_in_IP4_Network".left_pid,
               "FFM__Wireless_Interface_in_IP4_Network".mask_len,
               "FFM__Wireless_Interface_in_IP4_Network".pid,
               "FFM__Wireless_Interface_in_IP4_Network".right_pid,
               "FFM__Wireless_Interface_in_IP4_Network".type_name,
               "FFM__Wireless_Interface_in_IP4_Network".x_locked
        FROM "FFM__Wireless_Interface_in_IP4_Network"
    FFM.Virtual_Wireless_Interface_in_IP6_Network
        SELECT "FFM__Virtual_Wireless_Interface_in_IP6_Network".electric,
               "FFM__Virtual_Wireless_Interface_in_IP6_Network".last_cid,
               "FFM__Virtual_Wireless_Interface_in_IP6_Network".left_pid,
               "FFM__Virtual_Wireless_Interface_in_IP6_Network".mask_len,
               "FFM__Virtual_Wireless_Interface_in_IP6_Network".pid,
               "FFM__Virtual_Wireless_Interface_in_IP6_Network".right_pid,
               "FFM__Virtual_Wireless_Interface_in_IP6_Network".type_name,
               "FFM__Virtual_Wireless_Interface_in_IP6_Network".x_locked
        FROM "FFM__Virtual_Wireless_Interface_in_IP6_Network"
    FFM.Wired_Interface_in_IP6_Network
        SELECT "FFM__Wired_Interface_in_IP6_Network".electric,
               "FFM__Wired_Interface_in_IP6_Network".last_cid,
               "FFM__Wired_Interface_in_IP6_Network".left_pid,
               "FFM__Wired_Interface_in_IP6_Network".mask_len,
               "FFM__Wired_Interface_in_IP6_Network".pid,
               "FFM__Wired_Interface_in_IP6_Network".right_pid,
               "FFM__Wired_Interface_in_IP6_Network".type_name,
               "FFM__Wired_Interface_in_IP6_Network".x_locked
        FROM "FFM__Wired_Interface_in_IP6_Network"
    FFM.Wireless_Interface_in_IP6_Network
        SELECT "FFM__Wireless_Interface_in_IP6_Network".electric,
               "FFM__Wireless_Interface_in_IP6_Network".last_cid,
               "FFM__Wireless_Interface_in_IP6_Network".left_pid,
               "FFM__Wireless_Interface_in_IP6_Network".mask_len,
               "FFM__Wireless_Interface_in_IP6_Network".pid,
               "FFM__Wireless_Interface_in_IP6_Network".right_pid,
               "FFM__Wireless_Interface_in_IP6_Network".type_name,
               "FFM__Wireless_Interface_in_IP6_Network".x_locked
        FROM "FFM__Wireless_Interface_in_IP6_Network"
    FFM.Net_Link
        SELECT "FFM__Net_Link".electric,
               "FFM__Net_Link".last_cid,
               "FFM__Net_Link".left_pid,
               "FFM__Net_Link".pid,
               "FFM__Net_Link".right_pid,
               "FFM__Net_Link".type_name,
               "FFM__Net_Link".x_locked
        FROM "FFM__Net_Link"
    FFM.Person_acts_for_Legal_Entity
        SELECT "FFM__Person_acts_for_Legal_Entity".electric,
               "FFM__Person_acts_for_Legal_Entity".last_cid,
               "FFM__Person_acts_for_Legal_Entity".left_pid,
               "FFM__Person_acts_for_Legal_Entity".pid,
               "FFM__Person_acts_for_Legal_Entity".right_pid,
               "FFM__Person_acts_for_Legal_Entity".type_name,
               "FFM__Person_acts_for_Legal_Entity".x_locked
        FROM "FFM__Person_acts_for_Legal_Entity"
    FFM.Person_mentors_Person
        SELECT "FFM__Person_mentors_Person".electric,
               "FFM__Person_mentors_Person".last_cid,
               "FFM__Person_mentors_Person".left_pid,
               "FFM__Person_mentors_Person".pid,
               "FFM__Person_mentors_Person".right_pid,
               "FFM__Person_mentors_Person".type_name,
               "FFM__Person_mentors_Person".x_locked
        FROM "FFM__Person_mentors_Person"
    FFM.Wireless_Interface_uses_Antenna
        SELECT "FFM__Wireless_Interface_uses_Antenna".electric,
               "FFM__Wireless_Interface_uses_Antenna".last_cid,
               "FFM__Wireless_Interface_uses_Antenna".left_pid,
               "FFM__Wireless_Interface_uses_Antenna".pid,
               "FFM__Wireless_Interface_uses_Antenna".relative_height,
               "FFM__Wireless_Interface_uses_Antenna".right_pid,
               "FFM__Wireless_Interface_uses_Antenna".type_name,
               "FFM__Wireless_Interface_uses_Antenna".x_locked
        FROM "FFM__Wireless_Interface_uses_Antenna"
    FFM.Wireless_Interface_uses_Wireless_Channel
        SELECT "FFM__Wireless_Interface_uses_Wireless_Channel".electric,
               "FFM__Wireless_Interface_uses_Wireless_Channel".last_cid,
               "FFM__Wireless_Interface_uses_Wireless_Channel".left_pid,
               "FFM__Wireless_Interface_uses_Wireless_Channel".pid,
               "FFM__Wireless_Interface_uses_Wireless_Channel".right_pid,
               "FFM__Wireless_Interface_uses_Wireless_Channel".type_name,
               "FFM__Wireless_Interface_uses_Wireless_Channel".x_locked
        FROM "FFM__Wireless_Interface_uses_Wireless_Channel"
    FFM.Antenna_Type
        SELECT "FFM__Antenna_Type"."desc",
               "FFM__Antenna_Type".__raw_model_no,
               "FFM__Antenna_Type".__raw_name,
               "FFM__Antenna_Type".__raw_revision,
               "FFM__Antenna_Type".electric,
               "FFM__Antenna_Type".gain,
               "FFM__Antenna_Type".last_cid,
               "FFM__Antenna_Type".model_no,
               "FFM__Antenna_Type".name,
               "FFM__Antenna_Type".pid,
               "FFM__Antenna_Type".polarization,
               "FFM__Antenna_Type".revision,
               "FFM__Antenna_Type".type_name,
               "FFM__Antenna_Type".x_locked
        FROM "FFM__Antenna_Type"
    FFM.Net_Device_Type
        SELECT "FFM__Net_Device_Type"."desc",
               "FFM__Net_Device_Type".__raw_model_no,
               "FFM__Net_Device_Type".__raw_name,
               "FFM__Net_Device_Type".__raw_revision,
               "FFM__Net_Device_Type".electric,
               "FFM__Net_Device_Type".last_cid,
               "FFM__Net_Device_Type".model_no,
               "FFM__Net_Device_Type".name,
               "FFM__Net_Device_Type".pid,
               "FFM__Net_Device_Type".revision,
               "FFM__Net_Device_Type".type_name,
               "FFM__Net_Device_Type".x_locked
        FROM "FFM__Net_Device_Type"
    FFM.Firmware_Type
        SELECT "FFM__Firmware_Type".electric,
               "FFM__Firmware_Type".last_cid,
               "FFM__Firmware_Type".name,
               "FFM__Firmware_Type".pid,
               "FFM__Firmware_Type".type_name,
               "FFM__Firmware_Type".url,
               "FFM__Firmware_Type".x_locked
        FROM "FFM__Firmware_Type"
    FFM.IP4_Network
        SELECT "FFM__IP4_Network"."desc",
               "FFM__IP4_Network".__net_address_address,
               "FFM__IP4_Network".__net_address_mask_len,
               "FFM__IP4_Network".__net_address_numeric_address,
               "FFM__IP4_Network".__net_address_upper_bound,
               "FFM__IP4_Network".cool_down,
               "FFM__IP4_Network".electric,
               "FFM__IP4_Network".has_children,
               "FFM__IP4_Network".last_cid,
               "FFM__IP4_Network".owner_pid,
               "FFM__IP4_Network".pid,
               "FFM__IP4_Network".pool_pid,
               "FFM__IP4_Network".type_name,
               "FFM__IP4_Network".x_locked
        FROM "FFM__IP4_Network"
    FFM.IP6_Network
        SELECT "FFM__IP6_Network"."desc",
               "FFM__IP6_Network".__net_address_address,
               "FFM__IP6_Network".__net_address_mask_len,
               "FFM__IP6_Network".__net_address_numeric_address_high,
               "FFM__IP6_Network".__net_address_numeric_address_low,
               "FFM__IP6_Network".__net_address_upper_bound_high,
               "FFM__IP6_Network".__net_address_upper_bound_low,
               "FFM__IP6_Network".cool_down,
               "FFM__IP6_Network".electric,
               "FFM__IP6_Network".has_children,
               "FFM__IP6_Network".last_cid,
               "FFM__IP6_Network".owner_pid,
               "FFM__IP6_Network".pid,
               "FFM__IP6_Network".pool_pid,
               "FFM__IP6_Network".type_name,
               "FFM__IP6_Network".x_locked
        FROM "FFM__IP6_Network"
    FFM.Regulatory_Domain
        SELECT "FFM__Regulatory_Domain".__raw_countrycode,
               "FFM__Regulatory_Domain".countrycode,
               "FFM__Regulatory_Domain".electric,
               "FFM__Regulatory_Domain".last_cid,
               "FFM__Regulatory_Domain".pid,
               "FFM__Regulatory_Domain".type_name,
               "FFM__Regulatory_Domain".x_locked
        FROM "FFM__Regulatory_Domain"
    FFM.Wireless_Standard
        SELECT "FFM__Wireless_Standard".__raw_bandwidth,
               "FFM__Wireless_Standard".__raw_name,
               "FFM__Wireless_Standard".bandwidth,
               "FFM__Wireless_Standard".electric,
               "FFM__Wireless_Standard".last_cid,
               "FFM__Wireless_Standard".name,
               "FFM__Wireless_Standard".pid,
               "FFM__Wireless_Standard".type_name,
               "FFM__Wireless_Standard".x_locked
        FROM "FFM__Wireless_Standard"
    FFM.Zone
        SELECT "FFM__Zone".__raw_name,
               "FFM__Zone".electric,
               "FFM__Zone".last_cid,
               "FFM__Zone".name,
               "FFM__Zone".pid,
               "FFM__Zone".type_name,
               "FFM__Zone".x_locked
        FROM "FFM__Zone"
    PAP.Address_Position
        SELECT "PAP__Address_Position".__position___raw_lat,
               "PAP__Address_Position".__position___raw_lon,
               "PAP__Address_Position".__position_height,
               "PAP__Address_Position".__position_lat,
               "PAP__Address_Position".__position_lon,
               "PAP__Address_Position".electric,
               "PAP__Address_Position".last_cid,
               "PAP__Address_Position".left_pid,
               "PAP__Address_Position".pid,
               "PAP__Address_Position".type_name,
               "PAP__Address_Position".x_locked
        FROM "PAP__Address_Position"
    SRM.Boat
        SELECT "SRM__Boat".__raw_sail_number,
               "SRM__Boat".__raw_sail_number_x,
               "SRM__Boat".electric,
               "SRM__Boat".last_cid,
               "SRM__Boat".left_pid,
               "SRM__Boat".name,
               "SRM__Boat".nation,
               "SRM__Boat".pid,
               "SRM__Boat".sail_number,
               "SRM__Boat".sail_number_x,
               "SRM__Boat".type_name,
               "SRM__Boat".x_locked
        FROM "SRM__Boat"
    SRM.Race_Result
        SELECT "SRM__Race_Result".discarded,
               "SRM__Race_Result".electric,
               "SRM__Race_Result".last_cid,
               "SRM__Race_Result".left_pid,
               "SRM__Race_Result".pid,
               "SRM__Race_Result".points,
               "SRM__Race_Result".race,
               "SRM__Race_Result".status,
               "SRM__Race_Result".type_name,
               "SRM__Race_Result".x_locked
        FROM "SRM__Race_Result"
    SRM.Regatta
        SELECT "SRM__Regatta".__result_date,
               "SRM__Regatta".__result_software,
               "SRM__Regatta".__result_status,
               "SRM__Regatta".boat_class_pid,
               "SRM__Regatta".discards,
               "SRM__Regatta".electric,
               "SRM__Regatta".is_cancelled,
               "SRM__Regatta".kind,
               "SRM__Regatta".last_cid,
               "SRM__Regatta".left_pid,
               "SRM__Regatta".perma_name,
               "SRM__Regatta".pid,
               "SRM__Regatta".races,
               "SRM__Regatta".type_name,
               "SRM__Regatta".x_locked
        FROM "SRM__Regatta"
    SRM.Regatta_C SRM.Regatta
        SELECT "SRM__Regatta_C"."SRM__Regatta_pid",
               "SRM__Regatta_C".is_team_race
        FROM "SRM__Regatta_C"
    SRM.Regatta_H SRM.Regatta
        SELECT "SRM__Regatta_H"."SRM__Regatta_pid"
        FROM "SRM__Regatta_H"
    SRM.Sailor
        SELECT "SRM__Sailor".__raw_mna_number,
               "SRM__Sailor".club_pid,
               "SRM__Sailor".electric,
               "SRM__Sailor".last_cid,
               "SRM__Sailor".left_pid,
               "SRM__Sailor".mna_number,
               "SRM__Sailor".nation,
               "SRM__Sailor".pid,
               "SRM__Sailor".type_name,
               "SRM__Sailor".x_locked
        FROM "SRM__Sailor"
    SRM.Team
        SELECT "SRM__Team"."desc",
               "SRM__Team".__raw_name,
               "SRM__Team".club_pid,
               "SRM__Team".electric,
               "SRM__Team".last_cid,
               "SRM__Team".leader_pid,
               "SRM__Team".left_pid,
               "SRM__Team".name,
               "SRM__Team".pid,
               "SRM__Team".place,
               "SRM__Team".registration_date,
               "SRM__Team".type_name,
               "SRM__Team".x_locked
        FROM "SRM__Team"
    SWP.Clip_O
        SELECT "SWP__Clip_O".__date_finish,
               "SWP__Clip_O".__date_start,
               "SWP__Clip_O".__date_x_finish,
               "SWP__Clip_O".__date_x_start,
               "SWP__Clip_O".abstract,
               "SWP__Clip_O".contents,
               "SWP__Clip_O".electric,
               "SWP__Clip_O".last_cid,
               "SWP__Clip_O".left_pid,
               "SWP__Clip_O".pid,
               "SWP__Clip_O".prio,
               "SWP__Clip_O".type_name,
               "SWP__Clip_O".x_locked
        FROM "SWP__Clip_O"
    SWP.Picture
        SELECT "SWP__Picture".__photo_extension,
               "SWP__Picture".__photo_height,
               "SWP__Picture".__photo_width,
               "SWP__Picture".__thumb_extension,
               "SWP__Picture".__thumb_height,
               "SWP__Picture".__thumb_width,
               "SWP__Picture".electric,
               "SWP__Picture".last_cid,
               "SWP__Picture".left_pid,
               "SWP__Picture".name,
               "SWP__Picture".number,
               "SWP__Picture".pid,
               "SWP__Picture".type_name,
               "SWP__Picture".x_locked
        FROM "SWP__Picture"
    PAP.Person_has_Account
        SELECT "PAP__Person_has_Account".electric,
               "PAP__Person_has_Account".last_cid,
               "PAP__Person_has_Account".left_pid,
               "PAP__Person_has_Account".pid,
               "PAP__Person_has_Account".right_pid,
               "PAP__Person_has_Account".type_name,
               "PAP__Person_has_Account".x_locked
        FROM "PAP__Person_has_Account"
    PAP.Association_has_Address
        SELECT "PAP__Association_has_Address"."desc",
               "PAP__Association_has_Address".electric,
               "PAP__Association_has_Address".last_cid,
               "PAP__Association_has_Address".left_pid,
               "PAP__Association_has_Address".pid,
               "PAP__Association_has_Address".right_pid,
               "PAP__Association_has_Address".type_name,
               "PAP__Association_has_Address".x_locked
        FROM "PAP__Association_has_Address"
    PAP.Company_has_Address
        SELECT "PAP__Company_has_Address"."desc",
               "PAP__Company_has_Address".electric,
               "PAP__Company_has_Address".last_cid,
               "PAP__Company_has_Address".left_pid,
               "PAP__Company_has_Address".pid,
               "PAP__Company_has_Address".right_pid,
               "PAP__Company_has_Address".type_name,
               "PAP__Company_has_Address".x_locked
        FROM "PAP__Company_has_Address"
    PAP.Person_has_Address
        SELECT "PAP__Person_has_Address"."desc",
               "PAP__Person_has_Address".electric,
               "PAP__Person_has_Address".last_cid,
               "PAP__Person_has_Address".left_pid,
               "PAP__Person_has_Address".pid,
               "PAP__Person_has_Address".right_pid,
               "PAP__Person_has_Address".type_name,
               "PAP__Person_has_Address".x_locked
        FROM "PAP__Person_has_Address"
    PAP.Association_has_Email
        SELECT "PAP__Association_has_Email"."desc",
               "PAP__Association_has_Email".electric,
               "PAP__Association_has_Email".last_cid,
               "PAP__Association_has_Email".left_pid,
               "PAP__Association_has_Email".pid,
               "PAP__Association_has_Email".right_pid,
               "PAP__Association_has_Email".type_name,
               "PAP__Association_has_Email".x_locked
        FROM "PAP__Association_has_Email"
    PAP.Company_has_Email
        SELECT "PAP__Company_has_Email"."desc",
               "PAP__Company_has_Email".electric,
               "PAP__Company_has_Email".last_cid,
               "PAP__Company_has_Email".left_pid,
               "PAP__Company_has_Email".pid,
               "PAP__Company_has_Email".right_pid,
               "PAP__Company_has_Email".type_name,
               "PAP__Company_has_Email".x_locked
        FROM "PAP__Company_has_Email"
    PAP.Person_has_Email
        SELECT "PAP__Person_has_Email"."desc",
               "PAP__Person_has_Email".electric,
               "PAP__Person_has_Email".last_cid,
               "PAP__Person_has_Email".left_pid,
               "PAP__Person_has_Email".pid,
               "PAP__Person_has_Email".right_pid,
               "PAP__Person_has_Email".type_name,
               "PAP__Person_has_Email".x_locked
        FROM "PAP__Person_has_Email"
    PAP.Association_has_IM_Handle
        SELECT "PAP__Association_has_IM_Handle"."desc",
               "PAP__Association_has_IM_Handle".electric,
               "PAP__Association_has_IM_Handle".last_cid,
               "PAP__Association_has_IM_Handle".left_pid,
               "PAP__Association_has_IM_Handle".pid,
               "PAP__Association_has_IM_Handle".right_pid,
               "PAP__Association_has_IM_Handle".type_name,
               "PAP__Association_has_IM_Handle".x_locked
        FROM "PAP__Association_has_IM_Handle"
    PAP.Company_has_IM_Handle
        SELECT "PAP__Company_has_IM_Handle"."desc",
               "PAP__Company_has_IM_Handle".electric,
               "PAP__Company_has_IM_Handle".last_cid,
               "PAP__Company_has_IM_Handle".left_pid,
               "PAP__Company_has_IM_Handle".pid,
               "PAP__Company_has_IM_Handle".right_pid,
               "PAP__Company_has_IM_Handle".type_name,
               "PAP__Company_has_IM_Handle".x_locked
        FROM "PAP__Company_has_IM_Handle"
    PAP.Node_has_IM_Handle
        SELECT "PAP__Node_has_IM_Handle"."desc",
               "PAP__Node_has_IM_Handle".electric,
               "PAP__Node_has_IM_Handle".last_cid,
               "PAP__Node_has_IM_Handle".left_pid,
               "PAP__Node_has_IM_Handle".pid,
               "PAP__Node_has_IM_Handle".right_pid,
               "PAP__Node_has_IM_Handle".type_name,
               "PAP__Node_has_IM_Handle".x_locked
        FROM "PAP__Node_has_IM_Handle"
    PAP.Person_has_IM_Handle
        SELECT "PAP__Person_has_IM_Handle"."desc",
               "PAP__Person_has_IM_Handle".electric,
               "PAP__Person_has_IM_Handle".last_cid,
               "PAP__Person_has_IM_Handle".left_pid,
               "PAP__Person_has_IM_Handle".pid,
               "PAP__Person_has_IM_Handle".right_pid,
               "PAP__Person_has_IM_Handle".type_name,
               "PAP__Person_has_IM_Handle".x_locked
        FROM "PAP__Person_has_IM_Handle"
    PAP.Association_has_Nickname
        SELECT "PAP__Association_has_Nickname"."desc",
               "PAP__Association_has_Nickname".electric,
               "PAP__Association_has_Nickname".last_cid,
               "PAP__Association_has_Nickname".left_pid,
               "PAP__Association_has_Nickname".pid,
               "PAP__Association_has_Nickname".right_pid,
               "PAP__Association_has_Nickname".type_name,
               "PAP__Association_has_Nickname".x_locked
        FROM "PAP__Association_has_Nickname"
    PAP.Company_has_Nickname
        SELECT "PAP__Company_has_Nickname"."desc",
               "PAP__Company_has_Nickname".electric,
               "PAP__Company_has_Nickname".last_cid,
               "PAP__Company_has_Nickname".left_pid,
               "PAP__Company_has_Nickname".pid,
               "PAP__Company_has_Nickname".right_pid,
               "PAP__Company_has_Nickname".type_name,
               "PAP__Company_has_Nickname".x_locked
        FROM "PAP__Company_has_Nickname"
    PAP.Node_has_Nickname
        SELECT "PAP__Node_has_Nickname"."desc",
               "PAP__Node_has_Nickname".electric,
               "PAP__Node_has_Nickname".last_cid,
               "PAP__Node_has_Nickname".left_pid,
               "PAP__Node_has_Nickname".pid,
               "PAP__Node_has_Nickname".right_pid,
               "PAP__Node_has_Nickname".type_name,
               "PAP__Node_has_Nickname".x_locked
        FROM "PAP__Node_has_Nickname"
    PAP.Person_has_Nickname
        SELECT "PAP__Person_has_Nickname"."desc",
               "PAP__Person_has_Nickname".electric,
               "PAP__Person_has_Nickname".last_cid,
               "PAP__Person_has_Nickname".left_pid,
               "PAP__Person_has_Nickname".pid,
               "PAP__Person_has_Nickname".right_pid,
               "PAP__Person_has_Nickname".type_name,
               "PAP__Person_has_Nickname".x_locked
        FROM "PAP__Person_has_Nickname"
    PAP.Association_has_Phone
        SELECT "PAP__Association_has_Phone"."desc",
               "PAP__Association_has_Phone".electric,
               "PAP__Association_has_Phone".extension,
               "PAP__Association_has_Phone".last_cid,
               "PAP__Association_has_Phone".left_pid,
               "PAP__Association_has_Phone".pid,
               "PAP__Association_has_Phone".right_pid,
               "PAP__Association_has_Phone".type_name,
               "PAP__Association_has_Phone".x_locked
        FROM "PAP__Association_has_Phone"
    PAP.Company_has_Phone
        SELECT "PAP__Company_has_Phone"."desc",
               "PAP__Company_has_Phone".electric,
               "PAP__Company_has_Phone".extension,
               "PAP__Company_has_Phone".last_cid,
               "PAP__Company_has_Phone".left_pid,
               "PAP__Company_has_Phone".pid,
               "PAP__Company_has_Phone".right_pid,
               "PAP__Company_has_Phone".type_name,
               "PAP__Company_has_Phone".x_locked
        FROM "PAP__Company_has_Phone"
    PAP.Person_has_Phone
        SELECT "PAP__Person_has_Phone"."desc",
               "PAP__Person_has_Phone".electric,
               "PAP__Person_has_Phone".extension,
               "PAP__Person_has_Phone".last_cid,
               "PAP__Person_has_Phone".left_pid,
               "PAP__Person_has_Phone".pid,
               "PAP__Person_has_Phone".right_pid,
               "PAP__Person_has_Phone".type_name,
               "PAP__Person_has_Phone".x_locked
        FROM "PAP__Person_has_Phone"
    PAP.Association_has_Url
        SELECT "PAP__Association_has_Url"."desc",
               "PAP__Association_has_Url".electric,
               "PAP__Association_has_Url".last_cid,
               "PAP__Association_has_Url".left_pid,
               "PAP__Association_has_Url".pid,
               "PAP__Association_has_Url".right_pid,
               "PAP__Association_has_Url".type_name,
               "PAP__Association_has_Url".x_locked
        FROM "PAP__Association_has_Url"
    PAP.Company_has_Url
        SELECT "PAP__Company_has_Url"."desc",
               "PAP__Company_has_Url".electric,
               "PAP__Company_has_Url".last_cid,
               "PAP__Company_has_Url".left_pid,
               "PAP__Company_has_Url".pid,
               "PAP__Company_has_Url".right_pid,
               "PAP__Company_has_Url".type_name,
               "PAP__Company_has_Url".x_locked
        FROM "PAP__Company_has_Url"
    PAP.Node_has_Url
        SELECT "PAP__Node_has_Url"."desc",
               "PAP__Node_has_Url".electric,
               "PAP__Node_has_Url".last_cid,
               "PAP__Node_has_Url".left_pid,
               "PAP__Node_has_Url".pid,
               "PAP__Node_has_Url".right_pid,
               "PAP__Node_has_Url".type_name,
               "PAP__Node_has_Url".x_locked
        FROM "PAP__Node_has_Url"
    PAP.Person_has_Url
        SELECT "PAP__Person_has_Url"."desc",
               "PAP__Person_has_Url".electric,
               "PAP__Person_has_Url".last_cid,
               "PAP__Person_has_Url".left_pid,
               "PAP__Person_has_Url".pid,
               "PAP__Person_has_Url".right_pid,
               "PAP__Person_has_Url".type_name,
               "PAP__Person_has_Url".x_locked
        FROM "PAP__Person_has_Url"
    SRM.Boat_in_Regatta
        SELECT "SRM__Boat_in_Regatta".electric,
               "SRM__Boat_in_Regatta".last_cid,
               "SRM__Boat_in_Regatta".left_pid,
               "SRM__Boat_in_Regatta".pid,
               "SRM__Boat_in_Regatta".place,
               "SRM__Boat_in_Regatta".points,
               "SRM__Boat_in_Regatta".rank,
               "SRM__Boat_in_Regatta".registration_date,
               "SRM__Boat_in_Regatta".right_pid,
               "SRM__Boat_in_Regatta".skipper_pid,
               "SRM__Boat_in_Regatta".type_name,
               "SRM__Boat_in_Regatta".x_locked
        FROM "SRM__Boat_in_Regatta"
    SRM.Crew_Member
        SELECT "SRM__Crew_Member".electric,
               "SRM__Crew_Member".key,
               "SRM__Crew_Member".last_cid,
               "SRM__Crew_Member".left_pid,
               "SRM__Crew_Member".pid,
               "SRM__Crew_Member".right_pid,
               "SRM__Crew_Member".role,
               "SRM__Crew_Member".type_name,
               "SRM__Crew_Member".x_locked
        FROM "SRM__Crew_Member"
    SRM.Team_has_Boat_in_Regatta
        SELECT "SRM__Team_has_Boat_in_Regatta".electric,
               "SRM__Team_has_Boat_in_Regatta".last_cid,
               "SRM__Team_has_Boat_in_Regatta".left_pid,
               "SRM__Team_has_Boat_in_Regatta".pid,
               "SRM__Team_has_Boat_in_Regatta".right_pid,
               "SRM__Team_has_Boat_in_Regatta".type_name,
               "SRM__Team_has_Boat_in_Regatta".x_locked
        FROM "SRM__Team_has_Boat_in_Regatta"
    PAP.Address
        SELECT "PAP__Address"."desc",
               "PAP__Address".__raw_city,
               "PAP__Address".__raw_country,
               "PAP__Address".__raw_region,
               "PAP__Address".__raw_street,
               "PAP__Address".__raw_zip,
               "PAP__Address".city,
               "PAP__Address".country,
               "PAP__Address".electric,
               "PAP__Address".last_cid,
               "PAP__Address".pid,
               "PAP__Address".region,
               "PAP__Address".street,
               "PAP__Address".type_name,
               "PAP__Address".x_locked,
               "PAP__Address".zip
        FROM "PAP__Address"
    PAP.Email
        SELECT "PAP__Email"."desc",
               "PAP__Email".__raw_address,
               "PAP__Email".address,
               "PAP__Email".electric,
               "PAP__Email".last_cid,
               "PAP__Email".pid,
               "PAP__Email".type_name,
               "PAP__Email".x_locked
        FROM "PAP__Email"
    PAP.IM_Handle
        SELECT "PAP__IM_Handle"."desc",
               "PAP__IM_Handle".__raw_address,
               "PAP__IM_Handle".address,
               "PAP__IM_Handle".electric,
               "PAP__IM_Handle".last_cid,
               "PAP__IM_Handle".pid,
               "PAP__IM_Handle".protocol,
               "PAP__IM_Handle".type_name,
               "PAP__IM_Handle".x_locked
        FROM "PAP__IM_Handle"
    PAP.Nickname
        SELECT "PAP__Nickname"."desc",
               "PAP__Nickname".electric,
               "PAP__Nickname".last_cid,
               "PAP__Nickname".name,
               "PAP__Nickname".pid,
               "PAP__Nickname".type_name,
               "PAP__Nickname".x_locked
        FROM "PAP__Nickname"
    PAP.Phone
        SELECT "PAP__Phone"."desc",
               "PAP__Phone".area_code,
               "PAP__Phone".country_code,
               "PAP__Phone".electric,
               "PAP__Phone".last_cid,
               "PAP__Phone".number,
               "PAP__Phone".pid,
               "PAP__Phone".type_name,
               "PAP__Phone".x_locked
        FROM "PAP__Phone"
    PAP.Url
        SELECT "PAP__Url"."desc",
               "PAP__Url".electric,
               "PAP__Url".last_cid,
               "PAP__Url".pid,
               "PAP__Url".type_name,
               "PAP__Url".value,
               "PAP__Url".x_locked
        FROM "PAP__Url"
    FFM.Node
        SELECT "FFM__Node".__lifetime_finish,
               "FFM__Node".__lifetime_start,
               "FFM__Node".__position___raw_lat,
               "FFM__Node".__position___raw_lon,
               "FFM__Node".__position_height,
               "FFM__Node".__position_lat,
               "FFM__Node".__position_lon,
               "FFM__Node".__raw_name,
               "FFM__Node".address_pid,
               "FFM__Node".electric,
               "FFM__Node".last_cid,
               "FFM__Node".manager_pid,
               "FFM__Node".name,
               "FFM__Node".owner_pid,
               "FFM__Node".pid,
               "FFM__Node".show_in_map,
               "FFM__Node".type_name,
               "FFM__Node".x_locked
        FROM "FFM__Node"
    PAP.Association
        SELECT "PAP__Association".__lifetime_finish,
               "PAP__Association".__lifetime_start,
               "PAP__Association".__raw_name,
               "PAP__Association".__raw_short_name,
               "PAP__Association".electric,
               "PAP__Association".last_cid,
               "PAP__Association".name,
               "PAP__Association".pid,
               "PAP__Association".short_name,
               "PAP__Association".type_name,
               "PAP__Association".x_locked
        FROM "PAP__Association"
    PAP.Company
        SELECT "PAP__Company".__lifetime_finish,
               "PAP__Company".__lifetime_start,
               "PAP__Company".__raw_name,
               "PAP__Company".__raw_registered_in,
               "PAP__Company".__raw_short_name,
               "PAP__Company".electric,
               "PAP__Company".last_cid,
               "PAP__Company".name,
               "PAP__Company".pid,
               "PAP__Company".registered_in,
               "PAP__Company".short_name,
               "PAP__Company".type_name,
               "PAP__Company".x_locked
        FROM "PAP__Company"
    PAP.Person
        SELECT "PAP__Person".__lifetime_finish,
               "PAP__Person".__lifetime_start,
               "PAP__Person".__raw_first_name,
               "PAP__Person".__raw_last_name,
               "PAP__Person".__raw_middle_name,
               "PAP__Person".__raw_title,
               "PAP__Person".electric,
               "PAP__Person".first_name,
               "PAP__Person".last_cid,
               "PAP__Person".last_name,
               "PAP__Person".middle_name,
               "PAP__Person".pid,
               "PAP__Person".salutation,
               "PAP__Person".sex,
               "PAP__Person".title,
               "PAP__Person".type_name,
               "PAP__Person".x_locked
        FROM "PAP__Person"
    SRM.Club
        SELECT "SRM__Club".__raw_name,
               "SRM__Club".electric,
               "SRM__Club".last_cid,
               "SRM__Club".long_name,
               "SRM__Club".name,
               "SRM__Club".pid,
               "SRM__Club".type_name,
               "SRM__Club".x_locked
        FROM "SRM__Club"
    SRM.Page SWP.Page
        SELECT "SRM__Page"."SWP__Page_pid",
               "SRM__Page"."desc",
               "SRM__Page".event_pid
        FROM "SRM__Page"
    SRM.Regatta_Event
        SELECT "SRM__Regatta_Event"."desc",
               "SRM__Regatta_Event".__date_finish,
               "SRM__Regatta_Event".__date_start,
               "SRM__Regatta_Event".__raw_name,
               "SRM__Regatta_Event".club_pid,
               "SRM__Regatta_Event".electric,
               "SRM__Regatta_Event".is_cancelled,
               "SRM__Regatta_Event".last_cid,
               "SRM__Regatta_Event".name,
               "SRM__Regatta_Event".perma_name,
               "SRM__Regatta_Event".pid,
               "SRM__Regatta_Event".type_name,
               "SRM__Regatta_Event".x_locked
        FROM "SRM__Regatta_Event"
    SRM._Boat_Class_
        SELECT "SRM___Boat_Class_".__raw_name,
               "SRM___Boat_Class_".electric,
               "SRM___Boat_Class_".last_cid,
               "SRM___Boat_Class_".name,
               "SRM___Boat_Class_".pid,
               "SRM___Boat_Class_".type_name,
               "SRM___Boat_Class_".x_locked
        FROM "SRM___Boat_Class_"
    SRM.Boat_Class SRM._Boat_Class_
        SELECT "SRM__Boat_Class"."SRM___Boat_Class__pid",
               "SRM__Boat_Class".beam,
               "SRM__Boat_Class".loa,
               "SRM__Boat_Class".max_crew,
               "SRM__Boat_Class".sail_area
        FROM "SRM__Boat_Class"
    SRM.Handicap SRM._Boat_Class_
        SELECT "SRM__Handicap"."SRM___Boat_Class__pid"
        FROM "SRM__Handicap"
    SWP.Gallery
        SELECT "SWP__Gallery".__date_finish,
               "SWP__Gallery".__date_start,
               "SWP__Gallery".directory,
               "SWP__Gallery".electric,
               "SWP__Gallery".last_cid,
               "SWP__Gallery".perma_name,
               "SWP__Gallery".pid,
               "SWP__Gallery".short_title,
               "SWP__Gallery".title,
               "SWP__Gallery".type_name,
               "SWP__Gallery".x_locked
        FROM "SWP__Gallery"
    SWP.Page
        SELECT "SWP__Page".__date_finish,
               "SWP__Page".__date_start,
               "SWP__Page".contents,
               "SWP__Page".electric,
               "SWP__Page".format,
               "SWP__Page".head_line,
               "SWP__Page".hidden,
               "SWP__Page".last_cid,
               "SWP__Page".perma_name,
               "SWP__Page".pid,
               "SWP__Page".prio,
               "SWP__Page".short_title,
               "SWP__Page".text,
               "SWP__Page".title,
               "SWP__Page".type_name,
               "SWP__Page".x_locked
        FROM "SWP__Page"
    SWP.Clip_X SWP.Page
        SELECT "SWP__Clip_X"."SWP__Page_pid",
               "SWP__Clip_X".link_to
        FROM "SWP__Clip_X"
    SWP.Page_Y SWP.Page
        SELECT "SWP__Page_Y"."SWP__Page_pid",
               "SWP__Page_Y".year
        FROM "SWP__Page_Y"

"""

_test_tables = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...

    >>> show_tables (scope)
    Auth.Account_in_Group <Table Auth__Account_in_Group>
        Column electric                  : Boolean              Internal__Class_and_Instance_Value Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column left_pid                  : Integer              Link_Role Account left
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column right_pid                 : Integer              Link_Role Group right
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
    Auth.Certificate <Table Auth__Certificate>
        Column __validity_finish         : Datetime             Optional__Nested Date-Time finish
        Column __validity_start          : Datetime             Necessary__Nested Date-Time start
        Column desc                      : Varchar(40)          Primary_Optional String desc
        Column electric                  : Boolean              Internal__Class_and_Instance_Value Boolean electric
        Column email                     : Varchar(80)          Primary Email email
        Column last_cid                  : Integer              Internal Int last_cid
        Column pem                       : Blob                 Internal None pem
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column revocation_date           : Datetime             Optional Date-Time revocation_date
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
    Auth.Group <Table Auth__Group>
        Column desc                      : Varchar(20)          Optional String desc
        Column electric                  : Boolean              Internal__Class_and_Instance_Value Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column name                      : Varchar(32)          Primary Name name
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
    Auth._Account_ <Table Auth___Account_>
        Column electric                  : Boolean              Internal__Class_and_Instance_Value Boolean electric
        Column enabled                   : Boolean              Optional Boolean enabled
        Column last_cid                  : Integer              Internal Int last_cid
        Column name                      : Varchar(80)          Primary Email name
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column superuser                 : Boolean              Optional Boolean superuser
        Column suspended                 : Boolean              Internal Boolean suspended
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
    Auth.Account Auth._Account_ <Table Auth__Account>
        Column Auth___Account__pid       : Integer              ---------- primary ForeignKey(u'Auth___Account_.pid')
        Column password                  : Varchar(120)         Internal String password
        Column ph_name                   : Varchar(64)          Internal__Sticky String ph_name
    EVT.Event <Table EVT__Event>
        Column __date_finish             : Date                 Optional__Nested Date finish
        Column __date_start              : Date                 Necessary__Nested Date start
        Column __time_finish             : Time                 Optional__Nested Time finish
        Column __time_start              : Time                 Necessary__Nested Time start
        Column calendar_pid              : Integer              Primary_Optional__Id_Entity_Reference Entity calendar
        Column detail                    : Varchar(160)         Optional String detail
        Column electric                  : Boolean              Internal__Class_and_Instance_Value Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column left_pid                  : Integer              Link_Role__Init_Only Page left
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column short_title               : Varchar(64)          Optional__Computed_Set String short_title
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
    EVT.Event_occurs <Table EVT__Event_occurs>
        Column __time_finish             : Time                 Optional__Nested Time finish
        Column __time_start              : Time                 Necessary__Nested Time start
        Column date                      : Date                 Primary Date date
        Column last_cid                  : Integer              Internal Int last_cid
        Column left_pid                  : Integer              Link_Role__Init_Only Event left
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
    EVT.Recurrence_Rule <Table EVT__Recurrence_Rule>
        Column count                     : Integer              Optional Int count
        Column desc                      : Varchar(20)          Primary_Optional String desc
        Column easter_offset             : Blob                 Optional__Typed_Collection Int_List easter_offset
        Column electric                  : Boolean              Internal__Class_and_Instance_Value Boolean electric
        Column finish                    : Date                 Optional__Computed_Set Date finish
        Column is_exception              : Boolean              Primary_Optional Boolean is_exception
        Column last_cid                  : Integer              Internal Int last_cid
        Column left_pid                  : Integer              Link_Role__Init_Only Recurrence_Spec left
        Column month                     : Blob                 Optional__Typed_Collection Int_List month
        Column month_day                 : Blob                 Optional__Typed_Collection Int_List month_day
        Column period                    : Integer              Optional Int period
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column restrict_pos              : Blob                 Optional__Typed_Collection Int_List restrict_pos
        Column start                     : Date                 Optional__Computed_Set Date start
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column unit                      : Integer              Optional__Sticky Unit unit
        Column week                      : Blob                 Optional__Typed_Collection Int_List week
        Column week_day                  : Blob                 Optional__Typed_Collection Weekday_RR_List week_day
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
        Column year_day                  : Blob                 Optional__Typed_Collection Int_List year_day
    EVT.Recurrence_Spec <Table EVT__Recurrence_Spec>
        Column date_exceptions           : Blob                 Optional__Typed_Collection Date_List date_exceptions
        Column dates                     : Blob                 Optional__Typed_Collection Date_List dates
        Column electric                  : Boolean              Internal__Class_and_Instance_Value Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column left_pid                  : Integer              Link_Role__Init_Only Event left
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
    EVT.Calendar <Table EVT__Calendar>
        Column desc                      : Varchar(80)          Optional String desc
        Column electric                  : Boolean              Internal__Class_and_Instance_Value Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column name                      : Varchar(32)          Primary Name name
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
    FFM.Firmware_Binary <Table FFM__Firmware_Binary>
        Column electric                  : Boolean              Internal__Class_and_Instance_Value Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column left_pid                  : Integer              Link_Role__Init_Only Firmware_Version left
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
    FFM.Firmware_Bundle <Table FFM__Firmware_Bundle>
        Column electric                  : Boolean              Internal__Class_and_Instance_Value Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column name                      : Varchar(128)         Primary String name
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column version                   : Varchar(16)          Primary String version
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
    FFM.Antenna_Band <Table FFM__Antenna_Band>
        Column __band___raw_lower        : Varchar(60)          Necessary__Raw_Value__Nested Frequency lower
        Column __band___raw_upper        : Varchar(60)          Necessary__Raw_Value__Nested Frequency upper
        Column __band_lower              : Float                Necessary__Raw_Value__Nested Frequency lower
        Column __band_upper              : Float                Necessary__Raw_Value__Nested Frequency upper
        Column electric                  : Boolean              Internal__Class_and_Instance_Value Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column left_pid                  : Integer              Link_Role__Init_Only Antenna_Type left
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
    FFM.Antenna <Table FFM__Antenna>
        Column __raw_azimuth             : Varchar(60)          Required__Raw_Value Angle azimuth
        Column __raw_name                : Varchar(60)          Primary_Optional__Raw_Value String name
        Column azimuth                   : Float                Required__Raw_Value Angle azimuth
        Column desc                      : Text                 Optional Text desc
        Column electric                  : Boolean              Internal__Class_and_Instance_Value Boolean electric
        Column elevation                 : Smallint             Optional__Sticky Int elevation
        Column gain                      : Float                Optional__Computed_Set Float gain
        Column last_cid                  : Integer              Internal Int last_cid
        Column left_pid                  : Integer              Link_Role__Init_Only Antenna_Type left
        Column name                      : Varchar(40)          Primary_Optional__Raw_Value String name
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column polarization              : Integer              Optional__Computed_Set Antenna Polarization polarization
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
    FFM.Net_Device <Table FFM__Net_Device>
        Column __raw_name                : Varchar(60)          Primary_Optional__Raw_Value String name
        Column desc                      : Text                 Optional Text desc
        Column electric                  : Boolean              Internal__Class_and_Instance_Value Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column left_pid                  : Integer              Link_Role__Init_Only Net_Device_Type left
        Column name                      : Varchar(40)          Primary_Optional__Raw_Value String name
        Column node_pid                  : Integer              Query__Auto_Update__Id_Entity_Reference Entity belongs_to_node
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
    FFM.Firmware_Version <Table FFM__Firmware_Version>
        Column electric                  : Boolean              Internal__Class_and_Instance_Value Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column left_pid                  : Integer              Link_Role__Init_Only Firmware_Type left
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column version                   : Varchar(16)          Primary String version
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
    FFM.Net_Interface <Table FFM__Net_Interface>
        Column __raw_name                : Varchar(60)          Primary_Optional__Raw_Value String name
        Column desc                      : Text                 Optional Text desc
        Column electric                  : Boolean              Internal__Class_and_Instance_Value Boolean electric
        Column is_active                 : Boolean              Optional Boolean is_active
        Column last_cid                  : Integer              Internal Int last_cid
        Column left_pid                  : Integer              Link_Role__Init_Only Net_Device left
        Column mac_address               : Varchar(17)          Primary_Optional MAC-address mac_address
        Column name                      : Varchar(63)          Primary_Optional__Raw_Value String name
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
    FFM.Wired_Interface FFM.Net_Interface <Table FFM__Wired_Interface>
        Column FFM__Net_Interface_pid    : Integer              ---------- primary ForeignKey(u'FFM__Net_Interface.pid')
    FFM._Wireless_Interface_ FFM.Net_Interface <Table FFM___Wireless_Interface_>
        Column FFM__Net_Interface_pid    : Integer              ---------- primary ForeignKey(u'FFM__Net_Interface.pid')
        Column __raw_txpower             : Varchar(60)          Optional__Raw_Value TX Power txpower
        Column bssid                     : Varchar(17)          Optional MAC-address bssid
        Column essid                     : Varchar(32)          Optional String essid
        Column mode                      : Varchar(6)           Optional wl-mode mode
        Column standard_pid              : Integer              Necessary__Id_Entity_Reference Entity standard
        Column txpower                   : Float                Optional__Raw_Value TX Power txpower
    FFM.Virtual_Wireless_Interface FFM.Net_Interface <Table FFM__Virtual_Wireless_Interface>
        Column FFM___Wireless_Interface__pid : Integer              ---------- primary ForeignKey(u'FFM___Wireless_Interface_.FFM__Net_Interface_pid')
        Column hardware_pid              : Integer              Primary__Init_Only__Id_Entity_Reference Entity hardware
    FFM.Wireless_Interface FFM.Net_Interface <Table FFM__Wireless_Interface>
        Column FFM___Wireless_Interface__pid : Integer              ---------- primary ForeignKey(u'FFM___Wireless_Interface_.FFM__Net_Interface_pid')
    FFM.Regulatory_Permission <Table FFM__Regulatory_Permission>
        Column __band___raw_lower        : Varchar(60)          Necessary__Raw_Value__Nested Frequency lower
        Column __band___raw_upper        : Varchar(60)          Necessary__Raw_Value__Nested Frequency upper
        Column __band_lower              : Float                Necessary__Raw_Value__Nested Frequency lower
        Column __band_upper              : Float                Necessary__Raw_Value__Nested Frequency upper
        Column __raw_bandwidth           : Varchar(60)          Necessary__Raw_Value Frequency bandwidth
        Column __raw_eirp                : Varchar(60)          Optional__Raw_Value TX Power eirp
        Column bandwidth                 : Float                Necessary__Raw_Value Frequency bandwidth
        Column eirp                      : Float                Optional__Raw_Value TX Power eirp
        Column electric                  : Boolean              Internal__Class_and_Instance_Value Boolean electric
        Column gain                      : Float                Optional Float gain
        Column indoor_only               : Boolean              Necessary Boolean indoor_only
        Column last_cid                  : Integer              Internal Int last_cid
        Column left_pid                  : Integer              Link_Role__Init_Only Regulatory_Domain left
        Column need_DFS                  : Boolean              Necessary Boolean need_DFS
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
    FFM.Routing_Zone_OLSR <Table FFM__Routing_Zone_OLSR>
        Column electric                  : Boolean              Internal__Class_and_Instance_Value Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column left_pid                  : Integer              Link_Role__Init_Only Zone left
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
    FFM.Wireless_Channel <Table FFM__Wireless_Channel>
        Column __raw_frequency           : Varchar(60)          Necessary__Raw_Value Frequency frequency
        Column electric                  : Boolean              Internal__Class_and_Instance_Value Boolean electric
        Column frequency                 : Float                Necessary__Raw_Value Frequency frequency
        Column last_cid                  : Integer              Internal Int last_cid
        Column left_pid                  : Integer              Link_Role__Init_Only Wireless_Standard left
        Column number                    : Integer              Primary Int number
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
    FFM.WPA_Credentials <Table FFM__WPA_Credentials>
        Column electric                  : Boolean              Internal__Class_and_Instance_Value Boolean electric
        Column key                       : Varchar(32)          Required None key
        Column last_cid                  : Integer              Internal Int last_cid
        Column left_pid                  : Integer              Link_Role__Init_Only Net_Interface left
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
    FFM.Device_Type_made_by_Company <Table FFM__Device_Type_made_by_Company>
        Column electric                  : Boolean              Internal__Class_and_Instance_Value Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column left_pid                  : Integer              Link_Role Device_Type left
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column right_pid                 : Integer              Link_Role Company right
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
    FFM.Firmware_Binary_in_Firmware_Bundle <Table FFM__Firmware_Binary_in_Firmware_Bundle>
        Column electric                  : Boolean              Internal__Class_and_Instance_Value Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column left_pid                  : Integer              Link_Role Firmware_Binary left
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column right_pid                 : Integer              Link_Role Firmware_Bundle right
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
    FFM.Virtual_Wireless_Interface_in_IP4_Network <Table FFM__Virtual_Wireless_Interface_in_IP4_Network>
        Column electric                  : Boolean              Internal__Class_and_Instance_Value Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column left_pid                  : Integer              Link_Role Virtual_Wireless_Interface left
        Column mask_len                  : Integer              Required Int mask_len
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column right_pid                 : Integer              Link_Role IP4_Network right
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
    FFM.Wired_Interface_in_IP4_Network <Table FFM__Wired_Interface_in_IP4_Network>
        Column electric                  : Boolean              Internal__Class_and_Instance_Value Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column left_pid                  : Integer              Link_Role Wired_Interface left
        Column mask_len                  : Integer              Required Int mask_len
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column right_pid                 : Integer              Link_Role IP4_Network right
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
    FFM.Wireless_Interface_in_IP4_Network <Table FFM__Wireless_Interface_in_IP4_Network>
        Column electric                  : Boolean              Internal__Class_and_Instance_Value Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column left_pid                  : Integer              Link_Role Wireless_Interface left
        Column mask_len                  : Integer              Required Int mask_len
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column right_pid                 : Integer              Link_Role IP4_Network right
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
    FFM.Virtual_Wireless_Interface_in_IP6_Network <Table FFM__Virtual_Wireless_Interface_in_IP6_Network>
        Column electric                  : Boolean              Internal__Class_and_Instance_Value Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column left_pid                  : Integer              Link_Role Virtual_Wireless_Interface left
        Column mask_len                  : Integer              Required Int mask_len
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column right_pid                 : Integer              Link_Role IP6_Network right
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
    FFM.Wired_Interface_in_IP6_Network <Table FFM__Wired_Interface_in_IP6_Network>
        Column electric                  : Boolean              Internal__Class_and_Instance_Value Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column left_pid                  : Integer              Link_Role Wired_Interface left
        Column mask_len                  : Integer              Required Int mask_len
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column right_pid                 : Integer              Link_Role IP6_Network right
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
    FFM.Wireless_Interface_in_IP6_Network <Table FFM__Wireless_Interface_in_IP6_Network>
        Column electric                  : Boolean              Internal__Class_and_Instance_Value Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column left_pid                  : Integer              Link_Role Wireless_Interface left
        Column mask_len                  : Integer              Required Int mask_len
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column right_pid                 : Integer              Link_Role IP6_Network right
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
    FFM.Net_Link <Table FFM__Net_Link>
        Column electric                  : Boolean              Internal__Class_and_Instance_Value Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column left_pid                  : Integer              Link_Role Net_Interface left
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column right_pid                 : Integer              Link_Role Net_Interface right
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
    FFM.Person_acts_for_Legal_Entity <Table FFM__Person_acts_for_Legal_Entity>
        Column electric                  : Boolean              Internal__Class_and_Instance_Value Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column left_pid                  : Integer              Link_Role Person left
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column right_pid                 : Integer              Link_Role Legal_Entity right
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
    FFM.Person_mentors_Person <Table FFM__Person_mentors_Person>
        Column electric                  : Boolean              Internal__Class_and_Instance_Value Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column left_pid                  : Integer              Link_Role Person left
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column right_pid                 : Integer              Link_Role Person right
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
    FFM.Wireless_Interface_uses_Antenna <Table FFM__Wireless_Interface_uses_Antenna>
        Column electric                  : Boolean              Internal__Class_and_Instance_Value Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column left_pid                  : Integer              Link_Role Wireless_Interface left
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column relative_height           : Float                Optional__Sticky Float relative_height
        Column right_pid                 : Integer              Link_Role Antenna right
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
    FFM.Wireless_Interface_uses_Wireless_Channel <Table FFM__Wireless_Interface_uses_Wireless_Channel>
        Column electric                  : Boolean              Internal__Class_and_Instance_Value Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column left_pid                  : Integer              Link_Role Wireless_Interface left
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column right_pid                 : Integer              Link_Role Wireless_Channel right
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
    FFM.Antenna_Type <Table FFM__Antenna_Type>
        Column __raw_model_no            : Varchar(60)          Primary_Optional__Raw_Value String model_no
        Column __raw_name                : Varchar(60)          Primary__Raw_Value String name
        Column __raw_revision            : Varchar(60)          Primary_Optional__Raw_Value String revision
        Column desc                      : Text                 Optional Text desc
        Column electric                  : Boolean              Internal__Class_and_Instance_Value Boolean electric
        Column gain                      : Float                Necessary Float gain
        Column last_cid                  : Integer              Internal Int last_cid
        Column model_no                  : Varchar(40)          Primary_Optional__Raw_Value String model_no
        Column name                      : Varchar(40)          Primary__Raw_Value String name
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column polarization              : Integer              Necessary Antenna Polarization polarization
        Column revision                  : Varchar(32)          Primary_Optional__Raw_Value String revision
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
    FFM.Net_Device_Type <Table FFM__Net_Device_Type>
        Column __raw_model_no            : Varchar(60)          Primary_Optional__Raw_Value String model_no
        Column __raw_name                : Varchar(60)          Primary__Raw_Value String name
        Column __raw_revision            : Varchar(60)          Primary_Optional__Raw_Value String revision
        Column desc                      : Text                 Optional Text desc
        Column electric                  : Boolean              Internal__Class_and_Instance_Value Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column model_no                  : Varchar(40)          Primary_Optional__Raw_Value String model_no
        Column name                      : Varchar(40)          Primary__Raw_Value String name
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column revision                  : Varchar(32)          Primary_Optional__Raw_Value String revision
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
    FFM.Firmware_Type <Table FFM__Firmware_Type>
        Column electric                  : Boolean              Internal__Class_and_Instance_Value Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column name                      : Varchar(128)         Primary String name
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column url                       : Varchar(160)         Primary Url url
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
    FFM.IP4_Network <Table FFM__IP4_Network>
        Column __net_address_address     : Varchar(18)          Necessary__Nested IP4-network address
        Column __net_address_mask_len    : Integer              Internal__Auto_Update__Nested Int mask_len
        Column __net_address_numeric_address : Integer              Internal__Auto_Update__Nested Int numeric_address
        Column __net_address_upper_bound : Integer              Internal__Auto_Update__Nested Int upper_bound
        Column cool_down                 : Datetime             Internal Date-Time cool_down
        Column desc                      : Varchar(80)          Optional String desc
        Column electric                  : Boolean              Internal__Class_and_Instance_Value Boolean electric
        Column has_children              : Boolean              Internal Boolean has_children
        Column last_cid                  : Integer              Internal Int last_cid
        Column owner_pid                 : Integer              Optional__Id_Entity_Reference Entity owner
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column pool_pid                  : Integer              Optional__Id_Entity_Reference Entity pool
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
    FFM.IP6_Network <Table FFM__IP6_Network>
        Column __net_address_address     : Varchar(43)          Necessary__Nested IP6-network address
        Column __net_address_mask_len    : Integer              Internal__Auto_Update__Nested Int mask_len
        Column __net_address_numeric_address_high : Bigint               Internal__Auto_Update__Nested Int numeric_address_high
        Column __net_address_numeric_address_low : Bigint               Internal__Auto_Update__Nested Int numeric_address_low
        Column __net_address_upper_bound_high : Bigint               Internal__Auto_Update__Nested Int upper_bound_high
        Column __net_address_upper_bound_low : Bigint               Internal__Auto_Update__Nested Int upper_bound_low
        Column cool_down                 : Datetime             Internal Date-Time cool_down
        Column desc                      : Varchar(80)          Optional String desc
        Column electric                  : Boolean              Internal__Class_and_Instance_Value Boolean electric
        Column has_children              : Boolean              Internal Boolean has_children
        Column last_cid                  : Integer              Internal Int last_cid
        Column owner_pid                 : Integer              Optional__Id_Entity_Reference Entity owner
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column pool_pid                  : Integer              Optional__Id_Entity_Reference Entity pool
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
    FFM.Regulatory_Domain <Table FFM__Regulatory_Domain>
        Column __raw_countrycode         : Varchar(60)          Primary__Raw_Value String countrycode
        Column countrycode               : Varchar(2)           Primary__Raw_Value String countrycode
        Column electric                  : Boolean              Internal__Class_and_Instance_Value Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
    FFM.Wireless_Standard <Table FFM__Wireless_Standard>
        Column __raw_bandwidth           : Varchar(60)          Necessary__Raw_Value Frequency bandwidth
        Column __raw_name                : Varchar(60)          Primary__Raw_Value String name
        Column bandwidth                 : Float                Necessary__Raw_Value Frequency bandwidth
        Column electric                  : Boolean              Internal__Class_and_Instance_Value Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column name                      : Varchar(20)          Primary__Raw_Value String name
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
    FFM.Zone <Table FFM__Zone>
        Column __raw_name                : Varchar(60)          Primary__Raw_Value String name
        Column electric                  : Boolean              Internal__Class_and_Instance_Value Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column name                      : Varchar(64)          Primary__Raw_Value String name
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
    PAP.Address_Position <Table PAP__Address_Position>
        Column __position___raw_lat      : Varchar(60)          Necessary__Raw_Value__Nested Angle lat
        Column __position___raw_lon      : Varchar(60)          Necessary__Raw_Value__Nested Angle lon
        Column __position_height         : Float                Optional__Nested Float height
        Column __position_lat            : Float                Necessary__Raw_Value__Nested Angle lat
        Column __position_lon            : Float                Necessary__Raw_Value__Nested Angle lon
        Column electric                  : Boolean              Internal__Class_and_Instance_Value Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column left_pid                  : Integer              Link_Role__Init_Only Address left
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
    SRM.Boat <Table SRM__Boat>
        Column __raw_sail_number         : Varchar(60)          Primary_Optional__Raw_Value Int sail_number
        Column __raw_sail_number_x       : Varchar(60)          Primary_Optional__Raw_Value String sail_number_x
        Column electric                  : Boolean              Internal__Class_and_Instance_Value Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column left_pid                  : Integer              Link_Role__Init_Only Boat_Class left
        Column name                      : Varchar(48)          Optional String name
        Column nation                    : Varchar(3)           Primary_Optional Nation nation
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column sail_number               : Integer              Primary_Optional__Raw_Value Int sail_number
        Column sail_number_x             : Varchar(8)           Primary_Optional__Raw_Value String sail_number_x
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
    SRM.Race_Result <Table SRM__Race_Result>
        Column discarded                 : Boolean              Optional__Sticky Boolean discarded
        Column electric                  : Boolean              Internal__Class_and_Instance_Value Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column left_pid                  : Integer              Link_Role__Init_Only Boat_in_Regatta left
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column points                    : Integer              Necessary Int points
        Column race                      : Integer              Primary Int race
        Column status                    : Varchar(8)           Optional String status
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
    SRM.Regatta <Table SRM__Regatta>
        Column __result_date             : Datetime             Necessary__Nested Date-Time date
        Column __result_software         : Varchar(64)          Optional__Nested String software
        Column __result_status           : Varchar(64)          Optional__Nested String status
        Column boat_class_pid            : Integer              Primary__Id_Entity_Reference Entity boat_class
        Column discards                  : Integer              Optional Int discards
        Column electric                  : Boolean              Internal__Class_and_Instance_Value Boolean electric
        Column is_cancelled              : Boolean              Optional__Computed_Set Boolean is_cancelled
        Column kind                      : Varchar(32)          Optional String kind
        Column last_cid                  : Integer              Internal Int last_cid
        Column left_pid                  : Integer              Link_Role__Init_Only Regatta_Event left
        Column perma_name                : Varchar(64)          Internal__Auto_Update_Lazy__Computed_Set String perma_name
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column races                     : Integer              Optional Int races
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
    SRM.Regatta_C SRM.Regatta <Table SRM__Regatta_C>
        Column SRM__Regatta_pid          : Integer              ---------- primary ForeignKey(u'SRM__Regatta.pid')
        Column is_team_race              : Boolean              Optional Boolean is_team_race
    SRM.Regatta_H SRM.Regatta <Table SRM__Regatta_H>
        Column SRM__Regatta_pid          : Integer              ---------- primary ForeignKey(u'SRM__Regatta.pid')
    SRM.Sailor <Table SRM__Sailor>
        Column __raw_mna_number          : Varchar(60)          Primary_Optional__Raw_Value Int mna_number
        Column club_pid                  : Integer              Primary_Optional__Id_Entity_Reference Entity club
        Column electric                  : Boolean              Internal__Class_and_Instance_Value Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column left_pid                  : Integer              Link_Role__Init_Only Person left
        Column mna_number                : Integer              Primary_Optional__Raw_Value Int mna_number
        Column nation                    : Varchar(3)           Primary_Optional Nation nation
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
    SRM.Team <Table SRM__Team>
        Column __raw_name                : Varchar(60)          Primary__Raw_Value String name
        Column club_pid                  : Integer              Optional__Id_Entity_Reference Entity club
        Column desc                      : Varchar(160)         Optional String desc
        Column electric                  : Boolean              Internal__Class_and_Instance_Value Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column leader_pid                : Integer              Optional__Id_Entity_Reference Entity leader
        Column left_pid                  : Integer              Link_Role__Init_Only Regatta_C left
        Column name                      : Varchar(64)          Primary__Raw_Value String name
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column place                     : Integer              Optional Int place
        Column registration_date         : Date                 Internal Date registration_date
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
    SWP.Clip_O <Table SWP__Clip_O>
        Column __date_finish             : Date                 Optional__Nested Date finish
        Column __date_start              : Date                 Necessary__Nested Date start
        Column __date_x_finish           : Date                 Optional__Nested Date finish
        Column __date_x_start            : Date                 Necessary__Nested Date start
        Column abstract                  : Text                 Required Text abstract
        Column contents                  : Text                 Internal__Auto_Update Text contents
        Column electric                  : Boolean              Internal__Class_and_Instance_Value Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column left_pid                  : Integer              Link_Role__Init_Only Object_PN left
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column prio                      : Integer              Optional__Sticky Int prio
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
    SWP.Picture <Table SWP__Picture>
        Column __photo_extension         : Varchar(10)          Optional__Init_Only__Nested String extension
        Column __photo_height            : Smallint             Necessary__Nested Y height
        Column __photo_width             : Smallint             Necessary__Nested X width
        Column __thumb_extension         : Varchar(10)          Optional__Init_Only__Nested String extension
        Column __thumb_height            : Smallint             Necessary__Nested Y height
        Column __thumb_width             : Smallint             Necessary__Nested X width
        Column electric                  : Boolean              Internal__Class_and_Instance_Value Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column left_pid                  : Integer              Link_Role__Init_Only Gallery left
        Column name                      : Varchar(100)         Optional__Computed_Set String name
        Column number                    : Integer              Primary Int number
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
    PAP.Person_has_Account <Table PAP__Person_has_Account>
        Column electric                  : Boolean              Internal__Class_and_Instance_Value Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column left_pid                  : Integer              Link_Role Person left
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column right_pid                 : Integer              Link_Role Account right
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
    PAP.Association_has_Address <Table PAP__Association_has_Address>
        Column desc                      : Varchar(20)          Optional__Computed_Set String desc
        Column electric                  : Boolean              Internal__Class_and_Instance_Value Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column left_pid                  : Integer              Link_Role Association left
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column right_pid                 : Integer              Link_Role Address right
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
    PAP.Company_has_Address <Table PAP__Company_has_Address>
        Column desc                      : Varchar(20)          Optional__Computed_Set String desc
        Column electric                  : Boolean              Internal__Class_and_Instance_Value Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column left_pid                  : Integer              Link_Role Company left
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column right_pid                 : Integer              Link_Role Address right
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
    PAP.Person_has_Address <Table PAP__Person_has_Address>
        Column desc                      : Varchar(20)          Optional__Computed_Set String desc
        Column electric                  : Boolean              Internal__Class_and_Instance_Value Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column left_pid                  : Integer              Link_Role Person left
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column right_pid                 : Integer              Link_Role Address right
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
    PAP.Association_has_Email <Table PAP__Association_has_Email>
        Column desc                      : Varchar(20)          Optional__Computed_Set String desc
        Column electric                  : Boolean              Internal__Class_and_Instance_Value Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column left_pid                  : Integer              Link_Role Association left
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column right_pid                 : Integer              Link_Role Email right
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
    PAP.Company_has_Email <Table PAP__Company_has_Email>
        Column desc                      : Varchar(20)          Optional__Computed_Set String desc
        Column electric                  : Boolean              Internal__Class_and_Instance_Value Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column left_pid                  : Integer              Link_Role Company left
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column right_pid                 : Integer              Link_Role Email right
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
    PAP.Person_has_Email <Table PAP__Person_has_Email>
        Column desc                      : Varchar(20)          Optional__Computed_Set String desc
        Column electric                  : Boolean              Internal__Class_and_Instance_Value Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column left_pid                  : Integer              Link_Role Person left
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column right_pid                 : Integer              Link_Role Email right
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
    PAP.Association_has_IM_Handle <Table PAP__Association_has_IM_Handle>
        Column desc                      : Varchar(20)          Optional__Computed_Set String desc
        Column electric                  : Boolean              Internal__Class_and_Instance_Value Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column left_pid                  : Integer              Link_Role Association left
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column right_pid                 : Integer              Link_Role IM_Handle right
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
    PAP.Company_has_IM_Handle <Table PAP__Company_has_IM_Handle>
        Column desc                      : Varchar(20)          Optional__Computed_Set String desc
        Column electric                  : Boolean              Internal__Class_and_Instance_Value Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column left_pid                  : Integer              Link_Role Company left
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column right_pid                 : Integer              Link_Role IM_Handle right
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
    PAP.Node_has_IM_Handle <Table PAP__Node_has_IM_Handle>
        Column desc                      : Varchar(20)          Optional__Computed_Set String desc
        Column electric                  : Boolean              Internal__Class_and_Instance_Value Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column left_pid                  : Integer              Link_Role Node left
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column right_pid                 : Integer              Link_Role IM_Handle right
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
    PAP.Person_has_IM_Handle <Table PAP__Person_has_IM_Handle>
        Column desc                      : Varchar(20)          Optional__Computed_Set String desc
        Column electric                  : Boolean              Internal__Class_and_Instance_Value Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column left_pid                  : Integer              Link_Role Person left
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column right_pid                 : Integer              Link_Role IM_Handle right
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
    PAP.Association_has_Nickname <Table PAP__Association_has_Nickname>
        Column desc                      : Varchar(20)          Optional__Computed_Set String desc
        Column electric                  : Boolean              Internal__Class_and_Instance_Value Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column left_pid                  : Integer              Link_Role Association left
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column right_pid                 : Integer              Link_Role Nickname right
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
    PAP.Company_has_Nickname <Table PAP__Company_has_Nickname>
        Column desc                      : Varchar(20)          Optional__Computed_Set String desc
        Column electric                  : Boolean              Internal__Class_and_Instance_Value Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column left_pid                  : Integer              Link_Role Company left
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column right_pid                 : Integer              Link_Role Nickname right
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
    PAP.Node_has_Nickname <Table PAP__Node_has_Nickname>
        Column desc                      : Varchar(20)          Optional__Computed_Set String desc
        Column electric                  : Boolean              Internal__Class_and_Instance_Value Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column left_pid                  : Integer              Link_Role Node left
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column right_pid                 : Integer              Link_Role Nickname right
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
    PAP.Person_has_Nickname <Table PAP__Person_has_Nickname>
        Column desc                      : Varchar(20)          Optional__Computed_Set String desc
        Column electric                  : Boolean              Internal__Class_and_Instance_Value Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column left_pid                  : Integer              Link_Role Person left
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column right_pid                 : Integer              Link_Role Nickname right
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
    PAP.Association_has_Phone <Table PAP__Association_has_Phone>
        Column desc                      : Varchar(20)          Optional__Computed_Set String desc
        Column electric                  : Boolean              Internal__Class_and_Instance_Value Boolean electric
        Column extension                 : Varchar(5)           Primary_Optional Numeric_String extension
        Column last_cid                  : Integer              Internal Int last_cid
        Column left_pid                  : Integer              Link_Role Association left
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column right_pid                 : Integer              Link_Role Phone right
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
    PAP.Company_has_Phone <Table PAP__Company_has_Phone>
        Column desc                      : Varchar(20)          Optional__Computed_Set String desc
        Column electric                  : Boolean              Internal__Class_and_Instance_Value Boolean electric
        Column extension                 : Varchar(5)           Primary_Optional Numeric_String extension
        Column last_cid                  : Integer              Internal Int last_cid
        Column left_pid                  : Integer              Link_Role Company left
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column right_pid                 : Integer              Link_Role Phone right
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
    PAP.Person_has_Phone <Table PAP__Person_has_Phone>
        Column desc                      : Varchar(20)          Optional__Computed_Set String desc
        Column electric                  : Boolean              Internal__Class_and_Instance_Value Boolean electric
        Column extension                 : Varchar(5)           Primary_Optional Numeric_String extension
        Column last_cid                  : Integer              Internal Int last_cid
        Column left_pid                  : Integer              Link_Role Person left
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column right_pid                 : Integer              Link_Role Phone right
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
    PAP.Association_has_Url <Table PAP__Association_has_Url>
        Column desc                      : Varchar(20)          Optional__Computed_Set String desc
        Column electric                  : Boolean              Internal__Class_and_Instance_Value Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column left_pid                  : Integer              Link_Role Association left
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column right_pid                 : Integer              Link_Role Url right
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
    PAP.Company_has_Url <Table PAP__Company_has_Url>
        Column desc                      : Varchar(20)          Optional__Computed_Set String desc
        Column electric                  : Boolean              Internal__Class_and_Instance_Value Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column left_pid                  : Integer              Link_Role Company left
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column right_pid                 : Integer              Link_Role Url right
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
    PAP.Node_has_Url <Table PAP__Node_has_Url>
        Column desc                      : Varchar(20)          Optional__Computed_Set String desc
        Column electric                  : Boolean              Internal__Class_and_Instance_Value Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column left_pid                  : Integer              Link_Role Node left
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column right_pid                 : Integer              Link_Role Url right
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
    PAP.Person_has_Url <Table PAP__Person_has_Url>
        Column desc                      : Varchar(20)          Optional__Computed_Set String desc
        Column electric                  : Boolean              Internal__Class_and_Instance_Value Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column left_pid                  : Integer              Link_Role Person left
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column right_pid                 : Integer              Link_Role Url right
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
    SRM.Boat_in_Regatta <Table SRM__Boat_in_Regatta>
        Column electric                  : Boolean              Internal__Class_and_Instance_Value Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column left_pid                  : Integer              Link_Role Boat left
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column place                     : Integer              Optional Int place
        Column points                    : Integer              Optional Int points
        Column rank                      : Integer              Internal Int rank
        Column registration_date         : Date                 Internal__Init_Only Date registration_date
        Column right_pid                 : Integer              Link_Role Regatta right
        Column skipper_pid               : Integer              Required__Id_Entity_Reference Entity skipper
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
    SRM.Crew_Member <Table SRM__Crew_Member>
        Column electric                  : Boolean              Internal__Class_and_Instance_Value Boolean electric
        Column key                       : Integer              Optional__Sticky Int key
        Column last_cid                  : Integer              Internal Int last_cid
        Column left_pid                  : Integer              Link_Role Boat_in_Regatta left
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column right_pid                 : Integer              Link_Role Sailor right
        Column role                      : Varchar(32)          Optional String role
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
    SRM.Team_has_Boat_in_Regatta <Table SRM__Team_has_Boat_in_Regatta>
        Column electric                  : Boolean              Internal__Class_and_Instance_Value Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column left_pid                  : Integer              Link_Role Team left
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column right_pid                 : Integer              Link_Role Boat_in_Regatta right
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
    PAP.Address <Table PAP__Address>
        Column __raw_city                : Varchar(60)          Primary__Raw_Value String city
        Column __raw_country             : Varchar(60)          Primary__Raw_Value String country
        Column __raw_region              : Varchar(60)          Optional__Raw_Value String region
        Column __raw_street              : Varchar(60)          Primary__Raw_Value String street
        Column __raw_zip                 : Varchar(60)          Primary__Raw_Value String zip
        Column city                      : Varchar(30)          Primary__Raw_Value String city
        Column country                   : Varchar(20)          Primary__Raw_Value String country
        Column desc                      : Varchar(20)          Optional String desc
        Column electric                  : Boolean              Internal__Class_and_Instance_Value Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column region                    : Varchar(20)          Optional__Raw_Value String region
        Column street                    : Varchar(60)          Primary__Raw_Value String street
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
        Column zip                       : Varchar(6)           Primary__Raw_Value String zip
    PAP.Email <Table PAP__Email>
        Column __raw_address             : Varchar(60)          Primary__Raw_Value Email address
        Column address                   : Varchar(80)          Primary__Raw_Value Email address
        Column desc                      : Varchar(20)          Optional String desc
        Column electric                  : Boolean              Internal__Class_and_Instance_Value Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
    PAP.IM_Handle <Table PAP__IM_Handle>
        Column __raw_address             : Varchar(60)          Primary__Raw_Value String address
        Column address                   : Varchar(80)          Primary__Raw_Value String address
        Column desc                      : Varchar(20)          Optional String desc
        Column electric                  : Boolean              Internal__Class_and_Instance_Value Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column protocol                  : Varchar(16)          Primary im_protocol protocol
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
    PAP.Nickname <Table PAP__Nickname>
        Column desc                      : Varchar(20)          Optional String desc
        Column electric                  : Boolean              Internal__Class_and_Instance_Value Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column name                      : Varchar(32)          Primary String name
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
    PAP.Phone <Table PAP__Phone>
        Column area_code                 : Varchar(5)           Primary Numeric_String area_code
        Column country_code              : Varchar(3)           Primary Numeric_String country_code
        Column desc                      : Varchar(20)          Optional String desc
        Column electric                  : Boolean              Internal__Class_and_Instance_Value Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column number                    : Varchar(14)          Primary Numeric_String number
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
    PAP.Url <Table PAP__Url>
        Column desc                      : Varchar(20)          Optional String desc
        Column electric                  : Boolean              Internal__Class_and_Instance_Value Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column value                     : Varchar(160)         Primary Url value
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
    FFM.Node <Table FFM__Node>
        Column __lifetime_finish         : Date                 Optional__Nested Date finish
        Column __lifetime_start          : Date                 Necessary__Nested Date start
        Column __position___raw_lat      : Varchar(60)          Necessary__Raw_Value__Nested Angle lat
        Column __position___raw_lon      : Varchar(60)          Necessary__Raw_Value__Nested Angle lon
        Column __position_height         : Float                Optional__Nested Float height
        Column __position_lat            : Float                Necessary__Raw_Value__Nested Angle lat
        Column __position_lon            : Float                Necessary__Raw_Value__Nested Angle lon
        Column __raw_name                : Varchar(60)          Primary__Raw_Value String name
        Column address_pid               : Integer              Optional__Id_Entity_Reference Entity address
        Column electric                  : Boolean              Internal__Class_and_Instance_Value Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column manager_pid               : Integer              Required__Id_Entity_Reference Entity manager
        Column name                      : Varchar(63)          Primary__Raw_Value String name
        Column owner_pid                 : Integer              Optional__Computed_Set__Id_Entity_Reference Entity owner
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column show_in_map               : Boolean              Optional Boolean show_in_map
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
    PAP.Association <Table PAP__Association>
        Column __lifetime_finish         : Date                 Optional__Nested Date finish
        Column __lifetime_start          : Date                 Necessary__Nested Date start
        Column __raw_name                : Varchar(60)          Primary__Raw_Value String name
        Column __raw_short_name          : Varchar(60)          Optional__Raw_Value String short_name
        Column electric                  : Boolean              Internal__Class_and_Instance_Value Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column name                      : Varchar(64)          Primary__Raw_Value String name
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column short_name                : Varchar(12)          Optional__Raw_Value String short_name
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
    PAP.Company <Table PAP__Company>
        Column __lifetime_finish         : Date                 Optional__Nested Date finish
        Column __lifetime_start          : Date                 Necessary__Nested Date start
        Column __raw_name                : Varchar(60)          Primary__Raw_Value String name
        Column __raw_registered_in       : Varchar(60)          Primary_Optional__Raw_Value String registered_in
        Column __raw_short_name          : Varchar(60)          Optional__Raw_Value String short_name
        Column electric                  : Boolean              Internal__Class_and_Instance_Value Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column name                      : Varchar(64)          Primary__Raw_Value String name
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column registered_in             : Varchar(64)          Primary_Optional__Raw_Value String registered_in
        Column short_name                : Varchar(12)          Optional__Raw_Value String short_name
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
    PAP.Person <Table PAP__Person>
        Column __lifetime_finish         : Date                 Optional__Nested Date finish
        Column __lifetime_start          : Date                 Necessary__Nested Date start
        Column __raw_first_name          : Varchar(60)          Primary__Raw_Value String first_name
        Column __raw_last_name           : Varchar(60)          Primary__Raw_Value String last_name
        Column __raw_middle_name         : Varchar(60)          Primary_Optional__Raw_Value String middle_name
        Column __raw_title               : Varchar(60)          Primary_Optional__Raw_Value String title
        Column electric                  : Boolean              Internal__Class_and_Instance_Value Boolean electric
        Column first_name                : Varchar(32)          Primary__Raw_Value String first_name
        Column last_cid                  : Integer              Internal Int last_cid
        Column last_name                 : Varchar(48)          Primary__Raw_Value String last_name
        Column middle_name               : Varchar(32)          Primary_Optional__Raw_Value String middle_name
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column salutation                : Varchar(80)          Optional String salutation
        Column sex                       : Varchar(1)           Necessary Sex sex
        Column title                     : Varchar(20)          Primary_Optional__Raw_Value String title
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
    SRM.Club <Table SRM__Club>
        Column __raw_name                : Varchar(60)          Primary__Raw_Value String name
        Column electric                  : Boolean              Internal__Class_and_Instance_Value Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column long_name                 : Varchar(64)          Optional String long_name
        Column name                      : Varchar(8)           Primary__Raw_Value String name
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
    SRM.Page SWP.Page <Table SRM__Page>
        Column SWP__Page_pid             : Integer              ---------- primary ForeignKey(u'SWP__Page.pid')
        Column desc                      : Varchar(30)          Optional__Computed_Set String desc
        Column event_pid                 : Integer              Primary__Id_Entity_Reference Entity event
    SRM.Regatta_Event <Table SRM__Regatta_Event>
        Column __date_finish             : Date                 Optional__Computed_Set__Nested Date finish
        Column __date_start              : Date                 Necessary__Nested Date start
        Column __raw_name                : Varchar(60)          Primary__Raw_Value String name
        Column club_pid                  : Integer              Optional__Id_Entity_Reference Entity club
        Column desc                      : Varchar(160)         Optional String desc
        Column electric                  : Boolean              Internal__Class_and_Instance_Value Boolean electric
        Column is_cancelled              : Boolean              Optional Boolean is_cancelled
        Column last_cid                  : Integer              Internal Int last_cid
        Column name                      : Varchar(64)          Primary__Raw_Value String name
        Column perma_name                : Varchar(64)          Internal__Auto_Update_Lazy__Computed_Set String perma_name
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
    SRM._Boat_Class_ <Table SRM___Boat_Class_>
        Column __raw_name                : Varchar(60)          Primary__Raw_Value String name
        Column electric                  : Boolean              Internal__Class_and_Instance_Value Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column name                      : Varchar(48)          Primary__Raw_Value String name
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
    SRM.Boat_Class SRM._Boat_Class_ <Table SRM__Boat_Class>
        Column SRM___Boat_Class__pid     : Integer              ---------- primary ForeignKey(u'SRM___Boat_Class_.pid')
        Column beam                      : Float                Optional Float beam
        Column loa                       : Float                Optional Float loa
        Column max_crew                  : Smallint             Required Int max_crew
        Column sail_area                 : Float                Optional Float sail_area
    SRM.Handicap SRM._Boat_Class_ <Table SRM__Handicap>
        Column SRM___Boat_Class__pid     : Integer              ---------- primary ForeignKey(u'SRM___Boat_Class_.pid')
    SWP.Gallery <Table SWP__Gallery>
        Column __date_finish             : Date                 Optional__Nested Date finish
        Column __date_start              : Date                 Necessary__Sticky__Nested Date start
        Column directory                 : Text                 Necessary Directory directory
        Column electric                  : Boolean              Internal__Class_and_Instance_Value Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column perma_name                : Varchar(80)          Primary Date-Slug perma_name
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column short_title               : Varchar(30)          Necessary String short_title
        Column title                     : Varchar(120)         Necessary String title
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
    SWP.Page <Table SWP__Page>
        Column __date_finish             : Date                 Optional__Nested Date finish
        Column __date_start              : Date                 Necessary__Sticky__Nested Date start
        Column contents                  : Text                 Internal__Auto_Update Text contents
        Column electric                  : Boolean              Internal__Class_and_Instance_Value Boolean electric
        Column format                    : Varchar(8)           Optional__Sticky Format format
        Column head_line                 : Varchar(256)         Optional String head_line
        Column hidden                    : Boolean              Optional Boolean hidden
        Column last_cid                  : Integer              Internal Int last_cid
        Column perma_name                : Varchar(80)          Primary Date-Slug perma_name
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column prio                      : Integer              Optional__Sticky Int prio
        Column short_title               : Varchar(30)          Necessary String short_title
        Column text                      : Text                 Required Text text
        Column title                     : Varchar(120)         Necessary String title
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal__Class_and_Instance_Value Boolean x_locked
    SWP.Clip_X SWP.Page <Table SWP__Clip_X>
        Column SWP__Page_pid             : Integer              ---------- primary ForeignKey(u'SWP__Page.pid')
        Column link_to                   : Varchar(160)         Optional Url link_to
    SWP.Page_Y SWP.Page <Table SWP__Page_Y>
        Column SWP__Page_pid             : Integer              ---------- primary ForeignKey(u'SWP__Page.pid')
        Column year                      : Integer              Primary_Optional Int year

"""

__test__ = Scaffold.create_test_dict \
    ( dict
        ( test_select  = _test_select
        , test_tables  = _test_tables
        )
    , ignore = "HPS"
    )

### __END__ FFM.__test__.SAS_SQL
