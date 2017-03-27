import sys
from PyQt5.QtWidgets import QApplication
from openpyxl import load_workbook


class ReadFile(object):
    def __init__(self):
        super().__init__()
        self.ReadFile()

    def ReadFile(self):
        self.wb = load_workbook(filename="test.xlsx", read_only=True)
        self.ws = self.wb["Blad1"]
        print("not important")


