#!/bin/bash

if [ -f "/var/run/pigpio.pid" ]; then
   echo "Killing all pigpio process"
   PID=$(</var/run/pigpio.pid)
   echo "PID $PID"
   kill -9 $PID
fi

echo "Starting daemon pigpiod ..."
# for pigpiod options see http://abyz.me.uk/rpi/pigpio/pigpiod.html
#    option -g will run the deamon in the foreground.
#    option -a 1 should assure that we are not using GPU memory.
/usr/bin/pigpiod -g -a 1
echo "... daemon stopped unexpectedly."