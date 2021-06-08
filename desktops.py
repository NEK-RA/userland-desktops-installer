from subprocess import run

def shell(cmd,capture=False):
  # by default capture=False to provide shell("command") which will print ot stdout result of execution
  out = run(cmd, shell=True, capture_output=capture)
  if capture:
    # Not sure if it will work as expected
    # Expected that if stdout is empty then stderr shouln't be empty
    # So if stdout is empty, then stderr should be printed and vice-versa
    return out.stdout.decode("utf-8") or out.stderr.decode("utf-8")
  else:
    return out

supported = dict(
  # ~2MB total space usage
  twm = dict(
    packages2install = ["twm"],
    packages2remove = ["twm"],
    xstartup = """
    #!/bin/sh
    xrdb $HOME/.Xresources
    xsetroot -solid grey
    #x-terminal-emulator -geometry 80x24+10+10 -ls -title "$VNCDESKTOP Desktop" &
    #x-window-manager &
    # Fix to make GNOME work
    export XKL_XMODMAP_DISABLE=1
    /etc/X11/Xsession
    """
  ),
  # ~30MB total space usage
  icewm = dict(
    packages2install = ["icewm","xfe"],
    # not sure if packages2remove will be realy needed, or all other packages (like icewm-common) will be uninstalled on "apt autoremove"
    packages2remove = ["icewm", "icewm-common","xfe"],
    xstartup = """
    #!/bin/bash
    xrdb $HOME/.Xresources
    icewm-session &
    """
  )

)

def add(id):
  # TODO: Add selected de/wm if it's supported
  # TODO: Detect if it already installed
  if not detected(id):
    print("Adding " + id + "...")
  else:
    print("Package "+str(id) + " is already installed! Skipping")


def remove(id):
  # TODO: Remove selected de/wm if it's supported
  # TODO: Detect if it realy installer before removing
  if detected(id):
    print(f"""
    
    Removing main packages of {id}...

    WARNING: At the next step script will run next commands for {id} packages:
    "sudo apt purge" for each main package
    "sudo apt autoremove -y" after removing main packages to remove also autoinstalled

    You will be asked for sudo password!

    """)
    canceled = False
    for pkg in supported[id]["packages2install"]:
      info = shell("sudo apt purge "+pkg)
      if info.returncode == 1:
        canceled = True
        break
    if not canceled:
      shell("sudo apt autoremove -y")
      print(f"\n\n All packages related to {id} should be removed for now. Restart your UserLAnd session before installing another one desktop!")
    else:
      print(f"You canceled uninstallation of {id}")
  else:
    print(f"Package {id} is not installed! Nothing to remove!")

def detected(package):
  # Searching on debian based systems through dpkg. 
  # Packages installed with "apt install package-name" are listed as "ii  package-name" and some additional info in table-like interface
  # If I need exactly "package-name" whithout anything like "lib-something-package-name" or "package-name-plugin" and etc. (including substrings from description)
  # I'm searching exactly "^ii  package-name " which searchs from the line's start 
  # providing few symbols expected for line's start, then 2 spaces, then package name and finally one space to find exactly package-name
  found_package = shell("dpkg -l | grep \"^ii  "+str(package)+" \"",True)
  # If required package not found then empty string (0 length) will be received, otherwise required package found
  # TODO: probably it's better to return len(found_package) instead of checking it inside function and return true/false?
  if len(found_package) == 0:
    return False
  else:
    return True