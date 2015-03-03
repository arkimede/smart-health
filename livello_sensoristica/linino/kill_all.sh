#!/bin/sh

obd=$(pgrep -f "python2.7 obd.py")
sendmeasures=$(pgrep -f "python2.7 send_measures.py")
echo $sendmeasures
echo $obd
kill -9 $obd $sendmeasures
