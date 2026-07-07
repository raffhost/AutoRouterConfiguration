import tkinter as tk
import tkinter.ttk as ttk
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
        self.cut_verti = ttk.Separator(
            master=self,
            orient="vertical"
        )
        self.cut_verti.place(
            relx=0.75,
            rely=0,
            relheight=1,
            anchor="ne"
        )

        # Create a horizontal separator for status and output
        self.cut_horiz = ttk.Separator(
            master=self,
            orient="horizontal"
        )
        self.cut_horiz.place(
            relx=1,
            rely=0.8,
            relwidth=0.25,
            anchor="se"
        )

        # Create a horizontal separator inbetween label and selections
        self.cut_horiz_m1 = ttk.Separator(
            master=self,
            orient="horizontal"
        )
        self.cut_horiz_m1.place(
            relx=0.01,
            rely=0.15,
            relwidth=0.50,
            anchor="sw"
        )

        # Create a horizontal separator inbetween selections and passwords
        self.cut_horiz_m2 = ttk.Separator(
            master=self,
            orient="horizontal"
        )
        self.cut_horiz_m2.place(
            relx=0.01,
            rely=0.52,
            relwidth=0.50,
            anchor="sw"
        )


    def name_label(self):
        # Create a main label
        self.label = tk.Label(
            master=self,
            text="Auto Router Configuration Tool",
            font=("Arial", 28)
        )
        self.label.place(
            relx=0.01,
            rely=0.03,
            anchor="nw"
        )


    def firmware_selection(self):
        self.fm_label = tk.Label(
            master=self,
            text="Select Firmware",
            font=("Arial", 16)
        )
        self.fm_label.place(
            relx=0.01,
            rely=0.20
        )

        firmware_list = [item["Name"] for item in FIRMWARE_LIST]
        self.select_fm = ttk.Combobox(
            master=self,
            values=firmware_list,
            font=("Arial", 16)
        )
        self.select_fm.place(
            relx=0.25,
            rely=0.20
        )


    def isp_selection(self):
        # This function is going to be used to select the isp
        self.isp_label = tk.Label(
            master=self,
            text="Select ISP Profile",
            font=("Arial", 16)
        )
        self.isp_label.place(
            relx=0.01,
            rely=0.30
        )


        isp_list = [item["ISP"] for item in ISP_PROFILE_LIST]
        self.select_isp = ttk.Combobox(
            master=self,
            values=isp_list,
            font=("Arial", 16)
        )
        self.select_isp.place(
            relx=0.25,
            rely=0.30
        )

        self.show_ip = tk.Label(
            master=self,
            text=f"# IP = {self.get_ip()}",
            font=("Arial", 8)
        )
        self.show_ip.place(
            relx=0.25,
            rely=0.345
        )

        self.select_isp.bind("<<ComboboxSelected>>", self.update_ip)


    def provider_selection(self):
        self.apn_label = tk.Label(
            master=self,
            text="Select Provider",
            font=("Arial", 16)
        )
        self.apn_label.place(
            relx=0.01,
            rely=0.40
        )

        provider_list = [list(item.keys())[0] for item in PROVIDER_LIST]
        self.select_provider = ttk.Combobox(
            master=self,
            values=provider_list,
            font=("Arial", 16)
        )
        self.select_provider.place(
            relx=0.25,
            rely=0.40
        )

        self.select_provider.bind("<<ComboboxSelected>>", self.apn_selection)


    def apn_selection(self, event=None):
        self.apn_label = tk.Label(
            master=self,
            text="Select APN",
            font=("Arial", 16)
        )
        self.apn_label.place(
            relx=0.01,
            rely=0.46
        )

        selected_provider = self.select_provider.get()
        provider_data = next(item for item in PROVIDER_LIST if selected_provider in item)
        apn_list = [entry["APN"] for entry in provider_data[selected_provider]]

        self.select_apn = ttk.Combobox(
            master=self,
            values=apn_list,
            font=("Arial", 16)
        )
        self.select_apn.place(
            relx=0.25,
            rely=0.46
        )


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
        self.show_ip.configtext=f"# IP = {self.get_ip()}"


    def status(self):
        self.status_light = tk.Label(
            master=self,
            text="●",
            font=("Arial", 28),
            fg="red"
        )
        self.status_light.place(
            relx=0.77,
            rely=0.05
        )  

        self.after(1000, self.update_status)


    def update_status(self):
        if self.router.is_connected():
            self.status_light.config(fg="green")
        else:
            self.status_light.config(fg="red")
        

    def default_password_entry(self):
        self.def_pw_label = tk.Label(
            master=self,
            text="Password",
            font=("Arial", 20)
        )
        self.def_pw_label.place(
            relx=0.01,
            rely=0.70
        )

        self.def_pw = tk.Entry(
            master=self,
            font=("Arial", 20)
        )
        self.def_pw.insert(0, "admin01")
        self.def_pw.place(
            relx=0.138,
            rely=0.70
        )

    def connect_button(self):
        # Button to connect to the router
        self.con_button = tk.Button(
            master=self,
            text="Connect",
            font=("Arial", 24),
            command=lambda: self.router.connect(
                def_pw="Pils2018"
            )
        )
        self.con_button.place(
            relx=0.05,
            rely=0.80
        )


    def update_button(self):
        if self.router.is_connected() == False:
            self.connect_button()

        # Button to update the router
        self.upd_button = tk.Button(
            master=self,
            text="Update",
            font=("Arial", 24),
            command=self.router.update
        )
        self.upd_button.place(
            relx=0.30,
            rely=0.80
        )


    def start(self):
        self.screen_separation()
        self.name_label()
        
        self.firmware_selection()
        self.isp_selection()
        self.provider_selection()

        self.default_password_entry()

        self.connect_button()
        self.update_button()

        self.status()
        self.mainloop()




if __name__ == "__main__":
    router=Router()
    app = App(router)
    app.start()


# NOT FINISHED