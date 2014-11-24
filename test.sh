#!/bin/bash

INPUT=testcases.csv
OLDIFS=$IFS
IFS=,

COUNTER=1

[ ! -f $INPUT ] && { echo "$INPUT file not found"; exit 99; }

while read kripke ltl status 
do
	output=`python lmc.py -i $kripke $ltl 2>&1`
	rc=$?
	result="$(tput setaf 1) FAIL$(tput sgr0)"
	if (($rc == 10));
	then
		if [[ $status = "pos" ]]
		then
			result="$(tput setaf 2)PASS$(tput sgr0)"
		fi
	else
		if [[ $status = "neg" ]] 
		then
			result="$(tput setaf 2)PASS$(tput sgr0)"
		fi
	fi

	echo "$COUNTER   $kripke $ltl : $result"
	echo $output | sed 's/^/  /' 
	COUNTER=$(( $COUNTER + 1 ))
done < $INPUT

IFS=$OLDIFS

