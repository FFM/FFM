# -*- coding: utf-8 -*-
# Copyright (C) 2012-2013 Mag. Christian Tanzer All rights reserved
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
#    FFM.Antenna_Band
#
# Purpose
#    Model a supported frequency band of an Antenna_Type
#
# Revision Dates
#     7-Dec-2012 (RS) Creation
#    15-May-2013 (CT) Replace `auto_cache` by `link_ref_attr_name`
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _MOM.import_MOM            import *
from   _FFM                       import FFM
from   _MOM._Attr.Number_Interval import *

import _FFM.Entity

_Ancestor_Essence = FFM.Link1

class Antenna_Band (_Ancestor_Essence) :
    """Frequency Band of an antenna type"""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class left (_Ancestor.left) :
            """The antenna type for this band"""

            role_type          = FFM.Antenna_Type
            ui_allow_new       = False
            link_ref_attr_name = "band"

        # end class left

        class band (A_Frequency_Interval) :
            """Frequency range an antenna type supports."""

            kind               = Attr.Primary

        # end class frequency


    # end class _Attributes

# end class Antenna_Band

if __name__ != "__main__" :
    FFM._Export ("*")
### __END__ FFM.Antenna_Band
