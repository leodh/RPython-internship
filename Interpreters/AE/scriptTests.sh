#!/bin/sh

#To compare performances of AE-interpreter
export i=5
export name=""
export begin=0
export end=0
exporte time=0
until [ "$i" -gt 50 ];
do
    echo "Generating an example of depth $i"
    name="exampleDepth$i"
    python writeExpr.py -i $name $i
    echo  "Interpreting with python and interpreter.py"
#    begin=`date+%s`
    time python interpreter.py $name
 #   end=`date+%s`
  #  time=`expr $end - $begin`
#    echo "It took $time"
    rm *.pyc
    echo "interpreting with pypy and interpreter.py"
    time  pypy interpreter.py $name
    rm *.pyc
    echo "using translated version of RPinterpreter.py"
    time ./RPinterpreter-c $name
    i=`expr $i + 5`
done
