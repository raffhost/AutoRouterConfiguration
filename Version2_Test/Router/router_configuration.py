# Higher-level configuration that USE RouterConnection to actually talk to the
# router. This is where the "business logic" lives (which commands, in
# which order, for which purpose) - RouterConnection itself knows nothing
# about firmware, passwords or ISPs, only "send this / wait for that".


#----------------------------------
#       ROUTER CONFIGURATION
#----------------------------------

class RouterConfiguration():
    def __init__(self, connection):
        self.conn = connection  # RouterConnection instance


    def update_firmware(self, firmware_path, target_version, on_done=None):
        # 1. upload firmware via self.conn.upload_file()
        # 2. test compatibility (sysupgrade -T) via self.conn.send_command()
        # 3. if compatible: flash via self.conn.send_detached()
        # 4. if not compatible: report back via on_done (no flash!)
        pass

    def change_password(self, new_password, on_done=None):
        pass

    def change_isp(self, isp_name, on_done=None):
        pass

    def change_apn(self, apn, on_done=None):
        pass

    def restart_network(self, on_done=None):
        pass

    def reboot(self, on_done=None):
        pass