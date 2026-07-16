import customtkinter as ctk
import json
import tkinter as tk


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
        
    def create_frames(self):
        self.connection_frame = ctk.CTkFrame(
            master=self,
            fg_color="#333333",
            border_color="#000000",
            border_width=2
        )
        self.connection_frame.grid(
            sticky="w",

            padx=10,
            pady=5
        )
        self.configuration_frame = ctk.CTkFrame(
            master=self,
            fg_color="#333333",
            border_color="#000000",
            border_width=2
        )
        self.configuration_frame.grid(
            sticky="w",

            padx=10,
            pady=5
        )

        self.status_frame = ctk.CTkFrame(
            master=self,
            fg_color="#333333",
            border_color="#000000",
            border_width=2
        )
        self.status_frame.grid(
            sticky="e",

            padx=10,
            pady=5
        )

    def start(self):
        self.create_frames()
        self.mainloop()

if __name__ == "__main__":
    test = Test()
    test.start()
