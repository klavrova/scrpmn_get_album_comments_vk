import configparser
import os
import sys

filename = 'config.ini'
file = os.path.join(os.path.dirname(sys.argv[0]), filename)
config = configparser.RawConfigParser()
config.read(file)
tokens = [i[1] for i in config.items('Tokens')]
