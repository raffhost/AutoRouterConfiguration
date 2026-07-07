import paramiko


class Router():
    def __init__(self):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
    def is_connected(self):
        transport = self.client.get_transport()
        return transport is not None and transport.is_active()

    def connect(self, ip="192.168.1.1", user="root", def_pw="admin01"):
        self.client.connect(
            hostname=ip, 
            username=user, 
            password=def_pw
        )
        self.connected = True
    
    def show_network(self):
        stdin, stdout, stderr = self.client.exec_command("uci show network")
        return stdout.read().decode()

    def show_system(self):
        stdin, stdout, stderr = self.client.exec_command("uci show system")
        return stdout.read().decode()

    def update(self):
        pass
        # sftp = self.client.open_sftp() #file transfer protocol
        # sftp.put("", "/tmp/firmware.bin")
        # sftp.close()
        # router.run("sysupgrade -n /tmp/firmware.bin")  # -n = without saving last settings

    def change_password(self):
        pass
        
    def disconnect(self):
        self.client.close()
        

# if __name__ == "__main__":
#     router = Router()
#     router.connect(ip="192.168.1.1", user="root", def_pw="Pils2018")
#     print(router.is_connected())
#     print(router.show_network())
#     print(router.show_system())
