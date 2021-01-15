import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter.ttk import Progressbar
from igcconverter import IGCConverter, ConversionProgressObserver, IGCConverterExceptionObserver
from typing import Optional
import os
from threading import Thread


class IGCTKConverterGUI(ConversionProgressObserver, IGCConverterExceptionObserver):

    def __init__(self):
        self.app = tk.Tk()
        self.app.geometry('500x50')
        self.selected_igc_path = None
        self._num_converted_files = 0
        self._setup_dropdown()
        self._setup_buttons()
        self._setup_progressbar()
        self.selected_output_format = self._get_selected_export_format()

    def _get_selected_export_format(self) -> Optional[str]:
        if self._output_format_dropdown.get() == 'acmi-TacView':
            return 'acmi'
        elif self._output_format_dropdown.get() == 'csv':
            return 'csv'
        else:
            return None

    def mainloop(self):
        self.app.mainloop()

    def _setup_progressbar(self):
        self.progressbar = Progressbar(self.app)
        self.progressbar.pack()

    def _setup_dropdown(self):
        self._output_format_dropdown = tk.StringVar(self.app)
        self._output_format_dropdown.set(IGCConverter.SupportedFormats[0])
        opt = tk.OptionMenu(self.app, self._output_format_dropdown, *IGCConverter.SupportedFormats,
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
        if self.selected_igc_path is None:
            messagebox.showerror('Error', 'No input was selected!')
            return
        converter = IGCConverter(self.selected_igc_path, self.selected_output_format)
        converter.add_exception_observer(self)
        converter.add_progress_observer(self)
        t = Thread(target=converter.convert_igc)
        t.daemon = True
        t.start()

    def _on_select_input_button_clicked(self):
        self.open_filedialog()

    def _on_format_chosen(self, arg=None):
        self.selected_output_format = self._get_selected_export_format()

    def open_filedialog(self):
        self.selected_igc_path = filedialog.askdirectory(initialdir=os.getcwd(), title="Select a directory")

    def on_conversion_started(self, num_items: int):
        self.progressbar["maximum"] = num_items
        self.progressbar["value"] = 0

    def on_conversion_completed(self):
        messagebox.showinfo('Conversion Complete!', "Converted {} IGC files".format(self._num_converted_files))
        self._num_converted_files = 0

    def on_file_converted(self, filename):
        self._num_converted_files += 1
        self.progressbar["value"] = self._num_converted_files

    def on_exception_raised(self, e: Exception):
        messagebox.showerror('An Error Occurred!', e)
