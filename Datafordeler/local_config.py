from builtins import object
from qgis.PyQt.QtCore import QFile, QIODevice
import os.path
from .qlr_file import QlrFile

class LocalConfig(object):
    
    def __init__(self, settings):
        self.settings = settings
        self.reload()
    
    def reload(self):
        self.categories = []

    def read_local_qlr(self):
        f = QFile(self.local_qlr_filename)
        f.open(QIODevice.ReadOnly)
        return f.readAll()
        
    def get_local_categories(self):
        local_categories = []
        groups_with_layers = self.qlr_file.get_groups_with_layers()
        for group in groups_with_layers:
            local_category = {
                'name': group['name'],
                'selectables': []
            }
            for layer in group['layers']:
                local_category['selectables'].append({
                    'type': 'layer',
                    'source': 'local',
                    'name': layer['name'],
                    'id': layer['id']
                    }
                )
            if len(local_category['selectables']) > 0:
                local_categories.append(local_category)
        return local_categories
    
    def get_categories(self):
        return self.categories
    
    def get_maplayer_node(self, id):
         return self.qlr_file.get_maplayer_node(id)
     

        
