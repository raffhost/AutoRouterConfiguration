import paramiko
import threading
import subprocess
import time
import json


class Router():
    def __init__(self):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        

    def is_router_active(self, ip="192.168.1.1"):
        result = subprocess.run(["ping", "-n", "1", "-w", "1000", ip], capture_output=True)
        return result.returncode == 0


    def is_connected(self):
        try:
            result = self.run_command("echo ok")
            return result.strip() == "ok"
        except:
            return False


    def is_router_updated(self, given_version):
        current = self.get_firmware_version().strip()  # "RUT2_R_GPL_00.07.06.19"
        return current == given_version


    def connect(self, ip="192.168.1.1", user="root", default_password="admin01"):
        self.client.connect(
            hostname=ip,
            username=user, 
            password=default_password
        )
    

    def run_command(self, command):
        _, stdout, _ = self.client.exec_command(command)
        return stdout.read().decode()


    def show_network(self):
        return self.run_command("uci show network")


    def show_system(self):
        return self.run_command("uci show system")


    def get_firmware_name(self):
        board = self.run_command("cat /etc/board.json")
        board_data = json.loads(board)
        return board_data["model"]["id"] # "teltonika,rut2xx"


    def get_firmware_version(self):
        return self.run_command("cat /etc/version").strip() # "RUT2_R_GPL_00.07.06.19"

    def update(self, firmware_path):
        thread = threading.Thread(
            target=self._update_process,
            args=(firmware_path,)
        )
        thread.daemon = True
        thread.start()


    def _update_process(self, firmware_path):
        # Copy firmware on router in /tmp/
        sftp = self.client.open_sftp() # SSH File Transfer Protocol
        sftp.put(
            localpath=firmware_path,
            remotepath="/tmp/firmware.bin"
        )
        sftp.close()

        # Start update (-n = without saving last settings)
        self.run_command("sysupgrade -n /tmp/firmware.bin")
        
        # # Auto Reconnect with default password
        time.sleep(5)
        self._reconnect()

        
    def _reconnect(self, default_password="admin01"):
        while True:
            try:
                self.connect(default_password=default_password)
                break
            except:
                time.sleep(3)


    def change_password(self):
        pass
        

    def disconnect(self):
        self.client.close()
        

