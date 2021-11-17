#!/bin/bash

numTransfers="38"
numBatchess="4"
count="0"

pods=($(kubectl get pods | awk '{print $1}'))
for pod in $pods; do
    if [[ "$pod" == *"src-origin"* ]]; then
        kubectl exec $pod -- bash /home/mkfile.sh $count $numTransfers &
        count=$[$count+$numTransfer]
    fi
done
