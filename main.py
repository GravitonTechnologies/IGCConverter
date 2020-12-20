from parser import IGCParser


def main():
    parser = IGCParser('test.igc')
    print(parser.flight_info)


if __name__ == '__main__':
    main()
