#!/usr/bin/env python

# @Author: Joe Iannone <josephiannone>
# @Date:   2019-01-22T21:22:57-05:00
# @Filename: main.py
# @Last modified by:   josephiannone
# @Last modified time: 2019-05-13T19:35:05-04:00


import sys

# python version check and warning
pyv = sys.version_info
pyv_str = str(pyv[0]) + '.' + str(pyv[1])
if float(pyv_str) < 3.6:
    print('\nERROR: You must use python version 3.6 or higher.')
    print('This is version ' + pyv_str + '\n')
    sys.exit()


# check dependencies
try:
    from cli import swellCLI
except ImportError:
  print('\nDependencies not installed.')
  print('\nrun:\n\tpip install -r requirements.txt\n')
  sys.exit()


def main():
    cli = swellCLI()
    cli.run()

if __name__ == '__main__':
    main()
