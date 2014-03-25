# -*- coding: utf-8 -*-
# Copyright (C) 2012-2014 Mag. Christian Tanzer All rights reserved
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
#    FFM.__test__.Nodes
#
# Purpose
#    Test Node and associations
#
# Revision Dates
#    19-Sep-2012 (RS) Creation
#    24-Sep-2012 (RS) More tests, up to `Net_Interface_in_IP4_Network`
#    11-Oct-2012 (RS) Fix missing `raw` parameter
#    12-Oct-2012 (RS) Add tests for `Node` in role `Subject`
#    16-Oct-2012 (CT) Add tracebacks triggered by `FFM.Node.refuse_links`
#    17-Dec-2012 (RS) Add tests for attributes of `belongs_to_node`
#     5-Mar-2013 (CT) Adapt to changes in `Net_Interface_in_IP4_Network`
#     7-Mar-2013 (RS) Add test for duplicate network allocation
#    16-Apr-2013 (CT) Add test `auto_children`,
#                     remove `Node_has_Phone`, `Node_has_Email`
#    17-Apr-2013 (CT) Add tests `owner` and `refuse_e_types`
#    18-Apr-2013 (CT) Add test for `eligible_e_types`,
#                     `selectable_e_types_unique_epk`
#     7-Aug-2013 (CT) Adapt to major surgery of GTW.OMP.NET.Attr_Type
#    30-Sep-2013 (CT) Adapt to uplift of `belongs_to_node`
#    ««revision-date»»···
#--

from   __future__ import absolute_import, division, print_function, unicode_literals

from   _FFM.__test__.model      import *
from   _MOM.inspect             import children_trans_iter

from   datetime                 import datetime
from   rsclib.IP_Address        import IP4_Address as R_IP4_Address
from   rsclib.IP_Address        import IP6_Address as R_IP6_Address

_test_code = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...

    >>> FFM = scope.FFM
    >>> PAP = scope.PAP
    >>> Adr = str ### XXX FFM.IP4_Network.net_address.P_Type

    >>> mgr = PAP.Person \\
    ...     (first_name = 'Ralf', last_name = 'Schlatterbeck', raw = True)

    >>> comp = PAP.Company (name = "Open Source Consulting", raw = True)
    >>> node1 = FFM.Node \\
    ...     (name = "nogps", manager = mgr, position = None, raw = True)
    >>> gps1 = dict (lat = "48 d 17 m 9.64 s", lon = "15 d 52 m 27.84 s")
    >>> node2 = FFM.Node \\
    ...     (name = "node2", manager = mgr, position = gps1, raw = True)

    >>> nick = PAP.Nickname ('node-two', raw = True)
    >>> x = PAP.Node_has_Nickname (node2, nick)
    >>> url = PAP.Url ('http://example.com', raw = True)
    >>> x = PAP.Node_has_Url (node2, url)
    >>> adr = PAP.Address \\
    ...     ( street  = 'Example 23'
    ...     , zip     = '1010'
    ...     , city    = 'Wien'
    ...     , country = 'Austria'
    ...     )
    >>> node1.address = adr
    >>> node1.address
    PAP.Address (u'example 23', u'1010', u'wien', u'austria')

    >>> gps2 = dict (lat = "48.367088", lon = "16.187672")
    >>> node3 = FFM.Node \\
    ...    (name = "node3", manager = mgr, owner = comp, position = gps2)
    >>> fmt = '%%Y-%%m-%%d %%H:%%M:%%S'
    >>> t1 = datetime.strptime ("2009-05-05 17:17:17", fmt)
    >>> t2 = datetime.strptime ("2010-05-05 23:23:23", fmt)
    >>> scope.ems.convert_creation_change (node3.pid, c_time = t1, time = t2)
    >>> node3.creation_date
    datetime.datetime(2009, 5, 5, 17, 17, 17)
    >>> node3.last_changed
    datetime.datetime(2010, 5, 5, 23, 23, 23)

    >>> net = FFM.IP4_Network ('192.168.23.0/24', owner = mgr, raw = True)
    >>> a1  = net.reserve (Adr ('192.168.23.1/32'))
    >>> a2  = net.reserve (Adr ('192.168.23.2/32'))
    >>> a3  = net.reserve (Adr ('192.168.23.3/32'))
    >>> a4  = net.reserve (Adr ('192.168.23.4/32'))
    >>> ax  = net.reserve ('192.168.23.42/32')
    >>> devtype = FFM.Net_Device_Type.instance_or_new \\
    ...     (name = 'Generic', raw = True)
    >>> dev = FFM.Net_Device \\
    ...     (left = devtype, node = node3, name = 'dev', raw = True)
    >>> wr  = FFM.Wired_Interface (left = dev, name = 'wr', raw = True)
    >>> wl  = FFM.Wireless_Interface (left = dev, name = 'wl', raw = True)
    >>> ir1 = FFM.Net_Interface_in_IP4_Network (wr, a1, mask_len = 24)
    >>> il1 = FFM.Net_Interface_in_IP4_Network (wl, a2, mask_len = 32)
    >>> ir2 = FFM.Net_Interface_in_IP4_Network (wr, a3, mask_len = 24)
    >>> il2 = FFM.Net_Interface_in_IP4_Network (wl, a4, mask_len = 24)

    >>> irx = FFM.Net_Interface_in_IP4_Network (wr, ax, mask_len = 28)
    Traceback (most recent call last):
      ...
    Invariants: Condition `valid_mask_len` : The `mask_len` must match the one of `right` or of any
    network containing `right`. (mask_len in possible_mask_lens)
        mask_len = 28
        possible_mask_lens = [24, 32] << sorted ( right.ETM.query ( (Q.net_address.CONTAINS (right.net_address))& (Q.electric == False)).attr ("net_address.mask_len"))
        right = 192.168.23.42
        right.net_address = 192.168.23.42

    >>> net2 = FFM.IP4_Network (net_address = '10.0.0.0/8', owner = mgr, raw = True)
    >>> a2_1 = net2.reserve (Adr ('10.139.187.0/27'))
    >>> a2_2 = net2.reserve (Adr ('10.139.187.2'))
    >>> a2_f = net2.reserve (Adr ('10.139.187.0/27'))
    Traceback (most recent call last):
      ...
    Address_Already_Used: Address 10.139.187.0/27 already in use by 'Schlatterbeck Ralf'

    >>> at1 = FFM.Antenna_Type \\
    ...     ( name         = "Yagi1"
    ...     , desc         = "A Yagi"
    ...     , gain         = 17.5
    ...     , polarization = "vertical"
    ...     , raw          = True
    ...     )
    >>> args = dict (left = at1, azimuth = "180", elevation_angle = 0, raw = True)
    >>> a = FFM.Antenna (name = "1", ** args)
    >>> wia = FFM.Wireless_Interface_uses_Antenna (wl, a)

    >>> FFM.Antenna.query (Q.belongs_to_node == node3).count ()
    1

    >>> FFM.Belongs_to_Node.query (Q.belongs_to_node == node3).count ()
    6

    >>> FFM.Net_Device.query (Q.belongs_to_node == node3).count ()
    1

    >>> FFM.Net_Interface.query (Q.belongs_to_node == node3).count ()
    2

    >>> FFM.Node.query (Q.belongs_to_node == node3).count ()
    1

    >>> FFM.Wired_Interface.query (Q.belongs_to_node == node3).count ()
    1

    >>> FFM.Wireless_Interface.query (Q.belongs_to_node == node3).count ()
    1

    >>> FFM.Wireless_Interface_uses_Antenna.query (Q.belongs_to_node == node3).count ()
    1

    >>> FFM.Net_Device.query (Q.belongs_to_node.manager == mgr).count ()
    1

    >>> FFM.Net_Device.query (Q.belongs_to_node != node3).count ()
    0

"""

_test_auto_children = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...

    >>> FFM = scope.FFM
    >>> PAP = scope.PAP

    >>> for T, l in children_trans_iter (scope.PAP.Subject_has_Property) :
    ...     print ("%%-30s %%s" %% ("%%s%%s" %% ("  " * l, T.type_name), sorted (T.children_np_transitive)))
    PAP.Subject_has_Property       ['PAP.Association_has_Address', 'PAP.Association_has_Email', 'PAP.Association_has_IM_Handle', 'PAP.Association_has_Nickname', 'PAP.Association_has_Phone', 'PAP.Association_has_Url', 'PAP.Company_has_Address', 'PAP.Company_has_Email', 'PAP.Company_has_IM_Handle', 'PAP.Company_has_Nickname', 'PAP.Company_has_Phone', 'PAP.Company_has_Url', 'PAP.Node_has_IM_Handle', 'PAP.Node_has_Nickname', 'PAP.Node_has_Url', 'PAP.Person_has_Address', 'PAP.Person_has_Email', 'PAP.Person_has_IM_Handle', 'PAP.Person_has_Nickname', 'PAP.Person_has_Phone', 'PAP.Person_has_Url']
      PAP.Subject_has_IM_Handle    ['PAP.Association_has_IM_Handle', 'PAP.Company_has_IM_Handle', 'PAP.Node_has_IM_Handle', 'PAP.Person_has_IM_Handle']
        PAP.Association_has_IM_Handle ['PAP.Association_has_IM_Handle']
        PAP.Person_has_IM_Handle   ['PAP.Person_has_IM_Handle']
        PAP.Node_has_IM_Handle     ['PAP.Node_has_IM_Handle']
        PAP.Company_has_IM_Handle  ['PAP.Company_has_IM_Handle']
      PAP.Subject_has_Nickname     ['PAP.Association_has_Nickname', 'PAP.Company_has_Nickname', 'PAP.Node_has_Nickname', 'PAP.Person_has_Nickname']
        PAP.Association_has_Nickname ['PAP.Association_has_Nickname']
        PAP.Person_has_Nickname    ['PAP.Person_has_Nickname']
        PAP.Node_has_Nickname      ['PAP.Node_has_Nickname']
        PAP.Company_has_Nickname   ['PAP.Company_has_Nickname']
      PAP.Subject_has_Address      ['PAP.Association_has_Address', 'PAP.Company_has_Address', 'PAP.Person_has_Address']
        PAP.Association_has_Address ['PAP.Association_has_Address']
        PAP.Person_has_Address     ['PAP.Person_has_Address']
        PAP.Company_has_Address    ['PAP.Company_has_Address']
      PAP.Subject_has_Email        ['PAP.Association_has_Email', 'PAP.Company_has_Email', 'PAP.Person_has_Email']
        PAP.Association_has_Email  ['PAP.Association_has_Email']
        PAP.Person_has_Email       ['PAP.Person_has_Email']
        PAP.Company_has_Email      ['PAP.Company_has_Email']
      PAP.Subject_has_Phone        ['PAP.Association_has_Phone', 'PAP.Company_has_Phone', 'PAP.Person_has_Phone']
        PAP.Association_has_Phone  ['PAP.Association_has_Phone']
        PAP.Person_has_Phone       ['PAP.Person_has_Phone']
        PAP.Company_has_Phone      ['PAP.Company_has_Phone']
      PAP.Subject_has_Url          ['PAP.Association_has_Url', 'PAP.Company_has_Url', 'PAP.Node_has_Url', 'PAP.Person_has_Url']
        PAP.Association_has_Url    ['PAP.Association_has_Url']
        PAP.Person_has_Url         ['PAP.Person_has_Url']
        PAP.Node_has_Url           ['PAP.Node_has_Url']
        PAP.Company_has_Url        ['PAP.Company_has_Url']

    >>> for T, l in children_trans_iter (scope.PAP.Subject_has_Property) :
    ...     rr = T.relevant_root.type_name if T.relevant_root else sorted (T.relevant_roots)
    ...     print ("%%-30s %%-5s %%s" %% ("%%s%%s" %% ("  " * l, T.type_name), T.is_partial, rr))
    PAP.Subject_has_Property       True  PAP.Subject_has_Property
      PAP.Subject_has_IM_Handle    True  PAP.Subject_has_Property
        PAP.Association_has_IM_Handle False PAP.Subject_has_Property
        PAP.Person_has_IM_Handle   False PAP.Subject_has_Property
        PAP.Node_has_IM_Handle     False PAP.Subject_has_Property
        PAP.Company_has_IM_Handle  False PAP.Subject_has_Property
      PAP.Subject_has_Nickname     True  PAP.Subject_has_Property
        PAP.Association_has_Nickname False PAP.Subject_has_Property
        PAP.Person_has_Nickname    False PAP.Subject_has_Property
        PAP.Node_has_Nickname      False PAP.Subject_has_Property
        PAP.Company_has_Nickname   False PAP.Subject_has_Property
      PAP.Subject_has_Address      True  PAP.Subject_has_Property
        PAP.Association_has_Address False PAP.Subject_has_Property
        PAP.Person_has_Address     False PAP.Subject_has_Property
        PAP.Company_has_Address    False PAP.Subject_has_Property
      PAP.Subject_has_Email        True  PAP.Subject_has_Property
        PAP.Association_has_Email  False PAP.Subject_has_Property
        PAP.Person_has_Email       False PAP.Subject_has_Property
        PAP.Company_has_Email      False PAP.Subject_has_Property
      PAP.Subject_has_Phone        True  PAP.Subject_has_Property
        PAP.Association_has_Phone  False PAP.Subject_has_Property
        PAP.Person_has_Phone       False PAP.Subject_has_Property
        PAP.Company_has_Phone      False PAP.Subject_has_Property
      PAP.Subject_has_Url          True  PAP.Subject_has_Property
        PAP.Association_has_Url    False PAP.Subject_has_Property
        PAP.Person_has_Url         False PAP.Subject_has_Property
        PAP.Node_has_Url           False PAP.Subject_has_Property
        PAP.Company_has_Url        False PAP.Subject_has_Property

"""

_test_owner = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...

    >>> FFM = scope.FFM
    >>> PAP = scope.PAP
    >>> Adr = FFM.IP4_Network.net_address.P_Type

    >>> mgr = PAP.Person \\
    ...     (first_name = 'Ralf', last_name = 'Schlatterbeck', raw = True)

    >>> node1 = FFM.Node (name = "nogps", manager = mgr, position = None, raw = True)
    >>> node1.owner
    PAP.Person (u'schlatterbeck', u'ralf', u'', u'')

    >>> node4 = FFM.Node (name = "node4", manager = mgr, owner = node1)
    Traceback (most recent call last):
      ...
    Wrong_Type: Node 'nogps' not eligible for attribute owner,
        must be instance of Subject, but not Node

"""

_test_refuse_e_types = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...

    >>> FFM = scope.FFM
    >>> PAP = scope.PAP

    >>> for ET in scope.app_type._T_Extension :
    ...     for a in ET.id_entity_attr :
    ...         if getattr (a, "refuse_e_types", None) :
    ...             print (ET.type_name, a.name, sorted (a.refuse_e_types))
    FFM.Node owner ['FFM.Node']
    PAP.Subject_has_Address left ['FFM.Node']
    PAP.Subject_has_Email left ['FFM.Node']
    PAP.Subject_has_Phone left ['FFM.Node']

    >>> for ET in scope.app_type._T_Extension :
    ...     for a in ET.id_entity_attr :
    ...         if getattr (a, "refuse_e_types", None) :
    ...             print (ET.type_name, a.name, sorted (a.refuse_e_types_transitive))
    FFM.Node owner ['FFM.Node']
    PAP.Subject_has_Address left ['FFM.Node']
    PAP.Subject_has_Email left ['FFM.Node']
    PAP.Subject_has_Phone left ['FFM.Node']

    >>> sorted (FFM.Node.manager.eligible_e_types)
    ['PAP.Person']

    >>> sorted (FFM.Node.owner.eligible_e_types)
    ['PAP.Association', 'PAP.Company', 'PAP.Person']

    >>> sorted (FFM.Node.owner.selectable_e_types_unique_epk)
    ['PAP.Association', 'PAP.Company', 'PAP.Person']

    >>> sorted (PAP.Subject_has_Property.left.eligible_e_types)
    ['FFM.Node', 'PAP.Association', 'PAP.Company', 'PAP.Person']

    >>> sorted (PAP.Subject_has_Phone.left.eligible_e_types)
    ['PAP.Association', 'PAP.Company', 'PAP.Person']

    >>> AQ = FFM.Node.AQ
    >>> print (formatted (AQ.As_Template_Elem))
    [ Record
      ( attr = String `name`
      , full_name = 'name'
      , id = 'name'
      , name = 'name'
      , sig_key = 3
      , ui_name = 'Name'
      )
    , Record
      ( Class = 'Entity'
      , attr = Entity `manager`
      , attrs =
          [ Record
            ( attr = String `last_name`
            , full_name = 'manager.last_name'
            , id = 'manager__last_name'
            , name = 'last_name'
            , sig_key = 3
            , ui_name = 'Manager/Last name'
            )
          , Record
            ( attr = String `first_name`
            , full_name = 'manager.first_name'
            , id = 'manager__first_name'
            , name = 'first_name'
            , sig_key = 3
            , ui_name = 'Manager/First name'
            )
          , Record
            ( attr = String `middle_name`
            , full_name = 'manager.middle_name'
            , id = 'manager__middle_name'
            , name = 'middle_name'
            , sig_key = 3
            , ui_name = 'Manager/Middle name'
            )
          , Record
            ( attr = String `title`
            , full_name = 'manager.title'
            , id = 'manager__title'
            , name = 'title'
            , sig_key = 3
            , ui_name = 'Manager/Academic title'
            )
          , Record
            ( attr = Date_Interval `lifetime`
            , attrs =
                [ Record
                  ( attr = Date `start`
                  , full_name = 'manager.lifetime.start'
                  , id = 'manager__lifetime__start'
                  , name = 'start'
                  , sig_key = 0
                  , ui_name = 'Manager/Lifetime/Start'
                  )
                , Record
                  ( attr = Date `finish`
                  , full_name = 'manager.lifetime.finish'
                  , id = 'manager__lifetime__finish'
                  , name = 'finish'
                  , sig_key = 0
                  , ui_name = 'Manager/Lifetime/Finish'
                  )
                , Record
                  ( attr = Boolean `alive`
                  , choices =
                      [ 'no'
                      , 'yes'
                      ]
                  , full_name = 'manager.lifetime.alive'
                  , id = 'manager__lifetime__alive'
                  , name = 'alive'
                  , sig_key = 1
                  , ui_name = 'Manager/Lifetime/Alive'
                  )
                ]
            , full_name = 'manager.lifetime'
            , id = 'manager__lifetime'
            , name = 'lifetime'
            , ui_name = 'Manager/Lifetime'
            )
          , Record
            ( attr = Sex `sex`
            , choices =
                [
                  ( 'F'
                  , 'Female'
                  )
                ,
                  ( 'M'
                  , 'Male'
                  )
                ]
            , full_name = 'manager.sex'
            , id = 'manager__sex'
            , name = 'sex'
            , sig_key = 0
            , ui_name = 'Manager/Sex'
            )
          ]
      , full_name = 'manager'
      , id = 'manager'
      , name = 'manager'
      , sig_key = 2
      , type_name = 'PAP.Person'
      , ui_name = 'Manager'
      , ui_type_name = 'Person'
      )
    , Record
      ( attr = Date_Interval `lifetime`
      , attrs =
          [ Record
            ( attr = Date `start`
            , full_name = 'lifetime.start'
            , id = 'lifetime__start'
            , name = 'start'
            , sig_key = 0
            , ui_name = 'Lifetime/Start'
            )
          , Record
            ( attr = Date `finish`
            , full_name = 'lifetime.finish'
            , id = 'lifetime__finish'
            , name = 'finish'
            , sig_key = 0
            , ui_name = 'Lifetime/Finish'
            )
          , Record
            ( attr = Boolean `alive`
            , choices = <Recursion on list...>
            , full_name = 'lifetime.alive'
            , id = 'lifetime__alive'
            , name = 'alive'
            , sig_key = 1
            , ui_name = 'Lifetime/Alive'
            )
          ]
      , full_name = 'lifetime'
      , id = 'lifetime'
      , name = 'lifetime'
      , ui_name = 'Lifetime'
      )
    , Record
      ( Class = 'Entity'
      , attr = Entity `address`
      , attrs =
          [ Record
            ( attr = String `street`
            , full_name = 'address.street'
            , id = 'address__street'
            , name = 'street'
            , sig_key = 3
            , ui_name = 'Address/Street'
            )
          , Record
            ( attr = String `zip`
            , full_name = 'address.zip'
            , id = 'address__zip'
            , name = 'zip'
            , sig_key = 3
            , ui_name = 'Address/Zip code'
            )
          , Record
            ( attr = String `city`
            , full_name = 'address.city'
            , id = 'address__city'
            , name = 'city'
            , sig_key = 3
            , ui_name = 'Address/City'
            )
          , Record
            ( attr = String `country`
            , full_name = 'address.country'
            , id = 'address__country'
            , name = 'country'
            , sig_key = 3
            , ui_name = 'Address/Country'
            )
          , Record
            ( attr = String `desc`
            , full_name = 'address.desc'
            , id = 'address__desc'
            , name = 'desc'
            , sig_key = 3
            , ui_name = 'Address/Description'
            )
          , Record
            ( attr = String `region`
            , full_name = 'address.region'
            , id = 'address__region'
            , name = 'region'
            , sig_key = 3
            , ui_name = 'Address/Region'
            )
          ]
      , full_name = 'address'
      , id = 'address'
      , name = 'address'
      , sig_key = 2
      , type_name = 'PAP.Address'
      , ui_name = 'Address'
      , ui_type_name = 'Address'
      )
    , Record
      ( Class = 'Entity'
      , attr = Entity `owner`
      , children_np =
          [ Record
            ( Class = 'Entity'
            , attr = Entity `owner`
            , attrs =
                [ Record
                  ( attr = String `name`
                  , full_name = 'owner.name'
                  , id = 'owner__name'
                  , name = 'name'
                  , sig_key = 3
                  , ui_name = 'Owner[Association]/Name'
                  )
                ]
            , full_name = 'owner'
            , id = 'owner'
            , name = 'owner'
            , sig_key = 2
            , type_name = 'PAP.Association'
            , ui_name = 'Owner[Association]'
            , ui_type_name = 'Association'
            )
          , Record
            ( Class = 'Entity'
            , attr = Entity `owner`
            , attrs =
                [ Record
                  ( attr = String `name`
                  , full_name = 'owner.name'
                  , id = 'owner__name'
                  , name = 'name'
                  , sig_key = 3
                  , ui_name = 'Owner[Company]/Name'
                  )
                , Record
                  ( attr = String `registered_in`
                  , full_name = 'owner.registered_in'
                  , id = 'owner__registered_in'
                  , name = 'registered_in'
                  , sig_key = 3
                  , ui_name = 'Owner[Company]/Registered in'
                  )
                ]
            , full_name = 'owner'
            , id = 'owner'
            , name = 'owner'
            , sig_key = 2
            , type_name = 'PAP.Company'
            , ui_name = 'Owner[Company]'
            , ui_type_name = 'Company'
            )
          , Record
            ( Class = 'Entity'
            , attr = Entity `owner`
            , attrs =
                [ Record
                  ( attr = String `last_name`
                  , full_name = 'owner.last_name'
                  , id = 'owner__last_name'
                  , name = 'last_name'
                  , sig_key = 3
                  , ui_name = 'Owner[Person]/Last name'
                  )
                , Record
                  ( attr = String `first_name`
                  , full_name = 'owner.first_name'
                  , id = 'owner__first_name'
                  , name = 'first_name'
                  , sig_key = 3
                  , ui_name = 'Owner[Person]/First name'
                  )
                , Record
                  ( attr = String `middle_name`
                  , full_name = 'owner.middle_name'
                  , id = 'owner__middle_name'
                  , name = 'middle_name'
                  , sig_key = 3
                  , ui_name = 'Owner[Person]/Middle name'
                  )
                , Record
                  ( attr = String `title`
                  , full_name = 'owner.title'
                  , id = 'owner__title'
                  , name = 'title'
                  , sig_key = 3
                  , ui_name = 'Owner[Person]/Academic title'
                  )
                ]
            , full_name = 'owner'
            , id = 'owner'
            , name = 'owner'
            , sig_key = 2
            , type_name = 'PAP.Person'
            , ui_name = 'Owner[Person]'
            , ui_type_name = 'Person'
            )
          ]
      , default_child = 'PAP.Person'
      , full_name = 'owner'
      , id = 'owner'
      , name = 'owner'
      , sig_key = 2
      , type_name = 'PAP.Subject'
      , ui_name = 'Owner'
      , ui_type_name = 'Subject'
      )
    , Record
      ( attr = Position `position`
      , attrs =
          [ Record
            ( attr = Angle `lat`
            , full_name = 'position.lat'
            , id = 'position__lat'
            , name = 'lat'
            , sig_key = 4
            , ui_name = 'Position/Latitude'
            )
          , Record
            ( attr = Angle `lon`
            , full_name = 'position.lon'
            , id = 'position__lon'
            , name = 'lon'
            , sig_key = 4
            , ui_name = 'Position/Longitude'
            )
          , Record
            ( attr = Float `height`
            , full_name = 'position.height'
            , id = 'position__height'
            , name = 'height'
            , sig_key = 0
            , ui_name = 'Position/Height'
            )
          ]
      , full_name = 'position'
      , id = 'position'
      , name = 'position'
      , ui_name = 'Position'
      )
    , Record
      ( attr = Boolean `show_in_map`
      , choices =
          [ 'no'
          , 'yes'
          ]
      , full_name = 'show_in_map'
      , id = 'show_in_map'
      , name = 'show_in_map'
      , sig_key = 1
      , ui_name = 'Show in map'
      )
    , Record
      ( Class = 'Entity'
      , attr = Rev_Ref `creation`
      , attrs =
          [ Record
            ( attr = Date-Time `c_time`
            , full_name = 'creation.c_time'
            , id = 'creation__c_time'
            , name = 'c_time'
            , sig_key = 0
            , ui_name = 'Creation/C time'
            )
          , Record
            ( Class = 'Entity'
            , attr = Entity `c_user`
            , children_np =
                [ Record
                  ( Class = 'Entity'
                  , attr = Entity `c_user`
                  , attrs =
                      [ Record
                        ( attr = Email `name`
                        , full_name = 'c_user.name'
                        , id = 'c_user__name'
                        , name = 'name'
                        , sig_key = 3
                        , ui_name = 'C user[Account]/Name'
                        )
                      ]
                  , full_name = 'c_user'
                  , id = 'c_user'
                  , name = 'c_user'
                  , sig_key = 2
                  , type_name = 'Auth.Account'
                  , ui_name = 'C user[Account]'
                  , ui_type_name = 'Account'
                  )
                , Record
                  ( Class = 'Entity'
                  , attr = Entity `c_user`
                  , attrs =
                      [ Record
                        ( attr = String `last_name`
                        , full_name = 'c_user.last_name'
                        , id = 'c_user__last_name'
                        , name = 'last_name'
                        , sig_key = 3
                        , ui_name = 'C user[Person]/Last name'
                        )
                      , Record
                        ( attr = String `first_name`
                        , full_name = 'c_user.first_name'
                        , id = 'c_user__first_name'
                        , name = 'first_name'
                        , sig_key = 3
                        , ui_name = 'C user[Person]/First name'
                        )
                      , Record
                        ( attr = String `middle_name`
                        , full_name = 'c_user.middle_name'
                        , id = 'c_user__middle_name'
                        , name = 'middle_name'
                        , sig_key = 3
                        , ui_name = 'C user[Person]/Middle name'
                        )
                      , Record
                        ( attr = String `title`
                        , full_name = 'c_user.title'
                        , id = 'c_user__title'
                        , name = 'title'
                        , sig_key = 3
                        , ui_name = 'C user[Person]/Academic title'
                        )
                      ]
                  , full_name = 'c_user'
                  , id = 'c_user'
                  , name = 'c_user'
                  , sig_key = 2
                  , type_name = 'PAP.Person'
                  , ui_name = 'C user[Person]'
                  , ui_type_name = 'Person'
                  )
                ]
            , full_name = 'creation.c_user'
            , id = 'creation__c_user'
            , name = 'c_user'
            , sig_key = 2
            , type_name = 'MOM.Id_Entity'
            , ui_name = 'Creation/C user'
            , ui_type_name = 'Id_Entity'
            )
          , Record
            ( attr = String `kind`
            , full_name = 'creation.kind'
            , id = 'creation__kind'
            , name = 'kind'
            , sig_key = 3
            , ui_name = 'Creation/Kind'
            )
          , Record
            ( attr = Date-Time `time`
            , full_name = 'creation.time'
            , id = 'creation__time'
            , name = 'time'
            , sig_key = 0
            , ui_name = 'Creation/Time'
            )
          , Record
            ( Class = 'Entity'
            , attr = Entity `user`
            , children_np =
                [ Record
                  ( Class = 'Entity'
                  , attr = Entity `user`
                  , attrs =
                      [ Record
                        ( attr = Email `name`
                        , full_name = 'user.name'
                        , id = 'user__name'
                        , name = 'name'
                        , sig_key = 3
                        , ui_name = 'User[Account]/Name'
                        )
                      ]
                  , full_name = 'user'
                  , id = 'user'
                  , name = 'user'
                  , sig_key = 2
                  , type_name = 'Auth.Account'
                  , ui_name = 'User[Account]'
                  , ui_type_name = 'Account'
                  )
                , Record
                  ( Class = 'Entity'
                  , attr = Entity `user`
                  , attrs =
                      [ Record
                        ( attr = String `last_name`
                        , full_name = 'user.last_name'
                        , id = 'user__last_name'
                        , name = 'last_name'
                        , sig_key = 3
                        , ui_name = 'User[Person]/Last name'
                        )
                      , Record
                        ( attr = String `first_name`
                        , full_name = 'user.first_name'
                        , id = 'user__first_name'
                        , name = 'first_name'
                        , sig_key = 3
                        , ui_name = 'User[Person]/First name'
                        )
                      , Record
                        ( attr = String `middle_name`
                        , full_name = 'user.middle_name'
                        , id = 'user__middle_name'
                        , name = 'middle_name'
                        , sig_key = 3
                        , ui_name = 'User[Person]/Middle name'
                        )
                      , Record
                        ( attr = String `title`
                        , full_name = 'user.title'
                        , id = 'user__title'
                        , name = 'title'
                        , sig_key = 3
                        , ui_name = 'User[Person]/Academic title'
                        )
                      ]
                  , full_name = 'user'
                  , id = 'user'
                  , name = 'user'
                  , sig_key = 2
                  , type_name = 'PAP.Person'
                  , ui_name = 'User[Person]'
                  , ui_type_name = 'Person'
                  )
                ]
            , full_name = 'creation.user'
            , id = 'creation__user'
            , name = 'user'
            , sig_key = 2
            , type_name = 'MOM.Id_Entity'
            , ui_name = 'Creation/User'
            , ui_type_name = 'Id_Entity'
            )
          ]
      , full_name = 'creation'
      , id = 'creation'
      , name = 'creation'
      , sig_key = 2
      , type_name = 'MOM.MD_Change'
      , ui_name = 'Creation'
      , ui_type_name = 'MD_Change'
      )
    , Record
      ( Class = 'Entity'
      , attr = Rev_Ref `last_change`
      , attrs =
          [ Record
            ( attr = Date-Time `c_time`
            , full_name = 'last_change.c_time'
            , id = 'last_change__c_time'
            , name = 'c_time'
            , sig_key = 0
            , ui_name = 'Last change/C time'
            )
          , Record
            ( Class = 'Entity'
            , attr = Entity `c_user`
            , children_np =
                [ Record
                  ( Class = 'Entity'
                  , attr = Entity `c_user`
                  , attrs =
                      [ Record
                        ( attr = Email `name`
                        , full_name = 'c_user.name'
                        , id = 'c_user__name'
                        , name = 'name'
                        , sig_key = 3
                        , ui_name = 'C user[Account]/Name'
                        )
                      ]
                  , full_name = 'c_user'
                  , id = 'c_user'
                  , name = 'c_user'
                  , sig_key = 2
                  , type_name = 'Auth.Account'
                  , ui_name = 'C user[Account]'
                  , ui_type_name = 'Account'
                  )
                , Record
                  ( Class = 'Entity'
                  , attr = Entity `c_user`
                  , attrs =
                      [ Record
                        ( attr = String `last_name`
                        , full_name = 'c_user.last_name'
                        , id = 'c_user__last_name'
                        , name = 'last_name'
                        , sig_key = 3
                        , ui_name = 'C user[Person]/Last name'
                        )
                      , Record
                        ( attr = String `first_name`
                        , full_name = 'c_user.first_name'
                        , id = 'c_user__first_name'
                        , name = 'first_name'
                        , sig_key = 3
                        , ui_name = 'C user[Person]/First name'
                        )
                      , Record
                        ( attr = String `middle_name`
                        , full_name = 'c_user.middle_name'
                        , id = 'c_user__middle_name'
                        , name = 'middle_name'
                        , sig_key = 3
                        , ui_name = 'C user[Person]/Middle name'
                        )
                      , Record
                        ( attr = String `title`
                        , full_name = 'c_user.title'
                        , id = 'c_user__title'
                        , name = 'title'
                        , sig_key = 3
                        , ui_name = 'C user[Person]/Academic title'
                        )
                      ]
                  , full_name = 'c_user'
                  , id = 'c_user'
                  , name = 'c_user'
                  , sig_key = 2
                  , type_name = 'PAP.Person'
                  , ui_name = 'C user[Person]'
                  , ui_type_name = 'Person'
                  )
                ]
            , full_name = 'last_change.c_user'
            , id = 'last_change__c_user'
            , name = 'c_user'
            , sig_key = 2
            , type_name = 'MOM.Id_Entity'
            , ui_name = 'Last change/C user'
            , ui_type_name = 'Id_Entity'
            )
          , Record
            ( attr = String `kind`
            , full_name = 'last_change.kind'
            , id = 'last_change__kind'
            , name = 'kind'
            , sig_key = 3
            , ui_name = 'Last change/Kind'
            )
          , Record
            ( attr = Date-Time `time`
            , full_name = 'last_change.time'
            , id = 'last_change__time'
            , name = 'time'
            , sig_key = 0
            , ui_name = 'Last change/Time'
            )
          , Record
            ( Class = 'Entity'
            , attr = Entity `user`
            , children_np =
                [ Record
                  ( Class = 'Entity'
                  , attr = Entity `user`
                  , attrs =
                      [ Record
                        ( attr = Email `name`
                        , full_name = 'user.name'
                        , id = 'user__name'
                        , name = 'name'
                        , sig_key = 3
                        , ui_name = 'User[Account]/Name'
                        )
                      ]
                  , full_name = 'user'
                  , id = 'user'
                  , name = 'user'
                  , sig_key = 2
                  , type_name = 'Auth.Account'
                  , ui_name = 'User[Account]'
                  , ui_type_name = 'Account'
                  )
                , Record
                  ( Class = 'Entity'
                  , attr = Entity `user`
                  , attrs =
                      [ Record
                        ( attr = String `last_name`
                        , full_name = 'user.last_name'
                        , id = 'user__last_name'
                        , name = 'last_name'
                        , sig_key = 3
                        , ui_name = 'User[Person]/Last name'
                        )
                      , Record
                        ( attr = String `first_name`
                        , full_name = 'user.first_name'
                        , id = 'user__first_name'
                        , name = 'first_name'
                        , sig_key = 3
                        , ui_name = 'User[Person]/First name'
                        )
                      , Record
                        ( attr = String `middle_name`
                        , full_name = 'user.middle_name'
                        , id = 'user__middle_name'
                        , name = 'middle_name'
                        , sig_key = 3
                        , ui_name = 'User[Person]/Middle name'
                        )
                      , Record
                        ( attr = String `title`
                        , full_name = 'user.title'
                        , id = 'user__title'
                        , name = 'title'
                        , sig_key = 3
                        , ui_name = 'User[Person]/Academic title'
                        )
                      ]
                  , full_name = 'user'
                  , id = 'user'
                  , name = 'user'
                  , sig_key = 2
                  , type_name = 'PAP.Person'
                  , ui_name = 'User[Person]'
                  , ui_type_name = 'Person'
                  )
                ]
            , full_name = 'last_change.user'
            , id = 'last_change__user'
            , name = 'user'
            , sig_key = 2
            , type_name = 'MOM.Id_Entity'
            , ui_name = 'Last change/User'
            , ui_type_name = 'Id_Entity'
            )
          ]
      , full_name = 'last_change'
      , id = 'last_change'
      , name = 'last_change'
      , sig_key = 2
      , type_name = 'MOM.MD_Change'
      , ui_name = 'Last change'
      , ui_type_name = 'MD_Change'
      )
    , Record
      ( attr = Int `last_cid`
      , full_name = 'last_cid'
      , id = 'last_cid'
      , name = 'last_cid'
      , sig_key = 0
      , ui_name = 'Last cid'
      )
    , Record
      ( attr = Surrogate `pid`
      , full_name = 'pid'
      , id = 'pid'
      , name = 'pid'
      , sig_key = 0
      , ui_name = 'Pid'
      )
    , Record
      ( attr = String `type_name`
      , full_name = 'type_name'
      , id = 'type_name'
      , name = 'type_name'
      , sig_key = 3
      , ui_name = 'Type name'
      )
    , Record
      ( Class = 'Entity'
      , attr = Role_Ref_Set `addresses`
      , attrs =
          [ Record
            ( attr = String `street`
            , full_name = 'addresses.street'
            , id = 'addresses__street'
            , name = 'street'
            , sig_key = 3
            , ui_name = 'Addresses/Street'
            )
          , Record
            ( attr = String `zip`
            , full_name = 'addresses.zip'
            , id = 'addresses__zip'
            , name = 'zip'
            , sig_key = 3
            , ui_name = 'Addresses/Zip code'
            )
          , Record
            ( attr = String `city`
            , full_name = 'addresses.city'
            , id = 'addresses__city'
            , name = 'city'
            , sig_key = 3
            , ui_name = 'Addresses/City'
            )
          , Record
            ( attr = String `country`
            , full_name = 'addresses.country'
            , id = 'addresses__country'
            , name = 'country'
            , sig_key = 3
            , ui_name = 'Addresses/Country'
            )
          , Record
            ( attr = String `desc`
            , full_name = 'addresses.desc'
            , id = 'addresses__desc'
            , name = 'desc'
            , sig_key = 3
            , ui_name = 'Addresses/Description'
            )
          , Record
            ( attr = String `region`
            , full_name = 'addresses.region'
            , id = 'addresses__region'
            , name = 'region'
            , sig_key = 3
            , ui_name = 'Addresses/Region'
            )
          ]
      , full_name = 'addresses'
      , id = 'addresses'
      , name = 'addresses'
      , sig_key = 2
      , type_name = 'PAP.Address'
      , ui_name = 'Addresses'
      , ui_type_name = 'Address'
      )
    , Record
      ( Class = 'Entity'
      , attr = Role_Ref_Set `emails`
      , attrs =
          [ Record
            ( attr = Email `address`
            , full_name = 'emails.address'
            , id = 'emails__address'
            , name = 'address'
            , sig_key = 3
            , ui_name = 'Emails/Address'
            )
          , Record
            ( attr = String `desc`
            , full_name = 'emails.desc'
            , id = 'emails__desc'
            , name = 'desc'
            , sig_key = 3
            , ui_name = 'Emails/Description'
            )
          ]
      , full_name = 'emails'
      , id = 'emails'
      , name = 'emails'
      , sig_key = 2
      , type_name = 'PAP.Email'
      , ui_name = 'Emails'
      , ui_type_name = 'Email'
      )
    , Record
      ( Class = 'Entity'
      , attr = Role_Ref_Set `phones`
      , attrs =
          [ Record
            ( attr = Numeric_String `number`
            , full_name = 'phones.number'
            , id = 'phones__number'
            , name = 'number'
            , sig_key = 3
            , ui_name = 'Phones/Number'
            )
          , Record
            ( attr = Numeric_String `area_code`
            , full_name = 'phones.area_code'
            , id = 'phones__area_code'
            , name = 'area_code'
            , sig_key = 3
            , ui_name = 'Phones/Area code'
            )
          , Record
            ( attr = Numeric_String `country_code`
            , full_name = 'phones.country_code'
            , id = 'phones__country_code'
            , name = 'country_code'
            , sig_key = 3
            , ui_name = 'Phones/Country code'
            )
          , Record
            ( attr = String `desc`
            , full_name = 'phones.desc'
            , id = 'phones__desc'
            , name = 'desc'
            , sig_key = 3
            , ui_name = 'Phones/Description'
            )
          ]
      , full_name = 'phones'
      , id = 'phones'
      , name = 'phones'
      , sig_key = 2
      , type_name = 'PAP.Phone'
      , ui_name = 'Phones'
      , ui_type_name = 'Phone'
      )
    , Record
      ( Class = 'Entity'
      , attr = Role_Ref_Set `urls`
      , attrs =
          [ Record
            ( attr = Url `value`
            , full_name = 'urls.value'
            , id = 'urls__value'
            , name = 'value'
            , sig_key = 3
            , ui_name = 'Urls/Value'
            )
          , Record
            ( attr = String `desc`
            , full_name = 'urls.desc'
            , id = 'urls__desc'
            , name = 'desc'
            , sig_key = 3
            , ui_name = 'Urls/Description'
            )
          ]
      , full_name = 'urls'
      , id = 'urls'
      , name = 'urls'
      , sig_key = 2
      , type_name = 'PAP.Url'
      , ui_name = 'Urls'
      , ui_type_name = 'Url'
      )
    , Record
      ( Class = 'Entity'
      , attr = Role_Ref_Set `nicknames`
      , attrs =
          [ Record
            ( attr = String `name`
            , full_name = 'nicknames.name'
            , id = 'nicknames__name'
            , name = 'name'
            , sig_key = 3
            , ui_name = 'Nicknames/Name'
            )
          , Record
            ( attr = String `desc`
            , full_name = 'nicknames.desc'
            , id = 'nicknames__desc'
            , name = 'desc'
            , sig_key = 3
            , ui_name = 'Nicknames/Description'
            )
          ]
      , full_name = 'nicknames'
      , id = 'nicknames'
      , name = 'nicknames'
      , sig_key = 2
      , type_name = 'PAP.Nickname'
      , ui_name = 'Nicknames'
      , ui_type_name = 'Nickname'
      )
    , Record
      ( Class = 'Entity'
      , attr = Role_Ref_Set `im_handles`
      , attrs =
          [ Record
            ( attr = im_protocol `protocol`
            , choices =
                [
                  ( 'ICQ'
                  , 'ICQ [First internet-wide instant messaging service]'
                  )
                ,
                  ( 'IRC'
                  , 'IRC [Internet relay chat]'
                  )
                ,
                  ( 'XMPP'
                  , 'XMPP [Extensible messaging and presence protocol; used by Jabber and Google Talk]'
                  )
                ]
            , full_name = 'im_handles.protocol'
            , id = 'im_handles__protocol'
            , name = 'protocol'
            , sig_key = 0
            , ui_name = 'Im handles/Protocol'
            )
          , Record
            ( attr = String `address`
            , full_name = 'im_handles.address'
            , id = 'im_handles__address'
            , name = 'address'
            , sig_key = 3
            , ui_name = 'Im handles/Address'
            )
          , Record
            ( attr = String `desc`
            , full_name = 'im_handles.desc'
            , id = 'im_handles__desc'
            , name = 'desc'
            , sig_key = 3
            , ui_name = 'Im handles/Description'
            )
          ]
      , full_name = 'im_handles'
      , id = 'im_handles'
      , name = 'im_handles'
      , sig_key = 2
      , type_name = 'PAP.IM_Handle'
      , ui_name = 'Im handles'
      , ui_type_name = 'IM_Handle'
      )
    ]

"""

__test__ = Scaffold.create_test_dict \
  ( dict
      ( main            = _test_code
      , auto_children   = _test_auto_children
      , owner           = _test_owner
      , refuse_e_types  = _test_refuse_e_types
      )
  )

### __END__ FFM.__test__.Nodes
