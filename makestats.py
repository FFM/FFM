#!/usr/bin/env python

import pickle
import sys
import os

x = pickle.load(open(sys.argv[1]))
print x

# 193.238.158.181
# [['eth1', True, 'v13.freiesnetz.www.funkfeuer.at', 'Ad Hoc', '13', '26:A7:D4:E4:4F:4D']]
# ip
# [ interface name, isWirelessInterface, Essid, Wi-Fi mode, channel, BSSID], .... (fuer jedes interface)

for k,v in x.iteritems():
	print k
	print v
	print 
