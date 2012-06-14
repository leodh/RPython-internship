#!/bin/sh

export i=10
echo $i
i=`expr $i \\* 10`
if [ $i -gt 20 ]
then
    echo 0
else
    echo 1
fi
