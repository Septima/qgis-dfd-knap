# -*- coding: utf-8 -*-
import os
from PyQt5.QtCore import QFileInfo, QObject
from qgis.PyQt import QtCore

from .qgissettingmanager import *
CONFIG_FILE_URL ='https://apps2.kortforsyningen.dk/qgis_knap_config/Kortforsyningen/kf/kortforsyning_data.qlr'

class Settings(SettingManager):
    settings_updated = QtCore.pyqtSignal()

    def __init__(self):
        SettingManager.__init__(self, 'Datafordeler')
        self.add_setting(String('username', Scope.Global, ''))
        self.add_setting(String('password', Scope.Global, ''))
        path = QFileInfo(os.path.realpath(__file__)).path()
        dfd_path = path + '/dfd/'
        if not os.path.exists(dfd_path):
            os.makedirs(dfd_path)
            
        self.add_setting(String('cache_path', Scope.Global, dfd_path))
        self.add_setting(String('dfd_qlr_url', Scope.Global, CONFIG_FILE_URL))
        
    def is_set(self):
        if self.value('username') and self.value('password'):
            return True
        return False
    
    def emit_updated(self):
        self.settings_updated.emit()

