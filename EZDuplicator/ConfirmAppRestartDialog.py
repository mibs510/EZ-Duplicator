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
import sys
from pathlib import Path

from gi import require_version as gi_require_version

import EZDuplicator.lib.EZDuplicator

gi_require_version('Gtk', '3.0')
from gi.repository import Gtk


class ConfirmAppRestarDialog(Gtk.Dialog):
    """ Main window with all components. """

    def __init__(self, pids, parent):
        Gtk.Dialog.__init__(self)
        self.builder = Gtk.Builder()
        gladefile = str(Path(__file__).parent.absolute()) + '/res/window.ui'
        if not os.path.exists(gladefile):
            # Look for glade file in this project's directory.
            gladefile = os.path.join(sys.path[0], gladefile)

        try:
            self.builder.add_objects_from_file(
                gladefile,
                [
                    'ConfirmAppRestarDialog',
                    'ConfirmAppRestarDialog_Cancel',
                    'ConfirmAppRestarDialog_Confirm',
                ]
            )
        except Exception as ex:
            logging.exception(ex)
            sys.exit(1)

        # Get gui objects
        self.ConfirmAppRestarDialog = self.builder.get_object('ConfirmAppRestarDialog')
        self.ConfirmAppRestarDialog_Cancel = self.builder.get_object('ConfirmAppRestarDialog_Cancel')
        self.ConfirmAppRestarDialog_Confirm = self.builder.get_object('ConfirmAppRestarDialog_Confirm')
        self.builder.connect_signals(self)
        self.pids = pids

        self.ConfirmAppRestarDialog.show_all()
        self.ConfirmAppRestarDialog.set_transient_for(parent)

    def on_ConfirmAppRestarDialog_Cancel_clicked(self, widget, user_data=None):
        """ Handler for ConfirmAppRestarDialog_Cancel.clicked. """
        self.ConfirmAppRestarDialog.destroy()

    def on_ConfirmAppRestarDialog_Confirm_clicked(self, widget, user_data=None):
        """ Handler for ConfirmAppRestarDialog_Confirm.clicked. """
        logging.info("Restarting EZ Duplicator app...")
        argv = ""
        for pid in self.pids:
            pid = str(pid)
            if pid != str(self.pids[-1]):
                argv += pid + " "
            else:
                argv += pid
        command = "python3.9 {}/restart_app.py {}".format(EZDuplicator.lib.EZDuplicator.__root_dir__, argv)
        os.system(command)
