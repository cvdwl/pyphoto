#!/bin/bash

for i in ~/Desktop/Scotland/DCIM/*/*.jpg;
do
    #echo -ne '\n' `basename $i` ' '
    jhead $i | sed 's.Date/Time    : .XXR .;s/GPS.*: /XXX /' | grep XX  \
	| tr 'NWdmsX:\n' ' ' | sed 's/R/\n/g'
done | while read line
do
    (( `echo $line | wc -w` == 13 )) && {
#	echo $line
	echo $line | awk '{print $1,$2,$3,$4,$5,$6,-($10+$11/60),$7+$8/60}'
    }
done
