#!/bin/bash
while getopts ":f:" opt; do
  case ${opt} in
    f ) file=$OPTARG
        echo "The given file is ${file}"
      ;;
   \? )
      echo "Invalid option: $OPTARG"
      ;;
   : )
      echo "Invalid option: $OPTARG requires an argument"
      ;;
  esac
done
