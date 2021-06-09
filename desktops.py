from subprocess import run
from os.path import exists
from os import access, X_OK

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
    """.strip()
  ),
  # ~30MB total space usage
  icewm = dict(
    packages2install = ["icewm","xfe"],
    packages2remove = ["icewm", "icewm-common","xfe"],
    xstartup = """
#!/bin/bash
xrdb $HOME/.Xresources
icewm-session &
    """.strip()
  )

)

def change_xstartup(content):
  print("Changing xstartup")
  # After checking that it's working fine, need to replace ./ with ~/
  home = "./"
  vnc = ".vnc/"
  xstartup = "xstartup"
  # Check if .vnc folder exists
  # It should already exist in case of UserLAnd usage
  # But it's not exist in case Termux + AnLinux
  if not exists(home+vnc):
    print("folder not found, creating")
    shell(f"mkdir {home + vnc}")
  # Check if xstartup exists
  if exists(home+vnc+xstartup):
    print("gonna change content of xstartup")
  else:
    print("gonna create xstartup")
  # Change content of xstartup
  with open(home+vnc+xstartup, mode="w") as xfile:
    xfile.write(content)
    print("File overwritten")
  # Check if file may be executed and make it executable if not
  if not access(home+vnc+xstartup, X_OK):
    shell(f"chmod +x {home+vnc+xstartup}")
  

# TODO: Need to think about ~/.vncrc to control resolution for vnc sessions

def add(id):
  # TODO: Add selected de/wm if it's supported
  # TODO: Detect if it already installed
  if not detected(id):
    print(f"""
    
    Installing packages for {id}...

    WARNING: At the next step script will run next commands for {id} packages:
    "sudo apt update" to update repos
    "sudo apt install" for each main package related to {id}

    You will be asked for sudo password!

    """)
    canceled = False
    for pkg in supported[id]["packages2install"]:
      info = shell("sudo apt install "+pkg)
      if info.returncode == 1:
        canceled = True
        break
    if not canceled:
      change_xstartup(supported[id]["xstartup"])
      print(f"\n\n {id} desktop/window manager should be installed now. Stop your UserLAnd session and change it's protocol from SSH to VNC!")
    else:
      print(f"You canceled uninstallation of {id}")
  else:
    print(f"Looks like packages for {id} is already installed!")


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
    for pkg in supported[id]["packages2remove"]:
      info = shell("sudo apt purge "+pkg)
      if info.returncode == 1:
        canceled = True
        break
    if not canceled:
      shell("sudo apt autoremove -y")
      print(f"\n\nAll packages related to {id} should be removed for now. Restart your UserLAnd session before installing another one desktop!")
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