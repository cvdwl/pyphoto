#!/bin/bash

PHOTODIR=~/Pictures
CLEAN=1
CLEANALL=1
MOVE=1
MVCMD="mv"

# Input parser
while [ $# -gt 1 ]
  do
  case "$1" in
      "-d" ) shift;PHOTODIR=$1 ;;
      "-c" ) CLEAN=0 ;;
      "-a" ) CLEANALL=0 ;;
      "-m" ) MOVE=0 ;;
      "-h" ) 
          echo -e "-d PHOTODIR"
          exit;;
  esac
  shift
done

# Make sure we have a target destination
[[ $# -eq 1 ]] && [[ -d "$1" ]] && WORKDIR="$1" || exit

# Check to see if we have a camera model list for cleaning filenames
[[ ! -e ${PHOTODIR}/CameraModels ]] && CLEAN=0

# Cycle through files, renaming according to model list
(( CLEAN )) && find ${WORKDIR} -type f \
    | while read file;
do
    [[ `jhead "${file}" 2> /dev/null | grep model` ]] && \
	[[ `jhead "${file}" 2> /dev/null | \
	grep "Date/Time" | sed 's/^.*: //;s/[:,0, \t]//g'` ]] && \
	{
	cat ${PHOTODIR}/CameraModels | while read model;
	do
	    U=`echo $model | sed 's/;.*$//'`
	    M=`echo $model | sed 's/'$U';//;s/;.*$//;s/^[ \t]*//;s/[ \t]*$//'`
	    [[ -e "${file}" ]] && \
		jhead -exonly -model "${M}" \
		-autorot -nf"%y%m%d-%H%M%S.$U" "${file}" 2> /dev/null
	done
    }
done

# If we're cleaning, rename the unknown, improperly labeled, valid files
(( CLEANALL )) && \
    find ${WORKDIR} -type f ! -name "??????-??????.*.jpg" \
    -exec jhead -autorot -exonly -nf"%y%m%d-%H%M%S.XXX" {} \;

# Sort the properly labeled files
(( MOVE )) && find ${WORKDIR} -name "??????-??????.???.jpg" \
    | while read line;
do
    F=`basename "${line}"`
    P=${F:14:3}
    [[ $P == "CVL" ]] && \
	D=${PHOTODIR}/20${F:0:2}/${F:2:2} || \
	D=${PHOTODIR}/Others/20${F:0:2}/${F:2:2}
    [[ ! -e "$D/$F" ]] && {
	[[ -d $D ]] || mkdir -pv "${D}"
	$MVCMD -iv "${line}" "${D}"
    } || { \
	BUEXT=-1
	while [ -e "$D/$F" ] && [ -e "${line}" ];
	do
	    (( BUEXT == BUEXT++ ))
	    [[ $P == "CVL" ]] && \
		D=${PHOTODIR}.${BUEXT}/20${F:0:2}/${F:2:2} || \
		D=${PHOTODIR}.${BUEXT}/Others/20${F:0:2}/${F:2:2}
	    [[ ! -e "$D/$F" ]] && {
		[[ -d $D ]] || mkdir -pv "${D}"
		$MVCMD -iv "${line}" "${D}" 
	    }
	done
    }
done
