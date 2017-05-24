#!/bin/sh
for i in tests/parser/*.w
do
    ./eval.py $i
done
