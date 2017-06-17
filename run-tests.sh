#!/bin/sh
for i in tests/*.w
do
    echo "TESTING" "$i"
    python3 main.py $i
    echo 
done
