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

import os
import sys

import EZDuplicator.lib.DataOnlyDuplication
import EZDuplicator.lib.EZDuplicator


def main():
    json_file = EZDuplicator.lib.EZDuplicator.__mounts_map__

    if EZDuplicator.lib.DataOnlyDuplication.grep_mount("/dev/sd"):
        print("*** UNMOUNT ANY NON ESSENTIAL MEDIA FROM THE EZ DUPLICATOR! ***")
        print("*** EITHER: RESTART THE EZ DUPLICATOR OR UNMOUNT(8)! ***")
        sys.exit(1)

    print("*** TO PROCEED, VERIFY THAT THE SOURCE SLOT IS EMPTY! *** ")
    input("*** HIT ENTER TO CONTINUE ***")

    try:
        mount_to_json = EZDuplicator.lib.DataOnlyDuplication.get_mount2json()
    except Exception as ex:
        print(ex)
        sys.exit(1)

    if os.path.isfile(json_file):
        print("Removing existing mount_map.json")
        os.remove(json_file)

    print("")
    print("Generating a JSON serilaized mount map...")

    with open(json_file, 'w', encoding='utf-8') as map_of_ports_json:
        map_of_ports_json.write(mount_to_json)

    return True


if __name__ == '__main__':
    mainret = main()
    sys.exit(mainret)
