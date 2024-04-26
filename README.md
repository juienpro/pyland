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
- The `gdbus` binary ([Arch](https://archlinux.org/packages/core/x86_64/glib2/))

## How to use

There are two configurations: a dummy one just to listen and print all events, and my configuration ;-) 
These configurations are located in the `configs` folder. Each file has a class called `Main` where you define what you want to listen and what you want to do. 

Read both files to understand how it works. 

If you type `./pyland.py -l`, Pyland will be launched with the dummy configuration. Otherwise, it will be launched with the configuration mentioned at the top of the `pyland.py` file.

### Simplest configuration 

```
from libs.Log import logger
from libs.Config import Config

class Main(Config):
    def on_hyprland_event(self, event, argument):
        logger.info("Hyprland: Receveived '"+event +"' with argument "+argument.strip())        
    
    def on_idle(self, time_elapsed):
        logger.info('Current idle time (sec): '+ str(time_elapsed))

    def on_systemd_event(self, sender, signal, payload):
        logger.info("Systemd: Receveived from '"+sender+"': "+ signal +' with payload: '+payload)

```

### Real configuration

```
from libs.Log import logger
from libs.Config import Config

class Main(Config):

    def on_hyprland_event(self, event, argument):
        if event in [ "monitoradded", "monitorremoved" ]:
            logger.info('Handling hyprland event: ' + event)
            self.set_monitors()
   
    
    def set_idle_config(self):
        self.add_timeout(10, ['brightnessctl -s set 0'], ['brightnessctl -r'])
        self.add_timeout(20, ['hyprlock'])
        self.add_timeout(720, ['hyprctl dispatch dpms off'], ['hyprctl dispatch dpms on'])


    def on_idle(self, time_elapsed):
        self.do_idle_with_config(time_elapsed)

    def on_PrepareForSleep(self, payload):
        if 'true' in payload:
            logger.info("Locking the screen before suspend")
            self.command.shell_command("hyprlock")

    def set_monitors(self):
        logger.info('Setting monitors')
        if self.command.get_monitor(description="HP 22es") is not None:
            self.command.hyprctl_command('keyword monitor "eDP-1,disable"')
        else:
            self.command.hyprctl_command('keyword monitor "eDP-1,preferred,auto,2"')
            self.command.shell_command("brightnessctl -s set 0")
```

### Available listeners

| Sender            | Handler method to add to your class | Arguments                               |
|-------------------|-------------------------------------|---------------------------------------- |
| Hyprland          | on_hyprland_event                   | event, arguement                        |
| Systemd Logind    | on_systemd_event                    | sender, signal, payload                       |
| Systemd Logind     | on_[signal]                         | payload                                    |
| Pyland            | on_idle                             | Number of seconds since the last Hyprland event |


#### Hyprland events 

They are well documented [here](https://wiki.hyprland.org/IPC/). 

#### Systemd Logind events

These events are called "signals" in the Systemd terminology. 

They are not well documented but you can try to [read that](https://www.freedesktop.org/software/systemd/man/latest/org.freedesktop.login1.html) (good luck). 

The best way to implement what you want is to do first a `pyland.py -l` so you will get a dump of all signals received.

Some examples that can be useful:

| Member | Description  |
|------- |-------------------------------------------------------------------|
| PrepareForShutdown | Sent before a shutdown |
| PrepareForSleep | Sent before suspend |
| Lock | Sent when a lock is requested, eg `loginctrl lock-session` |
| Unlock | Sent when an unlock is requested | 
| SessionNew | When a session is created |

And probably others but I am not an expert of Systemd (yet!). I need to do some tests.

To see an example on how to lock your screen before suspend, check the `myConfig.py` file:

```
def on_PrepareForSleep(self, payload):
    if 'true' in payload:
        logger.info("Locking the screen before suspend")
        self.command.shell_command("hyprlock")
```
Yes, it's literally 4 lines to add to your class!

#### Idle event

This is a simple idle method that compute the number of seconds elapsed since the last hyprland activity sent through IPC. 

It's a workaround: if you launch a text editor and type in this editor without changing any focus, the timer will be increased without being reset to 0.

For my usage, it's enough, but for a real idling program, use `hypridle`.

To use it, you have two choices:
- Setting up an `on_idle` hook. This method takes the elapsed time as the argument. Then you are free to implement your workflow in this method.
- Use `set_idle_config` and `on_idle`, which is much easier as it will compute everything for you. 

```
def set_idle_config(self):
    self.add_timeout(10, ['brightnessctl -s set 0'], ['brightnessctl -r'])
    self.add_timeout(20, ['hyprlock &'])
    self.add_timeout(720, ['hyprctl dispatch dpms off'], ['hyprctl dispatch dpms on'])

def on_idle(self, time_elapsed):
    self.do_idle_with_config(time_elapsed)

```
You can add unlimited "timeouts" with `self.add_timeout`. This method takes three parameters:

- The timeout in itself (10 seconds, 20 seconds, 720 seconds respectively)
- The commands to apply when the elapsed time above the value
- The commands to apply when the elapsed time is reseted due to an activity


### Available helpers

There are two main helpers:

- `hyprctl_command` to send a command with hyprctl and to get the result in JSON
- `shell_command` to send a shell command and returns the result

Any shell command ending with '&' will be executed asynchronously. This allows to prevent any blocking thread. For instance, if you launch `hyprlock`, don't forget to add a '&' otherwise no other event can be processed anymore by Pyland.

See the file `libs/Command.py` for more information.


## Contributions

- I don't have enough knowledge to know how to connect to the Wayland API from Python, to interact directly with `wlroots` protocols. It would be a nice addition
- Integrating other DBUS services should be easy with Pyland (type `dbusctl` to list all avalable DBUS on your system).
- If someone has a solution to get the real idle time from Hyprland/Wlroots, it would be welcomed. This value is not exposed in DBUS signals.

If you see some bugs or propose patches, feel free to contribute.


## Thanks

Thanks to the developer(s) of [Hyprland](https://hyprland.org) for their fantastic compositor. I tried so many ones in the past, and this has been Hyprland that convinced me to do the switch from KDE :-)




