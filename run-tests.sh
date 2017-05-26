#!/bin/sh
for i in tests/*.w
do
    python3 main.py $i
done
