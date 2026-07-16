import tkinter as tk
import tkinter.ttk as ttk
from datetime import datetime
from tooltip import Tooltip
from router import Router
import threading
import json
import queue


# Firmware, ISP and APN
with open("config.json") as file:
    data = json.load(file)


FIRMWARE_LIST = data["FIRMWARE_LIST"]
ISP_PROFILE_LIST = data["ISP_PROFILE_LIST"]
APN_LIST = data["APN_LIST"]


class App(tk.Tk):
    def __init__(self, router=Router):
        super().__init__()
        self.title("ARCTIC")
        self.geometry("1080x720")
        # self.resizable(False, False)
        self.router = router
        self.status_light = "✲"

        # Track previous states to log only on change
        self._prev_active_state = None
        self._prev_connected_state = None
        self._prev_updated_state = None
        self._prev_ip = None

        # Create queue for multiple threading (safe) at the same time
        self.log_queue = queue.Queue()
        self.gui_queue = queue.Queue()
        self.after(100, self._process_queues)


    def run_in_thread(self, func, *args):
        threading.Thread(target=func, args=args, daemon=True).start()


    def _process_queues(self):
        # Queue for logs
        while not self.log_queue.empty():
            message = self.log_queue.get_nowait()
            self.write_in_log_chat(message)

        # Queue for GUI
        while not self.gui_queue.empty():
            func = self.gui_queue.get_nowait()
            func()
        
        self.after(100, self._process_queues)






    def create_help_label(self, relx, rely, text="?", font=("Arial", 16), fg="gray"):
        label = tk.Label(master=self, text=text, font=font, fg=fg)
        label.place(relx=relx, rely=rely)
        return label


    def screen_separation(self):
        self.cut_horizontal_m1 = ttk.Separator(master=self, orient="horizontal")
        self.cut_horizontal_m1.place(relx=0, rely=0.15, relwidth=1, anchor="sw")

        self.cut_horizontal_m2 = ttk.Separator(master=self, orient="horizontal")
        self.cut_horizontal_m2.place(relx=0, rely=0.50, relwidth=1, anchor="sw")

        self.cut_horizontal_m3 = ttk.Separator(master=self, orient="horizontal")
        self.cut_horizontal_m3.place(relx=0, rely=0.60, relwidth=1, anchor="sw")

        self.cut_horizontal_m4 = ttk.Separator(master=self, orient="horizontal")
        self.cut_horizontal_m4.place(relx=0, rely=0.90, relwidth=1, anchor="sw")

        self.cut_vertikal = ttk.Separator(master=self, orient="vertical")
        self.cut_vertikal.place(relx=0.56, rely=0, relheight=1, anchor="ne")






    def name_label(self):
        self.label = tk.Label(
            master=self,
            text="Auto router configuration tool",
            font=("Arial", 28, "bold")
        )
        self.label.place(relx=0.015, rely=0.035, anchor="nw")


    def active_status(self):
        self.active_text = tk.Label(
            master=self,
            text="Router Active",
            font=("Arial", 26, "bold"),
            fg="black"
        )
        self.active_text.place(relx=0.66, rely=0.035, anchor="nw")

        self.active_indicator = tk.Label(
            master=self,
            text=self.status_light,
            font=("Arial", 42, "bold"),
            fg="red"
        )
        self.active_indicator.place(relx=0.875, rely=0.015, anchor="nw")

        self.refresh_active()


    def refresh_active(self):
        self.run_in_thread(self._check_active)
        self.after(2000, self.refresh_active)


    def _check_active(self):
        current_ip = self.router_ip.get()
        current_state = self.router.is_router_active(current_ip)

        if current_ip != self._prev_ip:
            self._prev_ip = current_ip
            self.log_queue.put(f"Searching for router on {current_ip}...")

        if current_state != self._prev_active_state:
            
            if current_state:
                self.gui_queue.put(lambda: self.active_indicator.config(fg="green"))
                self.log_queue.put(f"Found a router on {current_ip}")

            elif self._prev_active_state != None:
                self.gui_queue.put(lambda: self.active_indicator.config(fg="red"))
                self.log_queue.put(f"Lost a router on {self._prev_ip}")

            else: # Will be used 1 time only, after starting programm
                self.gui_queue.put(lambda: self.active_indicator.config(fg="red"))

            self._prev_active_state = current_state






    def firmware_selection(self):
        self.firmware_label = tk.Label(
            master=self,
            text="Select firmware",
            font=("Arial", 20)
        )
        self.firmware_label.place(relx=0.01, rely=0.175)

        self.firmware_selection_help = self.create_help_label(relx=0.485, rely=0.18)
        Tooltip(
            widget=self.firmware_selection_help,
            text="Select the firmware version for your router model." \
            "\nMust match the exact model (e.g. RUT2_R_GPL for RUT240)." \
            "\nUsed for flashing and checking if the router is up to date."
        )

        firmware_list = [item["Name"] for item in FIRMWARE_LIST]
        self.select_firmware = ttk.Combobox(
            master=self,
            values=firmware_list,
            font=("Arial", 20)
        )
        self.select_firmware.place(relx=0.225, rely=0.175, relwidth=0.25)


    def isp_selection(self):
        self.isp_label = tk.Label(
            master=self,
            text="Select ISP profile",
            font=("Arial", 20)
        )
        self.isp_label.place(relx=0.01, rely=0.275)

        self.isp_help = self.create_help_label(relx=0.485, rely=0.28)
        Tooltip(
            widget=self.isp_help,
            text="Select the ISP profile for this router." \
            "\nEach profile has a different gateway IP." \
            "\nThe IP is shown below the dropdown."
        )

        isp_list = [item["ISP"] for item in ISP_PROFILE_LIST]
        self.select_isp = ttk.Combobox(
            master=self,
            values=isp_list,
            font=("Arial", 20)
        )
        self.select_isp.place(relx=0.225, rely=0.275, relwidth=0.25)
        
        self.select_isp.bind("<<ButtonPress>>", self.update_ip)


    def apn_selection(self):
        self.apn_label = tk.Label(
            master=self,
            text="Select APN",
            font=("Arial", 20)
        )
        self.apn_label.place(relx=0.01, rely=0.375)

        self.apn_help = self.create_help_label(relx=0.485, rely=0.38)
        Tooltip(
            widget=self.apn_help,
            text="APN (Access Point Name) is required for mobile data." \
            "\nFilled automatically when you select a provider." \
            "\nYou can also type it manually if you know the correct APN."
        )

        apn_list = [item["APN"] for item in APN_LIST]
        self.select_apn = ttk.Combobox(
            master=self,
            values=apn_list,
            font=("Arial", 20)
            )
        self.select_apn.place(relx=0.225, rely=0.375, relwidth=0.25)






    def new_password_entry(self):
        self.new_password_label = tk.Label(
            master=self,
            text="New password",
            font=("Arial", 20)
        )
        self.new_password_label.place(relx=0.01, rely=0.62)

        new_pw_list=["admin01", "Start2026!"]
        self.new_password = ttk.Combobox(
            master=self,
            values=new_pw_list,
            font=("Arial", 20)
        )
        self.new_password.insert(0, "admin01")
        self.new_password.place(relx=0.22, rely=0.62, relwidth=0.25)

        self.new_password_help = self.create_help_label(relx=0.485, rely=0.625)
        Tooltip(
            widget=self.new_password_help,
            text="The new password that will be set on the router." \
            "\nThis replaces the default password after setup." \
            "\nChoose something secure."
        )


    def default_password_entry(self):
        self.default_password_label = tk.Label(
            master=self,
            text="Default password",
            font=("Arial", 20)
        )
        self.default_password_label.place(relx=0.01, rely=0.72)

        def_pw_list=["admin01",]
        self.default_password = ttk.Combobox(
            master=self,
            values=def_pw_list,
            font=("Arial", 20)
        )
        self.default_password.insert(0, "admin01")
        self.default_password.place(relx=0.22, rely=0.72, relwidth=0.25, )

        self.default_password_help = self.create_help_label(relx=0.485, rely=0.725)
        Tooltip(
            widget=self.default_password_help,
            text="The current password on the router." \
            "\nAfter a factory reset this is always admin01." \
            "\nUsed to establish the SSH connection."
        )






    def router_ip_entry(self):
        self.router_ip_label = tk.Label(
            master=self,
            text="Router IP",
            font=("Arial", 20)
        )
        self.router_ip_label.place(relx=0.01, rely=0.82)

        ip_list = [item["IP"] for item in ISP_PROFILE_LIST]
        self.router_ip = ttk.Combobox(
            master=self,
            values=ip_list,
            font=("Arial", 20)
        )
        self.router_ip.insert(0, "192.168.1.1")
        self.router_ip.place(relx=0.22, rely=0.82, relwidth=0.25)

        self.router_ip_help = self.create_help_label(relx=0.485, rely=0.825)
        Tooltip(
            widget=self.router_ip_help,
            text="The IP address of the router." \
            "\nAfter a factory reset this is always 192.168.1.1." \
            "\nChange it if your router uses a different IP."
        )


    def update_ip(self, event=None):
        self.router_ip.delete(0, "end")
        self.router_ip.insert(0, ISP_PROFILE_LIST[self.select_isp.current()]["IP"])






    def button_for_updating_firmware(self):
        self.update_button = tk.Button(
            master=self,
            text="Update",
            font=("Arial", 20),
            bg="#CCCCCC",
            command=self._on_firmware_update
        )
        self.update_button.place(relx=0.01, rely=0.5225, relwidth=0.125, relheight=0.051)


    def _on_firmware_update(self):
        if not self.router.is_connected():
            self.log_queue.put("Error: Not connected. Press Connect first.")
            return
        
        if self.select_firmware.current() == -1:
            self.log_queue.put("Error: No firmware selected.")
            return
        
        selected = FIRMWARE_LIST[self.select_firmware.current()]
        current = self.router.get_firmware_version()

        if self.router.is_router_updated(selected["Version"]):
            self.log_queue.put(f"Router firmware is up to date. No update needed.")
            self.log_queue.put(f"Current firmware: {current}")
            return

        self.log_queue.put(f"Current firmware: {current}")
        self.log_queue.put(f"Updating to: {selected["Version"]}. Please wait...")
        self.router.update(
            firmware_path=selected["PATH"],
            log=self.log_queue.put
        )






    def button_for_updating_isp(self):
        self.isp_button = tk.Button(
            master=self,
            text="Set ISP",
            font=("Arial", 20),
            bg="#CCCCCC",
            command=self._on_change_isp
        )
        self.isp_button.place(relx=0.16, rely=0.5225, relwidth=0.125, relheight=0.051)


    def _on_change_isp(self):
        if not self.router.is_connected():
            self.log_queue.put("Error: Not connected. Press Connect first.")
            return
        
        isp = self.select_isp.get().strip()
        if not isp:
            self.log_queue.put("Error: No ISP profile selected.")
            return
        
        self.log_queue.put(f"Applying ISP profile: {isp}...")
        self.router.change_isp(
            isp=isp,
            log=self.log_queue.put
        )






    def button_for_updating_apn(self):
        self.apn_button = tk.Button(
            master=self,
            text="Set APN",
            font=("Arial", 20),
            bg="#CCCCCC",
            command=self._on_change_apn
        )
        self.apn_button.place(relx=0.31, rely=0.5225, relwidth=0.125, relheight=0.051)


    def _on_change_apn(self):
        if not self.router.is_connected():
            self.log_queue.put("Error: Not connected. Press Connect first.")
            return

        apn = self.select_apn.get().strip()
        if not apn:
            self.log_queue.put("Error: No APN selected or entered.")
            return

        self.router.change_apn(
            apn=apn,
            log=self.log_queue.put
        )






    def button_for_connection(self):
        self.connect_button = tk.Button(
            master=self,
            text="Connect",
            font=("Arial", 20),
            bg="#CCCCCC",
            command=self._on_connect
        )
        self.connect_button.place(relx=0.01, rely=0.927, relwidth=0.125, relheight=0.051)


    def _on_connect(self):
        ip = self.router_ip.get().strip()
        password = self.default_password.get().strip()
        
        if not ip:
            self.log_queue.put("Error: Router IP is empty.")
            return
        
        if not password:
            self.log_queue.put("Error: Default password is empty.")
            return

        self.router.connect(
            ip=ip,
            default_password=password,
            log=self.log_queue.put
        )





    
    def button_for_password_changing(self):
        self.change_password_button = tk.Button(
            master=self,
            text="Change PW",
            font=("Arial", 20),
            bg="#CCCCCC",
            command=self._on_change_password
        )
        self.change_password_button.place(relx=0.16, rely=0.927, relwidth=0.275, relheight=0.051)


    def _on_change_password(self):
        if not self.router.is_connected():
            self.log_queue.put("Error: Not connected. Press Connect first.")
            return
        
        password = self.new_password.get().strip()
        if not password:
            self.log_queue.put("Error: New password is empty.")
            return
        
        self.router.change_password(
            new_password=password,
            log=self.log_queue.put
        )






    def button_for_router_restart(self):
        self.change_password_button = tk.Button(
            master=self,
            text="Change PW",
            font=("Arial", 20),
            bg="#CCCCCC",
            command=self._on_router_restart
        )
        self.change_password_button.place(relx=0.675, rely=0.927, relwidth=0.275, relheight=0.051)

    
    def _on_router_restart(self):
        if not self.router.is_router_active():
            self.log_queue.put("Error: No active router.\nSwitch it on first and connect it to the LAN Port.")
            return
        
        self.router.save_and_restart_network(
            log=self.log_queue.put
        )






    def log_chat(self):
        self.log_chat_frame = tk.Frame(master=self)
        self.log_chat_frame.place(relx=0.558, rely=0.597, relwidth=0.44, relheight=0.30)

        self.log_chat_scrollbar = tk.Scrollbar(master=self.log_chat_frame)
        self.log_chat_scrollbar.pack(side="right", fill="y")

        self.log_chat_box = tk.Text(
            master=self.log_chat_frame,
            font=("Arial", 9),
            state="disabled",
            wrap="word",
            yscrollcommand=self.log_chat_scrollbar.set
        )
        self.log_chat_box.pack(fill="both", expand=True)
        self.log_chat_scrollbar.config(command=self.log_chat_box.yview)


    def write_in_log_chat(self, message):
        time = datetime.now().strftime("%H:%M:%S")
        self.log_chat_box.config(state="normal")
        self.log_chat_box.insert("end", f"[{time}] {message}\n")
        self.log_chat_box.see("end")
        self.log_chat_box.config(state="disabled")






    def start(self):
        self.screen_separation()

        self.name_label()

        self.firmware_selection()
        self.isp_selection()
        self.apn_selection()

        self.new_password_entry()
        self.default_password_entry()
        self.router_ip_entry()

        self.log_chat()
        self.log_queue.put(
            "Application started. Welcome to ARCTIC!"
        )

        self.active_status()

        self.button_for_connection()
        self.button_for_password_changing()

        self.button_for_updating_firmware()
        self.button_for_updating_isp()
        self.button_for_updating_apn()

        self.mainloop()






if __name__ == "__main__":
    router = Router()
    app = App(router)
    app.start()


# Version 1 - FINISHED