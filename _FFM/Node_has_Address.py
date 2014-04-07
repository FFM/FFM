# -*- coding: utf-8 -*-
# Copyright (C) 2012-2013 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package FFM.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# ****************************************************************************
#
#++
# Name
#    GTW.OMP.PAP.Node_has_Address
#
# Purpose
#    Model the link between a Node and an Address:
#    allow only one Address per Node
#
# Revision Dates
#    12-Oct-2012 (RS) Creation
#    16-Apr-2013 (CT) Update `auto_derive_np_kw` instead of explicit class
#    ««revision-date»»···
#--

from   __future__            import unicode_literals

from   _GTW._OMP._PAP.Subject_has_Property import Subject_has_Property

Subject_has_Property.auto_derive_np_kw \
    ["Node_has_Address"] ["left"].update (max_links = 1)

### __END__ FFM.Node_has_Address
