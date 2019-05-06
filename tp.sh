#!/bin/bash

OPTIONS=""
while [[ $# -gt 0 ]]
do
key="$1"

case $key in
    -e)
    EX_PATH="$2"
    shift
    ;;
    *)
        echo "Argument inconnu: ${1}"
        exit
    ;;
esac
shift
done


#python ./sol.py $EX_PATH $OPTIONS
python3 ./src/sol.py $EX_PATH $OPTIONS
