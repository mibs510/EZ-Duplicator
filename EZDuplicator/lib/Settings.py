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

import EZDuplicator.lib.EZDuplicator


def get_default_smtp_settings_process(pipe_connection, default_smtp_settings, exception):
    try:
        pipe_connection.send("self.DefaultSMTPSettings_Button_Spinner.start()")
        try:
            default_smtp_settings.append(EZDuplicator.lib.EZDuplicator.get_secret('mail_host'))
            default_smtp_settings.append(EZDuplicator.lib.EZDuplicator.get_secret('mail_port'))
            default_smtp_settings.append(EZDuplicator.lib.EZDuplicator.get_secret('mail_username'))
            default_smtp_settings.append(EZDuplicator.lib.EZDuplicator.get_secret('mail_password'))
        except Exception as ex:
            logging.error(ex)
            exception.set(str(ex))
            pipe_connection.send("self.DefaultSMTPSettings_Button_Spinner.stop()")
            pipe_connection.send("EZDuplicator.get_secret().Exception")
            EZDuplicator.lib.EZDuplicator.sleep_indfinite()

        pipe_connection.send("self.config")
        pipe_connection.send("self.set_text()")
        pipe_connection.send("self.DefaultSMTPSettings_Button_Spinner.stop()")
    except Exception as ex:
        logging.error(ex)


def test_email_process(pipe_connection, exception):
    try:
        pipe_connection.send("self.Test_Email_Button_Spinner.start()")
        try:
            EZDuplicator.lib.EZDuplicator.send_email_notification(None, None, None, test=True)
        except Exception as ex:
            logging.error(ex)
            exception.set(str(ex))
            pipe_connection.send("self.Test_Email_Button_Spinner.stop()")
            pipe_connection.send("EZDuplicator.send_email_notification().Exception")
            EZDuplicator.lib.EZDuplicator.sleep_indfinite()

        pipe_connection.send("self.Test_Email_Button_Spinner.stop()")
    except Exception as ex:
        logging.error(ex)
