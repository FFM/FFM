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
#    FFM.__test__.model
#
# Purpose
#    FFM-specific descendent of GTW.__test__.Test_Command
#
# Revision Dates
#    18-Sep-2012 (CT) Creation
#    ««revision-date»»···
#--

from   __future__ import absolute_import, division, print_function, unicode_literals

from   _FFM                       import FFM
from   _GTW.__test__.Test_Command import *

import _FFM.import_FFM
import _GTW._OMP._Auth.import_Auth
import _GTW._OMP._PAP.import_PAP

import _GTW._OMP._Auth.Nav
import _GTW._OMP._PAP.Nav
import _FFM.Nav

class _FFM_Test_Command_ (GTW_Test_Command) :

    _rn_prefix              = "_FFM_Test"

    ANS                     = FFM
    PNS_Aliases             = dict \
        ( Auth              = GTW.OMP.Auth
        , PAP               = GTW.OMP.PAP
        )

    def fixtures (self, scope) :
        if sos.environ.get ("GTW_FIXTURES") :
            pass ### XXX add fixtures if necessary
    # end def fixtures

    def _nav_admin_groups (self) :
        RST = GTW.RST
        return \
            [ self.nav_admin_group
                ( "FFM"
                , _ ("Administration of node database")
                , "FFM"
                , permission = RST.In_Group ("FFM-admin")
                )
            , self.nav_admin_group
                ( "PAP"
                , _ ("Administration of persons/addresses...")
                , "GTW.OMP.PAP"
                , permission = RST.In_Group ("FFM-admin")
                )
            , self.nav_admin_group
                ( _ ("Users")
                , _ ("Administration of user accounts and groups")
                , "GTW.OMP.Auth"
                , permission = RST.Is_Superuser ()
                )
            ]
    # end def _nav_admin_groups

_Command_  = _FFM_Test_Command_ # end class

Scaffold   = _Command_ ()

### __END__ FFM.__test__.model
