import tkinter as tk
import tkinter.ttk as ttk
import Config as cfg
import RMS as rms

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ARCT")
        self.geometry("800x600")
        self.resizable(False, False)

    def create_label(self):
        #Basic Label
        self.label = tk.Label(
            master=self, 
            text="Auto Router Configuration Tool", 
            font=("Arial", 28)
        )
        self.label.place(x=100, y=50)
    
    def apn_model_selection(self):
        #This function is going to be used to select the apn model
        self.select_apn = ttk.Combobox(
            master=self,
            values=["APN 1", "APN 2", "APN 3", "APN 4"],
            font=("Arial", 16),

        )
        self.select_apn.grid()

    def create_buttons(self):
        #A Button to update firmware, employ new password and select apn model
        self.button_cfg = tk.Button(
            master=self, 
            text="Configuration", 
            command=self.on_cfg_button_click
        )
        self.button_cfg.place(x=200, y=750)

        #rms for later use
        self.button_rms = tk.Button(
            master=self,
            text="RMS",
            command=self.on_rms_button_click
        )
        self.button_rms.place(x=400, y=750)
    
    def on_cfg_button_click(self):
        #CFG commands are goind to be executed here through other class
        self.cfg = cfg.Configuration()
        pass

    def on_rms_button_click(self):
        #RMS commands are going to be executed here through other class
        self.rms = rms.RMS()
        pass

    def create_entry(self):
        pass

    def start(self):
        self.create_label()
        self.apn_model_selection()
        self.create_buttons()
        self.mainloop()
        

if __name__ == "__main__":
    app = App()
    app.start()



    