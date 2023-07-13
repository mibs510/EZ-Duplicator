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

import EZDuplicator.version
import EZDuplicator.lib.EZDuplicator
import logging
import os
import pexpect
import psutil
import sys
from gi import require_version as gi_require_version

gi_require_version('Gtk', '3.0')


def check_for_update_process(pipe_connection, exception, update_status, secrets):
    try:
        update = get_available_update(secrets)

        if update is not None:
            update_status.set(str(update))
            pipe_connection.send("update_status.True")
        else:
            pipe_connection.send("update_status.None")
        pipe_connection.send("Finished")
    except Exception as ex:
        logging.exception(ex)
        exception.set(str(ex))
        pipe_connection.send("check_for_update_process().Exception")
        EZDuplicator.lib.EZDuplicator.sleep_indfinite()


def update_process(pipe_connection, exception, secrets):
    pipe_connection.send("self.UpdateDialog_UpdateSpinner.start()")
    index_url = ""
    if EZDuplicator.lib.EZDuplicator.get_config_setting("update_repo") == "dev":
        index_url = secrets.get("update_dev_repo_index_url")
        logging.info("Using development repository to update EZ Duplicator")
    elif EZDuplicator.lib.EZDuplicator.get_config_setting("update_repo") == "prod":
        index_url = secrets.get("update_prod_repo_index_url")
        logging.info("Using production repository to update EZ Duplicator")

    stdout = ""
    try:
        username = secrets.get("update_username")
        password = secrets.get("update_password")
        command = "python3.9 -m pip install -U --ignore-installed --index-url {} EZDuplicator " \
                  "--disable-pip-version-check --no-color --no-python-version-warning".format(index_url)
        pip = pexpect.spawn(command)
        pip.expect("User for")
        pip.sendline(username)
        pip.expect("Password:")
        pip.sendline(password)
        pip.expect(pexpect.EOF, timeout=None)
        stdout = pip.before
        pip.close()

        if pip.exitstatus != 0:
            raise Exception("python3.9/pip exited with a exit status code of {}".format(pip.exitstatus))
        else:
            logging.info("Update sucessful!")
            pipe_connection.send("Finished")
    except Exception as ex:
        logging.exception(ex)
        logging.debug("stdout = {}".format(stdout))
        exception.set(str(ex))
        pipe_connection.send("update_process().Exception")
        EZDuplicator.lib.EZDuplicator.sleep_indfinite()


def get_available_update(secrets):
    index = ""
    if secrets.oos:
        raise Exception("Error getting secrets: OOS")
    if EZDuplicator.lib.EZDuplicator.get_config_setting("update_repo") == "dev":
        index = secrets.get("update_dev_repo_index")
        logging.info("Using development repository to check for updates")
    elif EZDuplicator.lib.EZDuplicator.get_config_setting("update_repo") == "prod":
        index = secrets.get("update_prod_repo_index")
        logging.info("Using production repository to check for updates")

    stdout = ""
    try:
        username = secrets.get("update_username")
        password = secrets.get("update_password")
        command = "python3.9 -m pip search --index {} EZDuplicator --disable-pip-version-check --no-color " \
                  "--no-python-version-warning".format(index)
        pip = pexpect.spawn(command)
        pip.expect("User for")
        pip.sendline(username)
        pip.expect("Password:")
        pip.sendline(password)
        pip.expect(pexpect.EOF, timeout=None)
        stdout = pip.before
        pip.close()

        if pip.exitstatus != 0:
            logging.error("python3.9/pip exited with a exit status code of {}".format(pip.exitstatus))

        stdout = str(stdout, "utf-8")
        splitlines = stdout.splitlines()
        installed = splitlines[2].replace("  ", "", 1)
        available = splitlines[3].replace("  ", "", 1)
        semantic_installed = installed.replace("INSTALLED: ", "", 1)
        semantic_available = available.replace("LATEST:    ", "", 1)
        if semantic_available == semantic_installed:
            logging.info("EZ Duplicator is up-to-date! No update found from {} repository.".
                         format(EZDuplicator.lib.EZDuplicator.get_config_setting("update_repo")))
            return None
        else:
            logging.info("INSTALLED: {}".format(semantic_installed))
            logging.info("LATEST: {}".format(semantic_available))
            return "{}\n{}".format(installed, available)
    except Exception as ex:
        logging.exception(ex)
        logging.debug("stdout = {}".format(stdout))
