#!/usr/bin/env python
#-*- coding: utf-8 -*-

from ircutils import bot, format

class MyBot(bot.SimpleBot):

    first = True

    def on_welcome(self, event):
        self.send_message('[CYH]Bot', '!C1')

    def on_private_message(self, event):
        if self.first:
            self.first = False
            self.send_message('[CYH]Bot', '!A1 {0}'.format(event.message))
            print event.message

if __name__ == "__main__":
    bot = MyBot('_9258340d85ad')
    bot.connect('irc.idlemonkeys.net', 6667)
    bot.start()
