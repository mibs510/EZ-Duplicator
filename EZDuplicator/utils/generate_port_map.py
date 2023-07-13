#!/usr/bin/env python3

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
import os
import sys
from json import JSONEncoder
from time import sleep

import numpy as np

import EZDuplicator.lib.EZDuplicator


def main():
    json_file = EZDuplicator.lib.EZDuplicator.__ports_map__
    source_by_path = EZDuplicator.lib.EZDuplicator.get_source_by_path()
    if EZDuplicator.lib.EZDuplicator.get_number_or_list_of_usbs('number', source_by_path) > 0 \
            or EZDuplicator.lib.EZDuplicator.is_source_connected(source_by_path):
        print("*** REMOVE ALL USB DRIVES FROM THE EZ DUPLICATOR! ***")
        sys.exit(1)

    print("*** TO PROCEED, VERIFY THAT THE SOURCE SLOT IS EMPTY! *** ")
    input("*** HIT ENTER TO CONTINUE ***")
    columns = input("Number of USB hubs: ")
    rows = input("Number of USB ports per hub: ")
    input("Verify that the following information is correct\n Number of USB hubs: {}\n "
          "Number of USB ports per hub: {}\n Press Enter to continue, or press Ctrl + C to exit: ".
          format(columns, rows))

    matrix = [["/dev" for y in range(int(columns))] for x in range(int(rows))]
    array = np.array(matrix, dtype=object)

    for y in range(int(columns)):
        for x in range(int(rows)):
            valid = False
            while not valid:
                print("")
                input("From left to right, the first USB hub being the leftmost,\n"
                      "insert any USB drive into USB hub #{}, port #{} and hit Enter: ".format(y + 1, x + 1))
                sleep(3)
                path = generate_port_map()
                if not path:
                    pass
                else:
                    print("{},{} = {}".format(x + 1, y + 1, path))
                    array[x][y] = path
                    break

    """ Serialization """
    map_of_ports = {"map_of_ports": array}
    encoded_map_of_ports = json.dumps(map_of_ports, cls=numpy_array_encoder, ensure_ascii=False, indent=4)
    if os.path.isfile(json_file):
        print("Removing existing map_of_ports.json")
        os.remove(json_file)

    print("")
    print("Generating a JSON serilaized map array...")
    print(encoded_map_of_ports)

    with open(json_file, 'w', encoding='utf-8') as map_of_ports_json:
        map_of_ports_json.write(encoded_map_of_ports)

    print("")
    print("Generated file map_of_ports.json saved!")
    print("EZ Duplicator Application is ready to use! Be sure to configure additional settings (Menu > Settings) if "
          "not already configured.")
    return 0


def generate_port_map():
    """ Grab a list of paths without partition numbers, just the roots. """
    disk_by_path_path = glob.glob("/dev/disk/by-path/pci-*-scsi*")
    filtered = [i for i in disk_by_path_path if 'part' not in i]
    if len(filtered) > 1:
        print("*** MORE THAN 1 USB DRIVE DETECTED! ***")
        return False
    elif len(filtered) == 0:
        print("*** USB DRIVE NOT DETECTED? ***")
        return False
    return filtered[0]


class numpy_array_encoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)


if __name__ == '__main__':
    mainret = main()
    sys.exit(mainret)
