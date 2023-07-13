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

import logging
import os
import shutil
import subprocess
import time

import EZDuplicator.lib.EZDuplicator


def upload_process(pipe_connection, exception):
    pipe_connection.send("self.ConsentDialog_AcceptSpinner.start()")
    time_stamp = time.strftime('%m_%d_%y_%I%M%S')
    zip_file = "/tmp/{}-{}".format(EZDuplicator.lib.EZDuplicator.get_serial_number(), time_stamp)
    dmesg_file = EZDuplicator.lib.EZDuplicator.__log_dir__ + "dmesg-" + time_stamp + ".txt"
    dmesg_stdout_file = EZDuplicator.lib.EZDuplicator.__log_dir__ + "dmesg(8)-" + time_stamp + ".txt"
    kern_log_file = EZDuplicator.lib.EZDuplicator.__log_dir__ + "kern.log-" + time_stamp + ".txt"

    try:
        """ Get dmesg(8) output and save it as dmesg.txt """
        dmesg_stdout = subprocess.Popen("dmesg", stdout=open(dmesg_stdout_file, "w"))
        dmesg_stdout.communicate()
        """ Copy other vital logs """
        shutil.copyfile("/var/log/dmesg", dmesg_file)
        shutil.copyfile("/var/log/kern.log", kern_log_file)
        """ Zip everything in __log_dir__ """
        shutil.make_archive(zip_file, 'zip', EZDuplicator.lib.EZDuplicator.__log_dir__)
        """ Upload & get download link """
        download_link = EZDuplicator.lib.EZDuplicator.upload_file("{}.zip".format(zip_file))
        EZDuplicator.lib.EZDuplicator.send_cs_email_notification(
            EZDuplicator.lib.EZDuplicator.get_serial_number(), download_link)
        if os.path.isfile("{}.zip".format(zip_file)):
            os.remove("{}.zip".format(zip_file))
        if os.path.isfile(dmesg_file):
            os.remove(dmesg_file)
        if os.path.isfile(dmesg_stdout_file):
            os.remove(dmesg_stdout_file)
        if os.path.isfile(kern_log_file):
            os.remove(kern_log_file)
    except Exception as ex:
        logging.exception(ex)
        exception.set(str(ex))
        pipe_connection.send("WTHDialog.WTHDialog()")
        if os.path.isfile("{}.zip".format(zip_file)):
            os.remove("{}.zip".format(zip_file))
        if os.path.isfile(dmesg_file):
            os.remove(dmesg_file)
        if os.path.isfile(dmesg_stdout_file):
            os.remove(dmesg_stdout_file)
        if os.path.isfile(kern_log_file):
            os.remove(kern_log_file)
    finally:
        pipe_connection.send("self.ConsentDialog_AcceptSpinner.stop()")

