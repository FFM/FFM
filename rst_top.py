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
#    rst_top
#
# Purpose
#    Create navigation tree
#
# Revision Dates
#    26-Mar-2012 (CT) Creation
#    18-Jun-2012 (CT) Add `email_from` to `nav_kw_args`
#    29-Jul-2012 (CT) Change to use `GTW.RST.TOP` instead of `GTW.NAV`
#    29-Jul-2012 (CT) Rename to `rst_top`
#     4-Dec-2012 (CT) Remove `http:` (--> protocol-relative)
#     4-May-2013 (CT) Re-add `http:` for external URLs
#     4-May-2013 (CT) Add `RAT`
#     2-May-2014 (CT) Use option `webmaster`
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

import _GTW._RST.RAT
import _GTW._RST._TOP.import_TOP
import _GTW._RST._TOP._MOM.import_MOM

import _JNJ

from   _MOM.import_MOM        import Q

import _TFL.Record

from   Media_Parameters       import Media_Parameters

Media_Parameters = Media_Parameters ()

src_dir      = sos.path.dirname (__file__)
web_root_dir = "//ffm.funkfeuer.at"
web_src_root = sos.path.abspath (src_dir)

base_template_dir = sos.path.dirname (_JNJ.__file__)
template_dirs     = [src_dir, base_template_dir]

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

def root_kw_args (cmd, ** kw) :
    return dict \
        ( console_context   = dict
            ( FFM           = FFM
            , GTW           = GTW
            , JNJ           = JNJ
            , MOM           = MOM
            , Q             = MOM.Q
            , cmd           = cmd
            )
        , copyright_url     = "/impressum.html" ### XXX ???
        , Media_Parameters  = Media_Parameters
        , language          = "de"
        , owner             = "Funkfeuer"
        , web_links         = web_links
        , webmaster         = cmd.webmaster
        , entries           =
            [ GTW.RST.RAT (name = "RAT")
            ]
        , ** kw
        )
# end def root_kw_args

def create (cmd, ** kw) :
    return GTW.RST.TOP.Root (** root_kw_args (cmd, ** kw))
# end def create

### __END__ rst_top
