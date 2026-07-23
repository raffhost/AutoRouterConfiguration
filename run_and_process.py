# Здесь должны обрабатываться ВСЕ процессы по очереди друг за другом если иначе никак.
import threading
import queue





#-----------------------------
#       RUN AND PROCESS
#-----------------------------

class RunAndProcess():
    def __init__(self):
        # Start a single background queue thread
        self._queue()
        threading.Thread(target=self._queue, daemon=True).start()

    #--------------------------
    #       QUEUE SYSTEM
    #--------------------------

    def _queue(self):
        pass

    def add_task_queue(self):
        pass

    def clear_task_queue(self):
        pass

    def is_queue_busy(self):
        pass
