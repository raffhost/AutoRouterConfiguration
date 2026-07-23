# Handles everything related to text output: receiving log messages from
# ANY thread (main thread or background threads) and safely displaying
# them in the GUI.
#
# Two separate queues, because they solve two different problems:
# - log_queue: plain text messages to display in the log window
# - gui_queue: actual GUI-changing function calls (e.g. changing a
#   label's color) that are only allowed to run on the main thread
#
# This class does NOT use TaskQueue/threading.Thread - it is only ever
# drained via root.after(), i.e. from inside the tkinter mainloop.

import queue
from datetime import datetime


#-----------------------------
#       ARCTIC LOG
#-----------------------------

class ArcticLog():
    def __init__(self, text_widget):
        self.text_widget = text_widget
        self.log_queue = queue.Queue()
        self.gui_queue = queue.Queue()


    # def put_log(self, message):
    #     # Called from ANY thread to queue a text message for the log window.
    #     time = datetime.now().strftime("%H:%M:%S")
    #     self.log_chat.config(state="normal")
    #     self.log_chat.insert("end", f"[{time}] | {message}\n")
    #     self.log_chat.see("end")
    #     self.log_chat.config(state="disabled")
    #     pass

    def put_gui(self, func):
        # Called from ANY thread to queue a function that changes the GUI
        # (e.g. lambda: label.config(fg="green")).
        pass

    def process_queues(self):
        # Called repeatedly via root.after(...) - MAIN THREAD ONLY.
        # Drains both queues and applies everything safely.
        pass

    def _write(self, message):
        # Actually inserts text into the Text widget (with timestamp).
        # Main thread only - never call this directly from a background thread.
        pass