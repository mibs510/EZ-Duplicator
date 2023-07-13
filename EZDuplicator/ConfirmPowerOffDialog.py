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

gi_require_version('Gtk', '3.0')

from gi.repository import Gtk


class ConfirmPowerOffDialog(Gtk.Dialog):
    """ Main window with all components. """

    def __init__(self, parent):
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
                    'ConfirmPowerOffDialog',
                    'ConfirmPowerOffDialog_Cancel',
                    'ConfirmPowerOffDialog_Confirm',
                ]
            )
        except Exception as ex:
            logging.error(ex)
            sys.exit(1)

        # Get gui objects
        self.ConfirmPowerOffDialog = self.builder.get_object('ConfirmPowerOffDialog')
        self.ConfirmPowerOffDialog_Cancel = self.builder.get_object('ConfirmPowerOffDialog_Cancel')
        self.ConfirmPowerOffDialog_Confirm = self.builder.get_object('ConfirmPowerOffDialog_Confirm')
        self.ConfirmPowerOffDialog.show_all()
        self.ConfirmPowerOffDialog.set_transient_for(parent)
        self.builder.connect_signals(self)

    def on_ConfirmPowerOffDialog_Cancel_clicked(self, widget, user_data=None):
        """ Handler for ConfirmPowerOffDialog_Cancel.clicked. """
        self.ConfirmPowerOffDialog.destroy()

    def on_ConfirmPowerOffDialog_Confirm_clicked(self, widget, user_data=None):
        """ Handler for ConfirmPowerOffDialog_Confirm.clicked. """
        os.system("sudo poweroff")
