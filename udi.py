from sys import argv, exit
import texts
import desktops

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
  SWITCH = False,
  SWITCH_ID = "",
  ERROR = False,
  ERROR_MSG = ""
)

arg_list = ("-r","--remove","-a","--add","-l","--list","-h","--help","-v","--version","-d","--disclaimer","-s","--switch")

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

      # If asked to switch xstartup content to another one related to provided desktop
      if arg == "-s" or arg == "--switch":
        flags["SWITCH"] = True
        switch_id = argv.pop(0)
        if switch_id not in arg_list:
          flags["SWITCH_ID"] = switch_id
          flags["INTERACTIVE"] = False
        else:
          flags["ERROR"] = True
          flags["ERROR_MSG"] = "Another option specified, but name of desktop environment or window manager expected. Check what's going after -s or --switch option"
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

def throw_error():
  # According to https://docs.python.org/3/library/sys.html#sys.exit
  # > The standard way to exit is sys.exit(n)
  # > The optional argument arg can be an integer giving the exit status (defaulting to zero), or another type of object.
  # > ... and any other object is printed to stderr and results in an exit code of 1
  # Imported exit from sys
  exit(flags["ERROR_MSG"])

def chose_variant():
  chosen = input("Type number of your choice")
  print(chosen)

def run_interactive():
  print(texts.menu)

def run():
  global flags
  
  # If got errors in --add or --remove options
  if(flags["ERROR"]):
    throw_error()
  
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
    if flags["SWITCH"]:
      if flags["SWITCH_ID"] in desktops.supported.keys():
        print("Switching xstartup content to " + flags["REMOVE_ID"])
        desktops.switch(flags["SWITCH_ID"])
      else:
        flags["ERROR_MSG"] = f"Desktop  { flags['SWITCH_ID'] }  is NOT supported! Please run script with --list option to see all supported desktops"
        throw_error()

    if(flags["REMOVE"]):
      print(f"Removing de/wm with id: { flags['REMOVE_ID'] }")
      if flags["REMOVE_ID"] in desktops.supported.keys():
        desktops.remove(flags["REMOVE_ID"],False)
      else:
        flags["ERROR_MSG"] = f"Desktop { flags['REMOVE_ID'] } is NOT supported! Please run script with --list option to see all supported desktops"
        throw_error()
    
    if(flags["ADD"]):
      print(f"Adding de/wm with id: { flags['ADD_ID'] }")
      if flags["ADD_ID"] in desktops.supported.keys():
        desktops.add(flags["ADD_ID"],False)
      else:
        flags["ERROR_MSG"] = f"Desktop { flags['ADD_ID'] } is NOT supported! Please run script with --list option to see all supported desktops"
        throw_error()

get_flags()
run()