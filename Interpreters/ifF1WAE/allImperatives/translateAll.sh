#!/bin/sh

for i in `ls JIT*.py`
do
    RPtranslateJIT $i
done