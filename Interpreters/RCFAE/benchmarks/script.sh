#!/bin/sh

# To be run in RCFAE/benchmarks/

# Start by cleaning out the repertory
rm out* test* RP*

# Create file tests

export nodes=10
export runs=1000

export max_nodes=10000
export max_runs=1000000

until [ "$nodes" -gt "$max_nodes" ];
do
    if [ `expr $nodes - $max_nodes` -eq 0 ];
    then 
	max_runs=100000
    fi;
    until [ "$runs" -gt "$max_runs" ];
    do
    	pypy ../tests/writeProg.py $nodes $runs
    	runs=`expr $runs \\* 10`
    done
    echo "lapin $nodes"
    echo "ninja $max_runs"
    nodes=`expr $nodes \\* 10`
    runs=1000
done

# Create translated, non JITing version of the two interpreters

cd ..

RPtranslate interpretTramp.py
mv interpretTramp-c benchmarks/RPinterpretTramp
RPtranslate interpretIter.py
mv interpretIter-c benchmarks/RPinterpretIter

# Create translated, JITing version of the two interpreters

RPtranslate ./interpretTramp.py
mv interpretTramp-c benchmarks/RPJITinterpretTramp
RPtranslate ./interpretIter.py
mv interpretIter-c benchmarks/RPJITinterpretIter

cd benchmarks/

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