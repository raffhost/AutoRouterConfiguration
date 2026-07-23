# Pure read-only checks / status queries. Nothing here changes anything
# on the router - only reads and reports back.
#
# IMPORTANT: everything that needs SSH goes through self.conn (the SAME
# queue that router_actions.py uses) - never call self.conn.client
# directly. That direct-access pattern is exactly what caused the
# race-condition bugs earlier (two SSH commands running at once).


#-----------------------------
#       ROUTER STATUS
#-----------------------------

class RouterStatus():
    def __init__(self, connection):
        self.conn = connection  # RouterConnection instance


    def is_router_active(self, ip, callback):
        # Plain port-22 socket check (NOT SSH) - can run even without an
        # existing SSH session, so this does NOT need to go through the queue.
        pass

    def is_connected(self, callback):
        # Sends "echo ok" through the queue, checks the response.
        pass

    def is_router_updated(self, expected_version, callback):
        pass

    def is_isp_changed(self, expected_isp, callback):
        pass

    def is_apn_changed(self, expected_apn, callback):
        pass

    def get_banner(self, callback):
        pass

    def get_board_info(self, callback):
        pass

    def get_lan_mac(self, callback):
        pass