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
