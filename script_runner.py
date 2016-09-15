#!/usr/bin/python

import argparse

#argparse
parser = argparse.ArgumentParser()
parser.add_argument('-p', help = "Port number", action="store", dest="p", required = True)
args = parser.parse_args()

from script_runner_src import *

port = args.p

run(host='172.16.1.254', port=port, debug=True)