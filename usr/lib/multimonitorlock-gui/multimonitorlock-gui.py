#!/usr/bin/env python3

# =====================================================
#                  Author The-Repo-Club
# =====================================================

import sys
import getpass
import os
import re
import shutil
import subprocess
import Functions as fn
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *

def divide_chunks(l, n):

    # looping till length l
    for i in range(0, len(l), n):
        yield l[i:i + n]

class MultiMonitorLock(QWidget):
    EXIT_CODE_REBOOT = -464647564
    # - SELECT - LOAD - DEFAULT - SEARCH - APPLY
    find_button = None
    load_button = None
    default_button = None
    search_button = None
    close_button = None
    apply_button = None

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        if not fn.os.path.isdir(fn.home + "/.config/multilock"):
            fn.os.mkdir(fn.home + "/.config/multilock")

        if not fn.os.path.isfile(fn.home + "/.config/multilock/gui.conf"):
            shutil.copy(fn.root_config, fn.home + "/.config/multilock/gui.conf")

        self.settings = QSettings()
        self.directory = self.settings.value("settings/folder", None)

        fn.get_config(self, fn.config)
        if self.directory is None:
            self.directory = str(self.folder)
        else:
            self.folder = str(self.folder)

        self.image_file = None
        self.init_ui()

    def init_ui(self):
        vbox = QVBoxLayout()
        self.setWindowTitle("Shutdown menu")

        self.title = QLabel("Hello, " + getpass.getuser() + "! What background would you like to chose?")

        hbox1 = QHBoxLayout()
        hbox2 = QHBoxLayout()
        hbox3 = QHBoxLayout()
        hbox3.addStretch()
        sbox = QScrollArea()
        sbox.setWidgetResizable(True)
        sbox.setMinimumSize(QSize(1000, 500))
        sbox.scrollAreaWidgetContents = QWidget()
        sbox.setWidget(sbox.scrollAreaWidgetContents)
        gbox = QGridLayout(sbox.scrollAreaWidgetContents)

        ext = [".png", ".jpg", ".jpeg"]
        images = [x for x in fn.os.listdir(self.directory) for j in ext if j in x.lower()]
        imagesA = list(divide_chunks(images, 5))
        key = 0
        self.group = QButtonGroup()
        for imagearray in imagesA:
            key = key + 1
            val = 0
            for image in imagearray:
                val = val + 1
                self.image_select = QToolButton()
                self.image_select.setIcon(QIcon(self.directory + "/" + image))
                self.image_select.setIconSize(QSize(150, 150))
                self.image_select.setCheckable(True);
                self.image_select.setObjectName(self.directory + "/" + image)
                gbox.addWidget(self.image_select,key,val, Qt.AlignTop)
                self.group.addButton(self.image_select)
                self.image_select.clicked.connect(self.item)

        self.enter_loction_text = QLabel("Enter Location")
        self.enter_loction_box = QLineEdit(self.directory)
        self.enter_loction_box.setMinimumSize(QSize(400, 0))
        self.enter_loction_box.move(20, 20)

        self.find_button = QPushButton()
        self.find_button.setText("...")
        self.find_button.setToolTip("find_button")
        self.find_button.setShortcut("ctrl+f")
        self.find_button.clicked.connect(self.select)

        self.load_button = QPushButton()
        self.load_button.setText("Load")
        self.load_button.setToolTip("load_button")
        self.load_button.setShortcut("ctrl+l")
        self.load_button.clicked.connect(self.load)

        self.default_button = QPushButton()
        self.default_button.setText("Default")
        self.default_button.setToolTip("default_button")
        self.default_button.setShortcut("ctrl+d")
        self.default_button.clicked.connect(self.default)

        self.enter_search_text = QLabel("Search:")
        self.enter_search_box = QLineEdit()

        self.search_button = QPushButton()
        self.search_button.setText("Search")
        self.search_button.setToolTip("search_button")
        self.search_button.setShortcut("ctrl+s")
        self.search_button.clicked.connect(self.search)

        self.apply_text = QLabel()
        self.apply_button = QPushButton()
        self.apply_button.setText("Apply")
        self.apply_button.setToolTip("apply_button")
        self.apply_button.setShortcut("ctrl+a")
        self.apply_button.clicked.connect(self.apply)

        self.close_button = QPushButton()
        self.close_button.setText("Close")
        self.close_button.setToolTip("close_button")
        self.close_button.setShortcut("ctrl+c")
        self.close_button.clicked.connect(self.close)

        vbox.addWidget(self.title)
        hbox1.addWidget(self.enter_loction_text)
        hbox1.addWidget(self.enter_loction_box)
        hbox1.addWidget(self.find_button)
        # hbox1.addWidget(self.load_button)
        hbox1.addWidget(self.default_button)
        # hbox2.addWidget(self.enter_search_text)
        # hbox2.addWidget(self.enter_search_box)
        # hbox2.addWidget(self.search_button)
        hbox3.addWidget(self.apply_text)
        hbox3.addWidget(self.close_button)
        hbox3.addWidget(self.apply_button)
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addWidget(sbox)
        vbox.addLayout(hbox3)

        vbox.setAlignment(Qt.AlignCenter)
        vbox.setSpacing(25)
        # hbox.setAlignment(Qt.AlignCenter)
        # hbox.setSpacing(75)

        base = QWidget()
        base.setObjectName("base")
        base.setLayout(vbox)

        baseLyt = QVBoxLayout()
        baseLyt.addWidget(base)
        baseLyt.setContentsMargins(QMargins())
        self.setLayout(baseLyt)

    def select(self):
        self.disable_buttons()
        directory = QFileDialog.getExistingDirectory(self, 'Select directory')
        if directory:
            self.settings.setValue("settings/folder", directory)
            self.enter_loction_box.setText(directory)
        qApp.exit(MultiMonitorLock.EXIT_CODE_REBOOT)
        self.enable_buttons()

    def item(self):
        self.disable_buttons()
        self.image_file = self.sender().objectName()
        self.apply_text.setText(self.image_file)
        self.enable_buttons()


    def load(self):
        self.disable_buttons()
        self.directory = self.enter_loction_box.text()
        # reply = QMessageBox.question(
        #     self, "Message",
        #     "MultiMonitorLock-GUI is about to reload?",
        #     QMessageBox.Close, QMessageBox.Close)
        #
        # if reply == QMessageBox.Close:
        qApp.exit(MultiMonitorLock.EXIT_CODE_REBOOT)
        self.enable_buttons()

    def default(self):
        self.disable_buttons()
        self.enter_loction_box.setText(self.folder)
        self.settings.setValue("settings/folder", self.folder)
        qApp.exit(MultiMonitorLock.EXIT_CODE_REBOOT)
        self.enable_buttons()

    def search(self):
        self.disable_buttons()
        # suspend_systemctl(self.cmd_lock)
        self.enable_buttons()

    def apply(self):
        self.disable_buttons()
        if self.image_file is not None:
            command = ["multimonitorlock", "-u", self.image_file]
            self.apply_text.setText(self.image_file)
            print(command)
            with fn.subprocess.Popen(command, bufsize=1, stdout=fn.subprocess.PIPE, universal_newlines=True) as p:
                for line in p.stdout:
                    print(line)
                    QApplication.processEvents()
                    result = re.sub("[\(\[].*?[\)\]]", "", line)
                    self.apply_text.setText(str(result))
                    self.image_file = None
        self.enable_buttons()

    def close(self, event):
        self.disable_buttons()
        reply = QMessageBox.question(
            self, "Message",
            "Are you sure you want to quit?",
            QMessageBox.Close | QMessageBox.Cancel)

        if reply == QMessageBox.Close:
            app.quit()
        else:
            pass
            self.enable_buttons()

    def disable_buttons(self):
        self.find_button.setEnabled(False)
        self.load_button.setEnabled(False)
        self.default_button.setEnabled(False)
        self.search_button.setEnabled(False)
        self.close_button.setEnabled(False)
        self.apply_button.setEnabled(False)

    def enable_buttons(self):
        self.find_button.setEnabled(True)
        self.load_button.setEnabled(True)
        self.default_button.setEnabled(True)
        self.search_button.setEnabled(True)
        self.close_button.setEnabled(True)
        self.apply_button.setEnabled(True)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            reply = QMessageBox.question(
                self, "Message",
                "Are you sure you want to quit?",
                QMessageBox.Close | QMessageBox.Cancel)

            if reply == QMessageBox.Close:
                app.quit()
            else:
                pass


if __name__ == '__main__':
    currentExitCode = MultiMonitorLock.EXIT_CODE_REBOOT
    while currentExitCode == MultiMonitorLock.EXIT_CODE_REBOOT:
        app = QApplication(sys.argv)
        QCoreApplication.setOrganizationName("The-Repo-Club")
        QCoreApplication.setOrganizationDomain("github.com/The-Repo-Club")
        QCoreApplication.setApplicationName("MultiMonitorLock-Gui")
        Gui = MultiMonitorLock()
        Gui.show()
        currentExitCode = app.exec_()
        app = None
