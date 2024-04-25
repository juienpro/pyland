import libs.Daemon as Daemon
from libs.Log import logger

class Main():
    def __init__(self):
        self.daemon = Daemon.Daemon(self, ['hyprland', 'idle', 'systemd'])

    def on_hyprland_event(self, event, argument):
        logger.info("Hyprland: Receveived '"+event +"' with argument "+argument.strip())        
    
    
    def on_idle(self, time_elapsed):
        logger.info('Current idle time (sec): '+ str(time_elapsed))


    def on_systemd_event(self, interface, member):
        logger.info("Systemd: Receveived '"+member+"' from "+ interface)


