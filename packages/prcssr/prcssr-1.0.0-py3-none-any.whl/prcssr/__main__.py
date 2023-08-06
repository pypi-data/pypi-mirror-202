import sys

import argparse

from prcssr.Controller import Controller
from prcssr.model.Processor import Processor

def main(args_=None):
    """The main routine."""
    if args_ is None:
        args_ = sys.argv[1:]

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--cmd", type=str, required=True, help="The command")
    parser.add_argument("-l", "--log", type=str, default="prcssr.log", help="Path to log file")
    args = parser.parse_args()

    ctrl = Controller()
    ctrl.printHeader(args.log)

    p = Processor(logPath=args.log)
    p.process(args.cmd)

    ctrl.printCmd(args.cmd)
    ctrl.printExecutionTime()

if __name__ == "__main__":
    sys.exit(main())
