import tkinter as tk
import tkinter.ttk as ttk
from tooltip import Tooltip
from router import Router
import json


# Firmware, ISP and Providers(APN)
with open("config.json") as file:
    data = json.load(file)


FIRMWARE_LIST = data["FIRMWARE_LIST"]
ISP_PROFILE_LIST = data["ISP_PROFILE_LIST"]
PROVIDER_LIST = data["PROVIDER_LIST"]


class App(tk.Tk):
    def __init__(self, router=Router):
        super().__init__()
        self.title("ARCTIC")
        self.geometry("1080x720")
        self.resizable(False, False)
        self.router = router
        self.status_light = "✲"


    def create_help_label(self, relx, rely, text="?", font=("Arial", 16), fg="gray"):
        label = tk.Label(master=self, text=text, font=font, fg=fg)
        label.place(relx=relx, rely=rely)
        return label


    def screen_separation(self):
        self.cut_vertikal = ttk.Separator(master=self, orient="vertical")
        self.cut_vertikal.place(relx=0.56, rely=0, relheight=1, anchor="ne")

        self.cut_horizontal_m1 = ttk.Separator(master=self, orient="horizontal")
        self.cut_horizontal_m1.place(relx=0, rely=0.15, relwidth=0.558, anchor="sw")

        self.cut_horizontal_m2 = ttk.Separator(master=self, orient="horizontal")
        self.cut_horizontal_m2.place(relx=0, rely=0.60, relwidth=0.558, anchor="sw")

        self.cut_horizontal_m3 = ttk.Separator(master=self, orient="horizontal")
        self.cut_horizontal_m3.place(relx=1, rely=0.80, relwidth=0.30, anchor="se")


    def name_label(self):
        self.label = tk.Label(
            master=self,
            text="Auto router configuration tool ♛",
            font=("Arial", 28, "bold")
        )
        self.label.place(relx=0.015, rely=0.035, anchor="nw")


    def firmware_selection(self):
        self.firmware_label = tk.Label(
            master=self,
            text="Select firmware",
            font=("Arial", 20)
        )
        self.firmware_label.place(relx=0.01, rely=0.20)

        self.firmware_selection_help = self.create_help_label(relx=0.22, rely=0.205)
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
        self.select_firmware.place(relx=0.25, rely=0.20)


    def isp_selection(self):
        self.isp_label = tk.Label(
            master=self,
            text="Select ISP profile",
            font=("Arial", 20)
        )
        self.isp_label.place(relx=0.01, rely=0.30)

        self.isp_help = self.create_help_label(relx=0.22, rely=0.305)
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
        self.select_isp.place(relx=0.25, rely=0.30)

        self.show_ip = tk.Label(
            master=self,
            text=f"# IP = {self.get_ip()}",
            font=("Arial", 10)
        )
        self.show_ip.place(relx=0.25, rely=0.355)

        self.select_isp.bind("<<ComboboxSelected>>", self.update_ip)


    def provider_selection(self):
        self.provider_label = tk.Label(
            master=self,
            text="Select provider",
            font=("Arial", 20)
        )
        self.provider_label.place(relx=0.01, rely=0.40)

        self.provider_help = self.create_help_label(relx=0.22, rely=0.405)
        Tooltip(
            widget=self.provider_help,
            text="Select the mobile network provider (SIM card)." \
            "\nThe APN will be filled in automatically." \
            "\nYou can still change the APN manually if needed."
        )

        provider_list = [list(item.keys())[0] for item in PROVIDER_LIST]
        self.select_provider = ttk.Combobox(
            master=self,
            values=provider_list,
            font=("Arial", 20)
        )
        self.select_provider.place(relx=0.25, rely=0.40)

        self.select_provider.bind("<<ComboboxSelected>>", self.update_apn_list)


    def apn_selection(self):
        self.apn_label = tk.Label(
            master=self,
            text="Select APN",
            font=("Arial", 20)
        )
        self.apn_label.place(relx=0.01, rely=0.50)

        self.apn_help = self.create_help_label(relx=0.22, rely=0.505)
        Tooltip(
            widget=self.apn_help,
            text="APN (Access Point Name) is required for mobile data." \
            "\nFilled automatically when you select a provider." \
            "\nYou can also type it manually if you know the correct APN."
        )

        self.select_apn = ttk.Combobox(master=self, font=("Arial", 20))
        self.select_apn.place(relx=0.25, rely=0.50)


    def update_apn_list(self, event=None):
        selected_provider = self.select_provider.get()
        provider_data = next(item for item in PROVIDER_LIST if selected_provider in item)
        apn_list = [entry["APN"] for entry in provider_data[selected_provider]]
        self.select_apn.config(values=apn_list)
        self.select_apn.set(apn_list[0])


    def get_ip(self):
        isp = self.select_isp.get()
        if isp == "ISP 1":
            return "100.64.5.1"
        elif isp == "ISP 2":
            return "100.64.6.1"
        elif isp == "ISP 3":
            return "100.64.7.1"
        elif isp == "ISP 4":
            return "100.64.8.1"
        else:
            return "192.168.1.1"


    def update_ip(self, event=None):
        self.show_ip.config(text=f"# IP = {self.get_ip()}")


    def new_password_entry(self):
        self.new_password_label = tk.Label(
            master=self,
            text="New password",
            font=("Arial", 20)
        )
        self.new_password_label.place(relx=0.01, rely=0.62)

        self.new_password = tk.Entry(master=self, font=("Arial", 20))
        self.new_password.insert(0, "admin01")
        self.new_password.place(relx=0.22, rely=0.62)

        self.new_password_help = self.create_help_label(relx=0.51, rely=0.625)
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

        self.default_password = tk.Entry(master=self, font=("Arial", 20))
        self.default_password.insert(0, "admin01")
        self.default_password.place(relx=0.22, rely=0.72)

        self.default_password_help = self.create_help_label(relx=0.51, rely=0.725)
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

        self.router_ip = tk.Entry(master=self, font=("Arial", 20))
        self.router_ip.insert(0, "192.168.1.1")
        self.router_ip.place(relx=0.22, rely=0.82)

        self.router_ip_help = self.create_help_label(relx=0.51, rely=0.825)
        Tooltip(
            widget=self.router_ip_help,
            text="The IP address of the router." \
            "\nAfter a factory reset this is always 192.168.1.1." \
            "\nChange it if your router uses a different IP."
        )


    def active_status(self):
        self.active_text = tk.Label(
            master=self,
            text="Router Active",
            font=("Arial", 26),
            fg="black"
        )
        self.active_text.place(relx=0.71, rely=0.035)

        # Indicator
        self.active_indicator = tk.Label(
            master=self,
            text=self.status_light,
            font=("Arial", 42),
            fg="red"
        )
        self.active_indicator.place(relx=0.925, rely=0.010)

        Tooltip(
            widget=self.active_indicator,
            text="Shows whether the router is reachable on the network." \
            "\nGreen = router responds to ping on 192.168.1.1." \
            "\nRed = router not found or not connected via LAN."
        )

        self.refresh_active()


    def refresh_active(self):
        if self.router.is_router_active():
            self.active_indicator.config(fg="green")
        else:
            self.active_indicator.config(fg="red")
        self.after(1000, self.refresh_active)


    def connect_status(self):
        # Button
        self.connect_button = tk.Button(
            master=self,
            text="Connect",
            font=("Arial", 20),
            bg="#CCCCCC",
            command=lambda: self.router.connect(
                ip=self.router_ip.get(),
                default_password=self.default_password.get()
            )
        )
        self.connect_button.place(relx=0.57, rely=0.15)

        # Status text
        self.connect_text = tk.Label(
            master=self,
            text="Connected",
            font=("Arial", 26),
            fg="black"
        )
        self.connect_text.place(relx=0.71, rely=0.15)

        # Indicator
        self.connect_indicator = tk.Label(
            master=self,
            text=self.status_light,
            font=("Arial", 42),
            fg="red"
        )
        self.connect_indicator.place(relx=0.925, rely=0.125)

        Tooltip(
            widget=self.connect_indicator,
            text="Shows whether an active SSH session exists." \
            "\nGreen = successfully logged in to the router." \
            "\nRed = not connected or wrong password."
        )

        self.refresh_connect()


    def refresh_connect(self):
        if self.router.is_connected():
            self.connect_indicator.config(fg="green")
        else:
            self.connect_indicator.config(fg="red")
        self.after(1000, self.refresh_connect)


    def firmware_status(self):
        # Button
        self.update_button = tk.Button(
            master=self,
            text="Update",
            font=("Arial", 20),
            bg="#CCCCCC",
            command=lambda: self.router.update(
                firmware_path=FIRMWARE_LIST[self.select_firmware.current()]["PATH"]
            )
        )
        self.update_button.place(relx=0.57, rely=0.25)

        # Status text
        self.firmware_text = tk.Label(
            master=self,
            text="Updated",
            font=("Arial", 26),
            fg="black"
        )
        self.firmware_text.place(relx=0.71, rely=0.25)

        # Indicator
        self.firmware_indicator = tk.Label(
            master=self,
            text=self.status_light,
            font=("Arial", 42),
            fg="red"
        )
        self.firmware_indicator.place(relx=0.925, rely=0.225)

        Tooltip(
            widget=self.firmware_indicator,
            text="Shows whether the router has the selected firmware version." \
            "\nGreen = firmware on router matches selected version." \
            "\nRed = different version or not connected." \
            "\nTip: select the correct firmware first, then check this light."
        )

        self.refresh_firmware()


    def refresh_firmware(self):
        selected = FIRMWARE_LIST[self.select_firmware.current()]
        if self.router.is_connected() and self.router.is_router_updated(selected["Version"]):
            self.firmware_indicator.config(fg="green")
        else:
            self.firmware_indicator.config(fg="red")
        self.after(1000, self.refresh_firmware)


    def start(self):
        self.screen_separation()
        self.name_label()

        self.firmware_selection()
        self.isp_selection()
        self.provider_selection()
        self.apn_selection()

        self.new_password_entry()
        self.default_password_entry()
        self.router_ip_entry()

        self.active_status()
        self.connect_status()
        self.firmware_status()

        self.mainloop()


if __name__ == "__main__":
    router = Router()
    app = App(router)
    app.start()


# NOT FINISHED