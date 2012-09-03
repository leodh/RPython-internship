#!/bin/sh

# To be run in /RPython-internship/Interpreters/ifF1WAE/benchmarks/FirstRound

rm test* result* out*

# Useful variables

export i=1
export max_tests=20

export nodes=10
export runs=10
export max_nodes=1000
export max_runs=100000

export fileToWrite=''

export security=0

# Creation of tests files


until [ "$nodes" -gt $max_nodes ];
do
    until [ "$runs" -gt $max_runs ];
    do
	pypy ./writeProg.py $nodes $runs
	runs=`expr $runs \\* 10`
    done
    nodes=`expr $nodes \\* 10`
    runs=10
done

# Tests

# Tests of translated versions

for fileToRun in `ls *-c | sort`
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

# Tests of interpreted versions, with pypy and python

for fileToRun in `ls RP*.py | sort`
do
    fileToWrite="result-$fileToRun-interpreted-pypy"
    echo "Test of $fileToRun interpreted with pypy\n">>$fileToWrite
    for fileToTest in `ls test* | sort`
    do
	echo "Testing $fileToTest\n" >>$fileToWrite
	until [ "$i" -gt $max_tests ];
	do
	    echo "run $i" >> $fileToWrite
	    /usr/bin/time pypy $fileToRun $fileToTest 2>> $fileToWrite
	    security=`echo $?`
	    echo "" >> $fileToWrite
	    if [ "$security" -ne 0 ]; 
	    then
		echo "Abort tests of $fileToTest">>$fileToWrite
		i=`expr $max_tests + 1`
	    else
		echo "ninja"
		i=`expr $i + 1`
	    fi
	done
	i=1
    done

    fileToWrite="result-$fileToRun-interpreted-python"
    echo "Test of $fileToRun interpreted with python\n">>$fileToWrite
    for fileToTest in `ls test* | sort`
    do
    	echo "Testing $fileToTest\n" >>$fileToWrite
    	until [ "$i" -gt $max_tests ];
    	do
    	    echo "run $i" >> $fileToWrite
    	    /usr/bin/time python $fileToRun $fileToTest 2>> $fileToWrite
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


# Create a repertory for results and tests

mkdir generatedTests
mkdir obtainedResults

mv test* generatedTests/
mv result* obtainedResults/


