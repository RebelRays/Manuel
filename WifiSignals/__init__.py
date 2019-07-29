import time
import math
import sys
import subprocess
import datetime
import os.path
import csv

interface = "wlan0"

def calculateDistance(signalLevelInDb, freqInMHz):
    exp = (27.55 - (20 * math.log10(freqInMHz)) + math.fabs(signalLevelInDb)) / 20.0
    return math.pow(10,exp)

def getWifiContent():
    try:
        proc = subprocess.Popen(["iwlist", interface, "scan"],stdout=subprocess.PIPE, universal_newlines=True)
        out, err = proc.communicate()
        return out
    except:
        return "err"

class WifiSignals:
    todo=1
    def Record(self):
        wifiContent = getWifiContent()
        Cells = wifiContent.split("Cell")
        Attempts = 6
        while(len(Cells)<3 and Attempts>0):
            Attempts -=1
            time.sleep(10)
            wifiContent = getWifiContent()
            Cells = wifiContent.split("Cell")

        filename = '/DataRecording/Wifi.csv'
        LocationFileExist = os.path.isfile(filename) 
        with open(filename, 'a') as csvfile:
            fieldnames = ['Time', 'ESSID', 'Address', 'Quality', 'SignalLevel', 'FrequencyInMHZ', 'DistanceCalc', 'LastBeacon']
            writer = csv.DictWriter(csvfile, delimiter=";", lineterminator='\n', fieldnames=fieldnames)
            if(not LocationFileExist):
                writer.writeheader()
        
        wifidateTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(filename, 'a') as csvfile:
            for CellContent in wifiContent.split("Cell"):
                #ESSID, Quality, Signal level
                ESSIDSplit = CellContent.split("ESSID:\"")
                if(len(ESSIDSplit) == 1):
                    continue
                ESSID = ESSIDSplit[1].split("\"")[0]
                
                AddressSplit = CellContent.split("Address: ")
                if(len(ESSIDSplit) == 1):
                    continue
                Address = AddressSplit[1].split("\n")[0]
                
                QualitySplit = CellContent.split("Quality=")
                Quality = QualitySplit[1].split("/70")[0]

                SignalLevelSplit = CellContent.split("Signal level=-")
                SignalLevel = SignalLevelSplit[1].split(" dBm")[0]

                FrequencySplit = CellContent.split("Frequency:")
                Frequency = FrequencySplit[1].split(" GHz")[0]
                FrequencyInMHZ = float(Frequency)*1000

                LastBeacon=''
                LastBeaconSplit=CellContent.split("Last beacon: ")
                if(len(ESSIDSplit) > 1):
                    LastBeacon=LastBeaconSplit.split("ms")[0]
                distance=calculateDistance(float(SignalLevel),FrequencyInMHZ)
                writer.writerow({'Time': wifidateTime, 'ESSID': ESSID, 'Address':Address, 'Quality': Quality, 'SignalLevel':SignalLevel, 'FrequencyInMHZ':FrequencyInMHZ, 'DistanceCalc':distance, 'LastBeacon':LastBeacon})