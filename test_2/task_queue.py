# Central, reusable queue for background tasks.
# Process tasks sequentially (never in parallel)

import threading
import queue


#-----------------------------
#       TASK QUEUE
#-----------------------------

class TaskQueue:
    def __init__(self):
        self.task_queue = queue.Queue()
        self.threading_busy = threading.Event()

        # A single background thread processes the queue sequentially.
        threading.Thread(target=self._worker, daemon=True).start()


    #--------------------------
    #       QUEUE SYSTEM
    #--------------------------

    def add_task(self, func, *args, on_done=None, **kwargs):
        # Adds a task to the queue. on_done is called AFTER successful execution 
        # with the return value of function. This serves as the signal: "done, ready for the next command".
        self.threading_busy.set()
        self.task_queue.put((func, args, kwargs, on_done))


    def _worker(self):
        while True:
            func, args, kwargs, on_done = self.task_queue.get()
            result = None

            try:
                result = func(*args, **kwargs)

            except Exception as e:
                print(f"TaskQueue error in {getattr(func, '__name__', func)}: {e}")

            finally:
                # Only clear "threading_busy" when there is TRULY nothing left to do.
                # otherwise "threading_busy" would be False even though tasks are still pending
                if self.task_queue.empty():
                    self.threading_busy.clear()
                self.task_queue.task_done()

            if on_done:
                on_done(result)


    def is_threading_busy(self) -> bool:
        return self.threading_busy.is_set()


    def clear(self):
        # Clears all tasks that have not yet started (running tasks remain unaffected).
        with self.task_queue.mutex:
            self.task_queue.queue.clear()
