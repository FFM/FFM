# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************
# This module is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public License
# along with this module; if not, see <http://www.gnu.org/licenses/>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    deploy
#
# Purpose
#    Deploy command for FFM
#
# Revision Dates
#    23-May-2012 (CT) Creation
#    31-May-2012 (CT) Remove `lib_dir` from `_defaults`
#     1-Jun-2012 (CT) Add `python` to `_defaults`
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function #, unicode_literals

from   _GTW                   import GTW
import _GTW._OMP.deploy
import _GTW._Werkzeug.deploy

class Command (_GTW._Werkzeug.deploy.Command, GTW.OMP.deploy.Command) :
    """Manage deployment of FFM application."""

    _config_defaults        = \
        ( "~/.ffm.deploy.config"
        , "../../.ffm.deploy.config"
        )
    _defaults               = dict \
        ( app_dir           = "www/app"
        , app_module        = "./model.py"
        , bugs_address      = "tanzer@swing.co.at,ralf@runtux.com"
        , copyright_holder  = "Mag. Christian Tanzer, Ralf Schlatterbeck"
        , languages         = "de,en"
        , project_name      = "FFM"
        , python            = "~/PVE/active/bin/python"
        )

    class _Babel_ \
            ( GTW.Werkzeug.deploy.Command._Babel_
            , GTW.OMP.deploy.Command._Babel_
            ) :

        _package_dirs       = ["_FFM", "."]

    # end class _Babel_

# end class Command

command = Command ()

if __name__ == "__main__" :
    command ()
### __END__ deploy
