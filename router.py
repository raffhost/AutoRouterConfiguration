import paramiko
import threading
import time


class Router():
    def __init__(self):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        

    def run_command(self, command):
        _, stdout, _ = self.client.exec_command(command)
        return stdout.read().decode()


    def connect(self, ip="192.168.1.1", user="root", default_password="admin01"):
        thread = threading.Thread(
            target=self._connect_process,
            args=(ip, user, default_password)
        )
        thread.daemon = True
        thread.start()

    def _connect_process(self, ip, user, default_password):
        try:
            self.client.connect(hostname=ip, username=user, password=default_password)
        except:
            pass


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
        
        # Auto Reconnect with default password
        time.sleep(5)
        self._reconnect()
        
                
    def _reconnect(self, default_password="admin01"):
        while True:
            try:
                self.connect(default_password=default_password)
                break
            except:
                time.sleep(3)


    def change_password(self, new_password):
        self.run_command(f"echo 'root:{new_password}' | chpasswd")
        

    def change_isp_profile(self, isp):
        self.run_command(f"profile.sh -c {isp}")


    def change_apn(self, apn):
        self.run_command(f"uci set network.mob1s1a1.apn={apn}")
        self.run_command("uci commit network")
        self.run_command("/etc/init.d/network restart")
    
    
    def get_firmware_version(self):
        return self.run_command("cat /etc/version").strip() # "RUT2_R_GPL_00.07.06.19"


    def is_router_active(self, ip="192.168.1.1"):
        import socket
        try:
            sock = socket.create_connection((ip, 22), timeout=1)
            sock.close()
            return True
        except:
            return False


    def is_connected(self):
        try:
            result = self.run_command("echo ok")
            return result.strip() == "ok"
        except:
            return False


    def is_router_updated(self, given_version):
        current = self.get_firmware_version().strip()  # "RUT2_R_GPL_00.07.06.19"
        return current == given_version
    

    def show_network(self):
        return self.run_command("uci show network")


    def show_system(self):
        return self.run_command("uci show system")


    def disconnect(self):
        self.client.close()
        


# router = Router()
# router.connect()
# time.sleep(2)
# print(router.show_network())