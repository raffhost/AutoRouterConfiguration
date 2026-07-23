import paramiko
from Version2_Test.Extensions.task_queue import TaskQueue


#-----------------------------
#       ROUTER CONNECTION
#-----------------------------

class RouterConnection():
    def __init__(self):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        self.queue = TaskQueue()
        self.connected = False
        self.last_output = None  # Optional


    #-------------------------------
    #   PUBLIC API (asynchronous)
    #-------------------------------

    def connect(self, ip, user="root", password="admin01", on_done=None):
        # Puts _connect() into the queue
        self.queue.add_task(self._connect, ip, user, password, on_done)
        self.connected = True

    def send_command(self, command, store_output=False, on_done=None):
        # Puts _send_command into the queue
        self.queue.add_task(self._send_command, command, store_output)

    def send_detached(self, command, on_done=None):
        # Puts _send_detached into the queue
        self.queue.add_task(self._send_detached, command)

    def upload_file(self, local_path, remote_path="/tmp/firmware.bin", on_done=None):
        # Puts _upload_file into the queue
        self.queue.add_task(self._upload_file, local_path, remote_path)

    def disconnect(self, on_done=None):
        # Puts _disconnect into the queue
        self.queue.add_task(self._disconnect)

        
    #------------
    #   STATUS
    #------------

    def is_busy(self) -> bool:
        return self.queue.is_threading_busy()
    
    #-------------------------------
    #   INTERNAL (runs only inside the queue's worker thread,
    #   never call these directly from outside)
    #-------------------------------

    def _connect(self, ip, user, password):
        pass

    def _send_command(self, command, store_output):
        # Runs a command and waits for a response (exit_code, stdout, and stderr).
        # For normal commands, e.g. changing password, reading UCI values.

        _, stdout, stderr = self.client.exec_command(command)
        exit_code = stdout.channel.recv_exit_status()
        output = (exit_code, stdout.read().decode(), stderr.read().decode())
        if store_output: 
            self.last_output = output

        return output

    def _send_detached(self, command):
        # Protected execution: fires command and instantly closes channel.
        # Without waiting for a response. This prevents Paramiko from hanging
        # when commands like reboot, sysupgrade and network restart
        # terminate the connection themselves
        
        transport = self.client.get_transport()
        if transport and transport.is_active():
            channel = transport.open_session()
            channel.exec_command(command)

    def _upload_file(self, local_path, remote_path):
        # Uploads a file on router like firmware via SFTP.
        sftp = self.client.open_sftp()
        sftp.put(localpath=local_path, remotepath=remote_path)
        sftp.close()

    def _disconnect(self):
        # Instantly closes channel
        self.client.close()