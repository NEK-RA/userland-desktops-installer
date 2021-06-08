version = "0.0" # SCRIPT VERSION: {VERSION}
disclaimer= """
  ########################
  ##\t DISCLAIMER \t##
  ########################

  This script officially published at:
  https://github.com/NEK-RA/userland-desktops-installer

  Short link:
  https://git.io/JZOqe

  If you got it from any other source - use it on your own risk. (or remove and get from official repository)
  
  
  #############
  ## WARNING ##
  #############
  
  This script will use few system commands with SUDO. Especially for remove default TWM and to install packages with new desktop environment or window manager.
  Script will directly run commands like "sudo apt ...", so if you don't believe to this script, you can open it with any text editor and search for "sudo"
  
  """

menu = f"""
UDI(userland-desktops-installer) version: {version}
Available options:
1) Remove old DE/WM
2) Install new DE/WM
3) Display help
4) Exit
"""

usage = """
NAME
        UDI - UserLAnd Desktops Installer
        Official repo: https://github.com/NEK-RA/userland-desktops-installer

SYNOPSIS
        python3 udi.py [OPTIONS]

DESCRIPTION
        Script for removing and installation of desktop environments (or windows managers) inside of UserLAnd containers on Android.
        Not usable inside Termux yet (in plans)
        By default script will always run in interactive mode, showing disclaimer, menu and waiting for user's input.
        But there is two options to run in non-interactive mode.
        
        NOT FOR USAGE WITH DESKTOP OR SERVERS NOW

OPTIONS
        -a, --add           Add new desktop environment (or window manager) and use it for vnc sessions.
                            Option for non-interactive usage. Should be used with one of the names listed by --list option

        -d, --disclaimer    Don't show the disclaimer while running script

        -h, --help          Display this help message

        -l, --list          List of supported desktop environments and window managers.
                            Currently supported only few options from AnLinux (look for readme inside github repo)

        -r, --remove        Remove existing desktop environment or window manager
                            Option for non-interactive usage. Should be used with one of the names listed by --list option

        -v, --version       Show script version
"""

supported_de_wm = """
Supported by UserLAnd-desktops-installer:
        NONE

By default in UserLAnd:
        TWM

Planned - supported desktop environments and window managers by AnLinux:
        Debian-based:
                - Xfce4 (Recommended in AnLinux app)
                - MATE
                - LXQt
                - LXDE
                - Awesome
                - IceWM
        Arch:
                - LXDE
        Alpine:
                none
"""