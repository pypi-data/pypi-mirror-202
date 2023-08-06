import os
import time

from datetime import datetime

class Controller():
    def __init__(self) -> None:
        self.startTime = time.time()

    def printHeader(self, logPath):
        print("################################################################################")
        print("")
        print("prcssr by 5f0")
        print("Command Execution with Logging")
        print("")
        print("         Path to Log File: " + logPath)
        print("Current working directory: " + os.getcwd())
        print("")
        print("Datetime: " + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        print("")
        print("################################################################################")

    def printCmd(self, cmd):
        print("")
        print("CMD: " + str(cmd))


    def printExecutionTime(self):
        end = time.time()
        print("")
        print("################################################################################")
        print("")
        print("Execution Time: " + str(end-self.startTime)[0:8] + " sec")
        print("")