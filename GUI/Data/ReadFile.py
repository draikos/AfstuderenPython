import sys
from PyQt5.QtWidgets import QApplication
from openpyxl import load_workbook


class ReadFile:
    def __init__(self):
        super().__init__()
        self.ws;
        self.ReadFile()

    def ReadFile(self):
        wb = load_workbook(filename="test.xlsx", read_only=True)
        ws = wb["Blad1"]
        return ws








def main():
    app = QApplication(sys.argv)
    ex = ReadFile()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
