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

import argparse
import sys

import EZDuplicator.version
import EZDuplicator.lib.EZDuplicator
import logging
import pexpect


def update(debug=False):
    stdout = ""

    try:
        EZDuplicator.lib.EZDuplicator.init_logging()
        index_url = ""
        secrets = EZDuplicator.lib.EZDuplicator.Secrets()
        if secrets.oos:
            raise Exception(secrets.ex_msg)

        if EZDuplicator.lib.EZDuplicator.get_config_setting("update_repo") == "dev":
            index_url = secrets.get("update_dev_repo_index_url")
            logging.info("Using development repository to update EZ Duplicator")
        elif EZDuplicator.lib.EZDuplicator.get_config_setting("update_repo") == "prod":
            index_url = secrets.get("update_prod_repo_index_url")
            logging.info("Using production repository to update EZ Duplicator")

        username = secrets.get("update_username")
        password = secrets.get("update_password")
        command = "python3.9 -m pip install -U --ignore-installed --index-url {} EZDuplicator " \
                  "--disable-pip-version-check --no-color --no-python-version-warning".format(index_url)
        pip = pexpect.spawn(command)
        if debug:
            pip.logfile_read = sys.stdout
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
            return 0
    except Exception as ex:
        logging.exception(ex)
        logging.debug("stdout = {}".format(stdout))
        return 1


def main():
    """ Main entry point for the program. """
    parser = argparse.ArgumentParser(prog="EZDuplicator Updater",
                                     formatter_class=argparse.RawTextHelpFormatter,
                                     epilog="EZDuplicator Updater (From EZDuplicator v{})\n"
                                            "(c) 2021 Connor McMillan "
                                            "<connor@mcmillan.website>".format(EZDuplicator.version.__version__))
    parser.add_argument('-d', '--debug', help='Show pip stdout in relatime',
                        action='store_true')
    args = parser.parse_args()
    """ Main entry point for the program. """
    if args.debug:
        logging.info("Debug mode activated.")
        return update(debug=True)  # noqa
    else:
        return update()


if __name__ == '__main__':
    mainret = main()
    sys.exit(mainret)
