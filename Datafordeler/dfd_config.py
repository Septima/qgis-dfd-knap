from builtins import str
import codecs
import os.path
import datetime
from urllib.request import (
    urlopen
)
from urllib.error import (
    URLError,
    HTTPError
)
from qgis.gui import QgsMessageBar
from qgis.core import *
from qgis.PyQt.QtCore import QCoreApplication, QFileInfo, QFile, QUrl, QSettings, QTranslator, qVersion, QIODevice

from qgis.PyQt.QtWidgets import QAction, QMenu, QPushButton
from qgis.PyQt.QtGui import QIcon

from qgis.PyQt import QtCore, QtXml

import json

from .qlr_file import QlrFile

FILE_MAX_AGE = datetime.timedelta(hours=12)
DFD_SERVICES_URL = 'http://services.kortforsyningen.dk/service?request=GetServices&login={{kf_username}}&password={{kf_password}}'

def log_message(message):
    QgsMessageLog.logMessage(message, 'Datafordeler plugin')

class DfdConfig(QtCore.QObject):
    
    dfd_con_error = QtCore.pyqtSignal()
    dfd_settings_warning = QtCore.pyqtSignal()

    def __init__(self, settings):
        super(DfdConfig, self).__init__()
        self.settings = settings

    def load(self):
        self.cached_dfd_qlr_filename = self.settings.value('cache_path') + 'datafordeler_data.qlr'
        self.allowed_dfd_services = {}
        if self.settings.is_set():
            try:
                self.allowed_dfd_services = self.get_allowed_dfd_services()
                self.dfd_qlr_file = self.get_dfd_qlr_file()
                self.background_category, self.categories = self.get_dfd_categories()
            except Exception as e:
                self.dfd_con_error.emit()
                self.background_category = None
                self.categories = []
            self.debug_write_allowed_services()
        else:
            self.dfd_settings_warning.emit()
            self.background_category = None
            self.categories = []

    def get_allowed_dfd_services(self):
        allowed_dfd_services = {}
        allowed_dfd_services['any_type'] = {'services': []}
        url_to_get = self.insert_username_password(DFD_SERVICES_URL)
        response = urlopen(url_to_get)
        xml = response.read()
        doc = QtXml.QDomDocument()
        doc.setContent(xml)
        service_types = doc.documentElement().childNodes()
        i = 0
        while i<service_types.count():
            service_type = service_types.at(i)
            service_type_name= service_type.nodeName()
            allowed_dfd_services[service_type_name] = {'services': []}
            services = service_type.childNodes()
            j = 0
            while j<services.count():
                service = services.at(j)
                service_name = service.nodeName()
                allowed_dfd_services[service_type_name]['services'].append(service_name)
                allowed_dfd_services['any_type']['services'].append(service_name)
                j = j + 1
            i = i + 1
        return allowed_dfd_services

    def get_categories(self):
         return self.categories
         
    def get_background_category(self):
         return self.background_category

    def get_maplayer_node(self, id):
         return self.dfd_qlr_file.get_maplayer_node(id)
     
    def get_dfd_categories(self):
        dfd_categories = []
        dfd_background_category = None
        groups_with_layers = self.dfd_qlr_file.get_groups_with_layers()
        for group in groups_with_layers:
            dfd_category = {
                'name': group['name'],
                'selectables': []
            }
            for layer in group['layers']:
                if self.user_has_access(layer['service']):
                    dfd_category['selectables'].append({
                        'type': 'layer',
                        'source': 'dfd',
                        'name': layer['name'],
                        'id': layer['id']
                        }
                    )
            if len(dfd_category['selectables']) > 0:
                dfd_categories.append(dfd_category)
                if group['name'] == 'Baggrundskort':
                    dfd_background_category = dfd_category
        return dfd_background_category, dfd_categories

    def user_has_access(self, service_name):
        return service_name in self.allowed_dfd_services['any_type']['services']

    def get_custom_categories(self):
        return []

    def get_dfd_qlr_file(self):
        config = None
        load_remote_config = True

        local_file_exists = os.path.exists(self.cached_dfd_qlr_filename)
        if local_file_exists:
            config = self.read_cached_dfd_qlr()
            local_file_time = datetime.datetime.fromtimestamp(
                os.path.getmtime(self.cached_dfd_qlr_filename)
            )
            load_remote_config = local_file_time < datetime.datetime.now() - FILE_MAX_AGE

        if load_remote_config:
            try:
                config = self.get_remote_dfd_qlr()
            except Exception as e:
                log_message(u'No contact to the configuration at ' + self.settings.value('dfd_qlr_url') + '. Exception: ' + str(e))
                if not local_file_exists:
                    self.error_menu = QAction(
                        self.tr('No contact to Datafordeler'),
                        self.iface.mainWindow()
                    )
                return
            self.write_cached_dfd_qlr(config)
        if config:
            config = self.read_cached_dfd_qlr()
            return QlrFile(config)
        else:
            return None

    def read_cached_dfd_qlr(self):
        #return file(unicode(self.cached_kf_qlr_filename)).read()
        f = QFile(self.cached_dfd_qlr_filename)
        f.open(QIODevice.ReadOnly)
        return f.readAll()

        #with codecs.open(self.cached_kf_qlr_filename, 'r', 'utf-8') as f:
        #    return f.read()

    def get_remote_dfd_qlr(self):
        response = urlopen(self.settings.value('dfd_qlr_url'))
        content = response.read()
        content = str(content, 'utf-8')
        content = self.insert_username_password(content)
        return content

    def write_cached_dfd_qlr(self, contents):
        """We only call this function IF we have a new version downloaded"""
        # Remove old versions file
        if os.path.exists(self.cached_dfd_qlr_filename):
            os.remove(self.cached_dfd_qlr_filename)

        # Write new version
        with codecs.open(self.cached_dfd_qlr_filename, 'w', 'utf-8') as f:
            f.write(contents)

    def debug_write_allowed_services(self):
        try:
            debug_filename = self.settings.value('cache_path') + self.settings.value('username') + '.txt'
            if os.path.exists(debug_filename):
                os.remove(debug_filename)
            with codecs.open(debug_filename, 'w', 'utf-8') as f:
                f.write(json.dumps(self.allowed_dfd_services['any_type']['services'], indent=2).replace('[', '').replace(']', ''))
        except Exception as e:
            pass

    def insert_username_password(self, text):
        result = text
        replace_vars = {}
        replace_vars["kf_username"] = self.settings.value('username')
        replace_vars["kf_password"] = self.settings.value('password')
        for i, j in replace_vars.items():
            result = result.replace("{{" + str(i) + "}}", str(j))
        return result



