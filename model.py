# -*- coding: iso-8859-15 -*-
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

landing_page = """
Statt :q:`Ich will ins Netz` :q:`Wir sind das Netz`
===================================================

Was?
++++

Frei
----

FunkFeuer ist ein freies, experimentelles Netzwerk in Wien, Graz, der
Weststeiermark, in Teilen des Weinviertels (NÖ) und in Bad Ischl. Es wird
aufgebaut und betrieben von computerbegeisterten Menschen. Das Projekt verfolgt
keine kommerziellen Interessen.

Offen
-----

FunkFeuer ist offen für jeden und jede, der/die Interesse hat und bereit ist
mitzuarbeiten. Es soll dabei ein nicht reguliertes Netzwerk entstehen, welches
das Potential hat, den digitalen Graben zwischen den sozialen Schichten zu
überbrücken und so Infrastruktur und Wissen zur Verfügung zu stellen. Teilnahme
Zur Teilnahme an FunkFeuer braucht man einen WLAN Router (gibt's ab 60 Euro)
oder einen PC, das OLSR Programm, eine IP Adresse von FunkFeuer, etwas Geduld
und Motivation. Auf unserer Karte ist eingezeichnet, wo man FunkFeuer schon
überall (ungefähr) empfangen kann (bitte beachte, dass manchmal Häuser oder
ähnliches im Weg sind, dann geht's nur über Umwege).

*Wir bauen uns unser Netzwerk selber!*

WIE?
++++

Eine Einführung gibts als `PDF-Datei`_ (Danke Andreas!)
Die `ersten Schritte`_ werden im `wiki`_ erläutert.

.. _`PDF-Datei`:
    http://funkfeuer.at/fileadmin/Dokumente/vortraege/FunkFeuer_Intro.pdf
.. _`ersten Schritte`: http://wiki.funkfeuer.at/index.php/Erste_Schritte
.. _`wiki`: http://wiki.funkfeuer.at/

Siehe auch `die Geschichte von Funkfeuer`_.

.. _`die Geschichte von Funkfeuer`: http://www.funkfeuer.at/Geschichte.94.0.html

WARUM?
++++++

`Darum!`_

.. _`Darum!`:
    http://wiki.funkfeuer.at/index.php/Die_Konstruktion_der_Netzwerk-Allmende


Armin Medosch hat die Theorie der freien Netze sehr gut analyisiert und sogar
ein `Buch`_ darüber geschrieben.

.. _`Buch`: http://www.heise.de/tp/r4/buch/buch_11.html

Cooles Projekt, wie kann ich helfen?
++++++++++++++++++++++++++++++++++++

Vielseitig! wir sind ein kleines Team und können **jede** Unterstützung
gebrauchen.

Tritt einfach mit uns in Kontakt. Es gibt verschiedene Arbeitsgruppen. Die
meiste Kommunikation verläuft über die `Mailinglisten`_.

.. _`Mailinglisten`: http://funkfeuer.at/Mailinglisten.61.0.html
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
                [ GTW.RST.MOM.Scope (name = "v1")
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
            ( TOP.Dir
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
                    , RST_addons.User_Wired_Interface
                        ( name            = "wired-interface"
                        , short_title     = _T ("Wired IF")
                        )
                    , RST_addons.User_Wireless_Interface
                        ( name            = "wireless-interface"
                        , short_title     = _T ("Wireless IF")
                         )
                    ]
                )
            , TOP.Page_ReST
                ( name            = "Funkfeuer"
                , short_title     = "Funkfeuer?"
                , title           = "Was ist Funkfeuer?"
                , src_contents    = landing_page
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
            print ("RST.TOP root created, Scope", scope)
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
