#!/bin/sh

# To be run in RCFAE/benchmarks/

# Start by cleaning out the repertory
rm *

# Create file tests

export nodes=10
export runs=1000

export max_nodes=10000
export max_runs=1000000

until [ "$nodes" -gt $max_nodes ];
do
    until [ "$runs" -gt $max_runs ];
    do
	pypy ../tests/writeProg.py $nodes $runs
	runs=`expr $runs \\* 10`
    done
    nodes=`expr $nodes \\* 10`
    runs=10
done

# Create translated, non JITing version of the two interpreters

RPtranslate ../interpret.py
mv interpret-c RPinterpretTramp
RPtranslate ../interpretIter.py
mv interpretIter-c RPinterpretIter

# Create translated, JITing version of the two interpreters

RPtranslate ../interpret.py
mv interpret-c RPJITinterpretTramp
RPtranslate ../interpretIter.py
mv interpretIter-c RPJITinterpretIter

# Run tests

export i=1
export max_tests=20

export fileToWrite=''

export security=0

for fileToRun in `ls RP* | sort`
do
    fileToWrite="result-$fileToRun-0"
    echo "Tests of $fileToRun\n">>$fileToWrite
    for fileToTest in `ls test* | sort`
    do
	echo "Testing $fileToTest\n" >>$fileToWrite
	until [ "$i" -gt $max_tests ];
	do
	    echo "run $i" >> $fileToWrite
	    /usr/bin/time ./$fileToRun $fileToTest 2>> $fileToWrite
	    security=`echo $?`
	    echo "" >> $fileToWrite
	    if [ "$security" -ne 0 ]; 
	    then
		echo "Abort tests of $fileToTest">>$fileToWrite
		i=`expr $max_tests + 1`
	    else
		i=`expr $i + 1`
	    fi
	done
	i=1
    done
done

# Verify if a trace is produced or not

for fileToRun in `ls RPJIT* | sort `
do
    for fileToTest in `ls test* | sort`
    do
	fileToWrite="out-$fileToRun"
	echo "Trace $fileToTest" >> $fileToWrite
	echo "" >> $fileToWrite
	PYPYLOG=jit-log-opt:out ./$fileToRun $fileToTest
	echo "" >> $fileToWrite
	cat <out >>$fileToWrite
	rm out
    done
done