#!/usr/bin/python3
#-----------------------------------------------------------
# Librerias para Thingpeak
#
# tslib.py
#
# Funciones utilizadas para la Api de Thingspeak
#
# 
#-----------------------------------------------------------

#import datetime
import requests

# Proporciona los campos de la ultima entrada de un canal
# El canal se ingresa como numero entero
# Los datos del canal se presentan como una lista ordenanda de la sig. manera
# [fecha, field1, field2,....,field8,num_entrada]
def getlastcts(canal):
    url='https://api.thingspeak.com/channels/'+str(canal)+'/feeds/last.json'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            results = response.json()
            try:
               fecha=results.get('created_at')
               entrada=results.get('entry_id')
               f1=results.get('field1')
               f2=results.get('field2')
               f3=results.get('field3')
               f4=results.get('field4')
               f5=results.get('field5')
               f6=results.get('field6')
               f7=results.get('field7')
               f8=results.get('field8')
               data=[fecha,f1,f2,f3,f4,f5,f6,f7,f8,entrada]
               return data
            except:
               print('Canal privado')
               data=[-1,0,0,0,0,0,0,0,0,0]
               return data
        else:
            print("Error code %s" % response.status_code)
            data=[-1,0,0,0,0,0,0,0,0,0]
            return data
    except:
        data=[-2,0,0,0,0,0,0,0,0,0]
        return data
        

# https://api.thingspeak.com/channels/<channel_id>/fields/<field_id>/last.json
def getlastfield(canal,campo):
    url='https://api.thingspeak.com/channels/'+canal+'/fields/'+str(campo)+'/last.json'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            results = response.json()
            print(results)
            try:
                fecha=results.get('created_at')
                campoid='field'+str(campo)
                f1=results.get(campoid)
                entrada=results.get('entry_id')
                data=[fecha,f1,entrada]
                return data
            except:
                print('Canal privado o sin datos')
                data=['','','','']
                return data
        else:
            data=['','','','']
            return data
    except:
        print('Error en TS')
        data=['','','','']
        return data
   
def exetb(apitb,idtb):
    url='https://api.thingspeak.com/talkbacks/'+str(idtb)+'/commands/execute.json'
    payload = {'key' : apitb}
    try:
        r = requests.post(url,data=payload,timeout=5)
        if r.status_code==200:
            print("Consulta TB a TS OK")
            results = r.json()
            try:
                comando=results.get('command_string')
            except:
                comando=''
            return comando
        else:
          print("Error ejecutando Talkback (status code:"+str(r.status_code)+")")
          comando=''
          return comando
    except:
        print("Error consulta Talkback")        
        comando=''
        return comando
    
def sendThingspeak(url,key,field1,field2,temp1,temp2):
  if url=='' or key=='':
    return
  # Send event to internet site
  payload = {'key' : key,'field1' : temp1,'field2' : temp2}
  try:
    r = requests.post(url,data=payload,timeout=5)
    if r.status_code==200:
      print("Sent data to Thingspeak")
    else:
      print("Error sending data to Thingspeak (status code:"+str(r.status_code)+")")
  except:
    print("Error sending data to Thingspeak")
    
## Enviando datos a TS via GET
## apikey es tipo string
## valfeed es una lista con valores, no acepta strings  
def sndts(apikey,valfeed):
    url='https://api.thingspeak.com/update?api_key='+apikey
    cntr=0
    while cntr<8:
        if valfeed[cntr]!='':
            tmpstr=str(cntr+1)
            #url=url+'&field'+tmpstr+"="+str(valfeed[cntr])
            url=url+'&field'+tmpstr+"="+valfeed[cntr]
        cntr+=1
    try:
        response = requests.get(url)
        print(response)
        if response.status_code == 200:
            print('TX TS OK')
            enviado=1
            return enviado
        else:
            print("Error code %s" % response.status_code)
            enviado=0
            return enviado
    except:
            print('ERROR TS')
            enviado=0
            return enviado