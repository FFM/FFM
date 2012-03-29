# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012 Mag. Christian Tanzer All rights reserved
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
#    26-Mar-2012 (CT) Creation
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

def create (scope) :
    Auth = scope.Auth
    Auth.Account_Anonymous ("anonymous")
    Auth.Account_P.create_new_account_x \
        ( "christian.tanzer@gmail.com"
        , password = "123", enabled = True, superuser = True, suspended = False
        )
    Auth.Account_P.create_new_account_x \
        ( "tanzer@swing.co.at"
        , password = "456", enabled = True, suspended = False
        )
    Auth.Group ("FFM")
    Auth.Account_in_Group ("tanzer@swing.co.at", "FFM")
    scope.commit ()
# end def create

if __name__ == "__main__" :
    from model import *
    db_url  = sos.environ.get ("DB_url",  "hps://")
    db_name = sos.environ.get ("DB_name", None)
    scope   = Scaffold.scope  (db_url, db_name, False)
    TFL.Environment.py_shell  ()
### __END__ fixtures
