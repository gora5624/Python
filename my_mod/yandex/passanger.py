import sys
from pathlib import Path

from PyQt6.QtCore import QRunnable, Qt, QObject, QThreadPool, pyqtSignal as Signal, pyqtSlot as Slot
from PyQt6.QtWidgets import QApplication,  QMainWindow, QPushButton, QWidget, QGridLayout, QProgressBar, QTableWidget, QTableWidgetItem
from PyQt6.QtGui import QIcon

from lxml import html
import requests


class Signals(QObject):
    completed = Signal(dict)


class Stock(QRunnable):
    BASE_URL = 'https://finance.yahoo.com/quote/'

    def __init__(self, symbol):
        super().__init__()
        self.symbol = symbol
        self.signal = Signals()

    @Slot()
    def run(self):
        stock_url = f'{self.BASE_URL}{self.symbol}'
        response = requests.get(stock_url)
        if response.status_code != 200:
            self.signal.completed.emit({'symbol': self.symbol, 'price': 'N/A'})
            return

        tree = html.fromstring(response.text)
        price_text = tree.xpath(
            '//*[@id="quote-header-info"]/div[3]/div[1]/div[1]/fin-streamer[1]/text()'
        )

        if not price_text:
            self.signal.completed.emit({'symbol': self.symbol, 'price': 'N/A'})
            return

        price = float(price_text[0].replace(',', ''))

        self.signal.completed.emit({'symbol': self.symbol, 'price': price})


class Window(QMainWindow):
    def __init__(self, filename, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.symbols = self.read_symbols(filename)

        self.results = []

        self.setWindowTitle('Stock Listing')
        self.setGeometry(100, 100, 400, 300)
        self.setWindowIcon(QIcon('./assets/stock.png'))

        widget = QWidget()
        widget.setLayout(QGridLayout())
        self.setCentralWidget(widget)

        # set up button & progress bar
        self.btn_start = QPushButton('Get Prices', clicked=self.get_prices)
        self.progress_bar = QProgressBar(minimum=1, maximum=len(self.symbols))

        # set up table widget
        self.table = QTableWidget(widget)
        self.table.setColumnCount(2)
        self.table.setColumnWidth(0, 150)
        self.table.setColumnWidth(1, 150)

        self.table.setHorizontalHeaderLabels(['Symbol', 'Price'])

        widget.layout().addWidget(self.table, 0, 0, 1, 2)
        widget.layout().addWidget(self.progress_bar, 1, 0)
        widget.layout().addWidget(self.btn_start, 1, 1)

        # show the window
        self.show()

    def read_symbols(self, filename):
        """ 
        Read symbols from a file
        """
        path = Path(r'D:\Python\my_mod\yandex\symbols.txt')
        text = path.read_text()
        return [symbol.strip() for symbol in text.split('\n')]

    def reset_ui(self):
        self.progress_bar.setValue(1)
        self.table.setRowCount(0)

    def get_prices(self):
        # reset ui
        self.reset_ui()

        # start worker threads
        pool = QThreadPool.globalInstance()
        stocks = [Stock(symbol) for symbol in self.symbols]
        for stock in stocks:
            stock.signal.completed.connect(self.update)
            pool.start(stock)
        

    def update(self, data):
        # add a row to the table
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(data['symbol']))
        self.table.setItem(row, 1, QTableWidgetItem(str(data['price'])))

        # update the progress bar
        self.progress_bar.setValue(row + 1)

        # sort the list by symbols once completed
        if row == len(self.symbols) - 1:
            self.table.sortItems(0, Qt.SortOrder.AscendingOrder)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window('symbols.txt')
    sys.exit(app.exec())