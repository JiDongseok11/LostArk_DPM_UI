# -*- coding: utf-8 -*-
import sys
import json

from PyQt5.QtWidgets import *
from PyQt5 import uic

from lostark_sim import lostark_sim

CLASSNAME_LIST = ["class1", "class2", "class3"]
ARTIFACT_LIST = ["artifact1", "artifact2", "artifact3"]
ENGRAVING_LIST = ["engrave1", 'engrave2', "engrave3", "engrave4", "engrave5", "engrave6"]

CHARACTER_SETTING_FILEPATH = './DB/character_settings.json'

setting_form_class = uic.loadUiType("sample.ui")[0]
result_form_class = uic.loadUiType("sample_result.ui")[0]

class SettingWindowClass(QDialog, setting_form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.setFixedHeight(254)

        self.lostark_sim = lostark_sim()
        self.flag = False

        with open(CHARACTER_SETTING_FILEPATH, 'r') as load_file:
            self.loaded_data = json.load(load_file)
        self.character_setting_keys = list(self.loaded_data['character_settings'][0].keys())
        
        self.result_dict = dict()

        self.set_elements_enable(False)
        self.generate_class_CB()

        self.buttonBox.accepted.connect(self.accepted)
        self.buttonBox.rejected.connect(self.rejected)

        self.class_CB.currentIndexChanged.connect(self.class_selected_func)
        self.artifact_CB.currentIndexChanged.connect(self.artifact_selected_func)
        self.engraving_CB1.currentIndexChanged.connect(lambda: self.engraving_selected_func('1'))
        self.engraving_CB2.currentIndexChanged.connect(lambda: self.engraving_selected_func('2'))
        self.engraving_CB3.currentIndexChanged.connect(lambda: self.engraving_selected_func('3'))
        self.engraving_CB4.currentIndexChanged.connect(lambda: self.engraving_selected_func('4'))
        self.engraving_CB5.currentIndexChanged.connect(lambda: self.engraving_selected_func('5'))
        self.engraving_CB6.currentIndexChanged.connect(lambda: self.engraving_selected_func('6'))

    def set_elements_enable(self, bool):
        self.artifact_CB.setEnabled(bool)
        for i in range(4):
            getattr(self, 'stat_SB'+str(i+1)).setEnabled(bool)
        for j in range(6):
            getattr(self, 'engraving_CB'+str(j+1)).setEnabled(bool)

    def class_selected_func(self):
        if self.class_CB.currentIndex() == 0:
            self.flag = False
            self.set_elements_enable(False)
            self.clear_elements()
        else:
            self.flag = True
            print(f"{self.class_CB.currentText()} class has selected")
            self.set_elements_enable(True)
            self.update_artifact_CB()
            self.update_engraving_CB()    

    def artifact_selected_func(self):
        selected_index = self.artifact_CB.currentIndex()
        if selected_index == 0:
            self.flag = False
        else:
            self.flag = True
            print(f"{self.artifact_CB.currentText()} artifact has selected")

    def engraving_selected_func(self, index):
        selected_index = getattr(self, 'engraving_CB'+index).currentIndex()
        if selected_index == 0:
            return True
        else:
            print(f"{getattr(self, 'engraving_CB'+index).currentText()} engraving has selected as engraving "+index)
        
    def generate_class_CB(self):
        self.class_CB.addItem("Choose class")
        classnames = self.lostark_sim.get_character_file_names()
        for classname in classnames:
            classname = classname[10:-5]
            self.class_CB.addItem(classname)

    def generate_artifact_CB(self):
        self.artifact_CB.addItem("Choose artifact")
        self.flag = False
        artifacts = self.lostark_sim.get_artifacts()
        for artifact in artifacts:
            self.artifact_CB.addItem(artifact)

    def generate_engraving_CB(self):
        engravings = self.lostark_sim.get_engravings()
        for i in range(6):
            getattr(self, 'engraving_CB'+str(i+1)).addItem("Choose engraving")
            for engraving in engravings:
                getattr(self, 'engraving_CB'+str(i+1)).addItem(engraving)

    def update_artifact_CB(self):
        if self.artifact_CB.count():
            return True
        else:
            self.generate_artifact_CB()

    def update_engraving_CB(self):
        if self.engraving_CB1.count():
            return True
        else:
            self.generate_engraving_CB()

    def get_stat_SB_value(self, index):
        return getattr(self, 'stat_SB'+str(index)).value()

    def clear_elements(self):
        print("element clear")
        
    def accepted(self):
        if self.flag:
            skill_set_path = f"./db/skills/{self.class_CB.currentText()}.json"
            self.add_character_setting(self.character_setting_keys[0], self.lostark_sim.get_one_character_name(f"character_{self.class_CB.currentText()}.json"))
            for i in range(4):
                self.add_character_setting(self.character_setting_keys[i+1], getattr(self, 'stat_SB'+str(i+1)).value())
            for i in range(6):
                if getattr(self, 'engraving_CB'+str(i+1)).currentIndex() != 0:
                    self.add_character_setting(self.character_setting_keys[5], getattr(self, 'engraving_CB'+str(i+1)).currentText())
            #self.add_character_setting(self.character_setting_keys[6], None)
            self.add_character_setting(self.character_setting_keys[7], self.artifact_CB.currentText())
            self.add_character_setting(self.character_setting_keys[8],skill_set_path)

            self.result_json = dict()
            temp = []
            temp.append(self.result_dict)
            self.result_json.setdefault('character_settings', temp)
            self.test()
            self.lostark_sim.run_simulator(self.result_json)
            print("accepted")
            self.open_result_window()
        else:
            print("fail")

    def rejected(self):
        print("rejected")

    def add_character_setting(self, key, value):
        try:
            if type(self.result_dict[key]) is list:
                self.result_dict[key].append(value)
            else:
                self.result_dict[key] = value
        except:
            if key == "engravings" or key == "options" or key == "artifact_set":
                temp_value = []
                temp_value.append(value)
                self.result_dict.setdefault(key, temp_value)
            else:
                self.result_dict.setdefault(key, value)

    def open_result_window(self):
        self.hide()
        self.result_window = ResultWindowClass(self.result_json)
        self.result_window.exec()
        self.show()

    def test(self):
        file_path = "./saved_json.json"
        with open(file_path, 'w', encoding='UTF-8') as makefile:
            json.dump(self.result_json, makefile, indent = '\t')

class ResultWindowClass(QDialog, result_form_class) :
    def __init__(self, result_dict) :
        super().__init__()
        self.setupUi(self)
        self.show()
        self.result_dict = result_dict
        print(self.result_dict)
        #self.share_TW.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)

        def run_simulator(self):
            return True

if __name__ == "__main__" :
    app = QApplication(sys.argv) 

    myWindow = SettingWindowClass()

    myWindow.show()

    app.exec_()