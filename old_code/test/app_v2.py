import customtkinter as ctk
import tkinter as tk
import old_code.test.config as cfg
import json


# Firmware, ISP and APN
with open("config.json") as file:
    data = json.load(file)

FIRMWARE_LIST = data["FIRMWARE_LIST"]
ISP_PROFILE_LIST = data["ISP_PROFILE_LIST"]
APN_LIST = data["APN_LIST"]





class Test(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("ARCTIC_V2")
        self.geometry("1080x720")
        self.columnconfigure(0, weight=5)
        self.columnconfigure(1, weight=3)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

#-------------------------------------------------------------
#   FRAMES
#-------------------------------------------------------------
        
    def create_frames(self):
        self.connection_frame = ctk.CTkFrame(
            master=self,
            fg_color=("#BBBBBB","#333333"),
            border_color=("#888888","#444444"),
            border_width=2, corner_radius=20
        )
        self.connection_frame.grid(
            row=0, column=0,
            padx=(10, 5), pady=(10, 5),
            sticky='nsew'
        )
        self.connection_frame.columnconfigure(0, weight=5)
        self.connection_frame.columnconfigure(1, weight=1)
        self.connection_frame.columnconfigure(2, weight=7)
        self.connection_frame.columnconfigure(3, weight=2)
        self.connection_frame.rowconfigure(0, weight=1)
        self.connection_frame.rowconfigure(1, weight=1)
        self.connection_frame.rowconfigure(2, weight=1)
        self.connection_frame.grid_propagate(False)


        self.configuration_frame = ctk.CTkFrame(
            master=self,
            fg_color=("#BBBBBB","#333333"),
            border_color=("#888888","#444444"),
            border_width=2, corner_radius=20
        )
        self.configuration_frame.grid(
            row=1, column=0,
            padx=(10, 5), pady=(5, 10),
            sticky='nsew'
        )

        self.status_frame = ctk.CTkFrame(
            master=self,
            fg_color=("#BBBBBB","#333333"),
            border_color=("#888888","#444444"),
            border_width=2, corner_radius=20
        )
        self.status_frame.grid(
            row=0, column=1,
            padx=(5, 10), pady=10,
            sticky='nsew',
            rowspan=2
        )

#-------------------------------------------------------------
#   TOOLTIPS
#-------------------------------------------------------------

    def create_tooltip(self, master, tooltip_text, size=24):
        tooltip_icon = ctk.CTkLabel(
            master=master, text="?",
            width=size, height=size,
            corner_radius=6,
            fg_color=("#3B8ED0", "#1F6AA5"),
            text_color="white",
            font=("Arial", int(size*0.6), "bold"),
            cursor="arrow"
        )
        tooltip = None

        def show(event):
            nonlocal tooltip
            if tooltip: return
            
            tooltip = tk.Toplevel(tooltip_icon)
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{tooltip_icon.winfo_rootx() + size + 5}+{tooltip_icon.winfo_rooty()}")
            tooltip.configure(bg="#000001")
            tooltip.wm_attributes("-transparentcolor", "#000001")
            
            tooltip_label = ctk.CTkLabel(
                master=tooltip, text=tooltip_text, corner_radius=8,
                fg_color=("#FFFFFF", "#2B2B2B"),
                text_color=("#000000", "#FFFFFF"),
                border_color=("#888888", "#444444"),
                border_width=1, padx=10, pady=8,
                font=("Arial", 11)
            )
            tooltip_label.pack()

        def hide(event):
            nonlocal tooltip
            if tooltip:
                tooltip.destroy()
                tooltip = None

        tooltip_icon.bind("<Enter>", show)
        tooltip_icon.bind("<Leave>", hide)
        return tooltip_icon

#-------------------------------------------------------------
#   CONNECTION
#-------------------------------------------------------------

    def create_new_password(self):
        self.new_password_label = ctk.CTkLabel(
            master=self.connection_frame,
            text=cfg.NEW_PASSWORD_LABEL,
            fg_color="transparent",
            font=("Courier New", 28, "bold")
        )
        
        self.new_password_tooltip = self.create_tooltip(
            master=self.connection_frame, 
            tooltip_text=cfg.NEW_PASSWORD_TOOLTIP
        )

        self.new_password_cbox = ctk.CTkComboBox(
            master=self.connection_frame,
            values=["admin01",],
            font=("Arial", 24)
        )

        self.new_password_label.grid(
            row=0, column=0,
            padx=(15, 5), pady=(10, 5),
            sticky="w")
        self.new_password_tooltip.grid(
            row=0, column=1,
            padx=(5, 5), pady=(10, 5),
            sticky="we")
        self.new_password_cbox.grid(
            row=0, column=2,
            padx=(5, 5), pady=(10, 5),
            sticky="we")
        
    
    def create_def_password(self):
        self.def_password_label = ctk.CTkLabel(
            master=self.connection_frame,
            text=cfg.DEFAULT_PASSWORD_LABEL,
            fg_color="transparent",
            font=("Courier New", 28, "bold")
        )
        
        self.def_password_tooltip = self.create_tooltip(
            master=self.connection_frame, 
            tooltip_text=cfg.DEFAULT_PASSWORD_TOOLTIP
        )

        self.def_password_cbox = ctk.CTkComboBox(
            master=self.connection_frame,
            values=["admin01", "Start2026!"],
            font=("Arial", 20)
        )

        self.def_password_label.grid(
            row=1, column=0,
            padx=(15, 5), pady=(5, 5),
            sticky="w")
        self.def_password_tooltip.grid(
            row=1, column=1,
            padx=(5, 5), pady=(5, 5),
            sticky="we")
        self.def_password_cbox.grid(
            row=1, column=2,
            padx=(5, 5), pady=(5, 5),
            sticky="we")


    def create_ip_entry(self):
        self.ip_label = ctk.CTkLabel(
            master=self.connection_frame,
            text=cfg.ROUTER_IP_LABEL,
            fg_color="transparent",
            font=("Courier New", 28, "bold")
        )
        
        self.ip_tooltip = self.create_tooltip(
            master=self.connection_frame, 
            tooltip_text=cfg.ROUTER_IP_TOOLTIP
        )

        ip_list = [item["IP"] for item in ISP_PROFILE_LIST]
        self.ip_cbox = ctk.CTkComboBox(
            master=self.connection_frame,
            values=ip_list,
            font=("Arial", 20)
        )

        self.ip_label.grid(
            row=2, column=0,
            padx=(15, 5), pady=(5, 10),
            sticky="w")
        self.ip_tooltip.grid(
            row=2, column=1,
            padx=(5, 5), pady=(5, 10),
            sticky="we")
        self.ip_cbox.grid(
            row=2, column=2,
            padx=(5, 5), pady=(5, 10),
            sticky="we")


    def create_connect_button(self):
        self.connect_button = ctk.CTkButton(
            master=self.connection_frame,
            text=cfg.CONNECT_BUTTON, font=("Arial", 30),
            fg_color=("#CCCCCC","#444444"),
            text_color=("#000000","#FFFFFF"),
            border_color=("#888888","#222222"),
            hover_color=("#777777", "#888888"),
            border_width=2, corner_radius=20
        )

        self.connect_button.grid(
            row=0, column=3, rowspan=3,
            padx=(5, 10), pady=(10, 10),
            sticky="ns"
        )

#-------------------------------------------------------------
#   CONFIGURATION
#-------------------------------------------------------------

    def start(self):
        self.create_frames()
        self.create_new_password()
        self.create_def_password()
        self.create_ip_entry()
        self.create_connect_button()
        self.mainloop()

if __name__ == "__main__":
    test = Test()
    test.start()
