from gui import IGCConverterGUI
from cli import IGCConverterCLI
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--format", default='csv', type=str, help='output format')
    parser.add_argument("--input", type=str, help='IGC source', default='igc')
    parser.add_argument('--gui', action='store_true', help='start in GUI mode')
    args = parser.parse_args()

    if args.gui:
        gui = IGCConverterGUI()
        gui.mainloop()
    else:
        converter = IGCConverterCLI()
        converter.mainloop()


if __name__ == '__main__':
    main()
