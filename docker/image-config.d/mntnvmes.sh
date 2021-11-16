#! /bin/bash

nvmes=($(nvme list | awk '{print $1}'))
for i in ${!nvmes[@]}; do
    if [ "$i" -gt "2" ]; then
        mount -t xfs ${nvmes[$i]} /nvme${i}
    fi
done
chown xrootd:xrootd /nvme*
