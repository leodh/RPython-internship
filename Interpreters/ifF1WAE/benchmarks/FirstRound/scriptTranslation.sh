#!/bin/sh

# To be run in /RPython-internship/Interpreters/ifF1WAE/benchmarks/

# Start by cleaning the repertory

rm *-c test* result* *.pyc

# # Make the translations, to be sure to use last updated version of interpreters

for toTranslate in `ls RP*.py | sort`
do
    RPtranslate $toTranslate
done

for toTranslate in `ls JITRP*.py | sort`
do
    RPtranslateJIT $toTranslate
done
