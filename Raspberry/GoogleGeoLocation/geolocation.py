import requests
import json
import subprocess
import os
#import simlocator

privateKey = "AIzaSyD5UM68eHOiAlj02tVqsQmF-wu52VRucWA"
url = "https://www.googleapis.com/geolocation/v1/geolocate?key=" + privateKey


def getLocationWifi(accessPointMacAdress, dbm, channel):
    payload = {'considerIp': 'true', 'wifiAccessPoints': [
        {"macAddress": accessPointMacAdress, "signalStrength": dBm, "channel": channel}]}
    jsonPayload = json.dumps(payload)
    r = requests.post(url, data=jsonPayload)
    response = json.loads(r.text)
    # return (response['location']['lat'],response['location']['lng'],response['accuracy'])
    return response


def getAccessPointMacAddress(accessPointName):
    operatingSystems = {'nt': 'Windows', 'posix': 'Linux'}

    if operatingSystems[os.name] is not 'Windows':
        print('Error: OS is not Windows')
        return (0, 0, 0)

    r = subprocess.check_output(
        ["netsh", "wlan", "show", "network", "mode=bssid"])

    out = []
    buffer = ""
    found = False
    for char in str(r):
        if char is '\\':
            found = True
            continue
        if char is 'n' and found:
            found = False
            out.append(buffer)
            buffer = ""
        elif char is 'r' and found:
            found = False
            continue
        buffer += char

    APFound = False
    mac = signal = channel = ""

    for line in out:
        if accessPointName in line:
            APFound = True
            continue
        if APFound and "BSSID" in line:
            mac = line
            continue
        if APFound and "Signal" in line:
            signal = line
            continue
        if APFound and "Channel" in line:
            channel = line
            break

    try:
        mac = mac.split(": ", 1)[1]
        signal = signal.split(": ", 1)[1].split("%", 1)[0]
        channel = channel.split(": ", 1)[1]
        dBm = (int(signal) / 2) - 100
        print(mac, signal, channel, dBm)
    except:
        print('Accesspoint not found')
        return (0, 0, 0)
    return (mac, dBm, channel)


'''
def getLocation3G():
    (lac, cellTower,operator) = simlocator.getCellTowerInfo()
    #print lac, cellTower, operator
    codesDict =  {'Airtel':[404,93],'Idea':[404,78]} # replace this with codes in your location. Refer https://en.wikipedia.org/wiki/Mobile_country_code
    mcc = codesDict[operator][0]
    mnc = codesDict[operator][1]

    payload = {'considerIp':'false','cellTowers':[{'cellId':cellTower,'locationAreaCode':lac,'mobileCountryCode':mcc,'mobileNetworkCode':mnc}]}
    jsonPayload = json.dumps(payload)
    r = requests.post(url,data = jsonPayload)
    response = json.loads(r.text)
'''

mac, dBm, channel = getAccessPointMacAddress("Ziggo8CEDE8F")
print(getLocationWifi(mac, dBm, channel))
