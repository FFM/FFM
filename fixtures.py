# -*- coding: utf-8 -*-
# Copyright (C) 2012-2013 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the program FFM.
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
#    fixtures
#
# Purpose
#    Create standard objects for new scope
#
# Revision Dates
#    17-Dec-2012 (RS) Creation, move old fixtures.py to _FFM
#    27-May-2013 (CT) Remove trivial `password` values
#    ««revision-date»»···
#--

import _FFM.fixtures
from   _FFM import FFM

def create (scope) :
    FFM.fixtures.create (scope)
    Auth = scope.Auth
    Auth.Account.create_new_account_x \
        ( "christian.tanzer@gmail.com"
        , enabled = True, superuser = True, suspended = False
        )
    Auth.Account.create_new_account_x \
        ( "tanzer@swing.co.at"
        , enabled = True, suspended = False
        )
    Auth.Group ("FFM")
    Auth.Account_in_Group ("tanzer@swing.co.at", "FFM")
# end def create

if __name__ == "__main__" :
    from model import *
    db_url  = sos.environ.get ("DB_url",  "hps://")
    db_name = sos.environ.get ("DB_name", None)
    scope   = command.scope   (db_url, db_name, False)
    TFL.Environment.py_shell  ()
### __END__ fixtures
