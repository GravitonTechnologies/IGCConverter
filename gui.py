import tkinter as tk
from tkinter import filedialog
from igc_converter import convert_igc
import os


class IGCConverterGUI:
    SupportedFormats = ['csv', 'json']

    def __init__(self):
        self.app = tk.Tk()
        self.app.geometry('500x50')
        self.selected_igc_path = None
        self._setup_dropdown()
        self._setup_buttons()
        self.selected_output_format = self._output_format_dropdown.get()

    def mainloop(self):
        self.app.mainloop()

    def _setup_dropdown(self):
        self._output_format_dropdown = tk.StringVar(self.app)
        self._output_format_dropdown.set(IGCConverterGUI.SupportedFormats[0])
        opt = tk.OptionMenu(self.app, self._output_format_dropdown, *IGCConverterGUI.SupportedFormats,
                            command=self._on_format_chosen)
        opt.config(width=90, font=('Helvetica', 12))
        opt.pack()

    def _setup_buttons(self):
        frame = tk.Frame(self.app)
        frame.pack()
        send_button = tk.Button(frame, text="Convert!", command=self._on_convert_button_clicked)
        send_button.pack(side=tk.LEFT)

        save_button = tk.Button(frame, text="Select input", command=self._on_select_input_button_clicked)
        save_button.pack(side=tk.RIGHT)

    def _on_convert_button_clicked(self):
        convert_igc(self.selected_igc_path, self.selected_output_format)

    def _on_select_input_button_clicked(self):
        self.open_filedialog()

    def _on_format_chosen(self, arg=None):
        self.selected_output_format = self._output_format_dropdown.get()

    def open_filedialog(self):
        self.selected_igc_path = filedialog.askdirectory(initialdir=os.getcwd(), title="Select a directory")
