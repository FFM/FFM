# -*- coding: utf-8 -*-
# Copyright (C) 2012-2014 Mag. Christian Tanzer All rights reserved
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
#    model
#
# Purpose
#    Object model and command handler for FFM
#
# Revision Dates
#    26-Mar-2012 (CT) Creation
#    14-May-2012 (CT) Change `-config` to auto-split, `default_db_name` to `ffm`
#    17-May-2012 (CT) Derive from `GTW.Werkzeug.Command` instead of `.Scaffold`,
#                     rename `Scaffold` to `Command`
#    30-May-2012 (CT) Fix `opts`
#    31-May-2012 (CT) Add `"../../.ffm.config"` to `_config_defaults`
#     2-Jun-2012 (CT) Replace `config_defaults` by `Config`
#     3-Jun-2012 (CT) Factor `_Base_Command_`
#    11-Jun-2012 (CT) Correct `Auth` and `L10N`
#    29-Jul-2012 (CT) Change to use `GTW.RST.TOP` instead of `GTW.NAV`
#    11-Aug-2012 (CT) Add `GTW.RST.TOP.MOM.Doc` documentation
#    13-Sep-2012 (CT) Remove `GTW.AFS.MOM.Spec.setup_defaults`
#     2-Oct-2012 (CT) Add REST API to `create_top`
#     5-Oct-2012 (CT) Pass `json_indent` to `GTW.RST.MOM.Scope`
#    10-Oct-2012 (CT) Add `NET` to `PNS_Aliases`
#     7-Dec-2012 (CT) Add `User_Node`
#    17-Dec-2012 (CT) Add `User_Net_Device`, ...
#    17-Dec-2012 (CT) Wrap `User_...` resources in `TOP.Dir`
#    15-Apr-2013 (CT) Add `exclude_robots` to resource `/api`
#     3-May-2013 (CT) Rename `login_required` to `auth_required`
#     4-May-2013 (CT) Add `auth_required` to `RST.MOM.Scope`
#    20-May-2013 (CT) Import `_FFM.RST_Api_addons`
#    13-Jun-2013 (CT) Remove `PNS_Aliases`
#    23-Aug-2013 (CT) Add `-auth_required`, use it in `create_top`
#     7-Oct-2013 (CT) Add `RST_addons.User_Antenna`
#     1-Apr-2014 (CT) Add resource for `GTW.RST.MOM.Doc.App_Type`
#    14-Apr-2014 (CT) Add `pid="RESTful"` to resource `/api`
#    14-Apr-2014 (CT) Add `RST_addons.User_Net_Interface`
#    18-Apr-2014 (CT) Add `RST_addons.User_Person*`
#     5-May-2014 (CT) Replace `landing_page` bei `/about`; add `/impressum`
#    12-Jun-2014 (CT) DRY startup message
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _FFM                   import FFM
from   _GTW                   import GTW
from   _JNJ                   import JNJ
from   _MOM                   import MOM
from   _ReST                  import ReST
from   _TFL                   import TFL

from   _MOM.Product_Version   import Product_Version, IV_Number

import _FFM.import_FFM
import _GTW._OMP._Auth.import_Auth
import _GTW._OMP._PAP.import_PAP

import _GTW._RST._MOM.Doc
import _GTW._RST._MOM.Scope
import _GTW._RST._TOP._MOM.Doc
import _GTW._RST._TOP.ReST

import _GTW._Werkzeug.Command

import _GTW._OMP._Auth.Nav
import _GTW._OMP._PAP.Nav
import _FFM.Nav
import _FFM.RST_Api_addons

import _GTW.HTML
import _ReST.To_Html

from   _TFL                     import sos
from   _TFL.I18N                import _, _T, _Tn
from   _TFL.Regexp              import Re_Replacer
from   _TFL._Meta.Once_Property import Once_Property
from   _TFL._Meta.Property      import Class_Property

import _TFL.CAO

import _GTW._AFS._MOM.Spec

from   _Base_Command_           import _Base_Command_
import RST_addons

GTW.OMP.PAP.Phone.change_attribute_default         ("country_code", "43")

FFM.Version = Product_Version \
    ( productid           = u"FFM node data base"
    , productnick         = u"FFM"
    , productdesc         = u"Web application for FFM node data base"
    , date                = "29-Jul-2012 "
    , major               = 0
    , minor               = 2
    , patchlevel          = 0
    , author              = u"Christian Tanzer, Ralf Schlatterbeck"
    , copyright_start     = 2012
    , db_version          = IV_Number
        ( "db_version"
        , ("FFM", )
        , ("FFM", )
        , program_version = 1
        , comp_min        = 0
        , db_extension    = ".ffm"
        )
    )

impressum_contents = """

Name des Vereins
----------------

:email:`FunkFeuer Wien <vorstand@funkfeuer.at>` — Verein zur Förderung freier
Netze

`ZVR-Zahl`_: 814804682

Vereinssitz
-----------

1010 Wien, Gonzagagasse 11/25

.. _`ZVR-Zahl`: http://zvr.bmi.gv.at/Start

"""

impressum_contents_add = """
Copyright
---------

Die Inhalte dieser Seiten sind urheberrechtlich geschützt.

Haftungsausschluss
------------------

Jede Haftung für unmittelbare, mittelbare oder sonstige Schäden, unabhängig
von deren Ursachen, die aus der Benutzung oder Nichtverfügbarkeit der Daten
und Informationen dieser Homepage erwachsen, wird, soweit rechtlich zulässig,
ausgeschlossen.

"""
class Command (_Base_Command_, GTW.Werkzeug.Command) :
    """Manage database, run server or WSGI app."""

    ANS                     = FFM
    SALT                    = bytes ("fa89356c-0af1-4644-80d7-92702e4fd524")

    _default_db_name        = "ffm"
    _defaults               = dict \
        ( copyright_start   = 2012
        )
    _opts                   = \
        ( "-auth_required:B=True?Is authorization required?"
        ,
        )

    @Once_Property
    def src_dir (self) :
        import rst_top
        return rst_top.src_dir
    # end def src_dir

    @Once_Property
    def web_src_root (self) :
        import rst_top
        return rst_top.web_src_root
    # end def web_src_root

    def create_rst (self, cmd, ** kw) :
        return GTW.RST.Root \
            ( language          = "en"
            , entries           =
                [ GTW.RST.MOM.Scope        (name = "v1")
                , GTW.RST.MOM.Doc.App_Type (name = "v1-doc")
                ]
            , ** kw
            )
    # end def create_rst

    def create_top (self, cmd, ** kw) :
        import _GTW._RST._TOP.import_TOP
        import rst_top
        RST = GTW.RST
        TOP = RST.TOP
        auth_r \
            = TOP.MOM.Admin.E_Type._auth_required \
            = TOP.MOM.Admin.Group._auth_required \
            = cmd.auth_required
        result = rst_top.create (cmd, ** kw)
        result.add_entries \
            ( RST_addons.Dashboard
                ( auth_required   = auth_r
                , pid             = "DB"
                )
            , TOP.Page_ReST
                ( name            = "about"
                , short_title     = "Über Funkfeuer"
                , title           = "Über Funkfeuer"
                , page_template_name = "html/dashboard/about.jnj"
                )
            , TOP.Dir
                ( name            = "My-Funkfeuer"
                , short_title     = "My Funkfeuer"
                , auth_required   = auth_r
                , permission      = RST_addons.Login_has_Person
                , entries         =
                    [ RST_addons.User_Node
                        ( name            = "node"
                        )
                    , RST_addons.User_Net_Device
                        ( name            = "device"
                        , short_title     = _T ("Device")
                        )
                    , RST_addons.User_Net_Interface
                        ( name            = "interface"
                        , short_title     = _T ("Interface")
                        )
                    , RST_addons.User_Wired_Interface
                        ( name            = "wired-interface"
                        , short_title     = _T ("Wired_Interface")
                        )
                    , RST_addons.User_Wireless_Interface
                        ( name            = "wireless-interface"
                        , short_title     = _T ("Wireless_Interface")
                        )
                    , RST_addons.User_Antenna
                        ( name            = "antenna"
                        , short_title     = _T ("Antenna")
                        )
                    , RST_addons.User_Person
                        ( name            = "person"
                        , hidden          = True
                        )
                    , RST_addons.User_Person_has_Address
                        ( name            = "has_address"
                        , hidden          = True
                        )
                    , RST_addons.User_Person_has_Account
                        ( name            = "has_account"
                        , hidden          = True
                        )
                    , RST_addons.User_Person_has_Email
                        ( name            = "has_email"
                        , hidden          = True
                        )
                    , RST_addons.User_Person_has_IM_Handle
                        ( name            = "has_im_handle"
                        , hidden          = True
                        )
                    , RST_addons.User_Person_has_Phone
                        ( name            = "has_phone"
                        , hidden          = True
                        )
                    ]
                )
            , TOP.MOM.Doc.App_Type
                ( name            = "Doc"
                , short_title     = _ ("Model doc")
                , title           = _ ("Documentation for FFM object model")
                )
            , TOP.MOM.Admin.Site
                ( name            = "Admin"
                , short_title     = "Admin"
                , pid             = "Admin"
                , title           = _ ("Administration of FFM node database")
                , head_line       = _ ("Administration of FFM node database")
                , auth_required   = auth_r
                , entries         =
                    [ self.nav_admin_group
                        ( "FFM"
                        , _ ("Administration of node database")
                        , "FFM"
                        , permission = RST.In_Group ("FFM-admin")
                            if auth_r else None
                        )
                    , self.nav_admin_group
                        ( "PAP"
                        , _ ("Administration of persons/addresses...")
                        , "GTW.OMP.PAP"
                        , permission = RST.In_Group ("FFM-admin")
                            if auth_r else None
                        )
                    , self.nav_admin_group
                        ( _ ("Users")
                        , _ ("Administration of user accounts and groups")
                        , "GTW.OMP.Auth"
                        , permission = RST.Is_Superuser ()
                        )
                    ]
                )
            , GTW.RST.MOM.Scope
                ( name            = "api"
                , auth_required   = auth_r
                , exclude_robots  = True
                , json_indent     = 2
                , pid             = "RESTful"
                )
            , TOP.Page_ReST
                ( name               = "impressum"
                , short_title        = "Impressum"
                , title              = "Impressum"
                , page_template_name = "html/dashboard/static.jnj"
                , src_contents       = impressum_contents
                )
            , GTW.RST.MOM.Doc.App_Type
                ( name            = "api-doc"
                , hidden          = True
                )
            , TOP.Auth
                ( name            = _ ("Auth")
                , pid             = "Auth"
                , short_title     = _ (u"Authorization and Account handling")
                , hidden          = True
                )
            , TOP.L10N
                ( name            = _ ("L10N")
                , short_title     =
                  _ (u"Choice of language used for localization")
                , country_map     = dict (de = "AT")
                )
            , TOP.Robot_Excluder ()
            )
        if cmd.debug :
            result.add_entries \
                ( TOP.Console
                    ( name            = "Console"
                    , short_title     = _ ("Console")
                    , title           = _ ("Interactive Python interpreter")
                    , permission      = RST.Is_Superuser ()
                    )
                , RST.Raiser
                    ( name            = "RAISE"
                    , hidden          = True
                    )
                )
        if result.DEBUG :
            scope = result.__dict__.get ("scope", "*not yet created*")
            print ("RST.TOP root created,", scope)
        return result
    # end def create_nav

    def fixtures (self, scope) :
        import fixtures
        return fixtures.create (scope)
    # end def fixtures

    def _create_templateer (self, cmd, ** kw) :
        if cmd.UTP.use_templateer :
            import rst_top
            return self.__super._create_templateer \
                ( cmd
                , load_path         = rst_top.template_dirs
                , Media_Parameters  = rst_top.Media_Parameters
                , ** kw
                )
    # end def _create_templateer

# end class Scaffold

command = Command ()

opts = command.opts + command ["run_server"].opts

def scope (cmd = None) :
    args = (cmd.db_url, cmd.db_name, cmd.create) if cmd else ()
    return command.scope (* args)
# end def scope

if __name__ == "__main__" :
    command ()
### __END__ model
