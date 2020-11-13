import subprocess
from colorama import *
import os


# FUNCTIONS
def check_error(process):
    # Print the result of a process execution
    if process.returncode == 0:
        print(Fore.GREEN + "SUCCESS!" + Fore.RESET)
    else:
        print(Fore.RED + "Error!" + Fore.RESET)


def title(title_str):
    # Prints a title in green
    print(Fore.GREEN + title_str + Fore.RESET)


def execute_command(command_list):
    # Receive the list that conforms a command and execute it
    process = subprocess.run(command_list)
    check_error(process)
    print("\n\n")


def create_desktop_executable():
    # Creates an executable file for Linux base distros.
    # For this file to work properly it must not be moved, it must be inside the OC-Manager folder
    title("CREATING DESKTOP SHORTCUT")
    path_to_oc = os.path.abspath(os.getcwd())
    path_for_exec = os.path.join(os.environ['HOME'], 'Desktop')
    f = open(path_for_exec + '/OC-Manager.desktop', 'w+')
    f.write('[Desktop Entry]\n \
            Keywords=Chromatography\n \
            Name=OC-Manager\n \
            Comment=Chromatography-Manager Software\n \
            Exec=cd ' + path_to_oc + '/run.sh' + ' %F\n \
            Terminal=true\n \
            Type=Application\n \
            MimeType=text/plain\n \
            Categories=Education;Chromatography;\n')
    f.close()


class InstallationProcess:

    def __init__(self):
        self.version = 1.0
        self.main_title = "\n\t WELCOME TO OC-MANAGER INSTALLATION PROCESS\n"
        # The commands should be written as a list of strings, otherwise could fail.
        # Don't try to run RAW strings instead of list, if your string uses user input,
        # as they may inject arbitrary code!
        # https://queirozf.com/entries/python-3-subprocess-examples#run-raw-string-as-a-shell-command-line
        self.command = {
            "update": ["sudo", "apt-get", "update"],
            "upgrade": ["sudo", "apt-get", "upgrade"],
            "download_docker": ["sudo", "curl", "-fsSL", "https://get.docker.com", "-o", "get-docker.sh"],
            "install_docker": ["sudo", "sh", "get-docker.sh"],
            "install_docker_compose": ["sudo", "pip3", "install", "docker-compose"],
            "install_libraries": ["sudo", "apt-get", "install", "-y", "libffi-dev", "libssl-dev"],
        }

        title(self.main_title)
        self.installation_process()
        create_desktop_executable()

    def __str__(self):
        print(self.version)

    def installation_process(self):
        # Executes each of the commands in the dictionary 'commands'
        for key, value in self.command.items():
            title(key.upper())
            execute_command(value)


InstallationProcess()
