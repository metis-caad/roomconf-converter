#!/usr/bin/env bash

for f in $(ls -1 "$2")
do
  if [[ "$f" == *".agraphml" ]]; then
    echo "Processing $f "
    python3 agraphml2"$1".py -f "$2""$f"
  fi
done