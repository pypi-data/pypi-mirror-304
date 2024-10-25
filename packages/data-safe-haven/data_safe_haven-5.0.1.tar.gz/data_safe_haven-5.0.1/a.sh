#!/bin/bash

while getopts "abc" flag; do
    case ${flag} in
        a) a=${OPTARG}
           echo "Option -a is triggered with ${a}"
            ;;
        b) echo "Option -b is triggered."
            b=${OPTARG}
            ;;
        c) echo "Option -c is triggered."
            ;;
    esac
done

echo "Hello $a and $b"
