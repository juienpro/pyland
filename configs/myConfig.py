from libs.Log import logger
from libs.Config import Config

class Main(Config):

    def on_hyprland_event(self, event, argument):
        if event in [ "monitoradded", "monitorremoved" ]:
            logger.info('Handling hyprland event: ' + event)
            self.set_monitors()
    
    def set_idle_config(self):
        self.add_timeout(150, ['brightnessctl -s set 0'], ['brightnessctl -r'])
        self.add_timeout(600, ['hyprlock &'])
        self.add_timeout(720, ['hyprctl dispatch dpms off'], ['hyprctl dispatch dpms on'])

    def on_idle(self, time_elapsed):
        logger.info(time_elapsed)
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
