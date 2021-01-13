from igcconverter import IGCConverter, ConversionProgressObserver, IGCConverterExceptionObserver
import re


class IGCConverterCLI(ConversionProgressObserver, IGCConverterExceptionObserver):
    def __init__(self):
        self.num_converted_files = 0
        self.num_files_to_convert = 0
        self._prompt = '> '
        self._user_input = ''
        self._new_line_indentation = ' ' * 4
        self._formats_cmd_pattern = re.compile(r'formats?|fmts?', re.IGNORECASE)
        self._convert_cmd_pattern = re.compile(r"(conv?e?r?t?)")
        self._help_cmd_pattern = re.compile(r'help', re.IGNORECASE)
        self._quit_cmd_pattern = re.compile(r'quit')

    def mainloop(self):
        self._ask_user_input()
        while not re.fullmatch(self._quit_cmd_pattern, self._user_input):
            self._handle_user_input()
            self._ask_user_input()

    @property
    def _help_text(self) -> str:
        s = 'Available commands: \n'
        s += self._new_line_indentation + 'convert [input] [format] ... to convert igc files.\n'
        s += self._new_line_indentation + 'formats ... to get a list of available formats.'
        s += self._new_line_indentation + 'quit ... to quit.'
        s += self._new_line_indentation + 'help ... to view this.'
        return s

    def _ask_user_input(self):
        self._user_input = input(self._prompt).strip()

    def on_conversion_started(self, num_items: int):
        self.num_converted_files = 0
        self.num_files_to_convert = num_items

    def on_conversion_completed(self):
        print('Conversion completed.')
        print('Converted {} files.'.format(self.num_converted_files))

    def on_file_converted(self, filename):
        # print('Converted {}'.format(filename))
        self.num_converted_files += 1
        print('Progress {}/{}'.format(self.num_converted_files, self.num_files_to_convert))

    def on_exception_raised(self, e: Exception):
        print('An error occurred...')
        print(e)

    def _handle_user_input(self):
        if re.match(self._help_cmd_pattern, self._user_input):
            self._handle_help_cmd()
        elif re.match(self._convert_cmd_pattern, self._user_input):
            self._handle_convert_cmd()
        elif re.match(self._formats_cmd_pattern, self._user_input):
            self._handle_formats_cmd()
        else:
            print("Invalid command: '{}'".format(self._user_input))
            self._handle_help_cmd()

    def _handle_convert_cmd(self):
        match = re.match(r"(conv?e?r?t?)\s+(\w+)\s+(\w+)", self._user_input)
        if not match:
            print("invalid syntax, use: 'convert input format'")
            return

        source = match.group(2)
        output_format = match.group(3)
        converter = IGCConverter(source, output_format)
        converter.add_exception_observer(self)
        converter.add_progress_observer(self)
        converter.convert_igc()

    def _handle_formats_cmd(self):
        s = 'Available formats: \n'
        for f in IGCConverter.SupportedFormats:
            s += self._new_line_indentation + f + '\n'
        print(s)

    def _handle_help_cmd(self):
        print(self._help_text)
