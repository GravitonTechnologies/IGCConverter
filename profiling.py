from igcconverter import IGCConverter
import cProfile
import os
import pstats


def run_igc_converter():
    IGCConverter(os.getcwd() + os.sep + 'igc', 'acmi').convert_igc()


def main():
    pr = cProfile.Profile()

    pr.enable()
    run_igc_converter()
    pr.disable()

    with open('profiling_result.txt', 'w') as stream:
        stats = pstats.Stats(pr, stream=stream)
        stats.print_stats()


if __name__ == '__main__':
    main()
