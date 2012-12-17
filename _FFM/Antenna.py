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
#    FFM.Antenna
#
# Purpose
#    Model an antenna in FFM
#
# Revision Dates
#     6-Mar-2012 (CT) Creation
#    10-May-2012 (CT) Change `azimuth` and `orientation` to `A_Angle`
#    30-Aug-2012 (CT) Add `gain`
#    08-Oct-2012 (RS) `inclination` -> `elevation`
#    05-Dec-2012 (RS) Remove `orientation`, add `polarization`
#    06-Dec-2012 (RS) Add `belongs_to_node`
#    14-Dec-2012 (CT) Change `belongs_to_node.kind` to `Attr.Query`
#    17-Dec-2012 (CT) Set `belongs_to_node.hidden` to `True`
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _MOM.import_MOM        import *
from   _FFM                   import FFM
import _FFM.Antenna_Type
import _FFM.Device
import _FFM.Node
from   _FFM.Attr_Type         import A_Polarization

_Ancestor_Essence = FFM.Device

class Antenna (_Ancestor_Essence) :
    """Model an antenna used by a FFM node."""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        ### Primary attributes

        class left (_Ancestor.left) :
            """Type of antenna"""

            role_type          = FFM.Antenna_Type

        # end class left

        ### Non-primary attributes

        class azimuth (A_Angle) :
            """Azimuth of antenna orientation (in degrees)."""

            kind               = Attr.Required
            explanation        = """
              Azimuth is measured clockwise from north, i.e.,
              N <-> 0, E <-> 90, S <-> 180, W <-> 270.
              """

        # end class azimuth

        class belongs_to_node (A_Id_Entity) :
            """Node to which this antenna belongs."""

            kind               = Attr.Query
            auto_up_depends    = ("interface", )
            hidden             = True
            P_Type             = FFM.Node

            def query_fct (self) :
                return Q.interface.belongs_to_node
            # end def query_fct

        # end class belongs_to_node

        class elevation (A_Int) :
            """ Elevation angle of the beam from the horizontal plane
                (in degrees).
            """

            example            = "42"
            kind               = Attr.Optional
            Kind_Mixins        = (Attr.Sticky_Mixin, )
            default            = 0
            max_value          = 90
            min_value          = -90

        # end class elevation

        class gain (A_Float) :
            """Describes how well the antenna converts input power into radio
               waves headed in a specified direction (in dBi). Per default,
               `antenna_type.gain` is used, but can be overriden here.
            """

            kind               = Attr.Optional
            Kind_Mixins        = (Attr.Computed_Mixin, )

            def computed (self, obj) :
                if obj.left :
                    return obj.left.gain
            # end def computed

        # end class gain

        class polarization (A_Polarization) :
            """Antenna polarization. Per default,
               `antenna_type.polarization` is used, but can be overriden here.
            """

            kind               = Attr.Optional
            Kind_Mixins        = (Attr.Computed_Mixin, )

            def computed (self, obj) :
                if obj.left :
                    return obj.left.polarization
            # end def computed

        # end class polarization

    # end class _Attributes

# end class Antenna

if __name__ != "__main__" :
    FFM._Export ("*")
### __END__ FFM.Antenna
