import subprocess
import json
import os
import time
import threading
from libs.Log import logger

class Command():

    def __init__(self):
        pass

    def get_all_monitors(self):
        monitors = self.hyprctl_command("monitors")
        return monitors
    
    def get_monitor(self, name = None, description = None, make = None, model = None):
        monitors = self.get_all_monitors()

        for monitor in monitors:
            if name is not None:
                if name in monitor['name']:
                    return monitor

            if description is not None:
                if description in monitor['description']:
                    return monitor

            if make is not None:
                if make in monitor['make']:
                    return monitor

            if model is not None:
                if model in monitor['model']:
                    return monitor
        return None

    def hyprctl_command(self, command):
        cmd = "hyprctl -j " + command
        logger.info("Executing command: "+cmd) 
        output = subprocess.check_output(cmd, shell=True)
        decoded_output = output.decode("utf-8")
        
        try:
            json_output = json.loads(decoded_output)
        except json.decoder.JSONDecodeError as e:
            return decoded_output
        return json_output
    
    def shell_command(self, command):
        command = command.strip()
        if command.endswith('&'):
            command = command[:-1]
            logger.info("Executing background command: "+command)
            with open(os.devnull, 'w') as fp:
                subprocess.Popen(command, shell=True, stdout=fp)
        else:
            logger.info("Executing command: "+command) 
            output = subprocess.check_output(command, shell=True)
            decoded_output = output.decode("utf-8")
            return decoded_output


