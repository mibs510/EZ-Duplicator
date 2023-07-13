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
import multiprocessing
import os
import sys
from multiprocessing import Process
from pathlib import Path

from gi import require_version as gi_require_version

import EZDuplicator.WTHDialog
import EZDuplicator.lib.Consent

gi_require_version('Gtk', '3.0')

from gi.repository import Gtk, GLib


class ConsentDialog(Gtk.Dialog):
    """ Main window with all components. """

    def __init__(self):
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
                    'ConsentDialog',
                    'ConsentDialog_Accept',
                    'ConsentDialog_AcceptSpinner',
                    'ConsentDialog_Decline',
                ]
            )
        except Exception as ex:
            logging.exception(ex)
            sys.exit(1)

        # Get gui objects
        self.ConsentDialog = self.builder.get_object('ConsentDialog')
        self.ConsentDialog_Accept = self.builder.get_object('ConsentDialog_Accept')
        self.ConsentDialog_AcceptSpinner = self.builder.get_object('ConsentDialog_AcceptSpinner')
        self.ConsentDialog_Decline = self.builder.get_object('ConsentDialog_Decline')
        self.ConsentDialog.show_all()
        self.builder.connect_signals(self)
        self.manager = multiprocessing.Manager()
        self.exception = self.manager.Value(str, "")

        """ Accept & Send Process """
        self.upload_parent, self.upload_child = multiprocessing.Pipe(duplex=False)
        self.upload_proc = Process(target=EZDuplicator.lib.Consent.upload_process, args=(self.upload_child,
                                                                                         self.exception,), daemon=False)
        """ Do not close the child handle as stop() will not be able to communicate with stop_io_wait() """
        # self.upload_child.close()
        GLib.io_add_watch(self.upload_parent.fileno(), GLib.IO_IN, self.upload_io_watch)

    def on_ConsentDialog_Accept_clicked(self, widget, user_data=None):
        """ Handler for ConsentDialog_Accept.clicked. """
        self.upload_proc.start()

    def on_ConsentDialog_Decline_clicked(self, widget, user_data=None):
        """ Handler for ConsentDialog_Decline.clicked. """
        while self.upload_proc.is_alive():
            self.upload_proc.terminate()
        self.upload_proc.close()
        self.manager.shutdown()
        del self.manager
        self.ConsentDialog.destroy()

    def upload_io_watch(self, source, condition):
        assert self.upload_parent.poll()
        try:
            msg = self.upload_parent.recv()
        except EOFError:
            return False

        if msg == "self.ConsentDialog_AcceptSpinner.start()":
            self.ConsentDialog_Decline.set_sensitive(False)
            self.ConsentDialog_Accept.set_sensitive(False)
            self.ConsentDialog_AcceptSpinner.start()
            return True

        if msg == "WTHDialog.WTHDialog()":
            EZDuplicator.WTHDialog.WTHDialog(self.exception)
            return True

        if msg == "self.ConsentDialog_AcceptSpinner.stop()":
            self.ConsentDialog_AcceptSpinner.stop()
            self.ConsentDialog_Decline.set_label("Close")
            self.ConsentDialog_Decline.set_sensitive(True)
            return True
        return True