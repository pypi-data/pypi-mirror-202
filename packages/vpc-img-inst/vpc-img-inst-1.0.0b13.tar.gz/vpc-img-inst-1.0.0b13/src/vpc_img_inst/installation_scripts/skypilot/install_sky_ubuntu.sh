#!/bin/bash -i
# Executing script in interactive mode

function mylsof { p=$(for pid in /proc/{0..9}*; do i=$(basename "$pid"); for file in "$pid"/fd/*; do link=$(readlink -e "$file"); if [ "$link" = "$1" ]; then echo "$i"; fi; done; done); echo "$p"; };
sudo systemctl stop unattended-upgrades || true;
sudo systemctl disable unattended-upgrades || true;
sudo sed -i 's/Unattended-Upgrade "1"/Unattended-Upgrade "0"/g' /etc/apt/apt.conf.d/20auto-upgrades || true;
p=$(mylsof "/var/lib/dpkg/lock-frontend"); echo "$p";
sudo kill -9 `echo "$p" | tail -n 1` 2>/dev/null || true;
sudo rm /var/lib/dpkg/lock-frontend 2>/dev/null;
sudo pkill -9 dpkg;
sudo pkill -9 apt-get;
sudo dpkg --configure --force-overwrite -a;

pip3 --version > /dev/null 2>&1 || (curl -sSL https://bootstrap.pypa.io/get-pip.py -o get-pip.py && python3 get-pip.py && echo "PATH=$HOME/.local/bin:$PATH" >> ~/.bashrc);
(type -a python | grep -q python3) || echo 'alias python=python3' >> ~/.bashrc;
(type -a pip | grep -q pip3) || echo 'alias pip=pip3' >> ~/.bashrc;
(which conda > /dev/null 2>&1 && conda init > /dev/null && conda config --set auto_activate_base false) || (wget -nc https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && bash Miniconda3-latest-Linux-x86_64.sh -b && eval "$(~/miniconda3/bin/conda shell.bash hook)" && conda init && conda config --set auto_activate_base true);

source ~/.bashrc;
# pip3 install skypilot;
$(which python3) -m pip install skypilot
$(which python3) -m pip install skypilot
