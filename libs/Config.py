import libs.Command as Command 
import libs.Daemon as Daemon
from libs.Log import logger

class Config:
    def __init__(self):
        self.timeouts = [] 
        if callable(getattr(self, 'set_idle_config', None)):
            self.set_idle_config()

        self.current_timeout_commands = []
        self.current_resume_commands = []

        self.command = Command.Command()
        self.daemon = Daemon.Daemon(self, ['hyprland', 'idle', 'systemd'])
    
    def add_timeout(self, timeout, timeout_commands, resume_commands = []):
        self.timeouts.append([timeout, timeout_commands, resume_commands])
    
    def exec_timeout_command(self, command):
        if command.startswith('hyprctl'):
            command = command.replace('hyprctl', '')
            self.command.hyprctl_command(command) 
        else:
            self.command.shell_command(command)

    def do_idle_with_config(self, time_elapsed):
        if time_elapsed < 5:
            for resume_command in self.current_resume_commands:
                logger.info('Idling at ' + str(time_elapsed) + ' - Resuming with command: "' + resume_command + '"')
                self.exec_timeout_command(resume_command)
                self.current_resume_commands = []
                self.current_timeout_commands = []
        
        for timeout in self.timeouts:
            if time_elapsed >= timeout[0]:
                for timeout_command in timeout[1]:
                    if timeout_command not in self.current_timeout_commands:
                        logger.info('Idling at ' + str(time_elapsed) + ' - Timeout with command: "' + timeout_command + '"')
                        self.current_timeout_commands.append(timeout_command)
                        self.exec_timeout_command(timeout_command)

                for resume_command in timeout[2]:
                    if resume_command not in self.current_resume_commands:
                        self.current_resume_commands.append(resume_command)
