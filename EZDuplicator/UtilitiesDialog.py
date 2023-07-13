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


class UtilitiesDialog(Gtk.Dialog):
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
                    'UtilitiesDialog',
                    'UtilitiesDialog_CloseButton',
                    'UtilitiesDialog_FileManagerButton',
                    'UtilitiesDialog_TaskManagerButton',
                    'UtilitiesDialog_TerminalButton',
                    'UtilitiesDialog_TextEditorButton',
                    'UtilitiesDialog_WebBrowserButton',
                ]
            )
        except Exception as ex:
            logging.exception(ex)
            sys.exit(1)

        # Get gui objects
        self.UtilitiesDialog = self.builder.get_object('UtilitiesDialog')
        self.UtilitiesDialog_CloseButton = self.builder.get_object('UtilitiesDialog_CloseButton')
        self.UtilitiesDialog_FileManagerButton = self.builder.get_object('UtilitiesDialog_FileManagerButton')
        self.UtilitiesDialog_TaskManagerButton = self.builder.get_object('UtilitiesDialog_TaskManagerButton')
        self.UtilitiesDialog_TerminalButton = self.builder.get_object('UtilitiesDialog_TerminalButton')
        self.UtilitiesDialog_TextEditorButton = self.builder.get_object('UtilitiesDialog_TextEditorButton')
        self.UtilitiesDialog_WebBrowserButton = self.builder.get_object('UtilitiesDialog_WebBrowserButton')

        self.builder.connect_signals(self)
        self.UtilitiesDialog.show_all()

    def on_UtilitiesDialog_CloseButton_clicked(self, widget, user_data=None):
        """ Handler for UtilitiesDialog_CloseButton.clicked. """
        self.UtilitiesDialog.destroy()

    def on_UtilitiesDialog_FileManagerButton_clicked(self, widget, user_data=None):
        """ Handler for UtilitiesDialog_FileManagerButton.clicked. """
        os.system("nautilus &>/dev/null")

    def on_UtilitiesDialog_TaskManagerButton_clicked(self, widget, user_data=None):
        """ Handler for UtilitiesDialog_TaskManagerButton.clicked. """
        os.system("gnome-system-monitor &>/dev/null")

    def on_UtilitiesDialog_TerminalButton_clicked(self, widget, user_data=None):
        """ Handler for UtilitiesDialog_TerminalButton.clicked. """
        os.system("gnome-terminal")

    def on_UtilitiesDialog_TextEditorButton_clicked(self, widget, user_data=None):
        """ Handler for UtilitiesDialog_TextEditorButton.clicked. """
        os.system("gedit &>/dev/null")

    def on_UtilitiesDialog_WebBrowserButton_clicked(self, widget, user_data=None):
        """ Handler for UtilitiesDialog_WebBrowserButton.clicked. """
        os.system("export DISPLAY=\":0\" && firefox &>/dev/null")
