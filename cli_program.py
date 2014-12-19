#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ConfigParser
import sys
import urwid

from API import CodecookApi
from config import get_config_file
from menu import *



#
# Load settings
#
# print "opening config file..."
config = ConfigParser.ConfigParser()
config_file = get_config_file()
with open(config_file, 'r') as configfile:
    config.read(config_file)
    cc_user = config.get('DEFAULT', 'cc_user')
    cc_key = config.get('DEFAULT', 'cc_key')

if cc_user == None or cc_key == None:
    print "user data configuration not set. Please run config program."

api = CodecookApi()
api.configure(cc_user, cc_key)
# print "configuration loaded."


#
# Start command line UI
#
def exit_on_q(key):
    if key in ('q', 'Q', 'esc',):
        raise urwid.ExitMainLoop()


search_question = SearchQuestion(u"Search query?\n")
top_widget = MenuNavigator(search_question)


# start main loop an show top_widget
# copy_success = False
loop = urwid.MainLoop(top_widget, unhandled_input=exit_on_q)
try:
    loop.run()
except Exception as e:
    # catching exceptions to allow clean exit, otherwise urwid wreaks havoc to terminal session in and output

    print "attempting clean exit..."
    loop.screen.stop()
    loop.stop()

    print "exception encountered: "
    print e

    print "done."


# if copy_success:
print "code copied to clipboard, closing program."
# else:
    # print "closing program."
