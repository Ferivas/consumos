#consumos.py
# Programa para leer ultimo valor de los medidores de los DAA de Manta
# el resultado se va guardando en un archivo de texto

import tslib as ts
import datetime


namefile='Consumos_Manta.csv'
archivo=open(namefile,"a")

keys=['41583','41584','41585','41586','41587','41588','41589','38467']
cadena=''
formato1="%Y-%m-%dT%H:%M:%S"
tbl_campo=['1','1','1','1','1','1','1','8']
ptr=0
for canal in keys:
    campo=tbl_campo[ptr]
    ptr=ptr+1
    consumo=ts.getlastfield(canal,campo)
#    print(consumo)
    if consumo[1]!='':
        cadena=cadena+consumo[1]+','
    else:
        cadena=cadena+','+','
x=datetime.datetime.now()
fechastr=datetime.datetime.strftime(x,formato1)
cadena=fechastr+','+cadena+'\n'
print(cadena)
archivo.write(cadena)    
archivo.close()    