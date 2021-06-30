from subprocess import run, PIPE
from os.path import exists
from os import access, X_OK
from sys import version_info, exit
from udi import ask_choice

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
  icewm = dict(
    packages2install = ["icewm"],
    packages2remove = ["icewm", "icewm-common"],
    xstartup = """
#!/bin/bash
xrdb $HOME/.Xresources
icewm-session &
    """.strip()
  ),
  xfce = dict(
    packages2install = ["xfce4", "xfce4-terminal"],
    packages2remove = ["xfce4", "xfce4-terminal"],
    xstartup = """
#!/bin/sh
xrdb $HOME/.Xresources
startxfce4 &
    """.strip()
  ),
  lxde = dict(
    packages2install = ["lxde"],
    packages2remove = ["lxde"],
    xstartup = """
#!/bin/sh
xrdb $HOME/.Xresources
/usr/bin/startlxde &
    """.strip()
  )
  # Awesome WM commented as it failed to launch at least on ARMHF CPU on Debian, Ubuntu
  # Successfull launch was only on Kali
#   awesome = dict(
#     packages2install = ["awesome"],
#     packages2remove = ["awesome"],
#     xstartup = """
# #!/bin/bash
# xrdb $HOME/.Xresources
# awesome &
#     """.strip()
#   )
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

def detect_all_installed():
  # Returning list of all detected desktops. 
  detected_desktops = []
  for name,desktop in supported.items():
    if detected(desktop["packages2install"][0]):
      detected_desktops.append(name)
  return detected_desktops

def switch(de_id, interact):
  if not interact:
    if detected(de_id):
      change_xstartup(supported[de_id]["xstartup"])
    else:
      print(f"Looks like {de_id} is not installed in your system yet.")
      exit()
  else:
    print("Detecting installed desktops...")
    detected_desktops = detect_all_installed()
    print("Finally detected:")
    for i in range(0,len(detected_desktops)):
      print(f"{ i+1 }) { detected_desktops[i] }")
    target = ask_choice("Number of item or 0 to cancel: ",0,len(detected_desktops))
    if target == 0:
      return
    change_xstartup(supported[detected_desktops[target - 1]]["xstartup"])

def add(de_id,interact):
  if interact:
    installed = detect_all_installed()
    print("\nAlready installed:")
    available = []
    if len(installed) == 0:
      print("- None")
      for de in supported.keys():
        available.append(de)
    else:
      for de in installed:
        print(f"- { de }")
      for de in supported.keys():
        if de not in installed:
          available.append(de)
    print("\nAvailable to install:")
    for i in range(0,len(available)):
      print(f"{ i+1 }) { available[i] }")
    target = ask_choice("Number of item or 0 to cancel: ",0,len(available))
    if target == 0:
      return
    de_id = available[target - 1]
  if not detected(de_id):
    print(f"""
    
    Installing packages for {de_id}...

    WARNING: At the next step script will run next commands for {de_id} packages:
    "sudo apt install" for each main package related to {de_id}

    """)
    canceled = False
    install = "sudo apt install "
    if not interact:
      install += "-y "
    for pkg in supported[de_id]["packages2install"]:
      info = shell(install + pkg)
      if info.returncode == 1:
        canceled = True
        break
    if not canceled:
      change_xstartup(supported[de_id]["xstartup"])
      print(f"\n\n {de_id} desktop/window manager should be installed now. Stop your UserLAnd session and change it's protocol from SSH to VNC!")
    else:
      print(f"You canceled uninstallation of {de_id}")
  else:
    print(f"Looks like packages for {de_id} is already installed!")

def remove(de_id, interact):
  if interact:
    installed = detect_all_installed()
    print("Already installed:")
    if len(installed) == 0:
      print("- None")
      return
    else:
      for i in range(0,len(installed)):
        print(f"{ i+1 }) { installed[i] }")
      target = ask_choice("Number of item or 0 to cancel: ",0,len(installed))
      if target == 0:
        return
      de_id = installed[target - 1]
  if detected(de_id):
    print(f"""
    
    Removing main packages of {de_id}...

    WARNING: At the next step script will run next commands for {de_id} packages:
    "sudo apt purge" for each main package
    "sudo apt autoremove -y" after removing main packages to remove also autoinstalled

    """)
    purge = "sudo apt purge "
    if not interact:
      purge += "-y "
    canceled = False
    for pkg in supported[de_id]["packages2remove"]:
      info = shell(purge + pkg)
      if info.returncode == 1:
        canceled = True
        break
    if not canceled:
      shell("sudo apt autoremove -y")
      print(f"\n\nAll packages related to {de_id} should be removed for now. Restart your UserLAnd session before installing another one desktop!")
    else:
      print(f"You canceled uninstallation of {de_id}")
  else:
    print(f"Package {de_id} is not installed! Nothing to remove!")

# TODO: detect package manager (apt/apk/pacman) to add support of other containers
# TODO: Need to think about ~/.vncrc to control resolution for vnc sessions