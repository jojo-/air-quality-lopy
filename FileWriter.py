#from pytrack import Pytrack
from machine import SD
import os

class FileWriter(object):
    """docstring for [object Object]."""
    
    
    def __init__(self):
        self.sd = SD()
        os.mount(self.sd,'/sd/')
        print(os.listdir())

    def _write(self, filepath,mode,data):
        f = open(filepath,mode)
        f.write(data + "\n")
        f.close()
