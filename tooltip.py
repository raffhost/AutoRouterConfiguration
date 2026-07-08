import tkinter as tk


class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        widget.bind("<Enter>", self.show)  # when mouse cursor on widget
        widget.bind("<Leave>", self.hide)  # opposite of last one

    def show(self, event=None):
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + 20
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)  # without window frame
        self.tooltip.wm_geometry(f"+{x}+{y}")
        tk.Label(
            self.tooltip,
            text=self.text,
            background="white",
            relief="solid",
            borderwidth=1,
            font=("Arial", 12)
        ).pack()

    def hide(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None
