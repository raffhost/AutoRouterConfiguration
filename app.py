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


    def screen_separation(self):
        # Create a vertical separator for status and output
        self.cut_vertikal = ttk.Separator(
            master=self,
            orient="vertical"
        )
        self.cut_vertikal.place(
            relx=0.75,
            rely=0,
            relheight=1,
            anchor="ne"
        )

        # Create a horizontal separator for status and output
        self.cut_horizontal = ttk.Separator(
            master=self,
            orient="horizontal"
        )
        self.cut_horizontal.place(
            relx=1,
            rely=0.8,
            relwidth=0.25,
            anchor="se"
        )

        # Create a horizontal separator inbetween label and selections
        self.cut_horizontal_m1 = ttk.Separator(
            master=self,
            orient="horizontal"
        )
        self.cut_horizontal_m1.place(
            relx=0.01,
            rely=0.15,
            relwidth=0.50,
            anchor="sw"
        )

        # Create a horizontal separator inbetween selections and passwords
        self.cut_horizontal_m2 = ttk.Separator(
            master=self,
            orient="horizontal"
        )
        self.cut_horizontal_m2.place(
            relx=0.01,
            rely=0.60,
            relwidth=0.50,
            anchor="sw"
        )


    def name_label(self):
        # Create a main label
        self.label = tk.Label(
            master=self,
            text="Auto Router Configuration Tool",
            font=("Arial", 28, "bold")

        )
        self.label.place(
            relx=0.01,
            rely=0.03,
            anchor="nw"
        )


    def firmware_selection(self):
        self.firmware_label = tk.Label(
            master=self,
            text="Select Firmware",
            font=("Arial", 20)
        )
        self.firmware_label.place(
            relx=0.01,
            rely=0.20
        )

        firmware_list = [item["Name"] for item in FIRMWARE_LIST]
        self.select_firmware = ttk.Combobox(
            master=self,
            values=firmware_list,
            font=("Arial", 20)
        )
        self.select_firmware.place(
            relx=0.25,
            rely=0.20
        )



    def isp_selection(self):
        # This function is going to be used to select the isp
        self.isp_label = tk.Label(
            master=self,
            text="Select ISP Profile",
            font=("Arial", 20)
        )
        self.isp_label.place(
            relx=0.01,
            rely=0.30
        )


        isp_list = [item["ISP"] for item in ISP_PROFILE_LIST]
        self.select_isp = ttk.Combobox(
            master=self,
            values=isp_list,
            font=("Arial", 20)
        )
        self.select_isp.place(
            relx=0.25,
            rely=0.30
        )


        self.show_ip = tk.Label(
            master=self,
            text=f"# IP = {self.get_ip()}",
            font=("Arial", 10)
        )
        self.show_ip.place(
            relx=0.25,
            rely=0.355
        )

        self.select_isp.bind("<<ComboboxSelected>>", self.update_ip)


    def provider_selection(self):
        self.apn_label = tk.Label(
            master=self,
            text="Select Provider",
            font=("Arial", 20)
        )
        self.apn_label.place(
            relx=0.01,
            rely=0.40
        )

        provider_list = [list(item.keys())[0] for item in PROVIDER_LIST]
        self.select_provider = ttk.Combobox(
            master=self,
            values=provider_list,
            font=("Arial", 20)
        )
        self.select_provider.place(
            relx=0.25,
            rely=0.40
        )

        self.select_provider.bind("<<ComboboxSelected>>", self.update_apn_list)


    def apn_selection(self):
        self.apn_label = tk.Label(
            master=self,
            text="Select APN",
            font=("Arial", 20)
        )
        self.apn_label.place(
            relx=0.01,
            rely=0.50
        )

        self.select_apn = ttk.Combobox(
            master=self,
            font=("Arial", 20)
        )
        self.select_apn.place(
            relx=0.25,
            rely=0.50
        )
    

    def update_apn_list(self, event=None):
        selected_provider = self.select_provider.get()
        provider_data = next(item for item in PROVIDER_LIST if selected_provider in item)
        apn_list = [entry["APN"] for entry in provider_data[selected_provider]]
        self.select_apn.config(values=apn_list)
        self.select_apn.set(apn_list[0])


    def get_ip(self): # doesn't function for now
        isp = self.select_isp.get()
        if isp == "ISP 1":
            return "192.168.5.1"
        elif isp == "ISP 2":
            return "192.168.6.1"
        elif isp == "ISP 3":
            return "192.168.7.1"
        elif isp == "ISP 4":
            return "192.168.8.1"
        else:
            return "192.168.1.1"


    def update_ip(self, event=None):
        self.show_ip.config(text=f"# IP = {self.get_ip()}")


    def router_status(self):  
        self.router_status_text = tk.Label(
            master=self,
            text="Active",
            font=("Arial", 28),
            fg="black"
        )
        self.router_status_text.place(
            relx=0.76,
            rely=0.05
        )

        self.router_status_light = tk.Label(
            master=self,
            text="●",
            font=("Arial", 28),
            fg="red"
        )
        self.router_status_light.place(
            relx=0.96,
            rely=0.05
        )
        self.update_router_status()


    def update_router_status(self):
        if self.router.is_connected():
            self.router_status_light.config(fg="green")
        else:
            self.router_status_light.config(fg="red")

        self.after(1000, self.update_router_status)


    def connection_status(self):
        self.connection_status_text = tk.Label(
            master=self,
            text="Connected",
            font=("Arial", 28),
            fg="black"
        )
        self.connection_status_text.place(
            relx=0.76,
            rely=0.15
        )

        self.connection_status_light = tk.Label(
            master=self,
            text="●",
            font=("Arial", 28),
            fg="red"
        )
        self.connection_status_light.place(
            relx=0.96,
            rely=0.15
        )
        self.update_connection_status()


    def update_connection_status(self):
        if self.router.is_router_active():
            self.connection_status_light.config(fg="green")
        else:
            self.connection_status_light.config(fg="red")

        self.after(1000, self.update_connection_status)


    def firmware_status(self):
        self.firmware_status_text = tk.Label(
            master=self,
            text="Updated",
            font=("Arial", 28),
            fg="black"
        )
        self.firmware_status_text.place(
            relx=0.76,
            rely=0.25
        )

        self.firmware_status_light = tk.Label(
            master=self,
            text="●",
            font=("Arial", 28),
            fg="red"
        )
        self.firmware_status_light.place(
            relx=0.96,
            rely=0.25
        )
        self.update_firmware_status()


    def update_firmware_status(self):
        selected = FIRMWARE_LIST[self.select_firmware.current()]
        
        if self.router.is_connected() and self.router.is_router_updated(selected["Version"]):
            self.firmware_status_light.config(fg="green")
        else:
            self.firmware_status_light.config(fg="red")

        self.after(1000, self.update_firmware_status)


    def new_password_entry(self):
        self.new_password_label = tk.Label(
            master=self,
            text="Password",
            font=("Arial", 20)
        )
        self.new_password_label.place(
            relx=0.01,
            rely=0.62
        )
        
        self.new_password= tk.Entry(
            master=self,
            font=("Arial", 20)
        )
        self.new_password.insert(
            0, "admin01"
        )
        self.new_password.place(
            relx=0.138,
            rely=0.62
        )

        self.new_password_help = tk.Label(
            master=self,
            text="?",
            font=("Arial", 16),
            fg="gray"
        )
        self.new_password_help.place(
            relx=0.43,
            rely=0.625
        )
        Tooltip(
            widget=self.new_password_help,
            text="New router password\nWrite one to change it"
        )


    def default_password_entry(self):
        self.default_password_label = tk.Label(
            master=self,
            text="Password",
            font=("Arial", 20)
        )
        self.default_password_label.place(
            relx=0.01,
            rely=0.72
        )
        
        self.default_password= tk.Entry(
            master=self,
            font=("Arial", 20)
        )
        self.default_password.insert(
            0, "admin01"
        )
        self.default_password.place(
            relx=0.138,
            rely=0.72
        )

        self.default_password_help = tk.Label(
            master=self,
            text="?",
            font=("Arial", 16),
            fg="gray"
        )
        self.default_password_help.place(
            relx=0.43,
            rely=0.725
        )
        Tooltip(
            widget=self.default_password_help,
            text="Default router password\nUsually admin01 after factory reset"
        )


    def connect_button(self):
        # Button to connect to the router
        self.con_button = tk.Button(
            master=self,
            text="Connect",
            font=("Arial", 24),
            command=lambda: self.router.connect(
                default_password=self.default_password.get()
            )
        )
        self.con_button.place(
            relx=0.01,
            rely=0.90
        )


    def update_button(self):
        if self.router.is_connected() == False:
            self.connect_button()

        # Button to update the router
        self.upd_button = tk.Button(
            master=self,
            text="Update",
            font=("Arial", 24),
            command=lambda: self.router.update(
                firmware_path=FIRMWARE_LIST[self.select_firmware.current()]["PATH"]
            )
        )
        self.upd_button.place(
            relx=0.21,
            rely=0.90
        )


    def start(self):
        self.screen_separation()
        self.name_label()
        
        self.firmware_selection()
        self.isp_selection()
        self.provider_selection()
        self.apn_selection()

        self.new_password_entry()
        self.default_password_entry()

        self.connect_button()
        self.update_button()

        self.router_status()
        self.connection_status()
        self.firmware_status()
        
        self.mainloop()




if __name__ == "__main__":
    router=Router()
    app = App(router)
    app.start()


# NOT FINISHED