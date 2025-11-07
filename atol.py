import subprocess
import time
import csv

class Atol:
    def __init__(self):
        pass

    def enable_monitor_mode(self, interface="wlan1"):
        subprocess.run(["airmon-ng", "start", interface])

    def scan_for_aps(self, interface="wlan1", scan_time=1):
        prefix = "dump"
        cmd = ["airodump-ng", "--write", prefix, "--output-format", "csv", interface]
        process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        time.sleep(scan_time)

        process.kill()
        process.wait()


a = Atol()
a.enable_monitor_mode()
a.scan_for_aps()