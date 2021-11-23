#!/bin/bash

head -c 1073741824 </dev/zero > $3/mainFile
for i in $(seq $1 $[$1+$2-1])
do
    ln $3/mainFile /mnt/testSourceFile$i
done;
