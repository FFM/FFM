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
#    FFM.__test__.fixtures
#
# Purpose
#    fixtures for e.g. testing REST api
#
# Revision Dates
#     8-Jan-2013 (RS) Creation
#     1-Feb-2013 (RS) Fix rounding error with python2.6
#     5-Mar-2013 (CT) Adapt to signature change of `Net_Interface_in_IP_Network`
#    ««revision-date»»···
#--

from   __future__ import absolute_import, division, print_function, unicode_literals

from   _FFM                   import FFM
from   _GTW._OMP._PAP         import PAP

def create (scope) :
    FFM = scope.FFM
    PAP = scope.PAP
    Adr = FFM.IP4_Network.net_address.P_Type
    mgr = PAP.Person \
        (first_name = 'Ralf', last_name = 'Schlatterbeck', raw = True)
    node1 = FFM.Node (name = "nogps", manager = mgr, raw = True)
    gps1 = dict (lat = "48 d 15 m", lon = "15 d 52 m 27.84 s")
    node2 = FFM.Node \
        (name = "node2", manager = mgr, position = gps1, raw = True)
    net = FFM.IP4_Network (dict (address = '192.168.23.0/24'), raw = True)
    a1  = net.reserve (Adr ('192.168.23.1/32',  raw = True))
    a2  = net.reserve (Adr ('192.168.23.2/32',  raw = True))
    a3  = net.reserve (Adr ('192.168.23.3/32',  raw = True))
    a4  = net.reserve (Adr ('192.168.23.4/32',  raw = True))
    devtype = FFM.Net_Device_Type.instance_or_new \
        (name = 'Generic', raw = True)
    dev = FFM.Net_Device \
        (left = devtype, node = node2, name = 'dev', raw = True)
    wr  = FFM.Wired_Interface (left = dev, name = 'wr', raw = True)
    wl  = FFM.Wireless_Interface (left = dev, name = 'wl', raw = True)
    ir1 = FFM.Net_Interface_in_IP4_Network (wr, a1, mask_len = 24)
    il1 = FFM.Net_Interface_in_IP4_Network (wl, a2, mask_len = 32)
    ir2 = FFM.Net_Interface_in_IP4_Network (wr, a3, mask_len = 24)
    il2 = FFM.Net_Interface_in_IP4_Network (wl, a4, mask_len = 24)
# end def create

### __END__ FFM.__test__.fixtures
