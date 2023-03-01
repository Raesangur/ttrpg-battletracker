from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import sys


class TrackingTable(QWidget):
    def __init__(self, *args, **kwargs):
        super(TrackingTable, self).__init__(*args, **kwargs)
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.create_table()
        self.create_buttons()
        self.create_shortcut()

    def create_shortcut(self):
        self.addShortcut = QShortcut(QKeySequence(Qt.Key_Plus), self)
        self.addShortcut.activated.connect(self.handle_add)

    def create_buttons(self):
        self.addButton = QPushButton("+")
        self.layout.addWidget(self.addButton, 0, 0)
        self.addButton.clicked.connect(self.handle_add)

        # Align button left
        buttonLayoutWidget = QWidget()
        buttonLayout = QHBoxLayout()
        buttonLayoutWidget.setLayout(buttonLayout)
        self.layout.addWidget(buttonLayoutWidget)
        buttonLayout.addWidget(self.addButton, alignment=Qt.AlignLeft)

    def create_table(self):
        self.table = QTableWidget(1, 7)
        self.layout.addWidget(self.table)

        self.table.setHorizontalHeaderLabels(["Initiative", "Name", "HP", "AC", "Spell DC", "Status", "Comments"])
        self.table.verticalHeader().setVisible(False)

    def handle_add(self):
        print("Adding")


class InteractionBar(QWidget):
    def __init__(self, *args, **kwargs):
        super(InteractionBar, self).__init__(*args, **kwargs)
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.create_arrows()
        self.create_shortcuts()

    def create_shortcuts(self):
        self.upShortcut = QShortcut(QKeySequence('Up'), self)
        self.downShortcut = QShortcut(QKeySequence('Down'), self)

        self.upShortcut.activated.connect(self.handle_up)
        self.downShortcut.activated.connect(self.handle_down)


    def create_arrows(self):
        self.upArrow   = QPushButton("Previous")
        self.downArrow = QPushButton("Next")
        self.layout.addWidget(self.upArrow, 0, 0)
        self.layout.addWidget(self.downArrow, 0, 1)
        self.layout.addWidget(QWidget(), 0, 2, 1, 4)

        #self.upArrow.setIcon(QIcon("arrow_up.png"))
        #self.downArrow.setIcon(QIcon("arrow_down.png"))

        #self.upArrow.setFlat(True)
        #self.downArrow.setFlat(True)

        self.upArrow.clicked.connect(self.handle_up)
        self.downArrow.clicked.connect(self.handle_down)

        self.upArrow.show()
        self.downArrow.show()


    def handle_up(self):
        print("Up button pressed")

    def handle_down(self):
        print("Down button pressed")


class CharacterInfo(QWidget):
    def __init__(self, *args, **kwargs):
        super(CharacterInfo, self).__init__(*args, **kwargs)
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.layout.addWidget(QLabel("Character Info"))



class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("BattleTracker for Pathfinder 2e")

        self.create_layout()


    def create_layout(self):
        # Create centralwidget as splitter
        splitter = QSplitter()
        self.setCentralWidget(splitter)

        # Create left and right pane as QGridLayouts inside QWidgets
        leftWidget  = QWidget()
        rightWidget = QWidget()
        leftPane    = QGridLayout()
        rightPane   = QGridLayout()
        leftWidget.setLayout(leftPane)
        rightWidget.setLayout(rightPane)

        # Add panes to the splitter
        splitter.addWidget(leftWidget)
        splitter.addWidget(rightWidget)

        # Create application sections
        self.trackingTable  = TrackingTable()
        self.interactionBar = InteractionBar()
        self.characterInfo  = CharacterInfo()

        # Add sections to the panes
        leftPane.addWidget(self.trackingTable, 0, 0, 100, 1)
        leftPane.addWidget(self.interactionBar, 100, 0, 1, 1)
        rightPane.addWidget(self.characterInfo, 0, 1, 2, 1)



app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()