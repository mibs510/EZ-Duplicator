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
import logging
import os
import subprocess
import time
from pathlib import Path

import serial
from gi import require_version as gi_require_version

import EZDuplicator.AppCrashedDialog
import EZDuplicator.lib.EZDuplicator
import EZDuplicator.lib.webtail

gi_require_version('Gtk', '3.0')


def webtail_http_server_daemon():
    filename = EZDuplicator.lib.EZDuplicator.__dot_log_file__
    port = EZDuplicator.lib.EZDuplicator.__webtail_http_server_port__
    if filename is None:
        logging.error('No input file to tail')
        return
    try:
        EZDuplicator.lib.webtail.WebTailHTTPRequestHandler.filename = filename
        server_address = ('', int(port))
        httpd = EZDuplicator.lib.webtail.WebTailServer(server_address,
                                                       EZDuplicator.lib.webtail.WebTailHTTPRequestHandler)
        logging.info('Starting HTTP webtail server at port %d', server_address[1])
        httpd.serve_forever()
    except KeyboardInterrupt:
        logging.info('HTTP server stopped')


def update_date_and_time_daemon(pipe_connection):
    while True:
        pipe_connection.send("{}\n{}".format(time.strftime('%I:%M:%S %p'), time.strftime('%m/%d/%y')))
        time.sleep(1)


def update_number_of_usbs_daemon(pipe_connection):
    source_bypath = EZDuplicator.lib.EZDuplicator.get_config_setting('source_dev_path')
    while True:
        number_of_usbs = EZDuplicator.lib.EZDuplicator.get_number_or_list_of_usbs(
            'number', source_bypath, debug=False, warnings=True)
        pipe_connection.send(number_of_usbs)


def get_com_port():
    try:
        com_port = serial.Serial()
        com_port.port = EZDuplicator.lib.EZDuplicator.get_config_setting("twelve_v_com_port")
        com_port.baudrate = 115200
        com_port.bytesize = serial.EIGHTBITS  # number of bits per bytes
        com_port.parity = serial.PARITY_NONE  # set parity check: no parity
        com_port.stopbits = serial.STOPBITS_ONE  # number of stop bits
        com_port.timeout = 1  # non-block read
        com_port.xonxoff = False  # disable software flow control
        com_port.rtscts = False  # disable hardware (RTS/CTS) flow control
        com_port.dsrdtr = True  # disable hardware (DSR/DTR) flow control
        com_port.writeTimeout = 2  # timeout for write
        return com_port
    except Exception as ex:
        logging.error(ex)
