#!/bin/bash

head -c 1073741824 </dev/zero > /mnt/ramdisk/mainFile
for i in $(seq $1 $[$1+$2-1])
do
    ln /mnt/ramdisk/mainFile /mnt/ramdisk/testSourceFile$i
done;
