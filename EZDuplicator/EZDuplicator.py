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

import argparse
import logging
import sys

from elevate import elevate
from gi import require_version as gi_require_version

import EZDuplicator.App
import EZDuplicator.version
import EZDuplicator.lib.EZDuplicator

gi_require_version('Gtk', '3.0')

from gi.repository import Gtk


def main():
    elevate(graphical=False)
    try:
        parser = argparse.ArgumentParser(prog="EZDuplicator",
                                         formatter_class=argparse.RawTextHelpFormatter,
                                         epilog="EZDuplicator v{}\n"
                                                "(c) 2021 Connor McMillan "
                                                "<connor@mcmillan.website>".format(EZDuplicator.version.__version__))
        parser.add_argument('-d', '--debug', help='Disable 12VPM and other non-essentials.',
                            action='store_true')
        args = parser.parse_args()
        """ Main entry point for the program. """
        EZDuplicator.lib.EZDuplicator.create_default_config()
        EZDuplicator.lib.EZDuplicator.improve_software()
        EZDuplicator.lib.EZDuplicator.init_logging()
        if args.debug:
            logging.info("Debug mode activated.")
            app = EZDuplicator.App.App(debug=True)  # noqa
        else:
            app = EZDuplicator.App.App() # noqa
        return Gtk.main()
    except Exception as ex:
        logging.exception(ex)


if __name__ == '__main__':
    mainret = main()
    sys.exit(mainret)
