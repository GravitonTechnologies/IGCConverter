from tkgui import IGCTKConverterGUI
from qtgui import IGCQtConverterGUI
from cli import IGCConverterCLI
import argparse
from sys import platform


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--format", default='csv', type=str, help='output format')
    parser.add_argument("--input", type=str, help='IGC source', default='igc')
    parser.add_argument('--cli', action='store_true', help='start in CLI mode')
    args = parser.parse_args()

    if args.cli:
        converter = IGCConverterCLI()
        converter.mainloop()
    else:
        # if platform == "darwin":
        #     gui = IGCTKConverterGUI()
        # else:
        #     gui = IGCQtConverterGUI()

        gui = IGCTKConverterGUI()
        gui.mainloop()


if __name__ == '__main__':
    main()
