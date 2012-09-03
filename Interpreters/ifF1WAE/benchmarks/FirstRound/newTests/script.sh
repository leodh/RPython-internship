#!/bin/sh

# To be run in RCFAE/benchmarks/

# Start by cleaning out the repertory
rm out*

# Create translated, non JITing version of the interpreters

for fileToTranslate in `ls Interpret*.py | sort`
do
    RPtranslate $fileToTranslate
    export toRename="$fileToTranslate-c"
    export newName="RP$toRename"
    mv toRename newName
done

# Create translated, JITing version of the two interpreters

for fileToTranslate in `ls Interpret*.py | sort`
do
    RPtranslateJIT $fileToTranslate
    export toRename="$fileToTranslate-c"
    export newName="RPJIT$toRename"
    mv toRename newName
done

# Run tests

export i=0
export max_tests=10

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
	i=0
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