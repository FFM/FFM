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
            , 'manager.pid'
            , 'manager.url'
            , 'lifetime.start'
            , 'lifetime.finish'
            , 'owner.pid'
            , 'owner.url'
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
            , 'manager.pid'
            , 'manager.url'
            , 'lifetime.start'
            , 'lifetime.finish'
            , 'owner.pid'
            , 'owner.url'
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


    >>> r = show (R.get ("/v1/FFM-Net_Interface_in_IP4_Network?verbose&closure&order_by=pid&limit=1"))
    { 'json' :
        { 'attribute_names' :
            [ 'left.pid'
            , 'left.url'
            , 'right.pid'
            , 'right.url'
            , 'ip_address.address'
            ]
        , 'entries' :
            [ { 'attributes' :
                  { 'ip_address' :
                      { 'address' : '192.168.23.1' }
                  , 'left' :
                      { 'attributes' :
                          { 'left' :
                              { 'attributes' :
                                  { 'left' :
                                      { 'attributes' :
                                          { 'model_no' : ''
                                          , 'name' : 'generic'
                                          , 'revision' : ''
                                          }
                                      , 'cid' : 5
                                      , 'pid' : 5
                                      , 'type_name' : 'FFM.Net_Device_Type'
                                      , 'url' : '/v1/FFM-Net_Device_Type/5'
                                      }
                                  , 'name' : 'dev'
                                  , 'node' :
                                      { 'attributes' :
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
                                          , 'name' : 'node2'
                                          , 'owner' :
                                              { 'pid' : 1
                                              , 'url' : '/v1/PAP-Person/1'
                                              }
                                          , 'position' :
                                              { 'lat' : 48.28601111111111
                                              , 'lon' : 15.8744
                                              }
                                          }
                                      , 'cid' : 3
                                      , 'pid' : 3
                                      , 'type_name' : 'FFM.Node'
                                      , 'url' : '/v1/FFM-Node/3'
                                      }
                                  }
                              , 'cid' : 6
                              , 'pid' : 6
                              , 'type_name' : 'FFM.Net_Device'
                              , 'url' : '/v1/FFM-Net_Device/6'
                              }
                          , 'mac_address' : ''
                          , 'name' : 'wr'
                          }
                      , 'cid' : 7
                      , 'pid' : 7
                      , 'type_name' : 'FFM.Wired_Interface'
                      , 'url' : '/v1/FFM-Wired_Interface/7'
                      }
                  , 'right' :
                      { 'attributes' :
                          { 'net_address' :
                              { 'address' : '192.168.23.0/24' }
                          }
                      , 'cid' : 4
                      , 'pid' : 4
                      , 'type_name' : 'FFM.IP4_Network'
                      , 'url' : '/v1/FFM-IP4_Network/4'
                      }
                  }
              , 'cid' : 9
              , 'pid' : 9
              , 'type_name' : 'FFM.Wired_Interface_in_IP4_Network'
              , 'url' : '/v1/FFM-Net_Interface_in_IP4_Network/9'
              }
            ]
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/FFM-Net_Interface_in_IP4_Network?verbose&closure&order_by=pid&limit=1'
    }

    >>> server.terminate ()
"""

__test__ = Scaffold.create_test_dict \
    ( dict
        ( test_get = _test_get
        )
    )

if __name__ == "__main__" :
    rst_harness._main (Scaffold)
### __END__ FFM.__test__.RST
