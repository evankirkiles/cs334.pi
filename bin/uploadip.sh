#!/bin/bash

# copy our service file into the systemd directory
sudo cp ~/Desktop/cs334files/lib/uploadip/onwifi.service /etc/systemd/system/onwifi.service

# reload the systemctl daemon, in case service already existed
sudo systemctl daemon-reload

# start the service and enable it
sudo systemctl start onwifi.service
sudo systemctl enable onwifi.service