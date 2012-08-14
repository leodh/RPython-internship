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
    done
done

mkdir generatedTraces
mv `ls out*` generatedTraces/