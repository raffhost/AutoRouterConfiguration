# The window itself: layout, widgets, event handlers.
# IMPORTANT: this class talks to RouterConfiguration / RouterStatus only.
# It never touches RouterConnection or paramiko directly. 
# That keeps the GUI code free of any SSH/networking details.

import tkinter as tk
import tkinter.ttk as ttk
import threading
import json

from arctic_log import ArcticLog
from Extensions.tooltip import Tooltip
import Version2_Test.Configs.arctic_config as cfg

with open("config.json") as file:
    data = json.load(file)

FIRMWARE_LIST = data['FIRMWARE_LIST']
ISP_PROFILE_LIST = data['ISP_PROFILE_LIST']
APN_LIST = data['APN_LIST']


#------------------------
#       ARCTIC GUI
#------------------------

class ArcticGUI(tk.Tk):
    def __init__(self, configuration, status):
        super().__init__()
        self.title("ARCTIC")
        self.geometry("1080x720")
        self.configuration = configuration
        self.status = status

        # Events
        self.cancel_event = threading.Event()


    #-----------------------------
    #   LAYOUT / WINDOW HELPERS
    #-----------------------------

    def create_help_label(self, relx, rely, text="?", font=cfg.A16, fg="gray"):
        help_label = tk.Label(master=self, text=text, font=font, fg=fg)
        help_label.place(relx=relx, rely=rely)
        return help_label

    def create_screen_separation(self):
        self.cut_horizontal_m1 = ttk.Separator(self, orient="horizontal")
        self.cut_horizontal_m1.place(relx=0, rely=0.15, relwidth=1, anchor="sw")

        self.cut_horizontal_m2 = ttk.Separator(self, orient="horizontal")
        self.cut_horizontal_m2.place(relx=0, rely=0.50, relwidth=1, anchor="sw")

        self.cut_horizontal_m3 = ttk.Separator(self, orient="horizontal")
        self.cut_horizontal_m3.place(relx=0, rely=0.60, relwidth=1, anchor="sw")

        self.cut_horizontal_m4 = ttk.Separator(self, orient="horizontal")
        self.cut_horizontal_m4.place(relx=0, rely=0.90, relwidth=1, anchor="sw")

        self.cut_vertikal = ttk.Separator(self, orient="vertical")
        self.cut_vertikal.place(relx=0.56, rely=0, relheight=1, anchor="ne")

    def create_appname_label(self):
        self.appname_label = tk.Label(self, text=cfg.MAIN_LABEL, font=cfg.A28B)
        self.appname_label.place(relx=0.015, rely=0.035, anchor="nw")

    def create_active_status(self):
        self.active_text = tk.Label(self, text=cfg.STATUS_LABEL, font=cfg.A26B)
        self.active_text.place(relx=0.66, rely=0.035, anchor="nw")

        self.active_indicator = tk.Label(self, text="✲", font=cfg.A42B, fg="red")
        self.active_indicator.place(relx=0.875, rely=0.015, anchor="nw")

    def create_log_chat(self):
        self.log_chat_frame = tk.Frame(self)
        self.log_chat_frame.place(relx=0.558, rely=0.597, relwidth=0.44, relheight=0.30)

        self.log_chat_scrollbar = tk.Scrollbar(self.log_chat_frame)
        self.log_chat_scrollbar.pack(side="right", fill="y")

        self.log_chat_box = tk.Text(
            self.log_chat_frame, font=cfg.C9, state="disabled",
            wrap="word", yscrollcommand=self.log_chat_scrollbar.set)
        self.log_chat_box.pack(fill="both", expand=True)

        self.log_chat_scrollbar.config(command=self.log_chat_box.yview)


    #-------------------------------
    #   CONNECTION AND CONFIGURATION INPUTS
    #-------------------------------

    def firmware_selection(self):
        pass

    def isp_selection(self):
        pass

    def apn_selection(self):
        pass

    def new_password_entry(self):
        pass

    def default_password_entry(self):
        pass

    def router_ip_entry(self):
        pass

    def update_ip(self, event=None):
        pass


    #-------------------------------
    #   ACTION BUTTONS
    #-------------------------------

    def button_for_connection(self):
        pass

    def button_for_updating_firmware(self):
        pass

    def button_for_updating_isp(self):
        pass

    def button_for_updating_apn(self):
        pass

    def button_for_password_changing(self):
        pass

    def button_for_router_restart(self):
        pass

    def button_for_router_reboot(self):
        pass


    #-------------------------------
    #   AUTOMATIC CONFIGURATION
    #-------------------------------

    def button_for_auto_configuration(self):
        pass

    def _on_auto_configuration(self):
        pass

    def button_for_canceling_auto_configuration(self):
        pass


    #-------------------------------
    #   STARTUP
    #-------------------------------

    def start(self):
        pass