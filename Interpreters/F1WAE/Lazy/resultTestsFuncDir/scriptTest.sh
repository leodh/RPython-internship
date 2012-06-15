#!/bin/sh

cd /Users/leonarddeharo2/RPython-internship/Interpreters/F1WAE

rm resultTests



export i=1

for name in `ls exampleFunc* | sort`
do
    
    echo "Processing $name ..."
    echo "Treatment of $name" >> resultTests
    echo '' >> resultTests
    echo '##########################' >> resultTests
    echo '' >>resultTests

    echo "With python, without .pyc">> resultTests
    echo ''
    until [ $i -gt 20 ];
    do	
	echo "run $i"
	echo "run $i" >> resultTests
	rm *.pyc
	/usr/bin/time -p python ../interpret.py $name 2>> resultTests
	echo "" >> resultTests
	i=`expr $i + 1`
    done

    i=1
    echo "" >> resultTests
    echo "###########################" >> resultTests
    echo "With python, with *.pyc" >> resultTests
    echo ''
    until [ $i -gt 20 ];
    do	
	echo "run $i"
	echo "run $i" >> resultTests	
	echo "With python, with *.pyc" >> resultTests
	/usr/bin/time -p python ../interpret.py $name 2>> resultTests
	echo "" >> resultTests
	i=`expr $i + 1`
    done

    i=1
    echo "" >> resultTests
    echo "###########################" >> resultTests
    echo "With pypy, without .pyc">> resultTests
    echo ''
    until [ $i -gt 20 ];
    do	
	echo "run $i"
	echo "run $i" >> resultTests
	rm *.pyc
	/usr/bin/time -p pypy ../interpret.py $name 2>> resultTests
	echo "" >> resultTests
	i=`expr $i + 1`
    done

    i=1
    echo "" >> resultTests
    echo "###########################" >> resultTests
    echo "With pypy, with *.pyc" >> resultTests
    echo ''
    until [ $i -gt 20 ];
    do	
	echo "run $i"
	echo "run $i" >> resultTests
	/usr/bin/time -p pypy ../interpret.py $name 2>> resultTests
	echo "" >> resultTests
	i=`expr $i + 1`
    done

    i=1
    echo "" >> resultTests
    echo "###########################" >> resultTests
    echo "With translated RPinterpret" >> resultTests
    echo ''
    until [ $i -gt 20 ];
    do	
	echo "run $i"
	echo "run $i" >> resultTests
	/usr/bin/time -p .././RPinterpret-c $name 2>> resultTests
	echo "" >> resultTests
	i=`expr $i + 1`
    done
	
    i=1
    echo "" >> resultTests
    echo "###########################" >> resultTests
    echo "With translated and JITing JITRPinterpret" >> resultTests
    echo ''
    until [ $i -gt 20 ];
    do	
	echo "run $i"
	echo "run $i" >> resultTests
	/usr/bin/time -p .././JITRPinterpret-c $name 2>> resultTests
	echo "" >> resultTests
	i=`expr $i + 1`
    done

    export file="./resultTestsDir/resultTests$name"
    mv resultTests $file

done
