#!/bin/bash

# 1. get into the git repository
cd ~/Desktop/cs334files
git checkout raspberrypi
git pull origin raspberrypi

# 2. get the IP address into the ip.md file
hostname -I > ~/Desktop/cs334files/ip.md

# 2. push to the git repository
git add -A
git commit -m "AUTO: Raspi IP address [$(date)]"
git push origin raspberrypi