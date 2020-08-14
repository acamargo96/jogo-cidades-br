# Adaptado de: https://www.learnpyqt.com/courses/graphics-plotting/plotting-matplotlib/

import sys
import matplotlib
matplotlib.use('Qt5Agg')

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox, QLabel, QGridLayout

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from maps import Mapa

import mysql.connector
import cartopy.crs as ccrs

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # Cria a conexão com o banco de dados
        self.mysql = CidadesMySQL()
        self.bot = Bot(self.mysql)

        self.setWindowTitle('Cidades!')

        self.width = 768
        self.heigth = 1024
        self.setGeometry(10, 10, self.heigth, self.width)

        # Cria o mapa e adiciona na janela
        self.map = Mapa()
        self.canvas = FigureCanvasQTAgg(self.map.fig)
        self.canvas.move(100, 100)
        self.canvas.resize(1000, 700)
        self.setCentralWidget(self.canvas)

        # Label da caixa de entrada
        self.input_label = QLabel('Digite a cidade!', self.canvas)
        self.input_label.resize(280,20)
        self.input_label.move(0.5 * self.width, 10)
        self.input_label.setAlignment(QtCore.Qt.AlignCenter)

        # Entrada de texto do usuário
        self.city_input = QLineEdit('', self.canvas)
        self.city_input.resize(280,30)
        self.city_input.move(self.width/2, 40)
        self.city_input.setAlignment(QtCore.Qt.AlignCenter)

        # Conecta o Enter com o envio do input
        self.city_input.returnPressed.connect(self.check_input)

        # Contador de acertos e cidades faltando
        self.counter = 0
        self.remaining = 5570

        self.counter_label = QLabel('Contador: %d\nCidades Faltando: %d' % (self.counter, self.remaining), self)
        self.counter_label.resize(280,50)
        self.counter_label.move(self.width, 30)

        # Aviso de cidade não encontrada
        self.not_found_label = QLabel('', self)
        self.not_found_label.resize(280,50)
        self.not_found_label.move(0.1 * self.width, 30)
        self.not_found_label.setStyleSheet('color: red')

        # Usar bot
        self.bot_btn = QPushButton(text='Usar bot', parent=self)
        self.bot_btn.resize(100,100)
        self.bot_btn.move(0.1 * self.width, 300)
        self.bot_btn.clicked.connect(self.use_bot)

        self.show()

    def check_input(self):

        # Limpa o possível valor errado
        self.not_found_label.clear()

        city = self.city_input.text()

        coords = self.query_coord(city)
        matches = len(coords)

        if matches == 0:
            self.not_found_label.setText('Cidade %s não encontrada!' % city)
            
        else:
            # altera os contadores
            self.counter += matches
            self.remaining -= matches
            self.counter_label.setText('Contador: %d\nCidades Faltando: %d' % (self.counter, self.remaining))

            # mostra a cidade na figura
            for c in coords:
                lon = c[0]
                lat = c[1]
                self.map.ax.plot(lon, lat, marker='x', transform=ccrs.PlateCarree())
                self.map.fig.canvas.draw()
                self.map.fig.canvas.flush_events()

        self.city_input.clear()

    def query_coord(self, city):

        self.mysql.cursor.execute('SELECT longitude, latitude FROM municipios WHERE nome = "%s"' % city)
        coords = self.mysql.cursor.fetchall()
        return coords

    def use_bot(self):

        for name in self.bot.results:
            self.city_input.setText(name[0])
            self.check_input()

class CidadesMySQL():

    def __init__(self):

        self.db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="password",
                database="municipios"
        )

        self.cursor = self.db.cursor()

class Bot():

    def __init__(self, db):

        db.cursor.execute('SELECT nome FROM municipios')
        self.results = db.cursor.fetchall()





app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
app.exec_()