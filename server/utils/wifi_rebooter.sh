#!/bin/bash
# /etc/crontab: */5 *   * * *   root    /home/pi/ultraGarden/server/utils/wifi_rebooter.sh


SERVER=192.168.10.1

ping -c2 ${SERVER} > /dev/null
if [ $? -ne 0 ]
then
    ifdown --force wlan0
    ifup wlan0
fi
