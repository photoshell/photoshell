#!/bin/bash

while read line
do
    LIBRARY=$line
done < ~/.ph.sh

mkdir -p ${LIBRARY}/raw
mkdir -p ${LIBRARY}/thumbnail

while getopts ":i:" opt; do
    case $opt in
        i)
            for LINE in $(find $OPTARG -name '*.CR2') ; do
                HASH=$(cut -d ' ' -f1 <(sha1sum ${LINE}))
                NEWFILE=${LIBRARY}/raw/${HASH}.CR2
                cp ${LINE} ${NEWFILE}
                dcraw -c -e ${NEWFILE} > ${LIBRARY}/thumbnail/${HASH}.JPG
            done
            ;;
        \?)
            echo "ERROR: -$OPTARG is an invalid option." >&2
            ;;
        :)
            echo "ERROR: -$OPTARG takes an argument." >&2
        esac
done
