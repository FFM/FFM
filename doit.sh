#!/bin/bash


# set vars
export PYTHONPATH=$(pwd)

# spider it and archive it
now=$(date +"%Y%m%d-%H:%M")
out="history/$now-spider.out"
out2="history/$now-Funkfeuer-spider-pickle.dump"
python ./spider/spiderpool.py > $out
mv Funkfeuer-spider-pickle.dump $out2

# do statistics
#./makestats.py Funkfeuer-spider-pickle.dump
