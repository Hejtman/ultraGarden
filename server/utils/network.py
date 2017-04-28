import subprocess


def ping(address, count=3):
    return subprocess.call(['ping', '-c', str(count), address])


def restart(network):
    cmd = "sudo ifdown {0} && sleep(1) && sudo ifup {0}".format(network)
    return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)


def check_and_fix(address, network):
    if ping(address) != 0:
        restart(network)
