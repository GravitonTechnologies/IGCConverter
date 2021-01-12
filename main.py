from gui import IGCConverterGUI
import argparse
from igcconverter import IGCConverter
from igcparser import ParseError


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
        try:
            IGCConverter(args.input, args.format).convert_igc()
        except ParseError as e:
            print(e)
        except RuntimeError as e:
            print(e)


if __name__ == '__main__':
    main()
