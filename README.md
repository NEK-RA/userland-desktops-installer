# userland-desktops-installer

Simple script which will bring more desktop environments to UserLAnd from AnLinux

## Intro

I guess most of us knows about Termux ([F-Droid](https://f-droid.org/ru/packages/com.termux/), [Google Play](https://play.google.com/store/apps/details?id=com.termux))

Most of us tried some Unix tools including some that doesn't works in Termux. I'm not sure if all of us also tried to run minimalistic linux containers here, but I guess again that most of us tried it thanks to AnLinux ([F-Droid](https://f-droid.org/ru/packages/exa.lnx.a/), [Google Play](https://play.google.com/store/apps/details?id=exa.lnx.a)) Finally someone([@CypherpunkArmory](https://github.com/CypherpunkArmory)) decided that it's not comfortable always switch between to apps is not comfortable and created UserLand ([F-Droid](https://f-droid.org/ru/packages/tech.ula/), [Google Play](https://play.google.com/store/apps/details?id=tech.ula))

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
2. Each base container packed with preinstalled TightVNC and TWM([Tab Window Manager](https://en.wikipedia.org/wiki/Twm))

But the changing the Desktop Environment is "more advanced" task for simple users. Also UserLand provides only LXDE and Xfce, while from AnLinux scripts we can get also Mate, LXQt, IceWM and Awesome.

## About this repo

I will try to create script (or probably few scripts) on Python to simplify switching desktop environments inside UserLand on base of AnLinux scripts.

Why python? I guess it will be more comfortable than bash for big script.

Why not android-code? I don't have android development expirience yet, so script will be faster and more flexible.

## Targets

- [ ] Make script usable for Debian-based distros (Debian, Kali, Ubuntu and any other if such will be ever added)
- [ ] Add support of Arch-based
- [ ] Add support of Alpine
