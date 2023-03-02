from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import json
import sys

def clean_description(character, description):
    return description.replace("{spell-save}",   character.spellSave)         \
                      .replace("{spell-attack}", character.spellAtk)          \
                      .replace("{strenght}",     character.str)               \
                      .replace("{dexterity}",    character.dex)               \
                      .replace("{consitution}",  character.con)               \
                      .replace("{intelligence}", character.int)               \
                      .replace("{wisdom}",       character.wis)               \
                      .replace("{charisma}",     character.cha)               \
                      .replace("{size}",         character.size)


class Character():
    class Spell():
        def __init__(self, character, name="", level="", source="", description=""):
            self.name  = name
            self.level = level
            self.source = source
            self.description = clean_description(character, description)

        def __str__(self):
            return self.name + " (" + self.level + "): " + self.description

    class Feat():
        def __init__(self, character, name="", range_="", time="", type_="", traits="", source = "", description=""):
            self.name   = name
            self.range  = range_
            self.time   = time
            self.type   = type_
            self.traits = traits
            self.description = clean_description(character, description)

        def __str__(self):
            return self.name + " " +                                          \
                   self.time +                                                \
                   " (" + str(self.type) + "  " + str(self.traits) + ") " +   \
                   self.range + ": " +                                        \
                   self.description


    class Action():
        pass


    def __init__(self, filename):
        with open("./treerazer.json", "r") as f:
            self.data = json.load(f)

        self.parse_json()

    def parse_json(self):
        self.name = self.data["name"]

        if type(self.data["class"] == list):
            self.class_ = [self.data["class"][i] + " " + self.data["level"][i] for i in range(len(self.data["class"]))]
        else:
            self.class_ = self.data["class"] + " " + self.data["level"]

        self.source    = self.__get_data("source")
        self.ac        = self.__get_data("ac")
        self.size      = self.__get_data("size", "Medium")
        self.hp        = self.__get_data("hp")
        self.regen     = self.__get_data("regeneration", 0)
        self.immuns    = self.__get_data("immunity",   [])
        self.resists   = self.__get_data("resistance", [])
        self.weakness  = self.__get_data("weakness",   [])
        self.walkSpeed = self.__get_data("walking",  0, self.__get_data("speed"))
        self.flySpeed  = self.__get_data("flying",   0, self.__get_data("speed"))
        self.swimSpeed = self.__get_data("swimming", 0, self.__get_data("speed"))
        self.senses    = self.__get_data("senses", [])
        self.str       = self.__get_data("strenght",     "0", self.__get_data("ability-scores"))
        self.dex       = self.__get_data("dexterity",    "0", self.__get_data("ability-scores"))
        self.con       = self.__get_data("consitution",  "0", self.__get_data("ability-scores"))
        self.int       = self.__get_data("intelligence", "0", self.__get_data("ability-scores"))
        self.wis       = self.__get_data("wisdom",       "0", self.__get_data("ability-scores"))
        self.cha       = self.__get_data("charisma",     "0", self.__get_data("ability-scores"))
        self.fort      = self.__get_data("fortitude",    "0", self.__get_data("ability-scores"))
        self.ref       = self.__get_data("reflex",       "0", self.__get_data("ability-scores"))
        self.will      = self.__get_data("willpower",    "0", self.__get_data("ability-scores"))
        self.ini       = self.__get_data("initiative",   "0", self.__get_data("ability-scores"))
        self.skills    = self.__get_data("skills", [])
        self.items     = self.__get_data("items", [])
        self.languages = self.__get_data("languages", [])
        self.hasSpells = "spells" in self.data
        self.spellSave = self.__get_data("save",   "0", self.__get_data("spells"))
        self.spellAtk  = self.__get_data("attack", "0", self.__get_data("spells"))
        self.spells    = self.__get_spells()
        self.feats     = self.__get_feats()
        self.actions   = self.__get_data("actions", [])

    def __get_data(self, key, default="", dictionary=None):
        if dictionary is None:
            dictionary = self.data
        return dictionary[key] if key in dictionary else default

    def __get_spells(self):
        if self.hasSpells == False:
            return []

        dictionary = self.__get_data("spells", None, self.__get_data("spells"))
        if dictionary is None:
            return []

        return [self.Spell(self,                                              \
                           name       =self.__get_data("name",        "", s), \
                           level      =self.__get_data("level",       "", s), \
                           source     =self.__get_data("source",      "", s), \
                           description=self.__get_data("description", "", s)) \
                for s in dictionary]

    def __get_feats(self):
        dictionary = self.__get_data("feats", None)
        if dictionary is None:
            return []

        return [self.Feat(self,                                               \
                          name       =self.__get_data("name",   "", f),       \
                          range_     =self.__get_data("range",  "", f),       \
                          time       =self.__get_data("time",   "", f),       \
                          type_      =self.__get_data("type",   "", f),       \
                          traits     =self.__get_data("traits", "", f),       \
                          source     =self.__get_data("source", "", f),       \
                          description=self.__get_data("description",  "", f)) \
                for f in dictionary]


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

treerazer = Character("treerazer.json")

app.exec_()