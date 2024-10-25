#!/bin/bash

while getopts "u:p:" flag; do
   case "${flag}" in
       u) User=${OPTARG};;
       p) Password=${OPTARG};;
   esac
done

echo "user: ${User} password: ${Password}"
