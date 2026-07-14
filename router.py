import paramiko
import threading
import socket
import time


class Router():
    def __init__(self):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        

    def run_command(self, command):
        _, stdout, _ = self.client.exec_command(command)
        return stdout.read().decode()






    def connect(self, ip="192.168.1.1", user="root", default_password="admin01", log=None):
        thread = threading.Thread(
            target=self._connect_process,
            args=(ip, user, default_password, log)
        )
        thread.daemon = True
        thread.start()

    def _connect_process(self, ip, user, default_password, log=None):
        try:
            # Trying to connect to router
            self.client.connect(hostname=ip, username=user, password=default_password)
            if log:
                log(f"Successfully connected to {ip}.")
        except Exception as e:
            if log:
                log(f"Connection failed: {e}")






    def update(self, firmware_path, log=None):
        thread = threading.Thread(
            target=self._update_process,
            args=(firmware_path, log)
        )
        thread.daemon = True
        thread.start()

    def _update_process(self, firmware_path, log=None):
        # Copy firmware to router /tmp/
        if log: log("Uploading firmware to router...")
        sftp = self.client.open_sftp()
        sftp.put(localpath=firmware_path, remotepath="/tmp/firmware.bin")
        sftp.close()

        # Start update (-n = without saving last settings)
        self.run_command("sysupgrade -n /tmp/firmware.bin")
        if log:
            log("Flashing firmware... Router will reboot.")
            time.sleep(3)
            log("Waiting for router to reboot...")
        
        # Auto reconnect with default password
        time.sleep(5)
        self._reconnect()
        if log:
            log("Router is back online after update!")


    def _reconnect(self, default_password="admin01"):
        while True:
            try:
                self.connect(default_password=default_password)
                break
            except:
                time.sleep(3)






    def change_password(self, new_password, log=None):
        thread = threading.Thread(
            target=self._change_password_process,
            args=(new_password, log)
        )
        thread.daemon = True
        thread.start()

    def _change_password_process(self, new_password, log=None):
        # Change root password on router
        if log:
            log("Changing password...")
        self.run_command(f"echo 'root:{new_password}' | chpasswd")
        if log:
            log("Password changed successfully.")






    def change_isp(self, isp, log=None):
        thread = threading.Thread(
            target=self._change_isp_process,
            args=(isp, log)
        )
        thread.daemon = True
        thread.start()

    def _change_isp_process(self, isp, log=None):
        # Apply ISP profile — changes IP and APN automatically
        if log:
            log(f"Applying {isp} profile...")
        self.run_command(f"profile.sh -c {isp} &")
        if log:
            log(f"{isp} profile applied. Router IP have changed.")






    def change_apn(self, apn, log=None):
        thread = threading.Thread(
            target=self._change_apn_process,
            args=(apn, log)
        )
        thread.daemon = True
        thread.start()

    def _change_apn_process(self, apn, log=None):
        # Set APN and restart network interface
        if log:
            log(f"Setting APN to {apn}...")
        self.run_command(f"uci set network.mob1s1a1.apn={apn}")
        self.run_command("uci commit network")
        self.run_command("/etc/init.d/network restart")
        if log:
            log(f"APN set to {apn}. Network restarted.")






    def is_router_active(self, ip="192.168.1.1"):
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






    def get_firmware_version(self):
        return self.run_command("cat /etc/version").strip()  # "RUT2_R_GPL_00.07.06.19"


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