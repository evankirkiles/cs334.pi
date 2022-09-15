#!/bin/bash

# install zsh
sudo apt-get update && sudo apt-get install zsh

# install oh-my-zsh
sh -c "$(wget https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh -O -)"