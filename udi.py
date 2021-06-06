from os import system
from sys import argv
import texts

# Flags section
flags = dict ( 
  SHOW_DISCLAIMER = True,
  INTERACTIVE = True,
  HELP = False,
  VERSION = False,
  LIST_DEWM = False,
  ADD = False,
  ADD_ID = "",
  REMOVE = False,
  REMOVE_ID = "",
  ERROR = False,
  ERROR_MSG = ""
)

arg_list = ("-r","--remove","-a","--add","-l","--list","-h","--help","-v","--version","-d","--disclaimer")

def get_flags():
  # Enabling global variables
  global flags
  # Removing scriptname from list
  argv.pop(0)

  if len(argv) > 0:
    while len(argv) > 0:
      # Getting first element of list
      arg = argv.pop(0)
      
      # If asked to print version
      if arg=="-v" or arg=="--version":
        flags["VERSION"] = True
        break
      
      # If asked to print help
      if arg == "-h" or arg == "--help":
        flags["HELP"] = True
        break

      # If asked to print list of supported desktops and window managers
      if arg == "-l" or arg == "--list":
        flags["LIST_DEWM"] = True
        break

      # If asked to not show disclaimer. Acceptable both for interactive and non-interactive modes
      if arg == "-d" or arg == "--disclaimer":
        flags["SHOW_DISCLAIMER"] = False
        print("Disclaimer disabled for this run. If you want to see disclaimer, don't use -d or --disclaimer option")
      
      # If asked to remove old de/wm
      if arg == "-r" or arg == "--remove":
        flags["REMOVE"] = True
        remove_id = argv.pop(0)
        if remove_id not in arg_list:
          flags["REMOVE_ID"] = remove_id
          flags["INTERACTIVE"] = False
        else:
          flags["ERROR"] = True
          flags["ERROR_MSG"] = "Another option specified, but name of desktop environment or window manager expected. Check what's going after -r or --remove option"

      # If asked to add new de/wm
      if arg == "-a" or arg == "--add":
        flags["ADD"] = True
        add_id = argv.pop(0)
        if add_id not in arg_list:
          flags["ADD_ID"] = add_id
          flags["INTERACTIVE"] = False
        else:
          flags["ERROR"] = True
          flags["ERROR_MSG"] = "Another option specified, but name of desktop environment or window manager expected. Check what's going after -a or --add"

def chose_variant():
  chosen = input("Type number of your choice")
  print(chosen)

def run_interactive():
  print(texts.menu)

def run():
  global flags
  
  # If got errors in --add or --remove options
  if(flags["ERROR"]):
    print(flags["ERROR_MSG"])
    exit()
  
  # If user checking version of script
  if(flags["VERSION"]):
    print(texts.version)
    exit()
  
  # If user looks for usage help
  if(flags["HELP"]):
    print(texts.usage)
    exit()

  # If user looks for supported desktops
  if(flags["LIST_DEWM"]):
    print(texts.supported_de_wm)
    exit()
  
  # If using script interactive
  if(flags["INTERACTIVE"]):
    run_interactive()
  else:
    if(flags["REMOVE"]):
      print("User wants to remove de/wm with id: "+flags["REMOVE_ID"])
      # TODO: Check if remove_id exists in supported list
      # TODO: Handle error if remove_id doesn't supported
      # TODO: Remove selected de/wm if it's supported
      # TODO: Detect if it realy installer before removing
    
    if(flags["ADD"]):
      print("User want to add de/wm with id: "+flags["ADD_ID"])
      # TODO: Check if add_id exists in supported list
      # TODO: Handle error if add_id doesn't supported
      # TODO: Add selected de/wm if it's supported
      # TODO: Detect if it already installed


get_flags()
run()