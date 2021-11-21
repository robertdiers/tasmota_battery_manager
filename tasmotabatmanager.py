#!/usr/bin/env python

import pymodbus
import configparser
import os
from datetime import datetime
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder
from urllib.request import urlopen

#read config
config = configparser.SafeConfigParser()

#-----------------------------------------
# Routine to read a float    
def ReadFloat(client,myadr_dec,unitid):
    r1=client.read_holding_registers(myadr_dec,2,unit=unitid)
    FloatRegister = BinaryPayloadDecoder.fromRegisters(r1.registers, byteorder=Endian.Big, wordorder=Endian.Little)
    result_FloatRegister =round(FloatRegister.decode_32bit_float(),2)
    return(result_FloatRegister)   
#----------------------------------------- 
# Routine to write float
def WriteFloat(client,myadr_dec,feed_in,unitid):
    builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Little)
    builder.add_32bit_float( feed_in )
    payload = builder.to_registers() 
    client.write_registers(myadr_dec, payload, unit=unitid)

# read status from Tasmota
def StatusTasmota(tasmotaip):
    if not tasmotaip:
        return 'DISABLED'
    try:
        statuslink = urlopen('http://'+tasmotaip+'/?m=1')
        return statuslink.read().decode('utf-8')
    except Exception as e:
        print (e)
        return 'ERROR'

# set status Tasmota
def SwitchTasmota(tasmotaip, status):
    print (tasmotaip+' '+status)
    try:
        if 'ON' in status and 'OFF' in StatusTasmota(tasmotaip):
            switchlink = urlopen('http://'+tasmotaip+'/?m=1&o=1')
            retval = switchlink.read().decode('utf-8')
            print(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ' ' + tasmotaip + ': ' + retval)
        if 'OFF' in status and 'ON' in StatusTasmota(tasmotaip):
            switchlink = urlopen('http://'+tasmotaip+'/?m=1&o=1')
            retval = switchlink.read().decode('utf-8')
            print(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ' ' + tasmotaip + ': ' + retval)
    except Exception as e:
        print (e)

if __name__ == "__main__":  
    print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " START #####")
    try:
        #read config
        config.read('tasmotabatmanagerdefaults.ini')
        config.read('tasmotabatmanager.ini')

        #read config and default values
        inverter_ip = config['KostalSection']['inverter_ip']
        inverter_port = config['KostalSection']['inverter_port']
        tasmota_charge_ip = config['TasmotaSection']['tasmota_charge_ip']
        tasmota_charge_start = config['TasmotaSection']['tasmota_charge_start']  
        tasmota_charge_end = config['TasmotaSection']['tasmota_charge_end']  
        tasmota_stage1_ip = config['TasmotaSection']['tasmota_stage1_ip'] 
        tasmota_stage1_start = config['TasmotaSection']['tasmota_stage1_start'] 
        tasmota_stage1_end = config['TasmotaSection']['tasmota_stage1_end'] 
        tasmota_stage2_ip = config['TasmotaSection']['tasmota_stage2_ip'] 
        tasmota_stage2_start = config['TasmotaSection']['tasmota_stage2_start'] 
        tasmota_stage2_end = config['TasmotaSection']['tasmota_stage2_end'] 

        # override with environment variables
        if os.getenv('INVERTER_IP','None') != 'None':
            inverter_ip = os.getenv('INVERTER_IP')
            print ("using env: INVERTER_IP")
        if os.getenv('INVERTER_PORT','None') != 'None':
            inverter_port = os.getenv('INVERTER_PORT')
            print ("using env: INVERTER_PORT")
        if os.getenv('TASMOTA_CHARGE_IP','None') != 'None':
            tasmota_charge_ip = os.getenv('TASMOTA_CHARGE_IP')
            print ("using env: TASMOTA_CHARGE_IP")
        if os.getenv('TASMOTA_CHARGE_START','None') != 'None':
            tasmota_charge_start = os.getenv('TASMOTA_CHARGE_START')
            print ("using env: TASMOTA_CHARGE_START")
        if os.getenv('TASMOTA_CHARGE_END','None') != 'None':
            tasmota_charge_end = os.getenv('TASMOTA_CHARGE_END')
            print ("using env: TASMOTA_CHARGE_END")
        if os.getenv('TASMOTA_STAGE1_IP','None') != 'None':
            tasmota_stage1_ip = os.getenv('TASMOTA_STAGE1_IP')
            print ("using env: TASMOTA_STAGE1_IP")
        if os.getenv('TASMOTA_STAGE1_START','None') != 'None':
            tasmota_stage1_start = os.getenv('TASMOTA_STAGE1_START')
            print ("using env: TASMOTA_STAGE1_START")
        if os.getenv('TASMOTA_STAGE1_END','None') != 'None':
            tasmota_stage1_end = os.getenv('TASMOTA_STAGE1_END')
            print ("using env: TASMOTA_STAGE1_END")
        if os.getenv('TASMOTA_STAGE2_IP','None') != 'None':
            tasmota_stage2_ip = os.getenv('TASMOTA_STAGE2_IP')
            print ("using env: TASMOTA_STAGE2_IP")
        if os.getenv('TASMOTA_STAGE2_START','None') != 'None':
            tasmota_stage2_start = os.getenv('TASMOTA_STAGE2_START')
            print ("using env: TASMOTA_STAGE2_START")
        if os.getenv('TASMOTA_STAGE2_END','None') != 'None':
            tasmota_stage2_end = os.getenv('TASMOTA_STAGE2_END')
            print ("using env: TASMOTA_STAGE2_END")

        print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " inverter_ip: ", inverter_ip)
        print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " inverter_port: ", inverter_port)
        print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " tasmota_charge_ip: ", tasmota_charge_ip)
        print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " tasmota_charge_start: ", tasmota_charge_start)
        print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " tasmota_charge_end: ", tasmota_charge_end)
        print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " tasmota_stage1_ip: ", tasmota_stage1_ip)
        print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " tasmota_stage1_start: ", tasmota_stage1_start)
        print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " tasmota_stage1_end: ", tasmota_stage1_end)
        print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " tasmota_stage2_ip: ", tasmota_stage2_ip)
        print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " tasmota_stage2_start: ", tasmota_stage2_start)
        print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " tasmota_stage2_end: ", tasmota_stage2_end)
        
        #connection Kostal
        inverterclient = ModbusTcpClient(inverter_ip,port=inverter_port)            
        inverterclient.connect()       
        
        #all additional invertes will decrease my home consumption, so it might be negative - this is fine
        consumptionbat = ReadFloat(inverterclient,106,71)
        #print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " consumption battery: ", consumptionbat)
        consumptiongrid = ReadFloat(inverterclient,108,71)
        #print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " consumption grid: ", consumptiongrid)
        consumptionpv = ReadFloat(inverterclient,116,71)
        #print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " consumption pv: ", consumptionpv)
        consumption_total = consumptionbat + consumptiongrid + consumptionpv
        print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " consumption: ", consumption_total)
        
        inverter = ReadFloat(inverterclient,172,71)
        print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " inverter: ", inverter)         
        
        #this is not exact, but enough for us
        surplus = round(inverter - consumption_total,1)
        print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " surplus: ", surplus)
        
        inverterclient.close()
        
        #charging
        chargestatus = StatusTasmota(tasmota_charge_ip)
        if 'ON' in chargestatus:
            print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " chargestatus: ", 'ON')
        if 'OFF' in chargestatus:
            print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " chargestatus: ", 'OFF')

        #we will always charge between 12:00 and 12:05 to ensure a kind of "battery protect"
        now = datetime.now()
        if now.hour == 12 and now.minute < 5:
            if 'OFF' in chargestatus:
                SwitchTasmota(tasmota_charge_ip, 'ON')
                print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " start charging battery protect: ", surplus)
        else:
            if 'OFF' in chargestatus and surplus > int(tasmota_charge_start):
                SwitchTasmota(tasmota_charge_ip, 'ON')
                print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " start charging: ", surplus)
            if 'ON' in chargestatus and surplus < int(tasmota_charge_end):
                SwitchTasmota(tasmota_charge_ip, 'OFF')
                print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " stop charging: ", surplus)

        #feed-in stages
        stage1status = StatusTasmota(tasmota_stage1_ip)
        stage2status = StatusTasmota(tasmota_stage2_ip)
        print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " stage1status: ", stage1status)
        print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " stage2status: ", stage2status)

        if surplus < 0:
            #enable
            if 'OFF' in stage1status and surplus < int(tasmota_stage1_start):
                SwitchTasmota(tasmota_stage1_ip, 'ON')
                print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " start feed-in stage1: ", surplus)
            if 'ON' in stage1status and 'OFF' in stage2status and surplus < int(tasmota_stage2_start):
                SwitchTasmota(tasmota_stage2_ip, 'ON')
                print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " start feed-in stage2: ", surplus)
        else:
            #disable
            if 'ON' in stage2status and surplus > int(tasmota_stage2_end):
                SwitchTasmota(tasmota_stage2_ip, 'OFF')
                print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " end feed-in stage2: ", surplus)
            if ('OFF' in stage2status or 'DISABLED' in stage2status or 'ERROR' in stage2status) and 'ON' in stage1status and surplus > int(tasmota_stage1_end):
                SwitchTasmota(tasmota_stage1_ip, 'OFF')
                print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " end feed-in stage1: ", surplus)
        
        print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " END #####")
        
    except Exception as ex:
        print ("ERROR :", ex)        
