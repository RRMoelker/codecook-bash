codecook-bash
=============

# No longer supported, codecook-console is new project

Bash snippet tool that searches and inserts snippets from [CodeCook.io](http://codecook.io/).


![Plugin impression](https://raw.githubusercontent.com/RRMoelker/codecook-bash/master/codecook_bashplugin_impression.png)

## Important
This plugin is still *under development*. And an *user account* on CodeCook.io is *needed* for API authentication.


## Install
This package is not (yet) available in package control and no installation scripts are available at this time. For manual installation follow the steps:

1. Clone the repository or extract the zip in the packages folder.
1. install the python packages listed in the *requqirements.txt*. For example using: `pip install -r requirements.txt`

## Configuration
An api key and user account are needed to use this plugin. Run `codecook-bash-config.py` to set the needed credentials.

## Usage
Every time you wish to insert a code snippet you start the `cli_program.py`. The snippet you select will be copied to the clipboard. You can likely insert it using ctrl+shift+v
