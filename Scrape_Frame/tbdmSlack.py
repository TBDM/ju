# !/usr/bin/env python
# -*- coding: utf-8 -*-


#----------model import----------

import time

import slacker

import tbdmConfig
from tbdmLogging import tbdmLogger

#----------model import----------


#----------global variables----------


#----------global variables----------


#----------class definition----------
class tbdmSlack():
    slack = slacker.Slacker(tbdmConfig.SLACK_BENDER_TOKEN)
    logger = tbdmLogger('tbdmInfo').log

    def get_slack(self, slack_token = ''):
        if slack_token != '':
            try:
                newslack = self.slacker.Slacker(tbdmConfig.SLACK_BENDER_TOKEN)
            except Exception as _Eall:
                self.logger.warning(_Eall)
                return None
            else:
                return newslack
        else:
            return self.slack

    def post_message(self, text, channel = 'random', as_user = True, username = 'Undefined', whoiam = True):
        if whoiam:
            text = tbdmConfig.WHO_IAM + text
        try:
            rep = self.slack.chat.post_message(channel, text, as_user = as_user, username = username)
        except Exception as _Eall:
            self.logger.warning(_Eall)

#----------class definition----------


#----------function definition----------

#----------function definition----------


#----------main function----------

#----------main function----------
