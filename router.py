import paramiko
import threading
import socket
import time
import queue


class Router():
    def __init__(self):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Queue to store incoming tasks
        self.task_queue = queue.Queue()
        
        # Start a single background queue thread
        threading.Thread(target=self._queue, daemon=True).start()


    def run_command(self, command) -> str:
        _, stdout, _ = self.client.exec_command(command)
        return stdout.read().decode()


    def _run_detached(self, command):
        # Protected execution: fires command and instantly closes channel
        # This prevents Paramiko from hanging when connection drops
        transport = self.client.get_transport()
        if transport and transport.is_active():
            channel = transport.open_session()
            channel.exec_command(command)


    def add_to_queue(self, func, *args, **kwargs):
        self.task_queue.put((func, args, kwargs))


    def _queue(self):
        while True:
            func, args, kwargs = self.task_queue.get()
            try:
                func(*args, **kwargs)
            except Exception as e:
                print(f"Queue error: {e}")
            finally:
                self.task_queue.task_done()






    def connect(self, ip="192.168.1.1", user="root", default_password="admin01", log=None):
        self.add_to_queue(self._connect_process, ip, user, default_password, log)


    def update(self, firmware_path, log=None):
        self.add_to_queue(self._update_process, firmware_path, log)


    def change_password(self, new_password, log=None):
        self.add_to_queue(self._change_password_process, new_password, log)


    def change_isp(self, isp, log=None):
        self.add_to_queue(self._change_isp_process, isp, log)


    def change_apn(self, apn, log=None):
        self.add_to_queue(self._change_apn_process, apn, log)


    def reboot(self, log=None):
        self.add_to_queue(self._reboot_process, log)






    def _connect_process(self, ip, user, default_password, log=None):
        try:
            self.client.connect(
                hostname=ip, username=user, 
                password=default_password,
                timeout=3, banner_timeout=3
            )
            if log:
                log(f"Successfully connected to {ip}.")
        except Exception as e:
            if log:
                log(f"Connection failed: {e}")


    def _update_process(self, firmware_path, log=None):
        # Copy firmware to router /tmp/
        if log: log("Uploading firmware to router...")
        sftp = self.client.open_sftp()
        sftp.put(localpath=firmware_path, remotepath="/tmp/firmware.bin")
        sftp.close()

        # Start update (-n = without saving last settings)
        # PROTECTED: Handled via detached execution to avoid connection drop socket crash
        self._run_detached("nohup sysupgrade -n /tmp/firmware.bin > /dev/null 2>&1 &")
        if log:
            log("Flashing firmware... Router will reboot.")
            time.sleep(3)
            log("Waiting for router to reboot...")


    def _change_password_process(self, new_password, log=None):
        # Change root password on router
        if log:
            log("Changing password...")
        self.run_command(f"echo -e '{new_password}\n{new_password}\n' | passwd")
        
        if log:
            log("Password changed successfully.")


    def _change_isp_process(self, isp, log=None):
        # Apply ISP profile — changes IP and APN automatically
        isp = isp.strip().upper().replace(" ", "")
        if log:
            log(f"Applying {isp} profile..." \
                "\nRouter IP will change after restart."
            )
        # PROTECTED: Detached call since profiles frequently restart networking stack
        self._run_detached(f"profile.sh -c {isp}")

        if log:
            log(f"{isp} profile applied.")


    def _change_apn_process(self, apn, log=None):
        # Set APN and restart network interface
        if log:
            log(f"Setting APN to {apn}...")
        self.run_command(f"uci set network.mob1s1a1.auto_apn='0'")
        self.run_command(f"uci set network.mob1s1a1.apn='{apn}'")
        self.save_and_restart_network(log=log)


    def _reboot_process(self, log=None):
        if log:
            log("Sending reboot command to the router...")
        # PROTECTED: Fired via detached call so code doesn't freeze waiting for an dead connection
        self._run_detached("reboot")
        self.disconnect()
        if log:
            log("Router is rebooting. SSH connection closed.")






    def is_router_active(self, ip="192.168.1.1") -> bool:
        try:
            sock = socket.create_connection((ip, 22), timeout=1)
            sock.close()
            return True
        except:
            return False


    def is_connected(self) -> bool:
        try:
            result = self.run_command("echo ok")
            return result.strip() == "ok"
        except:
            return False


    def is_router_updated(self, given_version) -> bool:
        current_firmware = self.get_firmware_version().strip()  # "RUT2_R_GPL_00.07.06.19"
        return current_firmware == given_version # return True if correct
    

    def is_isp_changed(self, given_isp) -> bool:
        current_isp = self.run_command("uci get profiles.general.profile").strip().upper().replace(" ", "")
        return current_isp == given_isp


    def is_apn_changed(self, given_apn) -> bool:
        current_apn = self.run_command("uci get network.mob1s1a1.apn").strip()
        return current_apn == given_apn






    def save_changes(self, log=None):
        if log:
            log("Saving changes...")
        self.run_command("uci commit network")


    def restart_network(self, log=None):
        if log:
            log("Network restarting...")
        # PROTECTED: Detached call since network restart kills current routing/IP assignment
        self._run_detached("/etc/init.d/network restart")


    def save_and_restart_network(self, log=None):
        self.save_changes(log=log)
        self.restart_network(log=log)


    def get_firmware_version(self) -> str:
        return self.run_command("cat /etc/version").strip()  


    def show_network(self) -> str:
        return self.run_command("uci show network")


    def show_system(self) -> str:
        return self.run_command("uci show system")


    def disconnect(self):
        try:
            self.client.close()
        except:
            pass