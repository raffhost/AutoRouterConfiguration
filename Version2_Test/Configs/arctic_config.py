

#----------------------
#       LABELS
#----------------------

MAIN_LABEL = "Auto Router Configuration\nTool Interface"
STATUS_LABEL ="Router Active"
NEW_PASSWORD_LABEL = "New password:"
DEFAULT_PASSWORD_LABEL = "Def password:"
ROUTER_IP_LABEL = "Router IP:"
FIRMWARE_LABEL = "Select Firmware:"
ISP_LABEL = "Select ISP"
APN_LABEL = "Select APN"


#-------------------
#       FONTS
#-------------------
A16 = ("Arial", 16)
A28B = ("Arial", 28, "bold")
A26B = ("Arial", 26, "bold")
A42B = ("Arial", 42, "bold")
C9 = ("Consolas", 9)


#----------------------
#       LOGS
#----------------------


#----------------------
#       TOOLTIPS
#----------------------

NEW_PASSWORD_TOOLTIP = '''
The new password that will be set on the router.
\nThis replaces the default password after setup.
\nChoose something secure.
'''
DEFAULT_PASSWORD_TOOLTIP = '''
The current password on the router for SSH connection.
\nAfter a factory reset this is always
\nadmin01 or the password on the back of the router.
'''
ROUTER_IP_TOOLTIP = '''
The IP address of the router.
\nWill be changed after setting up different ISP.
\nDefault IP = 192.168.1.1
'''
FIRMWARE_TOOLTIP = '''
Select the firmware version for your router model and press update button.
\nIf router is not up to date, wait until update finishes.
'''
ISP_TOOLTIP = '''
Select the ISP profile for this router.
\nEach profile has a different gateway IP.
\nAfter setting up Router IP will be changed!
'''
APN_TOOLTIP = '''
Access Point Name (APN) is required for mobile data.
\nDifferent providers have different APNs!
\nYou can type it manually or choose one.
'''

