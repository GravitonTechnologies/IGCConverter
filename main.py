from gui import IGCConverterGUI
import argparse
from igc_converter import convert_igc


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--format", default='csv', type=str)
    parser.add_argument("input", type=str)
    parser.add_argument('--gui', action='store_true', help='start in GUI mode')
    args = parser.parse_args()

    if args.gui:
        gui = IGCConverterGUI()
        gui.mainloop()
    else:
        convert_igc(args.input, args.format)


if __name__ == '__main__':
    main()
