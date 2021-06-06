supported = dict(

  twm = dict(
    packages = ("twm"),
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

  icewm = dict(
    packages = ("icewm","xfe"),
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
  # detect(id)
  print("Adding " + id + "...")

def remove(id):
  # TODO: Remove selected de/wm if it's supported
  # TODO: Detect if it realy installer before removing
  # detect(id)
  print("Removing " + id + "...")

def detect(id):
  print("Detecting " + id)