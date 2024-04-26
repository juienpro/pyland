#!/usr/bin/env python3
import argparse
import importlib
import sys
from libs.Log import logger


version = '0.4'

# Change your config here
active_config = 'myConfig'


parser = argparse.ArgumentParser(description="Pyland - Manage Hyprland with Python")
parser.add_argument("-l", "--listen", action="store_true", help="Listen only")
parser.add_argument("-v", "--version", action="store_true", help="Listen only")
args = parser.parse_args()

if args.version:
    print('Pyland version: ' + version)
    sys.exit()

logger.info('Starting Pyland')
if args.listen:
    logger.info('Listening only')
    module = importlib.import_module('configs.listener')
    main = module.Main()

else:
    module = importlib.import_module('configs.' + active_config)
    main = module.Main()
    main.set_monitors() # Comment this line if not needed

