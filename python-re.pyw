# -*- coding: utf-8 -*-
from __future__ import print_function
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtUiTools import QUiLoader
import sys
import cgi
from re_calc import *


class UI_MainWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        loader = QUiLoader()
        self.ui = loader.load("main.ui")
        self.ui.show()
        self.cb = QApplication.clipboard()
        self.connect(self.ui.textEdit_regex, SIGNAL("textChanged()"), self.regex_changed)
        self.connect(self.ui.textEdit_replaceString, SIGNAL("textChanged()"), self.replace_changed)
        self.connect(self.ui.textEdit_input, SIGNAL("textChanged()"), self.input_changed)
        self.connect(self.ui.lineEdit_additParam, SIGNAL("textChanged(QString)"), self.additParam_changed)
        self.connect(self.ui.pushButton_flagI, SIGNAL("toggled(bool)"), self.flag_toggled)
        self.connect(self.ui.pushButton_flagL, SIGNAL("toggled(bool)"), self.flag_toggled)
        self.connect(self.ui.pushButton_flagM, SIGNAL("toggled(bool)"), self.flag_toggled)
        self.connect(self.ui.pushButton_flagS, SIGNAL("toggled(bool)"), self.flag_toggled)
        self.connect(self.ui.pushButton_flagU, SIGNAL("toggled(bool)"), self.flag_toggled)
        self.connect(self.ui.pushButton_findAll, SIGNAL("toggled(bool)"), self.toggle_function_buttons)
        self.connect(self.ui.pushButton_match, SIGNAL("toggled(bool)"), self.toggle_function_buttons)
        self.connect(self.ui.pushButton_split, SIGNAL("toggled(bool)"), self.toggle_function_buttons)
        self.connect(self.ui.pushButton_search, SIGNAL("toggled(bool)"), self.toggle_function_buttons)
        self.connect(self.ui.pushButton_sub, SIGNAL("toggled(bool)"), self.toggle_function_buttons)
        self.connect(self.ui.pushButton_clipboardInput, SIGNAL("clicked(bool)"), self.clipboardInput)
        self.connect(self.ui.pushButton_clipboardResult, SIGNAL("clicked(bool)"), self.clipboardResult)
        self.connect(self.ui.pushButton_clipboardReplace, SIGNAL("clicked(bool)"), self.clipboardReplace)
        self.connect(self.ui.pushButton_clipboardPattern, SIGNAL("clicked(bool)"), self.clipboardPattern)
        self.connect(self.ui.pushButton_unicodeResult, SIGNAL("toggled(bool)"), self.toggle_unicode)
        self.ui.label_additParam.hide()
        self.ui.lineEdit_additParam.hide()
        self.ui.label_replaceString.hide()
        self.ui.pushButton_clipboardReplace.hide()
        self.ui.textEdit_replaceString.hide()
        self.update_result()

    def toggle_unicode(self, pressed):
        self.update_result()

    def clipboardInput(self):
        self.cb.clear(mode=self.cb.Clipboard)
        self.cb.setText(self.ui.textEdit_input.toPlainText(), mode=self.cb.Clipboard)

    def clipboardResult(self):
        self.cb.clear(mode=self.cb.Clipboard)
        self.cb.setText(self.ui.textEdit_result.toPlainText(), mode=self.cb.Clipboard)

    def clipboardReplace(self):
        self.cb.clear(mode=self.cb.Clipboard)
        self.cb.setText(self.ui.textEdit_replaceString.toPlainText(), mode=self.cb.Clipboard)

    def clipboardPattern(self):
        self.cb.clear(mode=self.cb.Clipboard)
        self.cb.setText(self.ui.textEdit_regex.toPlainText(), mode=self.cb.Clipboard)

    def toggle_function_buttons(self, pressed):
        """toggle buttons of choice of regex functions"""
        if pressed:
            regex_struct.function = self.sender().objectName()[11:]
            functions = {'findAll', 'match', 'split', 'search', 'sub'}
            functions.remove(regex_struct.function)
            if regex_struct.function == 'sub':
                self.ui.label_replaceString.show()
                self.ui.pushButton_clipboardReplace.show()
                self.ui.textEdit_replaceString.show()
            else:
                self.ui.label_replaceString.hide()
                self.ui.pushButton_clipboardReplace.hide()
                self.ui.textEdit_replaceString.hide()
            if regex_struct.function in {'sub', 'split'}:
                self.ui.label_additParam.show()
                self.ui.lineEdit_additParam.show()
                if regex_struct.function == 'sub':
                    self.ui.label_additParam.setText("Count:")
                else:
                    self.ui.label_additParam.setText("Max split:")
            else:
                self.ui.label_additParam.hide()
                self.ui.lineEdit_additParam.hide()
            # disable pressed button
            eval("self.ui.pushButton_" + regex_struct.function + '.setDisabled(True)')
            for f in functions:
                # enable non pressed buttons
                eval("self.ui.pushButton_" + f + '.setDisabled(False)')
                # release previous chosen function button
                eval("self.ui.pushButton_" + f + '.setChecked(False)')
            self.ui.textEdit_regex.setFocus()
        self.update_result()

    def flag_toggled(self, pressed):
        """toggle buttons of flags"""
        eval('regex_struct.change_flags(re.' + str(self.sender().objectName())[15] + ', pressed)')
        self.update_result()

    def additParam_changed(self):
        """changed additional parameter"""
        self.update_result()

    def regex_changed(self):
        """changed text in Pattern plainTextEdit"""
        temp_str = self.ui.textEdit_regex.toPlainText()
        if '\n' in temp_str:
            temp_str = re.sub('\n', '', temp_str)
            self.ui.textEdit_regex.setPlainText(temp_str)
        regex_struct.regex_string = self.ui.textEdit_regex.toPlainText()
        self.update_result()

    def replace_changed(self):
        """change text in Replace plainTextEdit"""
        temp_str = self.ui.textEdit_replaceString.toPlainText()
        if '\n' in temp_str:
            temp_str = re.sub('\n', '', temp_str)
            self.ui.textEdit_replaceString.setPlainText(temp_str)
        regex_struct.replace_string = self.ui.textEdit_replaceString.toPlainText()
        self.update_result()

    def input_changed(self):
        """changed text in Input plainTextEdit"""
        regex_struct.input = self.ui.textEdit_input.toPlainText()
        self.update_result()

    def update_result(self):
        """update result textEdit with escaped characters"""
        regex_struct.calc_result(self.ui.pushButton_unicodeResult.isChecked(), self.ui.lineEdit_additParam.text())
        self.ui.textEdit_result.setText((cgi.escape(regex_struct.result)))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UI_MainWidget()
    sys.exit(app.exec_())