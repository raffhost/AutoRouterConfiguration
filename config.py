import json


# Window
TITLE = "ARCT"
GEOMETRY = "1080x720"


# Fonts and sizes
FONT_A8 = ("Arial", 8)
FONT_A12 = ("Arial", 12)
FONT_A16 = ("Arial", 16)
FONT_A20 = ("Arial", 20)
FONT_A24 = ("Arial", 24)
FONT_A28 = ("Arial", 28)


# Labels
NAMELABEL_TEXT = "Auto Router Configuration Tool"
FIRMWARE_TEXT = "Select Firmware"
ISP_TEXT = "Select ISP Profile"
PROVIDER_TEXT = "Select Provider"
TARIF_TEXT = "Select Tarif"


# Firmware, ISP and Providers(APN)
with open("config.json") as file:
    data = json.load(file)

FIRMWARE_LIST = data["FIRMWARE_LIST"]
ISP_PROFILE_LIST = data["ISP_PROFILE_LIST"]
PROVIDER_LIST = data["PROVIDER_LIST"]


# Username and Passwords
USERNAME = "admin"  # Replace with the actual username if needed
DEFAULT_PASSWORD = "admin01"  # Replace with the actual default password if needed
NEW_PASSWORD = "admin01"  # Replace with the actual new password if needed


# WebUI
WEB_UI_URL = "http://192.168.1.1"