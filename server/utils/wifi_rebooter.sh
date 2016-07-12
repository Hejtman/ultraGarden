#!/bin/bash
# /etc/crontab: */5 *   * * *   root    /usr/pi/bin/ultraGarden/server/utils/wifi_rebooter.sh


SERVER=192.168.10.1

ping -c2 ${SERVER} > /dev/null
if [ $? ]
then
    ifdown --force wlan0
    ifup wlan0
fi
