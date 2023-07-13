#!/bin/bash

#
# Copyright (c) 2021 Connor McMillan. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
# following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following
# disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the
# following disclaimer in the documentation and/or other materials provided with the distribution.
#
# 3. All advertising materials mentioning features or use of this software must display the following acknowledgement:
# This product includes software developed by Connor McMillan.
#
# 4. Neither Connor McMillan nor the names of its contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY CONNOR MCMILLAN "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
# EVENT SHALL CONNOR MCMILLAN BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR
# TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#

if [ "$(lsb_release -r | awk '{print $2}')" != "20.04" ]; then
  echo "WARNING: Use Ubuntu 20.04!"
fi

sudo apt update
sudo apt -y upgrade
sudo apt -y install avrdude
# sudo usermod -a -G ${USER} dialout
# sudo usermod -a -G root dialout
sudo apt install btrfs-progs exfat-utils f2fs-tools hfsutils hfsplus hfsprogs jfsutils cryptsetup dmsetup lvm2 \
util-linux nilfs-tools reiser4progs reiserfsprogs udftools xfsprogs xfsdump partclone disktype grub-imageboot isolinux \
makebootfat pxelinux extlinux syslinux syslinux-common syslinux-efi syslinux-legacy syslinux-utils python3.9 virtualenv \
libcairo2-dev libjpeg-dev libgif-dev libpango1.0-dev libgirepository1.0-dev python3-gi python-gobject-2-dev \
gobject-introspection libpython3.9 libpython3.9-dev python3-pip build-essential debhelper devscripts equivs python3-venv \
python3-dev dh-virtualenv python3-setuptools onboard python3-virtualenv glade

rm -rf venv
virtualenv --python=$(which python3.9) venv && source venv/bin/activate && pip install -r requirements.txt && \
echo "" && \
echo "Done!" && \
echo ""