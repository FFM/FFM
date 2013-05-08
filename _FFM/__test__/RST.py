# -*- coding: iso-8859-15 -*-
# Copyright (C) 2013 Mag. Christian Tanzer All rights reserved
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
#    FFM.__test__.RST
#
# Purpose
#    Test RESTful api for FFM
#
# Revision Dates
#     9-Jan-2013 (CT) Creation
#     1-Feb-2013 (RS) Fix rounding error with python2.6
#     5-Mar-2013 (CT) Adapt to changes in `Net_Interface_in_IP4_Network`
#    28-Mar-2013 (CT) Factor `_test_limit` from `_test_get`
#     3-May-2013 (CT) Add test for `META` query argument
#     8-May-2013 (CT) Remove `.pid`, `.url` from `attribute_names`, unless CSV
#    ««revision-date»»···
#--

from   __future__ import absolute_import, division, print_function, unicode_literals

from   _FFM                       import FFM
from   _GTW.__test__.rst_harness  import *
from   _GTW.__test__              import rst_harness

import _FFM.import_FFM
import _GTW._OMP._Auth.import_Auth
import _GTW._OMP._PAP.import_PAP

import _GTW._RST._MOM.Client

def run_server (db_url = "hps://", db_name = None) :
    return rst_harness.run_server ("_FFM.__test__.RST", db_url, db_name)
# end def run_server

class FFM_RST_Test_Command (GTW_RST_Test_Command) :

    ANS                     = FFM
    PNS_Aliases             = dict \
        ( Auth              = GTW.OMP.Auth
        , PAP               = GTW.OMP.PAP
        )

    def fixtures (self, scope) :
        from _FFM.__test__.fixtures import create
        create (scope)
        PAP = scope.PAP
        nod = scope.FFM.Node.query (name = "node2").one ()
        nod.address = PAP.Address \
            ( street  = 'Beispiel 23'
            , zip     = '1010'
            , city    = 'Wien'
            , country = 'Austria'
            )
        scope.commit ()
    # end def fixtures

# end class FFM_RST_Test_Command

Scaffold   = FFM_RST_Test_Command ()

### «text» ### The doctest follows::

_test_get = r"""
    >>> server = run_server (%(p1)s, %(n1)s)

    >>> CC = GTW.RST.MOM.Client.Requester (R.prefix, verify = False)
    >>> r = CC.get ("")
    >>> r._url
    u'http://localhost:9999/'

    >>> r = show (R.get ("/v1/FFM-Node"))
    { 'json' :
        { 'entries' :
            [ '/v1/FFM-Node/2'
            , '/v1/FFM-Node/3'
            ]
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/FFM-Node'
    }

    >>> r = show (R.get ("/v1/FFM-Node?verbose&order_by=pid&limit=1"))
    { 'json' :
        { 'attribute_names' :
            [ 'name'
            , 'manager'
            , 'lifetime.start'
            , 'lifetime.finish'
            , 'address'
            , 'owner'
            , 'position.lat'
            , 'position.lon'
            , 'position.height'
            , 'show_in_map'
            ]
        , 'entries' :
            [ { 'attributes' :
                  { 'manager' :
                      { 'pid' : 1
                      , 'url' : '/v1/PAP-Person/1'
                      }
                  , 'name' : 'nogps'
                  , 'owner' :
                      { 'pid' : 1
                      , 'url' : '/v1/PAP-Person/1'
                      }
                  }
              , 'cid' : 2
              , 'pid' : 2
              , 'type_name' : 'FFM.Node'
              , 'url' : '/v1/FFM-Node/2'
              }
            ]
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/FFM-Node?verbose&order_by=pid&limit=1'
    }

    >>> r = show (R.get ("/v1/FFM-Node?verbose&closure&order_by=pid&limit=1"))
    { 'json' :
        { 'attribute_names' :
            [ 'name'
            , 'manager'
            , 'lifetime.start'
            , 'lifetime.finish'
            , 'address'
            , 'owner'
            , 'position.lat'
            , 'position.lon'
            , 'position.height'
            , 'show_in_map'
            ]
        , 'entries' :
            [ { 'attributes' :
                  { 'manager' :
                      { 'attributes' :
                          { 'first_name' : 'ralf'
                          , 'last_name' : 'schlatterbeck'
                          , 'middle_name' : ''
                          , 'title' : ''
                          }
                      , 'cid' : 1
                      , 'pid' : 1
                      , 'type_name' : 'PAP.Person'
                      , 'url' : '/v1/PAP-Person/1'
                      }
                  , 'name' : 'nogps'
                  , 'owner' :
                      { 'pid' : 1
                      , 'url' : '/v1/PAP-Person/1'
                      }
                  }
              , 'cid' : 2
              , 'pid' : 2
              , 'type_name' : 'FFM.Node'
              , 'url' : '/v1/FFM-Node/2'
              }
            ]
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/FFM-Node?verbose&closure&order_by=pid&limit=1'
    }


    >>> r = show (R.get ("/v1/FFM-Net_Interface_in_IP4_Network?brief"))
    { 'json' :
        { 'entries' :
            [ 31
            , 32
            , 33
            , 34
            ]
        , 'url_template' : '/v1/FFM-Net_Interface_in_IP4_Network/{entry}'
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/FFM-Net_Interface_in_IP4_Network?brief'
    }

"""

_test_limit = r"""
    >>> server = run_server (%(p1)s, %(n1)s)

    >>> r = show (R.get ("/v1/FFM-Net_Interface_in_IP4_Network?verbose&closure&order_by=pid&limit=1"))
    { 'json' :
        { 'attribute_names' :
            [ 'left'
            , 'right'
            , 'mask_len'
            ]
        , 'entries' :
            [ { 'attributes' :
                  { 'left' :
                      { 'attributes' :
                          { 'left' :
                              { 'attributes' :
                                  { 'left' :
                                      { 'attributes' :
                                          { 'model_no' : ''
                                          , 'name' : 'generic'
                                          , 'revision' : ''
                                          }
                                      , 'cid' : 42
                                      , 'pid' : 27
                                      , 'type_name' : 'FFM.Net_Device_Type'
                                      , 'url' : '/v1/FFM-Net_Device_Type/27'
                                      }
                                  , 'name' : 'dev'
                                  , 'node' :
                                      { 'attributes' :
                                          { 'address' :
                                              { 'attributes' :
                                                  { 'city' : 'wien'
                                                  , 'country' : 'austria'
                                                  , 'street' : 'beispiel 23'
                                                  , 'zip' : '1010'
                                                  }
                                              , 'cid' : 50
                                              , 'pid' : 35
                                              , 'type_name' : 'PAP.Address'
                                              , 'url' : '/v1/PAP-Address/35'
                                              }
                                          , 'manager' :
                                              { 'attributes' :
                                                  { 'first_name' : 'ralf'
                                                  , 'last_name' : 'schlatterbeck'
                                                  , 'middle_name' : ''
                                                  , 'title' : ''
                                                  }
                                              , 'cid' : 1
                                              , 'pid' : 1
                                              , 'type_name' : 'PAP.Person'
                                              , 'url' : '/v1/PAP-Person/1'
                                              }
                                          , 'name' : 'node2'
                                          , 'owner' :
                                              { 'pid' : 1
                                              , 'url' : '/v1/PAP-Person/1'
                                              }
                                          , 'position' :
                                              { 'lat' : 48.25
                                              , 'lon' : 15.8744
                                              }
                                          }
                                      , 'cid' : 51
                                      , 'pid' : 3
                                      , 'type_name' : 'FFM.Node'
                                      , 'url' : '/v1/FFM-Node/3'
                                      }
                                  }
                              , 'cid' : 43
                              , 'pid' : 28
                              , 'type_name' : 'FFM.Net_Device'
                              , 'url' : '/v1/FFM-Net_Device/28'
                              }
                          , 'mac_address' : ''
                          , 'name' : 'wr'
                          }
                      , 'cid' : 44
                      , 'pid' : 29
                      , 'type_name' : 'FFM.Wired_Interface'
                      , 'url' : '/v1/FFM-Wired_Interface/29'
                      }
                  , 'mask_len' : 24
                  , 'right' :
                      { 'attributes' :
                          { 'net_address' :
                              { 'address' : '192.168.23.1' }
                          }
                      , 'cid' : 29
                      , 'pid' : 20
                      , 'type_name' : 'FFM.IP4_Network'
                      , 'url' : '/v1/FFM-IP4_Network/20'
                      }
                  }
              , 'cid' : 46
              , 'pid' : 31
              , 'type_name' : 'FFM.Wired_Interface_in_IP4_Network'
              , 'url' : '/v1/FFM-Net_Interface_in_IP4_Network/31'
              }
            ]
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/FFM-Net_Interface_in_IP4_Network?verbose&closure&order_by=pid&limit=1'
    }

    >>> r = show (R.get ("/v1/FFM-Net_Interface_in_IP4_Network?verbose&closure&order_by=pid&limit=1&META"), cleaner = date_cleaner)
    { 'json' :
        { 'attribute_names' :
            [ 'left'
            , 'right'
            , 'mask_len'
            ]
        , 'entries' :
            [ { 'attributes' :
                  { 'left' :
                      { 'attributes' :
                          { 'left' :
                              { 'attributes' :
                                  { 'left' :
                                      { 'attributes' :
                                          { 'model_no' : ''
                                          , 'name' : 'generic'
                                          , 'revision' : ''
                                          }
                                      , 'cid' : 42
                                      , 'creation' :
                                          { 'date' : <datetime> }
                                      , 'last_change' :
                                          { 'date' : <datetime> }
                                      , 'pid' : 27
                                      , 'type_name' : 'FFM.Net_Device_Type'
                                      , 'url' : '/v1/FFM-Net_Device_Type/27'
                                      }
                                  , 'name' : 'dev'
                                  , 'node' :
                                      { 'attributes' :
                                          { 'address' :
                                              { 'attributes' :
                                                  { 'city' : 'wien'
                                                  , 'country' : 'austria'
                                                  , 'street' : 'beispiel 23'
                                                  , 'zip' : '1010'
                                                  }
                                              , 'cid' : 50
                                              , 'creation' :
                                                  { 'date' : <datetime> }
                                              , 'last_change' :
                                                  { 'date' : <datetime> }
                                              , 'pid' : 35
                                              , 'type_name' : 'PAP.Address'
                                              , 'url' : '/v1/PAP-Address/35'
                                              }
                                          , 'manager' :
                                              { 'attributes' :
                                                  { 'first_name' : 'ralf'
                                                  , 'last_name' : 'schlatterbeck'
                                                  , 'middle_name' : ''
                                                  , 'title' : ''
                                                  }
                                              , 'cid' : 1
                                              , 'creation' :
                                                  { 'date' : <datetime> }
                                              , 'last_change' :
                                                  { 'date' : <datetime> }
                                              , 'pid' : 1
                                              , 'type_name' : 'PAP.Person'
                                              , 'url' : '/v1/PAP-Person/1'
                                              }
                                          , 'name' : 'node2'
                                          , 'owner' :
                                              { 'pid' : 1
                                              , 'url' : '/v1/PAP-Person/1'
                                              }
                                          , 'position' :
                                              { 'lat' : 48.25
                                              , 'lon' : 15.8744
                                              }
                                          }
                                      , 'cid' : 51
                                      , 'creation' :
                                          { 'date' : <datetime> }
                                      , 'last_change' :
                                          { 'date' : <datetime> }
                                      , 'pid' : 3
                                      , 'type_name' : 'FFM.Node'
                                      , 'url' : '/v1/FFM-Node/3'
                                      }
                                  }
                              , 'cid' : 43
                              , 'creation' :
                                  { 'date' : <datetime> }
                              , 'last_change' :
                                  { 'date' : <datetime> }
                              , 'pid' : 28
                              , 'type_name' : 'FFM.Net_Device'
                              , 'url' : '/v1/FFM-Net_Device/28'
                              }
                          , 'mac_address' : ''
                          , 'name' : 'wr'
                          }
                      , 'cid' : 44
                      , 'creation' :
                          { 'date' : <datetime> }
                      , 'last_change' :
                          { 'date' : <datetime> }
                      , 'pid' : 29
                      , 'type_name' : 'FFM.Wired_Interface'
                      , 'url' : '/v1/FFM-Wired_Interface/29'
                      }
                  , 'mask_len' : 24
                  , 'right' :
                      { 'attributes' :
                          { 'net_address' :
                              { 'address' : '192.168.23.1' }
                          }
                      , 'cid' : 29
                      , 'creation' :
                          { 'date' : <datetime> }
                      , 'last_change' :
                          { 'date' : <datetime> }
                      , 'pid' : 20
                      , 'type_name' : 'FFM.IP4_Network'
                      , 'url' : '/v1/FFM-IP4_Network/20'
                      }
                  }
              , 'cid' : 46
              , 'creation' :
                  { 'date' : <datetime> }
              , 'last_change' :
                  { 'date' : <datetime> }
              , 'pid' : 31
              , 'type_name' : 'FFM.Wired_Interface_in_IP4_Network'
              , 'url' : '/v1/FFM-Net_Interface_in_IP4_Network/31'
              }
            ]
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/FFM-Net_Interface_in_IP4_Network?verbose&closure&order_by=pid&limit=1&META'
    }

"""

__test__ = Scaffold.create_test_dict \
    ( dict
        ( test_get   = _test_get
        , test_limit = _test_limit
        )
    )

if __name__ == "__main__" :
    rst_harness._main (Scaffold)
### __END__ FFM.__test__.RST
