#!/bin/bash

# 1111 2222 3333 4444 5555

for seed in 1111 2222 3333 4444 5555 6666 7777 8888 9999
do
  for env in bumper obstacle step terrain
  do
    python search_morphology.py --seed $seed --env $env  
  done
done