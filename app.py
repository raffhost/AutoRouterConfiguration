import tkinter as tk
import tkinter.ttk as ttk
import config as conf
import router as rtr


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(conf.TITLE)
        self.geometry(conf.GEOMETRY)
        self.resizable(False, False)  # Disable window resizing

    def screen_separation(self):
        # Create a vertical separator for status and output
        self.cut_verti = ttk.Separator(master=self, orient="vertical")
        self.cut_verti.place(relx=0.75, rely=0, relheight=1, anchor="ne")

        # Create a horizontal separator for status and output
        self.cut_horiz = ttk.Separator(master=self, orient="horizontal")
        self.cut_horiz.place(relx=1, rely=0.8, relwidth=0.25, anchor="se")
            
        # Create a horizontal separator inbetween label and selections
        self.cut_horiz_m1 = ttk.Separator(master=self, orient="horizontal")
        self.cut_horiz_m1.place(relx=0.01, rely=0.15, relwidth=0.50, anchor="sw")

        # Create a horizontal separator inbetween selections and passwords
        self.cut_horiz_m2 = ttk.Separator(master=self, orient="horizontal")
        self.cut_horiz_m2.place(relx=0.01, rely=0.52, relwidth=0.50, anchor="sw")

    def name_label(self):
        # Create a main label
        self.label = tk.Label(master=self, text=conf.NAMELABEL_TEXT, font=conf.FONT_A28)
        self.label.place(relx=0.01, rely=0.03, anchor="nw")

    def firmware_selection(self):
        self.fm_label = tk.Label(master=self, text=conf.FIRMWARE_TEXT, font=conf.FONT_A16)
        self.fm_label.place(relx=0.01, rely=0.20)

        firmware_list = [item["Name"] for item in conf.FIRMWARE_LIST]
        self.select_fm = ttk.Combobox(master=self, values=firmware_list, font=conf.FONT_A16)
        self.select_fm.place(relx=0.25, rely=0.20)

    def isp_selection(self):
        # This function is going to be used to select the isp
        self.isp_label = tk.Label(master=self, text=conf.ISP_TEXT, font=conf.FONT_A16)
        self.isp_label.place(relx=0.01, rely=0.30)

        isp_list = [item["ISP"] for item in conf.ISP_PROFILE_LIST]
        self.select_isp = ttk.Combobox(master=self, values=isp_list, font=conf.FONT_A16)
        self.select_isp.place(relx=0.25, rely=0.30)

        self.show_ip = tk.Label(master=self, text=f"# IP = {self.get_ip()}", font=conf.FONT_A8)
        self.show_ip.place(relx=0.25, rely=0.345)

        self.select_isp.bind("<<ComboboxSelected>>", self.update_ip)

    def provider_selection(self):
        self.apn_label = tk.Label(master=self, text=conf.PROVIDER_TEXT, font=conf.FONT_A16)
        self.apn_label.place(relx=0.01, rely=0.40)

        provider_list = [list(item.keys())[0] for item in conf.PROVIDER_LIST]
        self.select_provider = ttk.Combobox(master=self, values=provider_list, font=conf.FONT_A16)
        self.select_provider.place(relx=0.25, rely=0.40)

        self.select_provider.bind("<<ComboboxSelected>>", self.tarif_selection)


    def tarif_selection(self, event=None):
        self.apn_label = tk.Label(master=self, text=conf.PROVIDER_TEXT, font=conf.FONT_A16)
        self.apn_label.place(relx=0.01, rely=0.45)
        
        selected_provider = self.select_provider.get()
        provider_data = next(item for item in conf.PROVIDER_LIST if selected_provider in item)
        apn_list = [entry["Tarif"] for entry in provider_data[selected_provider]]

        self.select_tarif = ttk.Combobox(master=self, values=apn_list, font=conf.FONT_A16)
        self.select_tarif.place(relx=0.25, rely=0.45)


    def get_ip(self):
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

    def start(self):
        self.screen_separation()
        self.name_label()
        self.firmware_selection()
        self.isp_selection()
        self.provider_selection()
        self.mainloop()



if __name__ == "__main__":
    app = App()
    app.start()


# NOT FINISHED
#     def apn_selection(self):
#         # This function is going to be used to select the apn
#         self.select_apn = ttk.Combobox(
#             master=self,
#             values=conf.APN_LIST,
#             font=conf.FONT_A16,
#         )
#         # columnspan=2 so the combobox spans the full width like the label
#         self.select_apn.grid(row=4, column=3, sticky="ew")

#     def create_buttons(self):
#         # A Button to update firmware, employ new password and select apn model
#         self.button_cfg = tk.Button(
#             master=self,
#             text="Configuration",
#             font=conf.FONT_A20,
#             command=self.on_configuration_button_click
#         )
#         self.button_cfg.grid(row=11, column=2, sticky="ew")

#         self.button_status = tk.Button(
#             master=self,
#             text="Status",
#             font=conf.FONT_A20,
#             command=self.on_status_button_click
#         )
#         self.button_status.grid(row=11, column=4, sticky="ew")

#     def password_entry(self):
#         # Placeholder for future password entry field
#         self.password_entry = tk.Entry(
#             master=self,
#             show="*",
#             font=conf.FONT
#         )
#         self.password_entry.grid(row=6, column=3, columnspan=2, sticky="ew")

#     def on_configuration_button_click(self):
#         # CFG commands are going to be executed here through other class
#         self.configuration = Configuration()
#         self.configuration.update_firmware()
#         self.configuration.change_password()
#         self.configuration.select_apn_model()

#     def on_status_button_click(self):
#         # Status commands are going to be executed here through other class
#         pass

#Main class for the Configuration commands.