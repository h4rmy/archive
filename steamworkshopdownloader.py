from time import sleep
from threading import Thread
import requests
import zipfile
import json
import os

url = "https://db.steamworkshopdownloader.io/prod/api/details/file"

def send_request(id):
    try:
        payload = f"[{id}]"
        response = requests.post(url, data=payload)
        the = json.loads(response.text)
        v1 = the[0]

        file_url = v1['file_url']
        file_name = v1['filename']
        mapname = file_name.removeprefix("mymaps/")

        i_am_running_out_of_names = requests.get(f"{file_url}")
        open(f"./compressed/{mapname}", "wb").write(i_am_running_out_of_names.content)
        global zippy
        zippy = os.path.abspath(f"./compressed/{mapname}")
        print(f"+ [{response.status_code}][{mapname}] {file_url}")
        return True

    except requests.RequestException as e:
        print(f"- [{response.status_code}][{mapname}] {file_url}")
        print(e)
        return False

def unzip(path):
    with zipfile.ZipFile(path, "r") as z:
        z.extractall("./content/")

def main():
    file_path = "input.txt"
    if not os.path.exists("compressed"):
        os.makedirs("compressed")
    if not os.path.exists("content"):
        os.makedirs("content")

    with open(file_path, "r") as file:
        for line in file:
            workshopid = line.strip().removeprefix("https://steamcommunity.com/sharedfiles/filedetails/?id=")
            if send_request(workshopid):
                Thread(target=unzip(zippy))

if __name__ == '__main__':
    main()
