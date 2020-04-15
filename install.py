#!/usr/bin/env python

# TODO:
# Needs Testing!!!!!!!!!!

import os, sys

try:
    os.system('pip install -r requirements.txt')
    os.system('pyinstaller --onefile main.py')
    os.system('cp ./dist/main /usr/local/bin/swell')
    os.system('rm -r build')
    os.system('rm -r dist')

except Exception as e:
    sys.exit("\nSomething went wrong with install: " + str(e) + "\n")


sys.exit("\n\nSuccess.\n\nUse the command 'swell' to run.\n\n")
