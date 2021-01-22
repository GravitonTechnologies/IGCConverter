from tkinter import Toplevel, Button


class TkModalWindow:
    """
    Example usage:
        m = TkModalWindow(self.app, 0, "Modal Window")
        self.app.wait_window(m.top)
    """

    def __init__(self, parent, title):
        self.top = Toplevel(parent)
        self.top.transient(parent)
        self.top.grab_set()
        if len(title) > 0:
            self.top.title(title)
        self.top.bind("<Return>", self.ok)
        b = Button(self.top, text="OK", command=self.ok)
        b.pack(pady=5)

    def ok(self, event=None):
        self.top.destroy()

    def cancel(self, event=None):
        self.top.destroy()
