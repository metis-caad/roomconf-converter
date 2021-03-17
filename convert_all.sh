#!/bin/bash

# shellcheck disable=SC2044
for class in $(find "$1" -type d -name '*o*'); do
    ./convert.sh "$2" "$class"/
done
