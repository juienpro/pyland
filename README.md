# Pyland

**Pyland** is a customizable event-driven Python listener for Hyprland. It currently supports three listeners:

- [Hyprland IPC](https://wiki.hyprland.org/IPC/) event list
- [Systemd Logind](https://wiki.hyprland.org/IPC/) signals
- A custom Idle function that allows you to know since how many seconds there was no activity

The tool allows to listen for these events and to execute commands (Shell or hyprctl commands) in response.


## Why this tool? 

Good question.

Initially, I was a bit stressed by the number of tools needed with Hyprland (Kanshi & hypridle notably), and also by the number of bugs despite the awesome efforts of the developers. 

I wanted to have a deeper control on my system, and to be able to script it as I wanted. 

To give an example, my laptop screen brightness was always at 100% when I undock it, and Kanshi does not allow to add shell commands. This is only one small example of the numerous limitations I met during my setup of Hyprland.

By scripting my Desktop in Python, I feel I have more control to implement what I want.

## Installation

This program needs the following tools: 
- Python3 with the following modules: argparse, importlib, logging, subprocess, threading
- The `socat` binary ([Arch](https://archlinux.org/packages/extra/x86_64/socat/))
- The `dbus-monitor` binary ([Arch](https://archlinux.org/packages/core/x86_64/dbus/))

## How to use

There are two configurations: a dummy one just to listen and print all events, and my configuration ;-) 
These configurations are located in the `configs` folder. Each file has a class called `Main` where you define what you want to listen and what you want to do. 

Read both files to understand how it works. 

If you type `./pyland.py -l`, Pyland will be launched with the dummy configuration. Otherwise, it will be launched with the configuration mentioned at the top of the `pyland.py` file.

### Available listeners

| Sender            | Handler method to add to your class | Arguments                               |
|-------------------|-------------------------------------|---------------------------------------- |
| Hyprland          | on_hyprland_event                   | event, arguement                        |
| Systemd Logind    | on_systemd_event                    | interface, member                       |
| Systemd Logind     | on_[Member]                         | None                                    |
| Pyland            | on_idle                             | Number of seconds since the last Hyprland event |


#### Hyprland events 

They are well documented [here](https://wiki.hyprland.org/IPC/). 

#### Systemd Logind events

These events are called "signals" in the Systemd terminology. The `interface` is the sender and the `member` is the payload.

They are not well documented but you can try to [read that](https://www.freedesktop.org/software/systemd/man/latest/org.freedesktop.login1.html) (good luck). 

Some examples that can be useful:

| Member | Description  |
|------- |-------------------------------------------------------------------|
| PrepareForShutdown | Sent before a shutdown |
| Lock | Sent when a lock is requested, eg `loginctrl lock-session` |
| Unlock | Sent when an unlock is requested | 
| SessionNew | When a session is created |

And probably others but I am not an expert of Systemd (yet!). I need to do some tests.

#### Idle event

This is a simple idle method that compute the number of seconds elapsed since the last hyprland activity sent through IPC. 

It's a workaround: if you launch a text editor and type in this editor without changing any focus, the timer will be increased without being reset to 0.

For my usage, it's enough, but for a real idling program, use `hypridle`.

### Available helpers

There are two main helpers:

- `hyprctl_command` to send a command with hyprctl and to get the result in JSON
- `shell_command` to send a shell command and returns the result

See the file `libs/Command.py` for more information.


## Contributions

- I don't have enough knowledge to know how to connect to the Wayland API from Python, to interact directly with `wlroots` protocols. It would be a nice addition
- Integrating other DBUS services should be easy with Pyland (type `dbusctl` to list all avalable DBUS on your system).

If you see some bugs or propose patches, feel free to contribute.


## Thanks

Thanks to the developer(s) of [Hyprland](https://hyprland.org) for their fantastic compositor. I tried so many ones in the past, and this has been Hyprland that convinced me to do the switch from KDE :-)




