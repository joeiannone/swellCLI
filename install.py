#!/usr/bin/env python

import os, sys

try:
  if os.system("pip install -r requirements.txt") != 0:
    raise Exception("Could not install requirements.")
  if os.system("pyinstaller --onefile main.py") != 0:
    raise Exception("Could not create build.")
  if os.system("sudo cp ./dist/main /usr/local/bin/swell") != 0:
    raise Exception("Could not publish build.")
  if os.system("rm -r build dist") != 0:
    raise Exception("Could not clean up project directory.")

except Exception as e:
  sys.exit("\nSomething went wrong with install: " + str(e) + "\n")


sys.exit("\n\nSuccess.\n\nUse the command 'swell' to run.\n\n")
