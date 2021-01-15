from PyQt5.QtWidgets import QApplication, QProgressBar, QPushButton, QVBoxLayout, \
    QComboBox, QWidget, QFileDialog, QMessageBox, QLabel
from igcconverter import IGCConverter, ConversionProgressObserver, IGCConverterExceptionObserver
from utilities import get_selected_export_format
from typing import Optional
from threading import Thread


class IGCQtConverterGUI(ConversionProgressObserver, IGCConverterExceptionObserver):
    def __init__(self):
        self._num_converted_files = 0
        self.selected_igc_path: Optional[str] = None
        self.app = QApplication([])
        self.window = QWidget()
        self.layout = QVBoxLayout()

        self._formats_devices_combo = QComboBox()
        self._setup_formats_devices_combo()
        self.selected_output_format = get_selected_export_format(str(self._formats_devices_combo.currentText()))

        self._status_label = QLabel()
        self.setup_status_label()

        self._progress_bar = QProgressBar()
        self._setup_progress_bar()

        self._convert_button = QPushButton()
        self._setup_convert_button()

        self._select_input_button = QPushButton()
        self._setup_select_input_button()

        self.window.setLayout(self.layout)

    def _setup_convert_button(self):
        self._convert_button.setText("Convert!")
        self._convert_button.clicked.connect(self._on_convert_button_clicked)
        self.layout.addWidget(self._convert_button)

    def setup_status_label(self):
        self._status_label.setText("")
        self.layout.addWidget(self._status_label)

    def _on_convert_button_clicked(self):
        if self.selected_igc_path is None:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("No Input Selected!")
            msg.setInformativeText("An input source must be selected.")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
        else:
            converter = IGCConverter(self.selected_igc_path, self.selected_output_format)
            converter.add_exception_observer(self)
            converter.add_progress_observer(self)
            t = Thread(target=converter.convert_igc)
            t.start()

    def _setup_select_input_button(self):
        self._select_input_button.setText("Choose Input")
        self._select_input_button.clicked.connect(self._on_select_input_button_clicked)
        self.layout.addWidget(self._select_input_button)

    def _on_select_input_button_clicked(self):
        self.selected_igc_path = str(QFileDialog.getExistingDirectory(None, "Select Directory"))

    def _setup_progress_bar(self):
        self._progress_bar.setMinimum(0)
        self.layout.addWidget(self._progress_bar)

    def _setup_formats_devices_combo(self):
        self._formats_devices_combo.addItems(IGCConverter.SupportedFormats)
        self._formats_devices_combo.currentTextChanged.connect(self._on_combobox_changed)
        self.layout.addWidget(self._formats_devices_combo)

    def _on_combobox_changed(self, value):
        self.selected_output_format = get_selected_export_format(str(value))

    def on_conversion_started(self, num_items: int):
        self._status_label.setText("Working...")
        self._num_converted_files = 0
        self._progress_bar.setMaximum(num_items)

    def on_conversion_completed(self):
        self._status_label.setText("Done!")

        # msg = QMessageBox()
        # msg.setIcon(QMessageBox.Information)
        # msg.setText("Conversion Complete!")
        # msg.setInformativeText("Converted {} files.".format(self._num_converted_files))
        # msg.setStandardButtons(QMessageBox.Ok)

        # TODO this causes a problem on mac...
        # msg.open()

    def on_file_converted(self, filename):
        self._num_converted_files += 1
        self._progress_bar.setValue(self._num_converted_files)

    def on_exception_raised(self, e: Exception):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("An Error Occurred!")
        msg.setInformativeText(str(e))
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def mainloop(self):
        self.window.show()
        self.app.exec_()
