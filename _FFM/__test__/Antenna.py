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
#    FFM.__test__.Antenna
#
# Purpose
#    Test Antenna and associations
#
# Revision Dates
#     5-Dec-2012 (RS) Creation
#     7-Dec-2012 (RS) Test predicate `band_exists` of `Antenna_Type`
#    17-Dec-2012 (RS) Add tests for attributes of `belongs_to_node`
#    26-Feb-2013 (CT) Disable tests `belongs_to_node`
#    14-Aug-2013 (CT) Reenable tests for `belongs_to_node`
#    ««revision-date»»···
#--

from   __future__ import absolute_import, division, print_function, unicode_literals

from   _FFM.__test__.model      import *
from   datetime                 import datetime

_test_code = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...

    >>> FFM = scope.FFM
    >>> PAP = scope.PAP
    >>> at1 = FFM.Antenna_Type \\
    ...     ( name         = "Yagi1"
    ...     , desc         = "A Yagi"
    ...     , gain         = 17.5
    ...     , polarization = "vertical"
    ...     , raw          = True
    ...     )
    >>> b1 = FFM.Antenna_Band (at1, band = ("2.4 GHz", "3 GHz"), raw = True)
    >>> at2 = FFM.Antenna_Type \\
    ...     ( name         = "Yagi2"
    ...     , desc         = "A Yagi"
    ...     , gain         = 11.5
    ...     , polarization = "horizontal"
    ...     , raw          = True
    ...     )
    >>> b2 = FFM.Antenna_Band (at2, band = ("5 GHz", "6 GHz"), raw = True)
    >>> scope.commit ()

    >>> at3 = FFM.Antenna_Type \\
    ...     ( name         = "Yagi3"
    ...     , desc         = "A Yagi"
    ...     , gain         = 11.5
    ...     , polarization = "horizontal"
    ...     , raw          = True
    ...     )
    >>> scope.commit ()
    Traceback (most recent call last):
      ...
    Invariants: Condition `band_exists` : There must be at least one frequency band for the antenna. (number_of_bands >= 1)
        bands = None
        number_of_bands = 0 << len (bands)

    >>> args = dict (left = at1, azimuth = "180", elevation = 0, raw = True)
    >>> a = FFM.Antenna (name = "1", ** args)
    >>> (a.gain, a.polarization)
    (17.5, 1)
    >>> a = FFM.Antenna (name = "2", gain = 11, ** args)
    >>> (a.gain, a.polarization)
    (11.0, 1)
    >>> a = FFM.Antenna (name = "3", polarization = "horizontal", ** args)
    >>> (a.gain, a.polarization)
    (17.5, 0)
    >>> args = dict (left = at2, azimuth = "90", elevation = 0, raw = True)
    >>> b = FFM.Antenna (name = "4", ** args)
    >>> (b.gain, b.polarization)
    (11.5, 0)
    >>> b = FFM.Antenna (name = "5", polarization = 'left circular', ** args)
    >>> (b.gain, b.polarization)
    (11.5, 2)
    >>> b = FFM.Antenna (name = "6", gain = 22, ** args)
    >>> (b.gain, b.polarization)
    (22.0, 0)

    >>> mgr = PAP.Person \\
    ...     (first_name = 'Ralf', last_name = 'Schlatterbeck', raw = True)
    >>> owner = PAP.Person ("Tanzer", "Christian", raw = True)
    >>> node = FFM.Node \\
    ...     (name = "nogps", manager = mgr, position = None, raw = True)
    >>> nod2 = FFM.Node \\
    ...     (name = "node2", manager = mgr, owner = owner, raw = True)
    >>> devtype = FFM.Net_Device_Type.instance_or_new \\
    ...     (name = 'Generic', raw = True)
    >>> dev = FFM.Net_Device \\
    ...     (left = devtype, node = node, name = 'dev', raw = True)
    >>> dev2 = FFM.Net_Device \\
    ...     (left = devtype, node = nod2, name = 'dev2', raw = True)
    >>> wl  = FFM.Wireless_Interface (left = dev, name = 'wl', raw = True)
    >>> wia = FFM.Wireless_Interface_uses_Antenna (wl, b)

    >>> b.__class__.belongs_to_node
    Entity `belongs_to_node`

    >>> a.belongs_to_node is None
    True

    >>> b.belongs_to_node
    FFM.Node (u'nogps')

    >>> FFM.Antenna.query (Q.interface == wl).count ()
    1
    >>> FFM.Antenna.query (Q.belongs_to_node.manager == mgr).count ()
    1
    >>> FFM.Wireless_Interface.query (Q.belongs_to_node.manager == mgr).count ()
    1
    >>> FFM.Wireless_Interface.query (Q.belongs_to_node.owner == mgr).count ()
    1

    >>> for x in scope.FFM.Net_Interface.query (Q.belongs_to_node.manager == mgr, sort_key = Q.pid) :
    ...     x
    FFM.Wireless_Interface (((u'generic', u'', u''), (u'nogps', ), u'dev'), u'', u'wl')

    >>> for x in scope.FFM.Wireless_Interface_uses_Antenna.query (Q.belongs_to_node.manager == mgr, sort_key = Q.pid) :
    ...     x
    FFM.Wireless_Interface_uses_Antenna ((((u'generic', u'', u''), (u'nogps', ), u'dev'), u'', u'wl'), ((u'yagi2', u'', u''), u'6'))

    >>> for x in scope.FFM.Net_Device.query (Q.belongs_to_node.manager == mgr, sort_key = Q.pid) :
    ...     x
    FFM.Net_Device ((u'generic', u'', u''), (u'nogps', ), u'dev')
    FFM.Net_Device ((u'generic', u'', u''), (u'node2', ), u'dev2')

    >>> for x in scope.FFM.Net_Device.query (Q.belongs_to_node.owner == owner, sort_key = Q.pid) :
    ...     x
    FFM.Net_Device ((u'generic', u'', u''), (u'node2', ), u'dev2')

    >>> for x in scope.FFM.Antenna.query (Q.belongs_to_node.manager == mgr, sort_key = Q.pid) :
    ...     x
    FFM.Antenna ((u'yagi2', u'', u''), u'6')

    >>> for x in scope.FFM.Node.query (Q.manager == mgr, sort_key = Q.pid) :
    ...     x
    FFM.Node (u'nogps')
    FFM.Node (u'node2')

    >>> for x in scope.FFM.Node.query (Q.owner == mgr, sort_key = Q.pid) :
    ...     x
    FFM.Node (u'nogps')

    >>> for x in scope.FFM.Node.query (Q.owner == owner, sort_key = Q.pid) :
    ...     x
    FFM.Node (u'node2')

"""

__test__ = Scaffold.create_test_dict \
  ( dict
      ( main_test  = _test_code
      )
  )

### __END__ FFM.__test__.Antenna
