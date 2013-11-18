#!/usr/bin/python
# -*- coding: utf-8 -*-
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

from   rsclib.HTML_Parse  import tag
from   rsclib.autosuper   import autosuper

class Version_Mixin (autosuper) :
    version      = "Unknown"
    luci_version = bf_version = None

    def try_get_version (self, div) :
        if div.get ('class') == 'footer' :
            for p in div.findall (".//%s" % tag ("p")) :
                if  (   p.get ('class') == 'luci'
                    and len (p)
                    and p [0].tag == tag ("a")
                    ) :
                    a = p [0]
                    if a.text.startswith ("Powered by LuCI") :
                        self.luci_version = a.text
        if div.get ('class') == 'header_right' :
            self.bf_version = div.text
        if div.get ('class') == 'hostinfo' :
            assert self.bf_version is None
            self.bf_version = div.text.split ('|') [0].strip ()
        if div.get ('id') == 'header' and not self.bf_version :
            p = div.find (".//%s" % tag ("p"))
            if p is not None :
                v = p.text.split (':', 1) [-1].split ('|', 1) [0]
                self.bf_version = v
    # end def try_get_version

    def set_version (self, root) :
        lv = self.luci_version
        if lv is None :
            p = root [-1][-1]
            if p.tag == tag ('p') and p.get ('class') == 'luci' :
                lv = self.luci_version = self.tree.get_text (p)
        if (lv and lv.startswith ('Powered by LuCI')) :
            lv = lv.split ('(', 1) [-1].split (')', 1) [0]
            self.luci_version = lv
        if self.bf_version and self.luci_version :
            self.version = "%s / Luci %s" % (self.bf_version, self.luci_version)
    # end def set_version

# end class Version_Mixin
