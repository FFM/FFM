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
#    ««revision-date»»···
#--

from   __future__ import absolute_import, division, print_function, unicode_literals

from   _FFM                   import FFM
from   _GTW._OMP._PAP         import PAP

def create (scope) :
    FFM = scope.FFM
    PAP = scope.PAP
    mgr = PAP.Person \
        (first_name = 'Ralf', last_name = 'Schlatterbeck', raw = True)
    node1 = FFM.Node (name = "nogps", manager = mgr, raw = True)
    gps1 = dict (lat = "48 d 17 m 9.64 s", lon = "15 d 52 m 27.84 s")
    node2 = FFM.Node \
        (name = "node2", manager = mgr, position = gps1, raw = True)
    net = FFM.IP4_Network (dict (address = '192.168.23.0/24'), raw = True)
    devtype = FFM.Net_Device_Type.instance_or_new \
        (name = 'Generic', raw = True)
    dev = FFM.Net_Device \
        (left = devtype, node = node2, name = 'dev', raw = True)
    wr  = FFM.Wired_Interface (left = dev, name = 'wr', raw = True)
    wl  = FFM.Wireless_Interface (left = dev, name = 'wl', raw = True)
    ir1 = FFM.Net_Interface_in_IP4_Network \
        (wr, net, dict (address = '192.168.23.1'), raw = True)
    il1 = FFM.Net_Interface_in_IP4_Network \
        (wl, net, dict (address = '192.168.23.2'), raw = True)
    ir2 = FFM.Net_Interface_in_IP4_Network \
        (wr, net, dict (address = '192.168.23.3'), raw = True)
    il2 = FFM.Net_Interface_in_IP4_Network \
        (wl, net, dict (address = '192.168.23.4'), raw = True)
# end def create

### __END__ FFM.__test__.fixtures
