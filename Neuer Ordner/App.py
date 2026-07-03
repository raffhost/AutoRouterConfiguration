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
        self.cut_horiz_m2.place(relx=0.01, rely=0.5, relwidth=0.50, anchor="sw")

    def name_label(self):
        # Create a main label
        self.label = tk.Label(master=self, text=conf.NAMELABEL_TEXT, font=conf.FONT_A28)
        self.label.place(relx=0.01, rely=0.03, anchor="nw")

    def firmware_selection(self):
        self.fm_label = tk.Label(master=self, text=conf.FIRMWARE_TEXT, font=conf.FONT_A16)
        self.fm_label.place(relx=0.01, rely=0.20)

        self.select_fm = ttk.Combobox(master=self, values=conf.FIRMWARE_LIST, font=conf.FONT_A16)
        self.select_fm.place(relx=0.25, rely=0.20)

    def isp_selection(self):
        # This function is going to be used to select the isp
        self.isp_label = tk.Label(master=self, text=conf.ISP_TEXT, font=conf.FONT_A16)
        self.isp_label.place(relx=0.01, rely=0.30)

        self.select_isp = ttk.Combobox(master=self, values=conf.ISP_LIST, font=conf.FONT_A16)
        self.select_isp.place(relx=0.25, rely=0.30)

        self.show_ip = tk.Label(master=self, text=f"# IP = {self.get_ip()}", font=conf.FONT_A8)
        self.show_ip.place(relx=0.25, rely=0.345)

        self.select_isp.bind("<<ComboboxSelected>>", self.update_ip)

    def apn_selection(self):
        self.apn_label = tk.Label(master=self, text=conf.APN_TEXT, font=conf.FONT_A16)
        self.apn_label.place(relx=0.01, rely=0.40)

        self.select_apn = ttk.Combobox(master=self, values=conf.APN_LIST, font=conf.FONT_A16)
        self.select_apn.place(relx=0.25, rely=0.40)

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
        self.apn_selection()
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
class Configuration:
    def __init__(self):
        pass

    def update_firmware(self):
        #Code to update firmware
        pass

    def change_password(self):
        #Code to change password
        pass

    def select_apn_model(self):
        #Code to select apn model
        pass


# NOT FINISHED