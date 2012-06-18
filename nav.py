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
#    nav
#
# Purpose
#    Create navigation tree
#
# Revision Dates
#    26-Mar-2012 (CT) Creation
#    18-Jun-2012 (CT) Add `email_from` to `nav_kw_args`
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _FFM                   import FFM
from   _GTW                   import GTW
from   _JNJ                   import JNJ
from   _MOM                   import MOM
from   _TFL                   import TFL

from   _TFL                   import sos
from   _TFL.Attr_Mapper       import Attr_Mapper
from   _TFL.I18N              import _, _T, _Tn

import _GTW.Media
import _GTW._NAV.Template_Media_Cache

import _GTW._NAV.import_NAV
import _GTW._NAV.Calendar
import _GTW._NAV.Console
import _GTW._NAV._E_Type.Gallery
import _GTW._NAV._E_Type.SRM

import _JNJ.Templateer

import _TFL.Record
import _TFL.SMTP

from   Media_Defaults import Media_Defaults
Media_Parameters = Media_Defaults ()

from   posixpath              import join  as pjoin

jnj_src      = sos.path.dirname (__file__)
web_root_dir = "http://ffm.funkfeuer.at"
web_src_root = sos.path.abspath \
    (sos.path.normpath (sos.path.join (jnj_src, "..")))
web_src      = sos.path.join (web_src_root, "src")

base_template_dir = sos.path.dirname (_JNJ.__file__)
template_dirs     = \
    [ jnj_src
    , sos.path.join (jnj_src, "html") ### XXX remove after final switch to Jinja
    , base_template_dir
    ]

web_links = \
    [ TFL.Record
        ( href        = "http://guifi.net/en/"
        , title       = "Spanish open wireless network"
        , short_title = "Guifi.net"
        )
    , TFL.Record
        ( href        = "http://wlan-si.net/"
        , title       = "Slovenian open wireless network"
        , short_title = "wlan-si"
        )
    ]

def nav_kw_args \
        ( cmd, home_url_root, permissive
        , App_Type          = None
        , DB_Url            = None
        , auto_delegate     = False
        , HTTP              = None
        , version           = "html/5.jnj"
        , ** kw
        ) :
    nav_context             = dict \
        ( GTW               = GTW
        , Q                 = MOM.Q
        , FFM               = FFM
        )
    return dict \
        ( App_Type          = App_Type
        , auto_delegate     = auto_delegate
        , console_context   = dict
            ( nav_context
            , cmd           = cmd
            , JNJ           = JNJ
            , MOM           = MOM
            )
        , copyright_start   = cmd.copyright_start
        , copyright_url     = "/impressum.html" ### XXX ???
        , Media_Parameters  = Media_Parameters
        , DB_Url            = DB_Url
        , DEBUG             = cmd.debug
        , email_from        = cmd.email_from or None
        , encoding          = cmd.output_encoding
        , hide_marginal     = True
        , HTTP              = HTTP
        , input_encoding    = cmd.input_encoding
        , language          = "de"
        , nav_context       = nav_context
        , owner             = "Funkfeuer"
        , permissive        = permissive
        , site_url          = home_url_root
        , smtp              = TFL.SMTP (cmd.smtp_server)
        , template_name     = cmd.template_file
        , Templateer        = JNJ.Templateer
            ( encoding          = cmd.input_encoding
            , globals           = dict (site_base = cmd.template_file)
            , i18n              = True
            , load_path         = template_dirs
            , trim_blocks       = True
            , version           = version
            , Media_Parameters  = Media_Parameters
            )
        , TEST              = cmd.TEST
        , web_links         = web_links
        , webmaster         =
            ("christian.tanzer@gmail.com", "Christian Tanzer") ### XXX ???
        , ** kw
        )
# end def nav_kw_args

def create (cmd, app_type, db_url, ** kw) :
    return GTW.NAV.Root \
        ( jnj_src
        , ** nav_kw_args
            ( cmd, cmd.home_url_root
            , auto_delegate   = False
            , DB_Url          = db_url
            , App_Type        = app_type
            , HTTP            = cmd.HTTP
            , permissive      = False
            , ** kw
            )
        )
# end def create

### __END__ nav
