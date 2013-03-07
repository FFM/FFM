# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012-2013 Mag. Christian Tanzer All rights reserved
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
#    17-Dec-2012 (RS) Temporary fix: `owner` can't be a `Company`
#     5-Mar-2013 (CT) Adapt to changes in `Net_Interface_in_IP4_Network`
#     7-Mar-2013 (RS) Add test for duplicate network allocation
#    ««revision-date»»···
#--

from   __future__ import absolute_import, division, print_function, unicode_literals

from   _FFM.__test__.model      import *
from   datetime                 import datetime
from   rsclib.IP_Address        import IP4_Address as R_IP4_Address
from   rsclib.IP_Address        import IP6_Address as R_IP6_Address

_test_code = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...

    >>> FFM = scope.FFM
    >>> PAP = scope.PAP
    >>> Adr = FFM.IP4_Network.net_address.P_Type

    >>> mgr = PAP.Person \\
    ...     (first_name = 'Ralf', last_name = 'Schlatterbeck', raw = True)

    # FIXME: should allow company again
    #>>> comp = PAP.Company (name = "Open Source Consulting", raw = True)
    >>> comp = mgr
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
    >>> x = PAP.Node_has_Address (node2, adr)

    >>> phone = PAP.Phone ('43', '2243', '26465')
    >>> x = PAP.Node_has_Phone (node2, phone)
    Traceback (most recent call last):
      ...
    Link_Type: PAP.Node_has_Phone, FFM.Node, Node, (u'node2'), FFM.Node

    >>> email = PAP.Email ('rsc@runtux.com')
    >>> x = PAP.Node_has_Email (node2, email)
    Traceback (most recent call last):
      ...
    Link_Type: PAP.Node_has_Email, FFM.Node, Node, (u'node2'), FFM.Node

    >>> adr2 = PAP.Address \\
    ...     ( street  = 'Example 44'
    ...     , zip     = '1010'
    ...     , city    = 'Wien'
    ...     , country = 'Austria'
    ...     )
    >>> x = PAP.Node_has_Address (node2, adr2)
    Traceback (most recent call last):
      ...
    Multiplicity: The new definition of Node_has_Address (FFM.Node (u'node2'), PAP.Address (u'example 44', u'1010', u'wien', u'austria')) would exceed the maximum number [1] of links allowed for FFM.Node (u'node2',).
      Already existing:
        PAP.Node_has_Address ((u'node2', 'FFM.Node'), (u'Example 23', u'1010', u'Wien', u'Austria', 'PAP.Address'))


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

    >>> net = FFM.IP4_Network (dict (address = '192.168.23.0/24'), owner = mgr, raw = True)
    >>> a1  = net.reserve (Adr ('192.168.23.1/32',  raw = True))
    >>> a2  = net.reserve (Adr ('192.168.23.2/32',  raw = True))
    >>> a3  = net.reserve (Adr ('192.168.23.3/32',  raw = True))
    >>> a4  = net.reserve (Adr ('192.168.23.4/32',  raw = True))
    >>> ax  = net.reserve (Adr ('192.168.23.42/32', raw = True))
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

    >>> net2 = FFM.IP4_Network (dict (address = '10.0.0.0/8'), owner = mgr, raw = True)
    >>> a2_1 = net2.reserve (Adr ('10.139.187.0/27',  raw = True))
    >>> a2_2 = net2.reserve (Adr ('10.139.187.2',     raw = True))
    >>> a2_f = net2.reserve (Adr ('10.139.187.0/27',  raw = True))
    Traceback (most recent call last):
      ...
    Address_Already_Used: Address ("10.139.187.0/27", ) already in use by 'Schlatterbeck Ralf'

    >>> FFM.Net_Device.query (Q.belongs_to_node == node3).count ()
    1
    >>> FFM.Net_Device.query (Q.belongs_to_node.manager == mgr).count ()
    1

    >>> scope.commit ()
"""

__test__ = Scaffold.create_test_dict \
  ( dict
      ( main       = _test_code
      )
  )

### __END__ FFM.__test__.Nodes
