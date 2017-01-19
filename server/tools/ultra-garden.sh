#!/bin/sh -e
### BEGIN INIT INFO
# Provides:          garden
# Required-Start:    mountkernfs $local_fs
# Required-Stop:     
# Default-Start:     S
# Default-Stop:      0 6
# Short-Description: Raise garden.
# Description:       Raise balcony garden.
### END INIT INFO

case "$1" in
start)
   python3 /home/pi/ultraGarden/server/utils/ultraGarden.py &
   ;;  

stop)
   killall python3
   ;;  

*)
   echo "Usage: /etc/init.d/ultra-garden {start|stop}"
   exit 1
   ;;  
esac

exit 0

