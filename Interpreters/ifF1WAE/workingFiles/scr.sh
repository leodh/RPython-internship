#!/bin/sh

export i=0
export name=""

until [ "$i" -eq 32 ];
do
    name="JITRPinterpretImperative$i.py"
    cp ./JITRPinterpretImperative.py $name
    i=`expr $i + 1`
    echo $i
done
