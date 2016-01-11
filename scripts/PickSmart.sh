#!/bin/bash

for F1 in ??????-??????.???.jpg;
do
    F2=`basename $F1 .jpg`0.jpg
    [[ -e $F2 ]] && \
	{
	S1=`md5sum $F1 | awk '{print $1}'`
	S2=`md5sum $F2 | awk '{print $1}'`
	[[ "$S1" == "$S2" ]] && rm -vf $F2
    }
done

for F1 in ??????-??????.???.jpg;
do
    F2=`basename $F1 .jpg`0.jpg
    [[ -e $F2 ]] && \
	{
	S1=`jhead $F1 2> /dev/null | grep AppleMark | wc -l`
	S2=`jhead $F2 2> /dev/null | grep AppleMark | wc -l`
	(( S1 )) && mv -v $F1 /tmp || \
	    {
	    (( S2 )) && mv -v $F2 /tmp
	}
    }
done

for F1 in ??????-??????.???.jpg;
do
    F2=`basename $F1 .jpg`0.jpg
    [[ -e $F2 ]] && \
	{
	S1=`ls -l $F1 | awk '{print $5}'`
	S2=`ls -l $F2 | awk '{print $5}'`
	(( S1 > S2 )) && ls -alt $F1 $F2 || echo $S1 $F1 lt $S2 $F2
    }
done
 
