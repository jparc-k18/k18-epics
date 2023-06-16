#!../../bin/linux-x86_64/K18Monitor

## You may have to change K18Monitor to something else
## everywhere it appears in this file

< envPaths

cd ${TOP}

## Register all support components
dbLoadDatabase "dbd/K18Monitor.dbd"
K18Monitor_registerRecordDeviceDriver pdbbase

## Load record instances

dbLoadTemplate("db/CAENHV3-2.substitutions")
dbLoadTemplate("db/CAENHV3-6.substitutions")
dbLoadTemplate("db/CAENHV3-9.substitutions")
dbLoadTemplate("db/CAENHV3-13.substitutions")

cd ${TOP}/iocBoot/${IOC}
iocInit

## Start any sequence programs
#seq sncxxx,"user=sksHost"
