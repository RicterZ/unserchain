import logging
import sys


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)
