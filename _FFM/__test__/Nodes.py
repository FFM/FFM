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
#    FFM.__test__.Nodes
#
# Purpose
#    Test Node and associations
#
# Revision Dates
#    19-Sep-2012 (RS) Creation
#    24-Sep-2012 (RS) More tests, up to `Net_Interface_in_IP4_Network`
#    11-Oct-2012 (RS) Fix missing `raw` parameter
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
    >>> mgr = PAP.Person \\
    ...     (first_name = 'Ralf', last_name = 'Schlatterbeck', raw = True)
    >>> comp = PAP.Company (name = "Open Source Consulting", raw = True)
    >>> node1 = FFM.Node \\
    ...     (name = "nogps", manager = mgr, position = None, raw = True)
    >>> gps1 = dict (lat = "48 d 17 m 9.64 s", lon = "15 d 52 m 27.84 s")
    >>> node2 = FFM.Node \\
    ...     (name = "node2", manager = mgr, position = gps1, raw = True)
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
    >>> net = FFM.IP4_Network (dict (address = '192.168.23.0/24'), raw = True)
    >>> devtype = FFM.Net_Device_Type.instance_or_new \\
    ...     (name = 'Generic', raw = True)
    >>> dev = FFM.Net_Device \\
    ...     (left = devtype, node = node3, name = 'dev', raw = True)
    >>> wr  = FFM.Wired_Interface (left = dev, name = 'wr', raw = True)
    >>> wl  = FFM.Wireless_Interface (left = dev, name = 'wl', raw = True)
    >>> ir1 = FFM.Net_Interface_in_IP4_Network \\
    ...     (wr, net, dict (address = R_IP4_Address ('192.168.23.1')))
    >>> il1 = FFM.Net_Interface_in_IP4_Network \\
    ...     (wl, net, dict (address = R_IP4_Address ('192.168.23.2')))
    >>> irx = FFM.Net_Interface_in_IP4_Network (wr, net)
    >>> x   = irx.set_raw (ip_address = dict (address = '192.168.23.99'))
    >>> ir2 = FFM.Net_Interface_in_IP4_Network \\
    ...     (wr, net, dict (address = '192.168.23.3'), raw = True)
    >>> il2 = FFM.Net_Interface_in_IP4_Network \\
    ...     (wl, net, dict (address = '192.168.23.4'), raw = True)
    >>> scope.destroy ()

"""

__test__ = Scaffold.create_test_dict \
  ( dict
      ( main       = _test_code
      )
  )

### __END__ FFM.__test__.Nodes
