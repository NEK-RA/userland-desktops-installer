from os import system
from sys import argv
import texts

# Flags section
SHOW_DISCLAIMER = True
INTERACTIVE = True
ASKED_HELP = False
ASKED_VERSION = False

def get_flags():
  #removing scriptname from list
  argv.pop(0)

  # Check for version args:
  if ("-v" in argv) or ("--version" in argv):
    global ASKED_VERSION
    ASKED_VERSION = True

  # Check for help args
  if ("-h" in argv) or ("--help" in argv):
    global ASKED_HELP 
    ASKED_HELP = True

  # Decide what comes first in args
  if ASKED_HELP == True and ASKED_VERSION == True:
    version = -1
    try:
      version = argv.index("-v")
    except ValueError:
      version = argv.index("--version")

    usage = -1
    try:
      usage = argv.index("-h")
    except ValueError:
      usage = argv.index("--help")

    if version < usage :
      ASKED_HELP = False
    else:
      ASKED_VERSION = False

  # Check if disclaimer not needed
  if ("-d" in argv) or ("--disclaimer" in argv):
    global SHOW_DISCLAIMER
    SHOW_DISCLAIMER = False

def chose_variant():
  chosen = input("Type number of your choice")
  print(chosen)

def menu():
  print(texts.menu)

def run():
  print("Asked version:" + str(ASKED_VERSION))
  # Show script version and exit
  if(ASKED_VERSION):
    print("Script version: %s" % texts.version)
    exit()
  print("Asked help:" + str(ASKED_HELP))
  # Show usage help and exit
  if(ASKED_HELP):
    print(texts.usage)
    exit()
  


get_flags()
run()
