from libs.Log import logger
from libs.Config import Config

class Main(Config):
    def on_hyprland_event(self, event, argument):
        logger.info("Hyprland: Receveived '"+event +"' with argument "+argument.strip())        
    
    
    def on_idle(self, time_elapsed):
        logger.info('Current idle time (sec): '+ str(time_elapsed))


    def on_systemd_event(self, sender, signal, payload):
        logger.info("Systemd: Receveived from '"+sender+"': "+ signal +' with payload: '+payload)


