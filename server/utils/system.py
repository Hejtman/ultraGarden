import os


def reboot():
    os.system('/sbin/shutdown -r now')
