import subprocess
import time
import csv

class Atol:
    def __init__(self):
        pass

    def scan_for_aps(self, interface="wlan1", scan_time=5):
        prefix = "dump"
        cmd = ["airodump-ng", "--write", prefix, "--output-format", "csv", interface]
        process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        time.sleep(scan_time)

        process.kill()
        process.wait()


a = Atol()
a.scan_for_aps()