import libs.Command as Command 
import libs.Daemon as Daemon
from libs.Log import logger

class Main():

    def __init__(self):
        self.command = Command.Command()
        self.daemon = Daemon.Daemon(self, ['hyprland', 'idle', 'systemd'])
        self.step = 0

    def on_hyprland_event(self, event, argument):
        if event in [ "monitoradded", "monitorremoved" ]:
            logger.info('Handling hyprland event: ' + event)
            self.set_monitors()
        
    def on_idle(self, time_elapsed):
        if time_elapsed < 150 and self.step != 0:
            if self.step == 1:
                self.command.shell_command("brightnessctl -r")
            elif self.step == 3:
                self.command.hyprctl_command("dispatch dpms on")
            step = 0

        if time_elapsed >= 150 and self.step == 0:
            self.step = 1
            self.command.shell_command("brightnessctl -s set 0")

        if time_elapsed > 600 and self.step != 2:
            self.step = 2
            self.command.shell_command("loginctl lock-session")

        if time_elapsed > 720 and self.step != 3:
            self.step = 3
            self.command.hyprctl_command("dispatch dpms off")
            
        
    def set_monitors(self):
        logger.info('Setting monitors')
        if self.command.get_monitor(description="HP 22es") is not None:
            self.command.hyprctl_command('keyword monitor "eDP-1,disable"')
        else:
            self.command.hyprctl_command('keyword monitor "eDP-1,preferred,auto,2"')
            self.command.shell_command("brightnessctl -s set 0")
