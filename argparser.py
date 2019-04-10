import argparse
import numpy as np
import pygame

DEFAULT_Z = 2
DEFAULT_N = 100
DEFAULT_D = "normal"
NEAT = "neat"

def get_args():
    prog_desc = "Flappy Bird Clone with NEAT.\n" \
        + "Dependencies tested on:\n" \
        + "\t numpy {}\n".format(np.__version__) \
        + "\t pygame {}\n".format(pygame.__version__)
    parser = argparse.ArgumentParser(
        description=prog_desc,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "-z",
        #nargs="?",
        #const=DEFAULT_Z,
        default=DEFAULT_Z,
        type=int,
        help="set zoom level for display; default value is 2",
        metavar="ZOOM",
        dest="z",
    )
    parser.add_argument(
        "-n",
        #nargs="?",
        #const=DEFAULT_N,
        default=DEFAULT_N,
        type=int,
        help="size of population for neat algorithm; only affects AI mode; default value is 100",
    )
    parser.add_argument(
        "-d",
        #nargs="?",
        #const=DEFAULT_D,
        choices=["easy", "normal", "hard"],
        default=DEFAULT_D,
        type=str,
        help="set difficulty for the game; options are 'easy', 'normal', and 'hard'",
        metavar="DIFFICULTY",
        dest="d",
    )
    parser.add_argument(
        "ai",
        nargs="?",
        choices=["neat"],
        default=None,
        help="type of AI to be used; currently this project only supports neat; " \
            + "if left empty, game starts in normal mode without any AI",
        metavar="AI",
    )
    args = parser.parse_args()

    # if ai is not given set it to 1
    if args.ai is None:
        args.n = 1

    return args
