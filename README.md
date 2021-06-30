# userland-desktops-installer

Simple script which will bring more desktop environments to UserLAnd from AnLinux

P.S.: Currently for Debian-based UserLAnd distros only, testing in Ubuntu UserLAnd

## Intro

I guess most of us knows about Termux ([Github](https://github.com/termux/termux-app), [F-Droid](https://f-droid.org/ru/packages/com.termux/), [Google Play](https://play.google.com/store/apps/details?id=com.termux))

Most of us tried some Unix tools including some that doesn't works in Termux. I'm not sure if all of us also tried to run minimalistic linux containers here, but I guess again that most of us tried them thanks to AnLinux ([Github](https://github.com/EXALAB/AnLinux-Adfree), [F-Droid](https://f-droid.org/ru/packages/exa.lnx.a/), [Google Play](https://play.google.com/store/apps/details?id=exa.lnx.a)) Finally (as I guess) [@CypherpunkArmory](https://github.com/CypherpunkArmory) decided that it's not comfortable always switch between two apps and created UserLand ([Github](https://github.com/CypherpunkArmory/UserLAnd), [F-Droid](https://f-droid.org/ru/packages/tech.ula/), [Google Play](https://play.google.com/store/apps/details?id=tech.ula))

P.S.: I don't realy know what was the reason of UserLand creation. Writen above is just how I see that :D

## Problem

Currently **UserLand** provide ability to install containers with

- Alpine
- Arch
- Debian
- Kali
- Ubuntu

Also provided some "Apps" options like installing LXDE/Xfce, Firefox, GIMP, InkScape and etc. But all of them will be installed in Debian container and you can't select base container for software installation.

That's not the problem for software like browsers and etc, because:

1. They can be installed easily from terminal
2. Each base container packed with preinstalled TightVNC and TWM([Tab Window Manager](https://en.wikipedia.org/wiki/Twm)) and they will be displayed normally

But the changing the Desktop Environment is "more advanced" task for simple users. Also UserLand provides only LXDE and Xfce, while from AnLinux scripts we can get also Mate, LXQt, IceWM and Awesome.

## About this repo

I will try to create script (or probably few scripts) on Python to simplify switching desktop environments inside UserLand on base of AnLinux scripts.

Why python? I guess it will be more comfortable than bash for big script.

Why not android-code? I don't have android development expirience yet, so script will be faster and more flexible.

## Targets

- [x] Make script usable for Debian-based distros (Debian, Kali, Ubuntu and any other if such will be ever added)
Currently only Debian-based are supported because of direct usage of `apt`

- [x] Make non-interactive mode
Options for non-interactive usage are: add, switch and remove desktop

- [ ] Make interactive mode
- [ ] Add support of Arch-based
- [ ] Add support of Alpine

## Planned usage options

- `-a`, `-add` - Add new desktop environment or window manager. Option just for non-interactive mode. Require also target name of DE/WM to add.
Example: `python udi.py --add xfce`

- `-r`, `--remove` - Remove any desktop environment or window manager. Option just for non-interactive mode. Require also target name of DE/WM to remove.
Example: `python udi.py --remove twm`

- `-s`, `--switch` - Switch xstartup file content to content specific for another desktop. For thoose who will keep few desktops installed and want a way to easily switch them.

- `-h`, `--help` - Print usage help with description and all options

- `-l`, `--list` - Print info about desktop environments and window managers which are planned and implemented

- `-d`, `--disclaimer` - Disable disclaimer in current running. By default disclaimer will be shown on each running.

- `-v`, `--version` - Show script version
