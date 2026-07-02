import tkinter as tk
import tkinter.ttk as ttk
import config as conf


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(conf.TITLE)
        self.geometry(conf.GEOMETRY)
        # 12 rows and 8 columns for the grid layout
        for row in range(conf.ROWS):
            self.rowconfigure(row, weight=1)
        for column in range(conf.COLUMNS):
            self.columnconfigure(column, weight=1)


    def create_label(self):
        # Basic Label
        self.label = tk.Label(
            master=self,
            text=conf.LABEL_TEXT,
            font=conf.FONT_A24
        )
        # columnspan=2 so it stays centered above both columns
        self.label.grid(row=0, column=3)

    def apn_model_selection(self):
        # This function is going to be used to select the apn model
        self.select_apn = ttk.Combobox(
            master=self,
            values=conf.APN_LIST,
            font=conf.FONT_A16,
        )
        # columnspan=2 so the combobox spans the full width like the label
        self.select_apn.grid(row=4, column=3, sticky="ew")

    def create_buttons(self):
        # A Button to update firmware, employ new password and select apn model
        self.button_cfg = tk.Button(
            master=self,
            text="Configuration",
            font=conf.FONT_A20,
            command=self.on_configuration_button_click
        )
        self.button_cfg.grid(row=11, column=2, sticky="ew")

        self.button_status = tk.Button(
            master=self,
            text="Status",
            font=conf.FONT_A20,
            command=self.on_status_button_click
        )
        self.button_status.grid(row=11, column=4, sticky="ew")

    def password_entry(self):
        # Placeholder for future password entry field
        self.password_entry = tk.Entry(
            master=self,
            show="*",
            font=conf.FONT
        )
        self.password_entry.grid(row=6, column=3, columnspan=2, sticky="ew")

    def on_configuration_button_click(self):
        # CFG commands are going to be executed here through other class
        self.configuration = Configuration()
        self.configuration.update_firmware()
        self.configuration.change_password()
        self.configuration.select_apn_model()

    def on_status_button_click(self):
        # Status commands are going to be executed here through other class
        pass

    def create_entry(self):
        # Placeholder for future input fields (e.g. password entry)
        pass

    def start(self):
        self.create_label()
        self.apn_model_selection()
        self.create_buttons()
        self.mainloop()


#Here is going to be the main class for the Configuration commands.
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


if __name__ == "__main__":
    app = App()
    app.start()



# NOT FINISHED