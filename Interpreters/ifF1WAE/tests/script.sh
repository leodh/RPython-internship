#!/bin/sh

# To be run in /RPython-internship/Interpreters/ifF1WAE/tests/

# Make the translations, to be sure to use last updated version of interpreters
RPtranslate ../RPinterpreter.py
RPtranslateJIT ../JITRPinterpreter.py

export i=1
export nodes=10
export runs=10
export fileToRun=''
export fileToWrite=''
export fileToTest=''

until [ "$nodes" -gt 10 ];
do
    until [ "$runs" -gt 10 ];
    do
	#
	echo "Creating test-file with $nodes node and $runs runs..."
	fileToTest=`pypy ./writeProg.py $nodes $runs`
	fileToWrite="resultsTest$nodesruns$runs"
	#
	# Begin of tests
	#
	fileToRun="../interpret.py"

	echo "With python, without .pyc\n">> $fileToWrite
	echo "Processing tests with python, without .pyc..."
	until [ "$i" -gt 20 ];
	do	
	    echo "run $i" >> $fileToWrite
	    rm ../*.pyc
	    /usr/bin/time -p python $fileToRun $fileToTest 2>> $fileToWrite
	    echo "" >> $fileToWrite
	    i=`expr $i + 1`
	done
	i=1
        
	echo "With python, with .pyc\n">> $fileToWrite
	echo "Processing tests with python, with .pyc..."
	until [ "$i" -gt 20 ];
	do	
	    echo "run $i" >> $fileToWrite
	    /usr/bin/time -p python $fileToRun $fileToTest 2>> $fileToWrite
	    echo "" >> $fileToWrite
	    i=`expr $i + 1`
	done
	i=1
        #
	echo "With pypy, without .pyc\n">> $fileToWrite
	echo "Processing tests with pypy, without .pyc..."
	until [ "$i" -gt 20 ];
	do	
	    echo "run $i" >> $fileToWrite
	    rm ../*.pyc
	    /usr/bin/time -p python $fileToRun $fileToTest 2>> $fileToWrite
	    echo "" >> $fileToWrite
	    i=`expr $i + 1`
	done
	i=1
        
	echo "With pypy, with .pyc\n">> $fileToWrite
	echo "Processing tests with pypy, with .pyc..."
	until [ "$i" -gt 20 ];
	do	
	    echo "run $i" >> $fileToWrite
	    /usr/bin/time -p python $fileToRun $fileToTest 2>> $fileToWrite
	    echo "" >> $fileToWrite
	    i=`expr $i + 1`
	done
	i=1
        #
	fileToRun="../RPinterpret-c"
        echo "With translated non-JITing version\n">> $fileToWrite
	echo "Processing tests with translated non-JITing version..."
	until [ "$i" -gt 20 ];
	do
	    echo "run $i" >> $fileToWrite
	    /usr/bin/time $fileToRun $fileToTest 2>> $fileToWrite
	    echo "" >> $fileToWrite
	    i=`expr $i + 1`
	done
	i=1
	#
	fileToRun="../JITRPinterpret-c"
        echo "With translated JITing version\n">> $fileToWrite
	echo "Processing tests with translated JITing version..."
	until [ "$i" -gt 20 ];
	do
	    echo "run $i" >> $fileToWrite
	    /usr/bin/time $fileToRun $fileToTest 2>> $fileToWrite
	    echo "" >> $fileToWrite
	    i=`expr $i + 1`
	done
	i=1
        #
	fileToRun="../JITRPinterpretCpsTailRec-c"
        echo "With translated JITing version (cpsed tail recursive)\n">> $fileToWrite
	echo "Processing tests with translated JITing version (cpsed tail recursive)..."
	until [ "$i" -gt 20 ];
	do
	    echo "run $i" >> $fileToWrite
	    /usr/bin/time $fileToRun $fileToTest 2>> $fileToWrite
	    echo "" >> $fileToWrite
	    i=`expr $i + 1`
	done
	i=1
    runs=`expr $runs \\* 10`
    done
nodes=`expr $nodes \\* 10`
done