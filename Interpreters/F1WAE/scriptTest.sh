#!/bin/sh

cd /Users/leonarddeharo2/RPython-internship/Interpreters/F1WAE

rm resultTests


for name in `ls exampleDepth* | sort`
do
    echo "Processing $name ..."
    echo "Treatment of $name" >> resultTests
    echo '' >> resultTests
    echo '' >> resultTests
    
    rm *.pyc
    echo "With python, without .pyc">> resultTests
    /usr/bin/time -p python interpret.py $name 2>> resultTests
    echo "" >> resultTests
    echo "With python, with *.pyc" >> resultTests
    /usr/bin/time -p python interpret.py $name 2>> resultTests
    echo "" >> resultTests

    echo "" >> resultTests
    
    rm *.pyc
    echo "With pypy, without .pyc">> resultTests
    /usr/bin/time -p pypy interpret.py $name 2>> resultTests
    echo "" >> resultTests
    echo "With pypy, with *.pyc" >> resultTests
    /usr/bin/time -p pypy interpret.py $name 2>> resultTests
    echo "" >> resultTests

    echo "" >> resultTests

    echo "With translated RPinterpret" >> resultTests
    /usr/bin/time -p ./RPinterpret-c $name 2>> resultTests
    echo "" >> resultTests

    echo "" >> resultTests

    echo "With translated and JITing JITRPinterpret" >> resultTests
    /usr/bin/time -p ./JITRPinterpret-c $name 2>> resultTests
    echo "" >> resultTests

done
