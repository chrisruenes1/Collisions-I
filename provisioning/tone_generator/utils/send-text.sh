#!/bin/bash
# The line above has to be bash (not sh) because we're using the printf builtin

#before we start, make sure we know whether we're under Linux or OS/X (Darwin)
uname -s | grep -i Linux > /dev/null
ISLINUX=$?

#$ISLINUX will be 0 (true) if we're on linux and 1 (false) if we're on mac

#First, get the name of the most recent Adafruit serial device connected
#Conveniently linux helps us by grouping them by manufacturer id
#Mac doesn't so we just take the most recently added serial device overall

if [ "$ISLINUX" -eq 0 ]; then

    DEVNAME=`ls -1t /dev/serial/by-id/ | grep Adafruit | head -1`

    if [[ -z "$DEVNAME" ]]; then
        echo "No Adafruit Device Found"
        exit
    fi

    FULLDEVPATH=/dev/serial/by-id/$DEVNAME
else
    DEVNAME=`ls -1t /dev/cu.usb* | head -1`
    if [[ -z "$DEVNAME" ]]; then
        echo "No Serial Device Found"
        exit
    fi
    FULLDEVPATH=$DEVNAME
fi

#Comment this to remove debug text
echo "Found recent Adafruit device at $FULLDEVPATH"

text=$@

if [[ -z "$text" ]]; then
    echo "Usage: colorChange.sh <Text To Send>"
    exit
fi

#Comment this to remove debug text
echo "Sending text '$text' to serial device"

printf "%b\r" $text > $FULLDEVPATH
#for some reason input() needs to have the serial port READ to return on linux
if [ "$ISLINUX" -eq 0 ]; then
	head -1 $FULLDEVPATH > /dev/null
fi