#!/bin/bash

while getopts ":i:" opt; do
    case $opt in
        i)
            for LINE in $(find $OPTARG -name '*.CR2') ; do
                cut -d ' ' -f1 <(sha1sum ${LINE})
            done
            ;;
        \?)
            echo "ERROR: -$OPTARG is an invalid option." >&2
            ;;
        :)
            echo "ERROR: -$OPTARG takes an argument." >&2
        esac
done
