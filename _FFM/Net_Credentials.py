# -*- coding: iso-8859-15 -*-
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
#    FFM.Net_Credentials
#
# Purpose
#    Model credentials for a network interface
#
# Revision Dates
#    14-Mar-2012 (CT) Creation
#     6-Dec-2012 (RS) Add `belongs_to_node`, add `max_links`
#    15-May-2013 (CT) Replace `auto_cache` by `link_ref_attr_name`
#    20-May-2013 (CT) Set `_Net_Credentials_.left.link_ref_suffix` to `None`
#    13-Aug-2013 (CT) Add `key.typ`
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _MOM.import_MOM        import *
from   _MOM.import_MOM        import _A_String_Ascii_
from   _FFM                   import FFM

import _FFM.Entity
import _FFM.Net_Interface
import _FFM._Belongs_to_Node_

from   _TFL.Regexp            import Regexp, re

_Ancestor_Essence = FFM.Link1
_Mixin = FFM._Belongs_to_Node_

class _Net_Credentials_ (_Mixin, _Ancestor_Essence) :
    """Model credentials used by a Net_Interface, e.g., `802.1x`
       authentication for a wired interface, or WPA authentication for a WiFi
       interface.
    """

    is_partial = True

    class _Attributes (_Mixin._Attributes, _Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        ### Primary attributes

        class left (_Ancestor.left) :
            """The network interface using these credentials."""

            role_type          = FFM.Net_Interface
            role_name          = "interface"
            link_ref_attr_name = "credentials"
            link_ref_suffix    = None
            max_links          = 1

        # end class left

        ### *** BEWARE ***
        ### To ensure that a `Net_Interface` has only one `credentials`, no
        ### other essential primary key attributes must be defined here or by
        ### derived classes

    # end class _Attributes

# end class _Net_Credentials_

_Ancestor_Essence = _Net_Credentials_

class WPA_Credentials (_Ancestor_Essence) :
    """Model credentials necessary for WPA authentication."""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class key (Eval_Mixin, _A_String_Ascii_) :
            """Key used for WPA authentication."""

            kind               = Attr.Required
            max_length         = 32
            typ                = "Key"

            ### allow characters up to "\xFF"
            _cooked_re        = Regexp \
                ( "^[\x00-\xFF]*$"
                , re.VERBOSE
                )

        # end class key

    # end class _Attributes

# end class WPA2

if __name__ != "__main__" :
    FFM._Export ("*")
### __END__ FFM.Net_Credentials
