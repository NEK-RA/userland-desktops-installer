from subprocess import run, PIPE
from os.path import exists
from os import access, X_OK
from sys import version_info

def shell(cmd,capture=False):
  # by default capture=False to provide shell("command") which will print ot stdout result of execution
  if not capture:
    out = run(cmd, shell=True)
    return out
  else:
    # UserLAnd 2.7.3 ubuntu container is "Ubuntu 18.04.5 LTS"
    # In it's repos there is 3.6.9 version of Python, which doesn't have param capture_output
    # So in version 3.5-3.6 need to use subprocess.PIPE value for std(in/out/err) to capture them
    # In 3.7 already using capture_output=True
    if version_info.minor >= 7:
      out = run(cmd, shell=True, capture_output=True)
    else:
      out = run(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    # Not sure if it will work as expected
    # Expected that if stdout is empty then stderr shouln't be empty
    # So if stdout is empty, then stderr should be printed and vice-versa
    return out.stdout.decode("utf-8") or out.stderr.decode("utf-8")
      

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
  home = "/home/" + shell("whoami",True).replace("\n","") + "/"
  vnc = ".vnc/"
  xstartup = "xstartup"
  # Check if .vnc folder exists
  # It should already exist in case of UserLAnd usage
  # But it's not exist in case Termux + AnLinux
  if not exists(home+vnc):
    print("folder not found, creating")
    shell(f"mkdir -p {home + vnc}")
  if not exists( home + vnc + xstartup ):
    shell(f"touch { home + vnc + xstartup }")
  # Create (if needed) and change content of xstartup
  with open(home+vnc+xstartup, mode="w") as xfile:
    xfile.write(content)
    print("xstartup ready now!")
  # Check if file may be executed and make it executable if not
  if not access( home + vnc + xstartup, X_OK):
    shell(f"chmod +x { home + vnc + xstartup }")
  

# TODO: Need to think about ~/.vncrc to control resolution for vnc sessions

def switch(id):
  if detected(id):
    change_xstartup(supported[id]["xstartup"])
  else:
    print(f"Looks like {id} is not installed in your system yet.")
    exit()

def add(id,interact):
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
    install = "sudo apt install "
    if not interact:
      install += "-y "
    for pkg in supported[id]["packages2install"]:
      info = shell(install + pkg)
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


def remove(id, interact):
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
    purge = "sudo apt purge "
    if not interact:
      purge += "-y "
    canceled = False
    for pkg in supported[id]["packages2remove"]:
      info = shell(purge + pkg)
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