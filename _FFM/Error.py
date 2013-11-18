# -*- coding: utf-8 -*-
# Copyright (C) 2013 Mag. Christian Tanzer All rights reserved
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
#    FFM.Error
#
# Purpose
#    Provide exception classes for package FFM
#
# Revision Dates
#     1-Mar-2013 (CT) Creation
#    ««revision-date»»···
#--

from   __future__ import absolute_import, division, print_function, unicode_literals

from   _FFM                     import FFM
from   _TFL                     import TFL
from   _MOM                     import MOM

import _MOM.Error

class _FFM_Error_ (MOM.Error.Error) :
    """Root class of FFM exceptions"""

    _real_name = "Error"

Error = _FFM_Error_ # end class

class Address_Already_Used (Error, ValueError) :
    """Address is already in use"""

    def __init__ (self, address, owner, requester, msg) :
        self.__super.__init__ (msg)
        self.address     = address
        self.owner       = owner
        self.requester   = requester
    # end def __init__

# end class Address_Already_Used

class Address_not_in_Network (Error, ValueError) :
    """Address is not in Network"""

    def __init__ (self, address, net_address, msg) :
        self.__super.__init__ (msg)
        self.address     = address
        self.net_address = net_address
    # end def __init__

# end class Address_not_in_Network

class No_Free_Address_Range (Error, ValueError) :
    """There is no free subrange available"""

    def __init__ (self, net_address, mask_len, message) :
        self.__super.__init__ (message)
        self.net_address = net_address
        self.mask_len    = mask_len
    # end def __init__

# end class No_Free_Address_Range

if __name__ != "__main__" :
    FFM._Export_Module ()
### __END__ FFM.Error
