from .dfd_config import DfdConfig
from .local_config import LocalConfig
from qgis.PyQt import (
    QtCore
)

class Config(QtCore.QObject):

    dfd_con_error = QtCore.pyqtSignal()
    dfd_settings_warning = QtCore.pyqtSignal()
            
    def __init__(self, settings):
        super(Config, self).__init__()
        self.settings = settings
        self.dfd_config = DfdConfig(settings)
        self.dfd_config.dfd_con_error.connect(self.propagate_dfd_con_error)
        self.dfd_config.dfd_settings_warning.connect(self.propagate_dfd_settings_warning)

        self.local_config = LocalConfig(settings)

    def propagate_dfd_settings_warning(self):
        self.dfd_settings_warning.emit()
        
    def propagate_dfd_con_error(self):
        self.dfd_con_error.emit()
        
    def load(self):
        
        self.dfd_config.load()

        self.categories = []
        self.categories_list = []

        self.dfd_categories = self.dfd_config.get_categories()
        
        self.categories = self.dfd_categories
        
        self.categories_list.append(self.dfd_categories)

    def get_category_lists(self):
        return self.categories_list
    
    def get_categories(self):
        return self.categories

    def get_dfd_maplayer_node(self, id):
        return self.dfd_config.get_maplayer_node(id)
    
    def get_local_maplayer_node(self, id):
        return self.local_config.get_maplayer_node(id)
