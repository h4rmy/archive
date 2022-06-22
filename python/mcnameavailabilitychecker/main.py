import requests, json, time
import colorama
from colorama import Fore, init
init(convert=True)
token = input("input bearer token\n")
namelist = open("input.txt").read().splitlines()
for name in namelist:
    if "-" in name:
        continue
    if "'" in name:
        continue
    if "." in name:
        continue
    if len(name) <= 2:
        continue
    if len(name) >= 16:
        continue

    else:
        try:
            r=requests.get(f'https://api.minecraftservices.com/minecraft/profile/name/{name}/available', headers={"Authorization":f'Bearer {token}'}).json()
            #print("[*] RESPONSE: " + str(r))
            status = r["status"]
            print(f'{Fore.GREEN}[+] {Fore.LIGHTWHITE_EX}{name} {status} {Fore.LIGHTBLACK_EX}| Response: {str(r)}')
            if status == "AVAILABLE":
                with open('available.txt', 'a') as f:
                    f.write(str(name + " " + status) + "\n")
            time.sleep(1)
        except KeyError:
            print(f'{Fore.RED}[!] {Fore.LIGHTWHITE_EX}KeyError at {name}')
            with open('ratelimited.txt', 'a') as o:
                o.write(str(name) + "\n")
            time.sleep(600)