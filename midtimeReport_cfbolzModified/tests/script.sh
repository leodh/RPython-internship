#!/bin/sh

# To be used in RPython-internship/midtimeReport/tests/

# RPtranslate and RPtranslateJIT are symbolic links that I created, you might need to use your own.

# Make the translations, to be sure to use last updated version of interpreters (optional)
# cd ..

# RPtranslate RPinterpreterRec.py
# RPtranslate RPinterpreterIter.py
# RPtranslateJIT JITRPinterpreterRec.py
# RPtranslateJIT JITRPinterpreterIter.py

# cd tests/

cp ../RPinterpretRec-c ../RPinterpretIter-c ../JITRPinterpretRec-c ../JITRPinterpretIter-c ./

export i=1
export nodes=10
export runs=10
export fileToTest=''

until [ "$nodes" -gt 10000 ];
do
    until [ "$runs" -gt 10000 ];
    do
	#
	echo "Creating test-file with $nodes node and $runs runs..."
	fileToTest=`pypy ./writeProg.py $nodes $runs`
	#
	# Begin of tests
	#
	for fileToRun in `ls *-c | sort` 
	# JITs will be run first, but the order will always be the same.
	do
	    echo "Processing tests with $fileToRun"
	    until [ "$i" -gt 10 ];
	    do
		echo "run $i"
		/usr/bin/time $fileToRun $fileToTest
		echo "" 
		i=`expr $i + 1`
	    done
	    i=1
	   echo "\n\n"
	done
	#
    runs=`expr $runs \\* 10`
    done
nodes=`expr $nodes \\* 10`
done