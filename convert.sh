#!/usr/bin/env bash

for f in $(ls -1 "$2")
do
  if [[ "$f" == *"graphml" ]]; then
    echo "Processing $f "
    if [[ "$1" == "zoned" ]]; then
      python3 agraphml2connmap.py -f "$2""$f" --zoned
    else
      python3 agraphml2"$1".py -f "$2""$f"
    fi
  fi
done