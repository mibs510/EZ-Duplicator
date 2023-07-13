#  Copyright (c) 2021 Connor McMillan. All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
#  following conditions are met:
#
#  1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following
#  disclaimer.
#
#  2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the
#  following disclaimer in the documentation and/or other materials provided with the distribution.
#
#  3. All advertising materials mentioning features or use of this software must display the following acknowledgement:
#  This product includes software developed by Connor McMillan.
#
#  4. Neither Connor McMillan nor the names of its contributors may be used to endorse or promote products derived from
#  this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY CONNOR MCMILLAN "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
#  EVENT SHALL CONNOR MCMILLAN BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
#  DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
#  OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR
#  TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
#  POSSIBILITY OF SUCH DAMAGE.

import glob
import json
import logging
import os

import EZDuplicator.lib.EZDuplicator


def get_disk_by_path(abs_blkdev):
    try:
        rtn = None
        for disk_by_path in glob.glob("/dev/disk/by-path/pci-*-scsi*"):
            if os.path.islink(disk_by_path):
                if os.readlink(disk_by_path).split("/")[2] == abs_blkdev.split("/")[2]:
                    rtn = disk_by_path
        return rtn
    except Exception as ex:
        logging.error(ex)
        return None


def get_x_and_y(disk_by_path):
    try:
        with open(EZDuplicator.lib.EZDuplicator.__ports_map__) as json_file:
            deserailized_map_of_ports = json.load(json_file)

        columns = 0
        while True:
            try:
                tmp = deserailized_map_of_ports['map_of_ports'][0][columns]
                columns += 1
            except Exception:
                break

        rows = 0
        while True:
            try:
                tmp = deserailized_map_of_ports['map_of_ports'][rows]
                rows += 1
            except Exception:
                break

        for y in range(columns):
            for x in range(rows):
                if deserailized_map_of_ports['map_of_ports'][x][y] == disk_by_path:
                    logging.info("{} = ({},{})".format(disk_by_path, x, y))
                    return "{}{}".format(x, y)
        return None
    except Exception as ex:
        logging.error(ex)
        return None
