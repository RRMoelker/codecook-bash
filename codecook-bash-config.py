#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script for setting CodeCook bash program configurations
"""
import ConfigParser
import os
import sys

from config import get_config_file


path = 'codecook-bash'
config_file = get_config_file()

print "Please supply the information needed to get the codecook-bash program up and running."

# check no accidental config overwrite
if os.path.isfile(config_file):
	print "Configuration file exists, overwrite it?"
	prompt = raw_input("[y/N] ")
	if prompt != "y":
		sys.exit("Not overwriting config file.")


# get config info
cc_user = raw_input("What is your username?: ")
cc_key = raw_input("What is your API key?: ")


# actually write config
print "writing config file..."
config = ConfigParser.ConfigParser()
config.set('DEFAULT', 'cc_user', cc_user)
config.set('DEFAULT', 'cc_key', cc_key)

with open(config_file, 'w') as configfile:
	config.write(configfile)

print "done, config complete"