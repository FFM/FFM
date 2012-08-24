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
#    fixtures
#
# Purpose
#    Create standard objects for new scope
#
# Revision Dates
#    26-Mar-2012 (CT) Creation
#    24-Aug-2012 (RS) Add Wireless channels and standards,
#                     add commented-out regulatory info for Austria.
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

def create (scope) :
    Auth = scope.Auth
    Auth.Account_Anonymous ("anonymous")
    Auth.Account_P.create_new_account_x \
        ( "christian.tanzer@gmail.com"
        , password = "123", enabled = True, superuser = True, suspended = False
        )
    Auth.Account_P.create_new_account_x \
        ( "tanzer@swing.co.at"
        , password = "456", enabled = True, suspended = False
        )
    Auth.Group ("FFM")
    Auth.Account_in_Group ("tanzer@swing.co.at", "FFM")
    FFM = scope.FFM
    FFM.Net_Device_Type \
        (name = "Generic", desc = "for unknown or planned devices", raw = True)
    s11a = FFM.Wireless_Standard \
        (name = "802.11a", bandwidth = "20 MHz", raw = True)
    s11b = FFM.Wireless_Standard \
        (name = "802.11b", bandwidth = "20 MHz", raw = True)
    s11g = FFM.Wireless_Standard \
        (name = "802.11g", bandwidth = "20 MHz", raw = True)
    s11n = FFM.Wireless_Standard \
        (name = "802.11n", bandwidth = "40 MHz", raw = True)
    for std in s11b, s11g :
        FFM.Wireless_Channel \
            (left = std, number =  "1", frequency = "2412 MHz", raw = True)
        FFM.Wireless_Channel \
            (left = std, number =  "2", frequency = "2417 MHz", raw = True)
        FFM.Wireless_Channel \
            (left = std, number =  "3", frequency = "2422 MHz", raw = True)
        FFM.Wireless_Channel \
            (left = std, number =  "4", frequency = "2427 MHz", raw = True)
        FFM.Wireless_Channel \
            (left = std, number =  "5", frequency = "2432 MHz", raw = True)
        FFM.Wireless_Channel \
            (left = std, number =  "6", frequency = "2437 MHz", raw = True)
        FFM.Wireless_Channel \
            (left = std, number =  "7", frequency = "2442 MHz", raw = True)
        FFM.Wireless_Channel \
            (left = std, number =  "8", frequency = "2447 MHz", raw = True)
        FFM.Wireless_Channel \
            (left = std, number =  "9", frequency = "2452 MHz", raw = True)
        FFM.Wireless_Channel \
            (left = std, number = "10", frequency = "2457 MHz", raw = True)
        FFM.Wireless_Channel \
            (left = std, number = "11", frequency = "2462 MHz", raw = True)
        FFM.Wireless_Channel \
            (left = std, number = "12", frequency = "2467 MHz", raw = True)
        FFM.Wireless_Channel \
            (left = std, number = "13", frequency = "2472 MHz", raw = True)
        FFM.Wireless_Channel \
            (left = std, number = "14", frequency = "2484 MHz", raw = True)
    # 802.11a
    FFM.Wireless_Channel \
        (left = s11a, number = "36",  frequency = "5180 MHz", raw = True)
    FFM.Wireless_Channel \
        (left = s11a, number = "40",  frequency = "5200 MHz", raw = True)
    FFM.Wireless_Channel \
        (left = s11a, number = "44",  frequency = "5220 MHz", raw = True)
    FFM.Wireless_Channel \
        (left = s11a, number = "48",  frequency = "5240 MHz", raw = True)
    FFM.Wireless_Channel \
        (left = s11a, number = "52",  frequency = "5260 MHz", raw = True)
    FFM.Wireless_Channel \
        (left = s11a, number = "56",  frequency = "5280 MHz", raw = True)
    FFM.Wireless_Channel \
        (left = s11a, number = "60",  frequency = "5300 MHz", raw = True)
    FFM.Wireless_Channel \
        (left = s11a, number = "64",  frequency = "5320 MHz", raw = True)
    FFM.Wireless_Channel \
        (left = s11a, number = "100", frequency = "5500 MHz", raw = True)
    FFM.Wireless_Channel \
        (left = s11a, number = "104", frequency = "5520 MHz", raw = True)
    FFM.Wireless_Channel \
        (left = s11a, number = "108", frequency = "5540 MHz", raw = True)
    FFM.Wireless_Channel \
        (left = s11a, number = "112", frequency = "5560 MHz", raw = True)
    FFM.Wireless_Channel \
        (left = s11a, number = "116", frequency = "5580 MHz", raw = True)
    FFM.Wireless_Channel \
        (left = s11a, number = "120", frequency = "5600 MHz", raw = True)
    FFM.Wireless_Channel \
        (left = s11a, number = "124", frequency = "5620 MHz", raw = True)
    FFM.Wireless_Channel \
        (left = s11a, number = "128", frequency = "5640 MHz", raw = True)
    FFM.Wireless_Channel \
        (left = s11a, number = "132", frequency = "5660 MHz", raw = True)
    FFM.Wireless_Channel \
        (left = s11a, number = "136", frequency = "5680 MHz", raw = True)
    FFM.Wireless_Channel \
        (left = s11a, number = "140", frequency = "5700 MHz", raw = True)
    FFM.Wireless_Channel \
        (left = s11a, number = "149", frequency = "5745 MHz", raw = True)
    FFM.Wireless_Channel \
        (left = s11a, number = "153", frequency = "5765 MHz", raw = True)
    FFM.Wireless_Channel \
        (left = s11a, number = "157", frequency = "5785 MHz", raw = True)
    FFM.Wireless_Channel \
        (left = s11a, number = "161", frequency = "5805 MHz", raw = True)
    FFM.Wireless_Channel \
        (left = s11a, number = "165", frequency = "5825 MHz", raw = True)
    FFM.Wireless_Channel \
        (left = s11a, number = "172", frequency = "5860 MHz", raw = True)
    FFM.Wireless_Channel \
        (left = s11a, number = "173", frequency = "5865 MHz", raw = True)
    FFM.Wireless_Channel \
        (left = s11a, number = "174", frequency = "5870 MHz", raw = True)
    FFM.Wireless_Channel \
        (left = s11a, number = "175", frequency = "5875 MHz", raw = True)
    FFM.Wireless_Channel \
        (left = s11a, number = "176", frequency = "5880 MHz", raw = True)
    FFM.Wireless_Channel \
        (left = s11a, number = "177", frequency = "5885 MHz", raw = True)
    FFM.Wireless_Channel \
        (left = s11a, number = "178", frequency = "5890 MHz", raw = True)
    FFM.Wireless_Channel \
        (left = s11a, number = "179", frequency = "5895 MHz", raw = True)
    FFM.Wireless_Channel \
        (left = s11a, number = "180", frequency = "5900 MHz", raw = True)
    FFM.Wireless_Channel \
        (left = s11a, number = "181", frequency = "5905 MHz", raw = True)
    FFM.Wireless_Channel \
        (left = s11a, number = "182", frequency = "5910 MHz", raw = True)
    FFM.Wireless_Channel \
        (left = s11a, number = "183", frequency = "5915 MHz", raw = True)

    # channels not listed on
    # http://linuxwireless.org/en/developers/Documentation/ChannelList
    #FFM.Wireless_Channel \
    #    (left = s11a, number = "147", frequency = "5735 MHz", raw = True)
    #FFM.Wireless_Channel \
    #    (left = s11a, number = "151", frequency = "5755 MHz", raw = True)
    #FFM.Wireless_Channel \
    #    (left = s11a, number = "155", frequency = "5775 MHz", raw = True)
    #FFM.Wireless_Channel \
    #    (left = s11a, number = "167", frequency = "5835 MHz", raw = True)

    # 802.11n
    FFM.Wireless_Channel \
        (left = s11n, number = "36",  frequency = "5180 MHz", raw = True)
    FFM.Wireless_Channel \
        (left = s11n, number = "40",  frequency = "5200 MHz", raw = True)
    FFM.Wireless_Channel \
        (left = s11n, number = "44",  frequency = "5220 MHz", raw = True)
    FFM.Wireless_Channel \
        (left = s11n, number = "48",  frequency = "5240 MHz", raw = True)
    FFM.Wireless_Channel \
        (left = s11n, number = "52",  frequency = "5260 MHz", raw = True)
    FFM.Wireless_Channel \
        (left = s11n, number = "56",  frequency = "5280 MHz", raw = True)
    FFM.Wireless_Channel \
        (left = s11n, number = "60",  frequency = "5300 MHz", raw = True)
    FFM.Wireless_Channel \
        (left = s11n, number = "64",  frequency = "5320 MHz", raw = True)
    FFM.Wireless_Channel \
        (left = s11n, number = "100", frequency = "5500 MHz", raw = True)
    FFM.Wireless_Channel \
        (left = s11n, number = "104", frequency = "5520 MHz", raw = True)
    FFM.Wireless_Channel \
        (left = s11n, number = "108", frequency = "5540 MHz", raw = True)
    FFM.Wireless_Channel \
        (left = s11n, number = "112", frequency = "5560 MHz", raw = True)
    FFM.Wireless_Channel \
        (left = s11n, number = "116", frequency = "5580 MHz", raw = True)
    FFM.Wireless_Channel \
        (left = s11n, number = "120", frequency = "5600 MHz", raw = True)
    FFM.Wireless_Channel \
        (left = s11n, number = "124", frequency = "5620 MHz", raw = True)
    FFM.Wireless_Channel \
        (left = s11n, number = "128", frequency = "5640 MHz", raw = True)
    FFM.Wireless_Channel \
        (left = s11n, number = "132", frequency = "5660 MHz", raw = True)
    FFM.Wireless_Channel \
        (left = s11n, number = "136", frequency = "5680 MHz", raw = True)
    FFM.Wireless_Channel \
        (left = s11n, number = "149", frequency = "5745 MHz", raw = True)
    FFM.Wireless_Channel \
        (left = s11n, number = "153", frequency = "5765 MHz", raw = True)
    FFM.Wireless_Channel \
        (left = s11n, number = "157", frequency = "5785 MHz", raw = True)
    FFM.Wireless_Channel \
        (left = s11n, number = "161", frequency = "5805 MHz", raw = True)

    # See
    # http://git.kernel.org/?p=linux/kernel/git/linville/wireless-regdb.git
    # FIXME: Use parser dbparse.py from above
    #        and import db.txt     from above
    dom = FFM.Regulatory_Domain (countrycode = "AT", raw = True)
#    FFM.Regulatory_Permission \
#        ( left      = dom
#        , band      = "2402 MHz - 2482 MHz"
#        , bandwidth = "40 MHz"
#        , eirp      = "20 dBm"
#        , raw       = True
#        )
#    FFM.Regulatory_Permission \
#        ( left      = dom
#        , band      = "5170 MHz - 5250 MHz"
#        , bandwidth = "40 MHz"
#        , eirp      = "20 dBm"
#        , raw       = True
#        )
#    FFM.Regulatory_Permission \
#        ( left      = dom
#        , band      = "5250 MHz - 5330 MHz"
#        , bandwidth = "40 MHz"
#        , eirp      = "20 dBm"
#        , need_DFS  = "yes"
#        , raw       = True
#        )
#    FFM.Regulatory_Permission \
#        ( left      = dom
#        , band      = "5490 MHz - 5710 MHz"
#        , bandwidth = "40 MHz"
#        , eirp      = "27 dBm"
#        , need_DFS  = "yes"
#        , raw       = True
#        )
    scope.commit ()
# end def create

if __name__ == "__main__" :
    from model import *
    db_url  = sos.environ.get ("DB_url",  "hps://")
    db_name = sos.environ.get ("DB_name", None)
    scope   = command.scope   (db_url, db_name, False)
    TFL.Environment.py_shell  ()
### __END__ fixtures
