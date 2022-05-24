import subprocess
import json
from urllib import response
import requests
import json
from datetime import datetime
from ping3 import ping

City = 'Sydney'
recomended_server_url = "https://api.nordvpn.com/v1/servers/recommendations?&filters\[servers_technologies\]\[identifier\]=wireguard_udp&city=" + City
VPN_Interface = "NORD_VPN"
Latency_threshold = 110
Ping_averaging = 5

def lineGet(file_name, string_to_search):
    line_number = 0
    with open(file_name, 'r') as read_obj:
        for line in read_obj:
            line_number += 1
            if string_to_search in line:
                line_number
                break
    return line_number

def replaceLine(file_name, line_num, text):
    lines = open(file_name, 'r').readlines()
    lines[line_num] = text
    out = open(file_name, 'w')
    out.writelines(lines)
    out.close()

def resetNetwork():
    bashCommand = "ifdown " + VPN_Interface
    process = subprocess.Popen(bashCommand.split())       
    bashCommand = "ifup " + VPN_Interface
    process = subprocess.Popen(bashCommand.split()) 

def findFasterVpn():
    rs = json.loads(requests.get(recomended_server_url).content)[0]
    rshostname = rs["hostname"]
    rsip = rs["station"]
    public_key = ""
    city = rs["locations"][0]["country"]["city"]["name"]
    for value in rs["technologies"]:
        if value['name'] == "Wireguard":
            public_key = value['metadata'][0]['value']
    #! The followin is very specific to your device as it modifies your config files.
    CONFIG_LINE = lineGet("/etc/config/network", "wireguard_NORD_VPN")
    replaceLine("/etc/config/network", int(CONFIG_LINE) + 1, "\toption public_key '" + public_key + "'\n")
    replaceLine("/etc/config/network", int(CONFIG_LINE) + 2, "\toption endpoint_host '" + rsip + "'\n")
    print(str(datetime.now()) + " || END POINT > " + city + " || " + rsip + " :: " + public_key)
    resetNetwork();



def main():
    pingRes = 0;
    for i in range(Ping_averaging):
        res = ping('czgzz.space', unit='ms', timeout=2, interface=VPN_Interface)
        if res is not None:
            pingRes += res
        else:
            pingRes += 0    
    avg = pingRes / Ping_averaging
    if avg >= Latency_threshold:
        findFasterVpn()
    exit()


if __name__ == "__main__":
    main()


