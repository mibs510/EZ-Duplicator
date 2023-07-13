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
import subprocess
import sys
from pathlib import Path

from gi import require_version as gi_require_version

import EZDuplicator.lib.EZDuplicator

gi_require_version('Gtk', '3.0')

from gi.repository import Gtk


class UnlockSettingsDialog(Gtk.Dialog):
    """ Main window with all components. """

    def __init__(self, theirself, parent):
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
                    'Cancel',
                    'IncorrectPINInfoBar_Message',
                    'IncorrectPIN_InfoBar',
                    'PinCode_Entry',
                    'Unlock',
                    'UnlockSettingsDialog',
                ]
            )
        except Exception as ex:
            logging.exception(ex)
            sys.exit(1)

        # Get gui objects
        self.Cancel = self.builder.get_object('Cancel')
        self.IncorrectPINInfoBar_Message = self.builder.get_object('IncorrectPINInfoBar_Message')
        self.IncorrectPIN_InfoBar = self.builder.get_object('IncorrectPIN_InfoBar')
        self.PinCode_Entry = self.builder.get_object('PinCode_Entry')
        self.Unlock = self.builder.get_object('Unlock')
        self.UnlockSettingsDialog = self.builder.get_object('UnlockSettingsDialog')
        self.builder.connect_signals(self)
        self.UnlockSettingsDialog.show_all()
        self.SettingsDialog = theirself
        self.UnlockSettingsDialog.set_transient_for(parent)

        self.IncorrectPIN_InfoBar.hide()
        self.pin_code = EZDuplicator.lib.EZDuplicator.get_secret('unlock_settings_pin')

    def on_Cancel_clicked(self, widget, user_data=None):
        """ Handler for Cancel.clicked. """
        self.UnlockSettingsDialog.destroy()

    def on_PinCode_Entry_focus_in_event(self, widget, event, user_data=None):
        """ Handler for PinCode_Entry.focus-in-event. """
        subprocess.Popen("onboard")

    def on_PinCode_Entry_focus_out_event(self, widget, event, user_data=None):
        """ Handler for PinCode_Entry.focus-out-event. """
        subprocess.Popen(["pkill", "onboard"])

    def on_Unlock_clicked(self, widget, user_data=None):
        """ Handler for Unlock.clicked. """
        if self.PinCode_Entry.get_text() != self.pin_code:
            logging.warning("Incorrect PIN!")
            self.IncorrectPIN_InfoBar.show()
        else:
            self.SettingsDialog.SourceDevPath.set_sensitive(True)
            self.SettingsDialog.TwelveVCOMPort.set_sensitive(True)
            self.SettingsDialog.Repo.set_sensitive(True)
            self.SettingsDialog.UnlockButton.set_sensitive(False)
            self.SettingsDialog.DebugUtilities.set_sensitive(True)
            self.UnlockSettingsDialog.destroy()
