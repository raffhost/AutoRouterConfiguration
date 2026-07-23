# Entry point ONLY. Creates all objects, wires them together, starts
# the app. No logic lives here. Later: base for building the .exe.
 
from router_connection import RouterConnection
from router_configuration import RouterConfiguration
from router_status import RouterStatus
from arctic_gui import ArcticGUI
 
 
if __name__ == "__main__":
    connection = RouterConnection()
    actions = RouterConfiguration(connection)
    status = RouterStatus(connection)
 
    app = ArcticGUI(actions, status)
    app.start()