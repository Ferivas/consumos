# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 10:13:07 2020
Busca canales de tanqueros que no generaron datos consecutivos de 0,val,0 en el field1
y por tanto no escribieron el saldo pendiente
@author: Fernando
"""

import requests
#import os
#import time
import datetime
#import json
import codecs
formato1="%Y-%m-%dT%H:%M:%SZ"

# Leer los ultimos R resultados de un canal
def getriot(canal,R)        :
    url='https://api.thingspeak.com/channels/'+canal+'/feeds.json?results='+str(R)
#    print('Feeds de ',url)
    response = requests.get(url)
    if response.status_code == 200:
        results = response.json()
        #return results
        try:
           feeds=results.get('feeds')
           return feeds
        except:
           print('Sin datos')
           feeds=[]
           return feeds
           #data=[-1,0,0,0,0,0,0,0,0,0]
    else:
        print("Error code %s" % response.status_code) 


def getlastfield(canal,campo):
    #print(type(canal),type(campo))
    url='https://api.thingspeak.com/channels/'+canal+'/fields/'+str(campo)+'/last.json'
    #print(url)
    response = requests.get(url)
    if response.status_code == 200:
        results = response.json()
        #print(results)
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
print("BUSCA ERRORES SALDO")
with codecs.open("TManta2018.csv", "r",encoding='utf-8', errors='ignore') as listaib:
    #listaib=open("LISTA_DITEC.csv","r")
    listado=listaib.readlines()
    print('LISTADO leido')
    x=datetime.datetime.now()    
    namefile="ERRSALDO"+"_"+str(x.year)+"_"+str(x.month)+"_"+str(x.day)+"_"+str(x.hour)+str(x.minute)+str(x.second)+".csv"        
    numr=30
    archivo=open(namefile,"a")
    cntr=0
    indice=-2
    
    for linea in listado:
        param=linea.split(',')
        nombre=param[1]
        llave=param[2]
        indice=indice+1
        print(indice,llave)
        canal=param[4]
        feeds=getriot(canal,numr)   # feeds es una lista con cada elemento como una entrada         
        
        data=getlastfield(canal,1)
        #print(data)
        if data[0]!="":
            #print(data[0])
            fechad=datetime.datetime.strptime(data[0],formato1)
            dif=x-fechad
            adif=abs(dif.days)
            if adif<2:
                try:
                    lfeeds=len(feeds)
                except:
                    lfeeds=0
                if lfeeds>0:
                    cadena=""
                    for entrada in feeds:
                #                    print(entrada)
                        if entrada['field1']!=None:
                            fecha=entrada['created_at']
                            f1=entrada['field1']
                            if f1!="0":
                                f1="C"
                            cadena=cadena+f1
                        else:
                            f1="N"
                            #print(fecha,f1)
                    #print(cadena)
                    errsaldo=cadena.count("000")
                    if errsaldo>0:
                        cntr=cntr+1
                        #print(errsaldo)
                        msg=str(cntr)+","+llave+","+nombre+","+canal+","+str(errsaldo)+","+fecha+'\r'
                        print(msg)
                        archivo.write(msg)
                
            else:
                print("NO tx antiguo, ",fechad)
            
        else:
            print("Err ultima fecha")


            
    archivo.close()