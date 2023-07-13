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

import EZDuplicator.PowerOnHubDialog

gi_require_version('Gtk', '3.0')

from gi.repository import Gtk


class SecureEraseDialog_1(Gtk.Dialog):
    """ Main window with all components. """

    def __init__(self, option):
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
                    'SecureEraseDialog_1',
                    'SecureEraseDialog_1_CancelButton',
                    'SecureEraseDialog_1_ContinueButton',
                ]
            )
        except Exception as ex:
            logging.error(ex)
            sys.exit(1)

        # Get gui objects
        self.SecureEraseDialog_1 = self.builder.get_object('SecureEraseDialog_1')
        self.SecureEraseDialog_1_CancelButton = self.builder.get_object('SecureEraseDialog_1_CancelButton')
        self.SecureEraseDialog_1_ContinueButton = self.builder.get_object('SecureEraseDialog_1_ContinueButton')
        self.SecureEraseDialog_1.show_all()
        self.builder.connect_signals(self)
        self.option = option

    def on_SecureEraseDialog_1_CancelButton_clicked(self, widget, user_data=None):
        """ Handler for SecureEraseDialog_1_CancelButton.clicked. """
        self.SecureEraseDialog_1.destroy()

    def on_SecureEraseDialog_1_ContinueButton_clicked(self, widget, user_data=None):
        """ Handler for SecureEraseDialog_1_ContinueButton.clicked. """
        EZDuplicator.PowerOnHubDialog.PowerOnHubDialog(self.option)
        self.SecureEraseDialog_1.destroy()

