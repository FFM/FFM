# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012 Mag. Christian Tanzer All rights reserved
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
#    FFM.Wireless_Mode
#
# Purpose
#    Model the mode a wireless device operates in
#
# Revision Dates
#    14-Mar-2012 (CT) Creation
#    10-May-2012 (CT) Add `is_linkable`
#     6-Dec-2012 (RS) Add `belongs_to_node`, add `max_links`
#    17-Dec-2012 (CT) Change from essential type to basis for `A_Wireless_Mode`
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _FFM                     import FFM
from   _TFL                     import TFL

from   _TFL.I18N                import _, _T, _Tn

import _TFL._Meta.Object

class M_Wireless_Mode (TFL.Meta.Object.__class__) :
    """Meta class for wireless-mode classes"""

    Table = {}

    def __init__ (cls, name, bases, dct) :
        cls.__m_super.__init__ (name, bases, dct)
        if name != "Wireless_Mode" :
            cls._m_add (name, cls.Table)
    # end def __init__

    def __str__ (cls) :
        return cls.__name__
    # end def __str__

    def _m_add (cls, name, Table) :
        name = unicode (name)
        assert name not in Table, "Name clash: `%s` <-> `%s`" % \
            (name, Table [name].__class__)
        Table [name] = cls
    # end def _m_add

# end class M_Wireless_Mode

class Wireless_Mode (TFL.Meta.Object) :

    __metaclass__ = M_Wireless_Mode

# end class Wireless_Mode

class Ad_Hoc (Wireless_Mode) :
    """Ad-Hoc mode."""

    @classmethod
    def is_linkable (cls, other) :
        return other is cls
    # end def is_linkable

# end class Ad_Hoc

class AP (Wireless_Mode) :
    """Access point mode."""

    @classmethod
    def is_linkable (cls, other) :
        return other is Client
    # end def is_linkable

# end class AP

class Client (Wireless_Mode) :
    """Client mode."""

    @classmethod
    def is_linkable (cls, other) :
        return other is AP
    # end def is_linkable

# end class Client

if __name__ != "__main__" :
    FFM._Export ("*")
### __END__ FFM.Wireless_Mode
