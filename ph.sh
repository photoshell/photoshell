#!/bin/bash

while getopts ":i:" opt; do
    case $opt in
        i)
            echo "Importing $OPTARG"
            ;;
        \?)
            echo "ERROR: -$OPTARG is an invalid option." >&2
            ;;
        :)
            echo "ERROR: -$OPTARG takes an argument." >&2
        esac
done
