import sys
from PyQt5.QtWidgets import QApplication
import numpy as np
import os



class ReadFile(object):
    def __init__(self):
        super().__init__()
        self.ReadFile()

    def ReadFile(self):
        filename = r"C:\Users\758051\Desktop\Jelle van den Toren\Hovig_20_10_14_AF_LA2.E01"
        with open(filename, 'rb') as fid:
            fid.seek(4608, os.SEEK_SET)
            data_array = np.fromfile(fid, np.int16).reshape((-1, 256)).T
            test = max(np.gradient(data_array[191]))
        i = 0
        for value in data_array:
            for i in range(len(value)):
                while i < 100:
                    print(value[i] / test)
                    i += 1
                break


