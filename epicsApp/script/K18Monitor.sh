#!/bin/sh

ioc_dir=$(dirname $(readlink -f $0))/../iocBoot/iocK18Monitor
ioc_cmd=$1

if [ -z $ioc_cmd ]; then
    echo "Usage: $(basename $0) [ioc_cmd]"
    exit
fi

echo "debug ioc_dir $ioc_dir"

if [ ! -d $ioc_dir ]; then
    echo "Not found such dir: $ioc_dir"
    exit
fi
cd $ioc_dir

while true
do
    ../../bin/linux-`uname -m`/K18Monitor $ioc_cmd
    # ../bin/linux-`uname -m`/K18Monitor $ioc_cmd
    sleep 1
done
