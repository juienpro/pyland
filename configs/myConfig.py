import libs.Command as Command 
import libs.Daemon as Daemon
from libs.Log import logger

class Main():

    def __init__(self):
        self.command = Command.Command()
        self.daemon = Daemon.Daemon(self, ['hyprland', 'idle', 'systemd'])

    def on_hyprland_event(self, event, argument):
        if event in [ "monitoradded", "monitorremoved" ]:
            logger.info('Handling hyprland event: ' + event)
            self.set_monitors()
        
    def on_idle(self, time_elapsed):
        step = 0
        if time_elapsed < 150 and step != 0:
            if step == 1:
                self.command.shell_command("brightnessctl -r")
            elif step == 3:
                self.command.hyprctl_command("dispatch dpms on")
            step = 0

        if time_elapsed >= 150 and step == 0:
            step = 1
            self.command.shell_command("brightnessctl -s set 0")

        if time_elapsed > 600 and step != 2:
            step = 2
            self.command.shell_command("loginctl lock-session")

        if time_elapsed > 720 and step != 3:
            step = 3
            self.command.hyprctl_command("dispatch dpms off")
            
        
    def set_monitors(self):
        logger.info('Setting monitors')
        if self.command.get_monitor(description="HP 22es") is not None:
            self.command.hyprctl_command('keyword monitor "eDP-1,disable"')
        else:
            self.command.hyprctl_command('keyword monitor "eDP-1,preferred,auto,2"')
            self.command.shell_command("brightnessctl -s set 0")
