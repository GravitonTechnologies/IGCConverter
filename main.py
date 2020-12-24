from gui import IGCConverterGUI
import argparse
from igc_converter import convert_igc
from igcparser import ParseError


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--format", default='csv', type=str, help='output format')
    parser.add_argument("--input", type=str, help='IGC source', default='.')
    parser.add_argument('--gui', action='store_true', help='start in GUI mode')
    args = parser.parse_args()

    if args.gui:
        gui = IGCConverterGUI()
        gui.mainloop()
    else:
        try:
            convert_igc(args.input, args.format)
        except ParseError as e:
            print(e)
        except RuntimeError as e:
            print(e)


if __name__ == '__main__':
    main()
