#!/bin/bash

MASK=CVL
DEST="/Storage/Media/Pictures/SORTED"

find . \( -name "*${MASK}*.jpg" -or -name "*${MASK}*.JPG" \) -exec jhead {} \; | \
    grep model | \
    sort | \
    uniq | \
    while read line;
        do 
            CAMERA=`echo $line | sed 's/^.*: //'`;
            echo $CAMERA;
            find . \( -name "*${MASK}*.jpg" -or -name "*${MASK}*.JPG" \) | \
            while read line;
            do  
                jhead -ft -model "$CAMERA" -exonly \
                -nf"${DEST}/$CAMERA/%Y/%m/%y%m%d-%H%M%S_CVL" "$line" 
            done;
        done
