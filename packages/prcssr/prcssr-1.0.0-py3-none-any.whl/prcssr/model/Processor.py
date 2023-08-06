import os
import logging
import subprocess


class Processor():
    def __init__(self, logPath="prcssr.log") -> None:
        format = "[%(asctime)s] | %(levelname)s | %(message)s"
        logging.basicConfig(filename=logPath, level=logging.DEBUG, format=format)
        
    def process(self, cmd):
        logging.info("CMD: " + cmd)
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        logging.info("----------")
        for line in p.stdout.readlines():
            l = line.decode("utf8").replace("\n", "").replace("\r", "")
            logging.info(l)
        logging.info("----------")

    def processGetStdOut(self, cmd):
        logging.info("CMD: " + cmd)
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        logging.info("----------")
        return p.stdout
    
    def logInfo(self, info):
        logging.info(info)

    def logWarn(self, warn):
        logging.warn(warn)