import tkinter as tk
import tkinter.ttk as ttk
from datetime import datetime
from router import Router
import config as conf
import threading
import json
import queue
import time
import sys
import os

def get_base_path():
    if getattr(sys, "frozen", False):   # True if running as a .exe
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

BASE_PATH = get_base_path()
CONFIG_PATH = os.path.join(BASE_PATH, "arctic_config.json")

# Firmware, ISP and APN
with open(CONFIG_PATH, encoding="utf-8") as file:
    data = json.load(file)

ROUTER_PASSWORD_LIST = data.get("ROUTER_PASSWORD_LIST", "")
NEW_PASSWORD_LIST = data.get("NEW_PASSWORD_LIST", "")
FIRMWARE_FOLDER = data.get("FIRMWARE_FOLDER", "")
FIRMWARE_LIST = data['FIRMWARE_LIST']
ISP_PROFILE_LIST = data['ISP_PROFILE_LIST']
APN_LIST = data['APN_LIST']


class App(tk.Tk):
    def __init__(self, router: Router | None = None):
        super().__init__()
        self.title("ARCTIC")
        self.geometry("1080x720")
        # self.resizable(False, False)
        self.router = router if router is not None else Router()
        self.status_light = "✲"

        # Track previous states to log only on change
        self._prev_active_state = None
        self._prev_connected_state = None
        self._prev_updated_state = None
        self._prev_ip = None

        # Signals cancellation while Auto Configuration is running
        self.cancel_event = threading.Event()

        # Queues used to safely pass data from background threads to the GUI thread
        self.log_queue = queue.Queue()
        self.gui_queue = queue.Queue()
        self.after(100, self._process_queues)
        


    #-------------------------------------------------------------
    #   INITIALIZATION AND THREADING
    #   (Start background threads, process log and GUI queues)
    #-------------------------------------------------------------

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


    #-------------------------------------------------------------
    #   UI HELPERS AND WINDOW LAYOUT
    #   (Helper functions for layout: tooltip labels, separators)
    #-------------------------------------------------------------

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


    # --- Title & status display "Router Active" (indicator + poll loop) ---

    def name_label(self):
        self.label = tk.Label(
            master=self,
            text="Auto router configuration tool",
            font=conf.LABELS_FONT_2
        )
        self.label.place(relx=0.015, rely=0.035, anchor="nw")


    def active_status(self):
        self.active_text = tk.Label(
            master=self,
            text="Router Active",
            font=conf.LABELS_FONT_2,
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
        self.after(1000, self.refresh_active)


    def _check_active(self):
        current_ip=self.router_ip.get().strip()
        current_state = self.router.is_router_active(current_ip)

        if current_ip != self._prev_ip:
            self._prev_ip = current_ip
            if not self.router.threading_busy.is_set():
                self.router.disconnect(
                    ip=current_ip
                )
            self.log_queue.put(f"Searching for router on {current_ip}...")

        if current_state != self._prev_active_state:
            
            if current_state:
                self.gui_queue.put(lambda: self.active_indicator.config(fg="green"))
                self.log_queue.put(f"Found a router on {current_ip}")

            elif self._prev_active_state != None:
                self.gui_queue.put(lambda: self.active_indicator.config(fg="red"))
                self.log_queue.put(f"Lost a router on {self._prev_ip}")

            else: # Used only once, right after the program starts
                self.gui_queue.put(lambda: self.active_indicator.config(fg="red"))

            self._prev_active_state = current_state


#-------------------------------------------------------------
#   TOOLTIPS
#-------------------------------------------------------------

    def create_tooltip(self, master, tooltip_text, size=24):
        icon = tk.Label(
            master=master, text="?",
            font=("Arial", int(size*0.6), "bold")
        )
        tooltip = None

        def show(event):
            nonlocal tooltip
            if tooltip: return
            
            tooltip = tk.Toplevel(icon)
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(
                f"+{icon.winfo_rootx()
                +icon.winfo_width()+5
                }+{icon.winfo_rooty()}"
            )
            
            tooltip_label = tk.Label(
                master=tooltip, text=tooltip_text,
                padx=10, pady=8, font=("Arial", 11),
                bg="#FFFFFF", borderwidth=1,
                highlightbackground="#000000",
                highlightthickness=1
            )
            tooltip_label.pack()

        def hide(event):
            nonlocal tooltip
            if tooltip:
                tooltip.destroy()
                tooltip = None

        icon.bind("<Enter>", show)
        icon.bind("<Leave>", hide)
        return icon


    #-------------------------------------------------------------
    #   CONNECTION AND CONFIGURATION INPUTS
    #   (Input fields: firmware/ISP/APN, passwords, router IP)
    #-------------------------------------------------------------

    # --- Firmware, ISP and APN selection (comboboxes from config.json) ---

    def firmware_selection(self):
        self.firmware_label = tk.Label(
            master=self,
            text="Select firmware",
            font=conf.LABELS_FONT_1
        )
        self.firmware_label.place(relx=0.01, rely=0.62)

        self.firmware_selection_help = self.create_tooltip(
            master=self,
            tooltip_text=conf.FIRMWARE_TOOLTIP
        )
        self.firmware_selection_help.place(relx=0.485, rely=0.625)

        firmware_list = [item['Name'] for item in FIRMWARE_LIST]
        self.select_firmware = ttk.Combobox(
            master=self,
            values=firmware_list,
            font=conf.LABELS_FONT_1
        )
        self.select_firmware.place(relx=0.225, rely=0.62, relwidth=0.25)


    def isp_selection(self):
        self.isp_label = tk.Label(
            master=self,
            text="Select ISP profile",
            font=conf.LABELS_FONT_1
        )
        self.isp_label.place(relx=0.01, rely=0.72)

        self.isp_help = self.create_tooltip(
            master=self,
            tooltip_text=conf.ISP_TOOLTIP
        )
        self.isp_help.place(relx=0.485, rely=0.725)

        isp_list = [item['ISP'] for item in ISP_PROFILE_LIST]
        self.select_isp = ttk.Combobox(
            master=self,
            values=isp_list,
            font=conf.LABELS_FONT_1
        )
        self.select_isp.place(relx=0.225, rely=0.72, relwidth=0.25)

        self.select_isp.bind("<<ButtonPress>>", self.update_ip)


    def apn_selection(self):
        self.apn_label = tk.Label(
            master=self,
            text="Select APN",
            font=conf.LABELS_FONT_1
        )
        self.apn_label.place(relx=0.01, rely=0.82)

        self.apn_help = self.create_tooltip(
            master=self,
            tooltip_text=conf.APN_TOOLTIP
        )
        self.apn_help.place(relx=0.485, rely=0.825)


        apn_list = [item['APN'] for item in APN_LIST]
        self.select_apn = ttk.Combobox(
            master=self,
            values=apn_list,
            font=conf.LABELS_FONT_1
            )
        self.select_apn.place(relx=0.225, rely=0.82, relwidth=0.25)


    # --- Password fields (new password / current router password) ---

    def new_password_entry(self):
        self.new_password_label = tk.Label(
            master=self,
            text="New password",
            font=conf.LABELS_FONT_1
        )
        self.new_password_label.place(relx=0.01, rely=0.375)

        self.new_password = ttk.Combobox(
            master=self,
            values=NEW_PASSWORD_LIST,
            font=conf.LABELS_FONT_1
        )
        self.new_password.insert(0, "admin01")
        self.new_password.place(relx=0.22, rely=0.375, relwidth=0.25)

        self.new_password_help = self.create_tooltip(
            master=self,
            tooltip_text=conf.NEW_PASSWORD_TOOLTIP
        )
        self.new_password_help.place(relx=0.485, rely=0.38)



    def router_password_entry(self):
        self.router_password_label = tk.Label(
            master=self,
            text="Router PW",
            font=conf.LABELS_FONT_1
        )
        self.router_password_label.place(relx=0.01, rely=0.275)

        self.router_password = ttk.Combobox(
            master=self,
            values=ROUTER_PASSWORD_LIST,
            font=conf.LABELS_FONT_1
        )
        self.router_password.insert(0, "admin01")
        self.router_password.place(relx=0.22, rely=0.275, relwidth=0.25)

        self.router_password_help = self.create_tooltip(
            master=self,
            tooltip_text=conf.ROUTER_PASSWORD_TOOLTIP
        )
        self.router_password_help.place(relx=0.485, rely=0.28)


    # --- Router IP field (incl. auto-fill of IP when ISP changes) ---

    def router_ip_entry(self):
        self.router_ip_label = tk.Label(
            master=self,
            text="Router IP",
            font=conf.LABELS_FONT_1
        )
        self.router_ip_label.place(relx=0.01, rely=0.175)

        ip_list = [item['IP'] for item in ISP_PROFILE_LIST]
        self.router_ip = ttk.Combobox(
            master=self,
            values=ip_list,
            font=conf.LABELS_FONT_1
        )
        self.router_ip.insert(0, "192.168.1.1")
        self.router_ip.place(relx=0.22, rely=0.175, relwidth=0.25)

        self.router_ip_help = self.create_tooltip(
            master=self,
            tooltip_text=conf.ROUTER_IP_TOOLTIP
        )
        self.router_ip_help.place(relx=0.485, rely=0.18)


    def update_ip(self, event=None):
        self.router_ip.delete(0, "end")
        self.router_ip.insert(0, ISP_PROFILE_LIST[self.select_isp.current()]['IP'])


    #-------------------------------------------------------------
    #   ACTION BUTTONS AND ROUTER OPERATIONS
    #   (Buttons and their click handlers, which call into router.py)
    #-------------------------------------------------------------

    # --- Connection to router ---

    def button_for_connection(self):
        self.connect_button = tk.Button(
            master=self,
            text="Connect",
            font=conf.BUTTONS_FONT_2,
            bg="#CCCCCC",
            command=lambda: self._on_connect(show_banner=True)
        )
        self.connect_button.place(relx=0.01, rely=0.5225, relwidth=0.125, relheight=0.051)


    def _on_connect(self, show_banner=False) -> bool:
        ip = self.router_ip.get().strip()
        password = self.router_password.get().strip()

        if not self.router.is_router_active(ip):
            self.log_queue.put("Error: No active router.")
            return False
            
        if not ip:
            self.log_queue.put("Error: Router IP is empty.")
            return False
        
        if not password:
            self.log_queue.put("Error: router password is empty.")
            return False

        self.router.connect(
            ip=ip,
            router_password=password,
            log=self.log_queue.put, 
            show_banner=show_banner   
        )
        return True


    # --- Reconnection to router ---

    def _wait_for_router_and_reconnect(self, show_banner=False):
        while not self.router.is_router_active(self.router_ip.get()):
            if self.cancel_event.is_set():
                raise InterruptedError("RECONNECTION")
            time.sleep(1)
        self._on_connect(show_banner=show_banner)

    # --- Change router password ---

    def button_for_password_changing(self):
        self.change_password_button = tk.Button(
            master=self,
            text="Change PW",
            font=conf.BUTTONS_FONT_2,
            bg="#CCCCCC",
            command=self._on_change_password
        )
        self.change_password_button.place(relx=0.16, rely=0.5225, relwidth=0.275, relheight=0.051)


    def _on_change_password(self) -> bool:
        ip=self.router_ip.get().strip()
        if not self.router.is_router_active(ip):
            self.log_queue.put("Error: No active router.")
            return False

        if not self.router.is_connected():
            self.log_queue.put("Error: Not connected. Press Connect first.")
            return False
        
        password = self.new_password.get().strip()
        if not password:
            self.log_queue.put("Error: New password is empty.")
            return False
        
        self.router_password.delete(0, "end")
        self.router_password.insert(0, self.new_password.get())
        self.router.change_password(
            new_password=password,
            log=self.log_queue.put
        )
        return True


    # --- Router disconnect ---

    def button_for_disconnect(self):
        self.connect_button = tk.Button(
            master=self,
            text="Stop",
            font=conf.BUTTONS_FONT_2,
            bg="#CCCCCC",
            command=self._on_disconnect
        )
        self.connect_button.place(relx=0.46, rely=0.5225, relwidth=0.075, relheight=0.051)

    def _on_disconnect(self):
        ip = self.router_ip.get().strip()
        if not self.router.is_router_active(ip):
            self.log_queue.put("Error: No active router.")
            return False

        if not self.router.is_connected():
            self.log_queue.put("Error: Not connected. Press Connect first.")
            return False
    
        if not ip:
            self.log_queue.put("Error: Router IP is empty.")
            return False

        self.router.disconnect(
            ip=ip,
            log=self.log_queue.put
        )
        return True

    # --- Firmware update ---

    def button_for_updating_firmware(self):
        self.update_button = tk.Button(
            master=self,
            text="Update",
            font=conf.BUTTONS_FONT_2,
            bg="#CCCCCC",
            command=self._on_firmware_update
        )
        self.update_button.place(relx=0.01, rely=0.927, relwidth=0.125, relheight=0.051)


    def _on_firmware_update(self):
        ip=self.router_ip.get().strip()
        if not self.router.is_router_active(ip):
            self.log_queue.put("Error: No active router.")
            return False
        
        if not self.router.is_connected():
            self.log_queue.put("Error: Not connected. Press Connect first.")
            return False
        
        if self.select_firmware.current() == -1:
            self.log_queue.put("Error: No firmware selected.")
            return False
        
        selected = FIRMWARE_LIST[self.select_firmware.current()]
        current = self.router.get_firmware_version()

        if self.router.is_router_updated(selected['Version']) and self.update_checkbox_state.get()==0:
            self.log_queue.put(f"Router firmware is up to date. No update needed.")
            self.log_queue.put(f"Current firmware: {current}\n If you still want to update, toogle checkbox on. ")
            self.update_checkbox.config(state="normal")
            return False
        
        self.log_queue.put(f"Current firmware: {current}")
        self.log_queue.put(f"Updating to: {selected['Version']}. Please wait...")
        firmware_path = os.path.join(FIRMWARE_FOLDER, selected['File'])
        self.router.update(
            firmware_path=firmware_path,
            log=self.log_queue.put
        )
        return True


    def checkbox_for_updating(self):
        self.update_checkbox_state=tk.IntVar()
        self.update_checkbox = tk.Checkbutton(
            master=self,
            text="Update",
            variable=self.update_checkbox_state,
            state="disabled"
        )
        self.update_checkbox.place(relx=0.225, rely=0.675)

    # --- Set/change ISP profile ---

    def button_for_updating_isp(self):
        self.isp_button = tk.Button(
            master=self,
            text="Set ISP",
            font=conf.BUTTONS_FONT_2,
            bg="#CCCCCC",
            command=self._on_change_isp
        )
        self.isp_button.place(relx=0.16, rely=0.927, relwidth=0.125, relheight=0.051)


    def _on_change_isp(self):
        ip=self.router_ip.get().strip()
        if not self.router.is_router_active(ip):
            self.log_queue.put("Error: No active router.")
            return False
        
        if not self.router.is_connected():
            self.log_queue.put("Error: Not connected. Press Connect first.")
            return False
        
        isp = self.select_isp.get().strip()
        if not isp:
            self.log_queue.put("Error: No ISP profile selected.")
            return False
        
        if self.router.is_isp_changed(isp):
            self.log_queue.put(f"ISP is up to date. No update needed.")
            self.log_queue.put(f"Current ISP: {isp}")
            return False

        try:
            self.router.change_isp(
            isp=isp,
            log=self.log_queue.put
            )

            if not self.router.is_isp_changed(isp):
                return False
        except:
            return False
        
        finally:
            self.update_ip()

        return True


    # --- Set/change APN ---

    def button_for_updating_apn(self):
        self.apn_button = tk.Button(
            master=self,
            text="Set APN",
            font=conf.BUTTONS_FONT_2,
            bg="#CCCCCC",
            command=self._on_change_apn
        )
        self.apn_button.place(relx=0.31, rely=0.927, relwidth=0.125, relheight=0.051)


    def _on_change_apn(self) -> bool:
        ip=self.router_ip.get().strip()
        if not self.router.is_router_active(ip):
            self.log_queue.put("Error: No active router.")
            return False
        
        if not self.router.is_connected():
            self.log_queue.put("Error: Not connected. Press Connect first.")
            return False

        apn = self.select_apn.get().strip()
        if not apn:
            self.log_queue.put("Error: No APN selected or entered.")
            return False

        self.router.change_apn(
            apn=apn,
            log=self.log_queue.put
        )
        return True


    # --- Network restart ---

    def button_for_router_restart(self):
        self.router_restart_button = tk.Button(
            master=self,
            text="NETRestart",
            font=conf.BUTTONS_FONT_2,
            bg="#CCCCCC",
            command=self._on_router_restart
        )
        self.router_restart_button.place(relx=0.600, rely=0.927, relwidth=0.150, relheight=0.051)

    
    def _on_router_restart(self) -> bool:
        ip=self.router_ip.get().strip()
        if not self.router.is_router_active(ip):
            self.log_queue.put("Error: No active router.")
            return False

        if not self.router.is_connected():
            self.log_queue.put("Error: Not connected. Press Connect first.")
            return False
        
        self.router.save_and_restart_network(
            log=self.log_queue.put
        )
        return True


    # --- Router reboot ---

    def button_for_router_reboot(self):
        self.router_reboot_button = tk.Button(
            master=self,
            text="Reboot",
            font=conf.BUTTONS_FONT_2,
            bg="#CCCCCC",
            command=self._on_router_reboot
        )
        self.router_reboot_button.place(relx=0.800, rely=0.927, relwidth=0.150, relheight=0.051)

    
    def _on_router_reboot(self) -> bool:
        ip=self.router_ip.get().strip()
        if not self.router.is_router_active(ip):
            self.log_queue.put("Error: No active router.")
            return False

        if not self.router.is_connected():
            self.log_queue.put("Error: Not connected. Press Connect first.")
            return False
        
        self.router.reboot(
            log=self.log_queue.put
        )
        return True


    #-------------------------------------------------------------
    #   ROUTER INFO PANEL (IP, ISP, APN, firmware, LAN-MAC, ...)
    #   AND STATUS CHECKS (SIM state, data connection, network state)
    #-------------------------------------------------------------

    def create_router_info(self):
        self.router_info_frame = tk.Frame(master=self, bg="#FFFFFF")
        self.router_info_frame.place(relx=0.558, rely=0.147, relwidth=0.442, relheight=0.35)

        self.router_info_x1_textbox = tk.Text(
            master=self.router_info_frame,
            font=("Consolas", 12),
            state="disabled",
            wrap="word"
        )
        self.router_info_x1_textbox.place(relx=0, rely=0, relwidth=0.503, relheight=1)

        self.router_info_x2_textbox = tk.Text(
            master=self.router_info_frame,
            font=("Consolas", 12),
            state="disabled",
            wrap="word"
        )
        self.router_info_x2_textbox.place(relx=0.5, rely=0, relwidth=0.503, relheight=1)


    def get_router_info(self):
        info_ip = None
        info_isp = None
        info_apn = None
        info_firmware = None
        info_lanmac = None

        ip = self.router_ip.get().strip()
        if not self.router.is_router_active(ip):
            return f"Router is not active"

        info_ip = ip
        if not self.router.is_connected():
            return f"Router active on {info_ip} but not connected."

        info_isp = self.router.get_isp()
        info_apn = self.router.get_apn()
        info_firmware = self.router.get_firmware_version()
        info_lanmac = self.router.get_lan_mac()
        serial_number = self.router.get_serial_number()
        imei = self.router.get_imei()

        lines_x1 = []
        if info_ip: lines_x1.append(f"IP: {info_ip}\n")
        if info_isp: lines_x1.append(f"ISP: {info_isp}\n")
        if info_apn: lines_x1.append(f"APN: {info_apn}\n")
        if info_firmware: lines_x1.append(f"Firmware: \n{info_firmware}\n")
        if info_lanmac: lines_x1.append(f"LAN MAC: \n{info_lanmac}\n")
        if serial_number: lines_x1.append(f"Serial Nummer: \n{serial_number}\n")
        if imei and self.imei_check.get(): lines_x1.append(f"IMEI: \n{imei}\n")
        lines_x1.append("\n\n\n")

        info_data_connection = self.router.get_data_connection()
        info_sim_state = self.router.get_sim_state()
        info_network_state = self.router.get_network_state()

        lines_x2 = []
        if info_data_connection: lines_x2.append(f"Data connection :\n{info_data_connection}\n")
        if info_sim_state: lines_x2.append(f"SIM info :\n{info_sim_state}\n")
        if info_network_state: lines_x2.append(f"Network state :\n{info_network_state}\n")
        lines_x2.append("\n\n\n")

        info_x1="\n".join(lines_x1)
        info_x2="\n".join(lines_x2)

        return info_x1, info_x2


    # --- Copy router info ---

    def button_for_router_info_copy(self):
        self.copy_button = tk.Button(
            master=self.router_info_frame,
            text="Copy",
            font=("Arial", 12, "bold"),
            bg="#CCCCCC",
            command=self._on_router_info_copy
        )
        self.copy_button.place(relx=0.300, rely=0.900, relwidth=0.200, relheight=0.100)


    def _on_router_info_copy(self):
        self.clipboard_clear()
        text_to_copy = self.router_info_x1_textbox.get("1.0", "end-1c")
        self.clipboard_append(text_to_copy)


    # --- Refresh router info ---

    def button_for_router_info_refresh(self):
        self.refresh_button = tk.Button(
            master=self.router_info_frame,
            text="Refresh",
            font=("Arial", 12, "bold"),
            bg="#CCCCCC",
            command=self._on_router_info_refresh
        )
        self.refresh_button.place(relx=0.505, rely=0.900, relwidth=0.200, relheight=0.100)


    def _on_router_info_refresh(self):
        info_x1, info_x2 = self.get_router_info()

        self.router_info_x1_textbox.config(state="normal")
        self.router_info_x1_textbox.delete("1.0", "end")
        self.router_info_x1_textbox.insert("end", info_x1)
        self.router_info_x1_textbox.config(state="disabled")


        self.router_info_x2_textbox.config(state="normal")
        self.router_info_x2_textbox.delete("1.0", "end")
        self.router_info_x2_textbox.insert("end", info_x2)
        self.router_info_x2_textbox.config(state="disabled")


    # --- IMEI Toggle Box Check ---

    def create_imei_checkbox(self):
        self.imei_check=tk.IntVar()
        self.imei_checkbox = tk.Checkbutton(
            master=self.router_info_frame,
            text="IMEI",
            variable=self.imei_check,
            state="normal"
        )
        self.imei_checkbox.place(relx=0.750, rely=0.900, relheight=0.100)

    #-------------------------------------------------------------
    #   AUTOMATIC CONFIGURATION 
    #   (a button that triggers multiple steps in sequence)
    #-------------------------------------------------------------
    
    def wait_until(self, func, check, comment=None):
        if comment:
            self.log_queue.put(comment)
        func()
        while self.router.threading_busy.is_set() or not check():
            if self.cancel_event.is_set():
                raise InterruptedError(comment)
            time.sleep(1)


    def button_for_auto_configuration(self):
        self.auto_configuration_button = tk.Button(
            master=self,
            text="Auto Configuration",
            font=conf.BUTTONS_FONT_2,
            bg="#CCCCCC",
            command=lambda: self.run_in_thread(
                self._on_auto_configuration
            )
        )
        self.auto_configuration_button.place(relx=0.600, rely=0.5225,relwidth=0.350, relheight=0.051)


    def _on_auto_configuration(self) -> bool:
        ip=self.router_ip.get().strip()
        if not self.router.is_router_active(ip):
            self.log_queue.put("Error: No active router.")
            return False

        self.cancel_event.clear()
        self.button_for_canceling_auto_configuration()
        self.gui_queue.put(self._show_cancel_button)
        
        steps = [ # label, func, check
            ("CONNECTION",
            lambda: self._on_connect(show_banner=True),
            self.router.is_connected
            ),
            ("UPDATE",
            self._on_firmware_update,
            lambda: self.router.is_router_updated(
                FIRMWARE_LIST[self.select_firmware.current()]['Version']
                )
            ),
            ("RECONNECTION",
            self._wait_for_router_and_reconnect,
            self.router.is_connected
            ),
            ("NEW PASSWORD",
            self._on_change_password,
            self.router.is_connected
            ),
            ("ISP",
            self._on_change_isp,
            lambda: not self.router.is_connected()
            ),
            ("RECONNECTION",
            self._wait_for_router_and_reconnect,
            self.router.is_connected
            ),
            ("APN",
            self._on_change_apn,
            lambda: not self.router.is_connected()
            ),
            ("RECONNECTION",
            lambda: self._wait_for_router_and_reconnect(show_banner=True),
            self.router.is_connected
            ),
        ]

        self.log_queue.put("##### CONFIGURATION STARTED #####")
        completed_idx = 0
        try:
            for i, (label, func, check) in enumerate(steps):
                self.wait_until(func=func, check=check, comment=f"----- {label} -----")
                completed_idx = i + 1
                time.sleep(2)
            self.log_queue.put("##### CONFIGURATION FINISHED #####")
            return True

        except InterruptedError:
            done = [label for label, _, _ in steps[:completed_idx]]
            remaining = [label for label, _, _ in steps[completed_idx:]]

            lines = ["----- CONFIGURATION CANCELLED BY USER -----", "", "Completed:"]
            lines += [f"  ✔ {label}" for label in done] if done else ["  (none)"]
            lines += ["", "Not completed:"]
            lines += [f"  ✘ {label}" for label in remaining] if remaining else ["  (none)"]

            self.log_queue.put("\n".join(lines))
            return False

        finally:
            self.gui_queue.put(self._hide_cancel_button)


    def button_for_canceling_auto_configuration(self):
        self.cancel_button = tk.Button(
            master=self,
            text="Cancel",
            font=conf.BUTTONS_FONT_2,
            bg="#E28C8C",
            command=self.cancel_event.set
        )


    def _show_cancel_button(self):
        self.auto_configuration_button.place_forget()
        self.cancel_button.place(relx=0.600, rely=0.5225, relwidth=0.350, relheight=0.051)

    def _hide_cancel_button(self):
        self.cancel_button.place_forget()
        self.auto_configuration_button.place(relx=0.600, rely=0.5225, relwidth=0.350, relheight=0.051)


    #-------------------------------------------------------------
    #   LOGGING AND APPLICATION STARTUP
    #   (Log window plus the final assembly of all UI elements)
    #-------------------------------------------------------------

    # --- Log window (display + write log messages) ---

    def log_chat(self):
        self.log_chat_frame = tk.Frame(master=self)
        self.log_chat_frame.place(relx=0.558, rely=0.597, relwidth=0.442, relheight=0.30)

        self.log_chat_scrollbar = tk.Scrollbar(master=self.log_chat_frame)
        self.log_chat_scrollbar.pack(side="right", fill="y")

        self.log_chat_box = tk.Text(
            master=self.log_chat_frame,
            font=conf.CHAT_FONT_1,
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


    # --- App start (assembles all layout elements and starts mainloop) ---

    def start(self):
        self.screen_separation()

        self.name_label()

        self.router_ip_entry()
        self.new_password_entry()
        self.router_password_entry()

        self.firmware_selection()
        self.checkbox_for_updating()
        self.isp_selection()
        self.apn_selection()

        self.log_chat()
        self.log_queue.put(
            "Application started. Welcome to ARCTIC!"
        )

        self.active_status()

        self.button_for_connection()
        self.button_for_password_changing()
        self.button_for_disconnect()

        self.button_for_updating_firmware()
        self.button_for_updating_isp()
        self.button_for_updating_apn()

        self.button_for_router_restart()
        self.button_for_router_reboot()

        self.create_router_info()
        self.button_for_router_info_copy()
        self.button_for_router_info_refresh()
        self.create_imei_checkbox()

        self.button_for_auto_configuration()

        self.mainloop()


#-------------------------------------------------------------
#   ENTRY POINT
#-------------------------------------------------------------

if __name__ == "__main__":
    router = Router()
    app = App(router)
    app.start()


# Version 1 - NOT FINISHED