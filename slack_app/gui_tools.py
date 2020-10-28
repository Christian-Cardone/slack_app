import tkinter as tk
import schedule
import time
import queue
import threading
from slack_app.slack_message import *


class CheckBar(tk.Frame):
    def __init__(self, options_list, parent=None, side=tk.TOP, anchor=tk.W):
        tk.Frame.__init__(self, parent)
        self.vars = list()
        for opt in options_list:
            var = tk.IntVar()
            chk = tk.Checkbutton(self, text=opt, variable=var)
            chk.pack(side=side, anchor=anchor)
            self.vars.append(var)

    def state(self):
        return map((lambda var: var.get()), self.vars)


def center(win):
    """
    centers a tkinter window
    :param win: the root or Toplevel window to center
    """
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()


def include_greetings():
    def user_click(button_id):
        nonlocal u_selection
        nonlocal root
        if button_id == 'cancel':
            u_selection = 'cancel'
        root.destroy()

    u_selection = 'submit'
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.title("Greetings App")
    winroot = tk.Frame(root)
    winroot.pack(side="top", fill="both", expand=True)
    tk.Label(winroot, text="COMPLETE AND SELECT THE OPTIONS"). \
        pack(pady=(1, 10), padx=(4, 4))

    # Channel
    selected_channel = tk.StringVar(winroot)
    tk.Label(winroot, text="Channel (include '#' or '@')").pack()
    tk.Entry(winroot, textvariable=selected_channel).pack(pady=(1, 5))

    # Message
    selected_message = tk.StringVar(winroot)
    tk.Label(winroot, text="Message").pack()
    tk.Entry(winroot, textvariable=selected_message).pack(pady=(1, 5))

    # Time request
    selected_time = tk.StringVar(winroot)
    tk.Label(winroot, text="Time of the Day (hh:mm)").pack()
    tk.Entry(winroot, textvariable=selected_time).pack(pady=(1, 5))

    # Days of the week
    weekdays = [
        "Monday", "Tuesday", "Wednesday", "Thursday",
        "Friday", "Saturday", "Sunday"
    ]
    tk.Label(winroot, text="Weekdays to send the message").pack()
    cb = CheckBar(weekdays, winroot)
    cb.pack()
    tk.Button(winroot, text="Cancel", command=lambda: user_click('cancel')). \
        pack(side=tk.LEFT)
    tk.Button(winroot, text="Submit", command=lambda: user_click('submit')).\
        pack(side=tk.RIGHT)
    center(root)
    winroot.mainloop()
    return (u_selection,
            selected_channel.get(),
            selected_message.get(),
            selected_time.get(),
            [day for (day, state) in zip(weekdays, list(cb.state())) if state == 1])


def info_message(message):
    winroot = tk.Tk()
    winroot.geometry("300x200")
    winroot.attributes("-topmost", True)
    winroot.title("Info")
    tk.Label(winroot, text=message).pack()
    tk.Button(winroot, text='OK', command=winroot.destroy).pack(side=tk.BOTTOM)
    center(winroot)
    winroot.mainloop()




class GuiPart(object):
    def __init__(self, master, queue, end_command):
        self.queue = queue
        # Set up the GUI
        tk.Button(master, text='Stop', command=end_command).pack(side=tk.BOTTOM)
        # Add more GUI stuff here depending on your specific needs

    def processIncoming(self):
        """ Handle all messages currently in the queue, if any. """
        while self.queue.qsize():
            try:
                msg = self.queue.get_nowait()
                # Check contents of message and do whatever is needed. As a
                # simple example, let's print it (in real life, you would
                # suitably update the GUI's display in a richer fashion).
                print(msg)
            except queue.Empty:
                # just on general principles, although we don't expect this
                # branch to be taken in this case, ignore this exception!
                pass


class ThreadedJob(object):
    """
    Launch the main part of the GUI and the worker thread. periodic_call()
    and end_application() could reside in the GUI part, but putting them
    here means that you have all the thread controls in a single place.
    """
    def __init__(self, master):
        """
        Start the GUI and the asynchronous threads.  We are in the main
        (original) thread of the application, which will later be used by
        the GUI as well.  We spawn a new thread for the worker (I/O).
        """
        self.master = master
        # Create the queue
        self.queue = queue.Queue()

        # Set up the GUI part
        self.gui = GuiPart(master, self.queue, self.end_application)

        # Set up the thread to do asynchronous I/O
        # More threads can also be created and used, if necessary
        self.running = True
        self.thread1 = threading.Thread(target=self.worker_thread1)
        self.thread1.start()

        # Start the periodic call in the GUI to check the queue
        self.periodic_call()

    def periodic_call(self):
        """ Check every 200 ms if there is something new in the queue. """
        self.master.after(200, self.periodic_call)
        self.gui.processIncoming()
        if not self.running:
            # This is the brutal stop of the system.  You may want to do
            # some cleanup before actually shutting it down.
            import sys
            sys.exit(1)

    def worker_thread1(self):
        """
        This is where we handle the asynchronous I/O.  For example, it may be
        a 'select()'.  One important thing to remember is that the thread has
        to yield control pretty regularly, be it by select or otherwise.
        """
        while self.running:
            # Execute jobs until stopped
            #time.sleep(rand.random() * 1.5)
            #msg = rand.random()
            schedule.run_pending()
            time.sleep(1)
            #self.queue.put(msg)

    def end_application(self):
        self.running = False  # Stops worker_thread1 (invoked by "Done" button).










