#!/bin/sh

for i in `ls RP*.py`
do
    chmod -w $i
    cat <$i > JIT$i
    chmod +w $i
done
