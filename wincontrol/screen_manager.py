import time
import tkinter as tk
import multiprocessing

class Blocker(multiprocessing.Process):
    def __init__(self, close_event):
        super().__init__()
        self.close_event = close_event

    def run(self):
        self.root = tk.Tk()
        self.root.title("Virtual Shield")

        self.root.attributes("-topmost", True)
        self.root.attributes("-fullscreen", True)

        self.root.configure(bg='#101010')

        def check_queue():
            if self.close_event.is_set():  # Check if the event is set
                self.root.destroy()
            else:
                self.root.after(10, check_queue)

        self.root.after(10, check_queue)

        self.root.mainloop()

    def close(self):
        print("hello_world")
        self.close_event.set()

gui_process = None

def block_screen():
    global gui_process
    gui_process = Blocker(multiprocessing.Event())
    gui_process.start()


def remove_screen_block():
    global gui_process
    if gui_process and gui_process.is_alive():
        gui_process.terminate()
        gui_process.join()
        gui_process = None

if __name__ == "__main__":
    block_screen()
    time.sleep(1)
    remove_screen_block()
