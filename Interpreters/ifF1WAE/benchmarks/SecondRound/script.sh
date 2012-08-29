#!/bin/sh

# To be run in /RPython-internship/Interpreters/ifF1WAE/benchmarks/SecondRun

# Start by cleaning the repertory

rm *-c test* result* *.pyc

# Make the translations, to be sure to use last updated version of interpreters

for toTranslate in `ls RP*.py | sort`
do
    RPtranslate $toTranslate
done

for toTranslate in `ls JITRP*.py | sort`
do
    RPtranslateJIT $toTranslate
done

# Actual testing 

# Useful variables

export i=1
export max_tests=11

export nodes=6
export runs=1000
export max_nodes=11
export max_runs=100000

export fileToWrite=''

export security=0

# Creation of tests files


until [ "$nodes" -gt $max_nodes ];
do
    until [ "$runs" -gt $max_runs ];
    do
	pypy ./newWriteProg.py $nodes $runs
	runs=`expr $runs \\* 10`
    done
    nodes=`expr $nodes + 1`
    runs=1000
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


# Trace every execution

for fileToRun in `ls JIT*-c | sort `
do
    for fileToTest in `ls generatedTests/test* | sort`
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

# Create a repertory for results and tests

mkdir generatedTests
mkdir obtainedResults
mkdir generatedTraces

mv out* generatedTraces/
mv test* generatedTests/
mv result* obtainedResults/


