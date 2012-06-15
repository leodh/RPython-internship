#!/bin/sh

export i=10
export name=""

until [ $i -gt 100000 ];
do
    name="exampleFunc$i"
    pypy writeProgFunc.py -i $name $i
    i=`expr $i \\* 10`
done
