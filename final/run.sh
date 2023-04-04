#!/bin/bash

# 1111 2222 3333 4444 5555

# for seed in 1111 2222 3333 4444 5555 6666 7777 8888 9999
# do
#   for env in bumper obstacle step terrain
#   do
#     python search_morphology.py --seed $seed --env $env  
#   done
# done

# for seed in 3131 3232
# do
#   for env in terrain
#   do
#     python search_morphology.py --seed $seed --env $env  
#   done
# done

# for i in $(seq 1 50)
# do
#   for env in terrainx
#   do
#     python search_morphology.py --seed 1234 --env $env  
#   done
# done

for env in terrain36199 terrain10203 terrain31708 terrain14573 terrain29801 terrain1717 terrain12820 terrain17777 terrain39951 terrain23053 terrain4593 terrain22820 terrain31626 terrain28497 terrain20691 terrain7340 terrain47634 terrain39015 terrain4420 terrain12336 terrain9506 terrain4766 terrain9849 terrain36362 terrain49000 terrain14168 terrain12784 terrain22590 terrain36679 terrain47239 terrain28955 terrain23201 terrain33336 terrain25341 terrain9786 terrain39369 terrain24026 terrain48485 terrain1921 terrain18200 terrain42058 terrain7115 terrain37200 terrain17885 terrain4736 terrain27816 terrain49696 terrain36398 terrain46255 terrain36314
do
  python3 search_morphology.py --seed 2345 --env $env  
done
