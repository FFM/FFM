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
#    FFM.__test__.example
#
# Purpose
#    Example how to use test scaffolding for FFM
#
# Revision Dates
#    18-Sep-2012 (CT) Creation
#    ««revision-date»»···
#--

from   __future__ import absolute_import, division, print_function, unicode_literals

from   _GTW.__test__.model      import *

_test_code = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...

    >>> for T in scope.T_Extension :
    ...     if hasattr (T, "refuse_links") :
    ...         print (T.type_name, sorted (T.refuse_links))
    MOM.Id_Entity []
    MOM.Link []
    MOM.Link1 []
    MOM._MOM_Link_n_ []
    MOM.Link2 []
    MOM.Link2_Ordered []
    MOM.Link3 []
    MOM.Object []
    MOM.Named_Object []
    Auth.Link1 []
    Auth.Link2 []
    Auth.Link2_Ordered []
    Auth.Link3 []
    Auth.Object []
    Auth.Id_Entity []
    Auth.Named_Object []
    Auth.Account []
    Auth.Account_Anonymous [u'GTW.OMP.Auth.Account_in_Group']
    Auth.Account_P []
    Auth.Group []
    Auth.Account_in_Group []
    Auth._Account_Action_ []
    Auth.Account_Activation []
    Auth.Account_Password_Change_Required []
    Auth._Account_Token_Action_ []
    Auth.Account_EMail_Verification []
    Auth.Account_Password_Reset []
    EVT.Link1 []
    EVT.Link2 []
    EVT.Link2_Ordered []
    EVT.Link3 []
    EVT.Object []
    EVT.Id_Entity []
    EVT.Named_Object []
    EVT.Calendar []
    PAP.Link1 []
    PAP.Link2 []
    PAP.Link2_Ordered []
    PAP.Link3 []
    PAP.Object []
    PAP.Id_Entity []
    PAP.Named_Object []
    PAP.Subject []
    PAP.Person []
    SWP.Link1 []
    SWP.Link2 []
    SWP.Link2_Ordered []
    SWP.Link3 []
    SWP.Object []
    SWP.Id_Entity []
    SWP.Named_Object []
    SWP.Object_PN []
    SWP.Page []
    SWP.Page_Y []
    EVT.Event []
    EVT.Event_occurs []
    EVT._Recurrence_Mixin_ []
    EVT.Recurrence_Spec []
    EVT.Recurrence_Rule []
    PAP.Address []
    PAP.Company []
    PAP.Email []
    PAP.Phone []
    PAP.Subject_has_Property []
    PAP.Subject_has_Address []
    PAP.Company_has_Address []
    PAP.Subject_has_Email []
    PAP.Company_has_Email []
    PAP.Subject_has_Phone []
    PAP.Company_has_Phone []
    PAP.Entity_created_by_Person [u'GTW.OMP.PAP.Entity_created_by_Person', u'PAP.Entity_created_by_Person']
    PAP.Person_has_Address []
    PAP.Person_has_Email []
    PAP.Person_has_Phone []
    SRM.Link1 []
    SRM.Link2 []
    SRM.Link2_Ordered []
    SRM.Link3 []
    SRM.Object []
    SRM.Id_Entity []
    SRM.Named_Object []
    SRM._Boat_Class_ []
    SRM.Boat_Class []
    SRM.Handicap []
    SRM.Boat []
    SRM.Club []
    SRM.Regatta_Event []
    SWP.Clip_O []
    SWP.Clip_X []
    SWP.Gallery []
    SWP.Picture []
    SRM.Page []
    SRM.Regatta []
    SRM.Regatta_C []
    SRM.Regatta_H []
    SRM.Sailor []
    SRM.Boat_in_Regatta []
    SRM.Race_Result []
    SRM.Team []
    SRM.Crew_Member []
    SRM.Team_has_Boat_in_Regatta []

    >>> scope.destroy ()

"""

__test__ = Scaffold.create_test_dict \
  ( dict
      ( main       = _test_code
      )
  )

### __END__ FFM.__test__.example
