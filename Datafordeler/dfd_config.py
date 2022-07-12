from builtins import str
import codecs
import os.path
import datetime
#from urllib.request import (
#    urlopen
#
from urllib import (
    request
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

from qgis.PyQt.QtNetwork import QNetworkRequest

import hashlib
import glob
import json
import traceback

from .qlr_file import QlrFile

FILE_MAX_AGE = datetime.timedelta(hours=12)


def log_message(message):
    QgsMessageLog.logMessage(message, 'Datafordeler plugin')

def log_error(error):
    QgsMessageLog.logMessage(message=error, tag='Datafordeler plugin', level= Qgis.MessageLevel.Critical)

class DfdConfig(QtCore.QObject):
    
    dfd_con_error = QtCore.pyqtSignal()
    dfd_settings_warning = QtCore.pyqtSignal()

    def __init__(self, settings):
        super(DfdConfig, self).__init__()
        self.settings = settings

    def load(self):
        username_password_combined = self.settings.value('password') + self.settings.value('username')
        self.cached_dfd_qlr_filename = self.settings.value('cache_path') + hashlib.md5(username_password_combined.encode()).hexdigest() + '_datafordeler_data.qlr'
        self.allowed_dfd_services = {}
        if self.settings.is_set():
            try:
                self.dfd_qlr_file = self.get_dfd_qlr_file()
                self.categories = self.get_dfd_categories()
            except Exception as e:
                self.dfd_con_error.emit()
                self.categories = []
            self.debug_write_allowed_services()
        else:
            self.dfd_settings_warning.emit()
            self.categories = []

    def get_categories(self):
         return self.categories
         
    def get_maplayer_node(self, id):
         return self.dfd_qlr_file.get_maplayer_node(id)
     
    def get_dfd_categories(self):
        dfd_categories = []
        groups_with_layers = self.dfd_qlr_file.get_groups_with_layers()
        for group in groups_with_layers:
            dfd_category = {
                'name': group['name'],
                'selectables': []
            }
            for layer in group['layers']:
                dfd_category['selectables'].append({
                    'type': 'layer',
                    'source': 'dfd',
                    'name': layer['name'],
                    'id': layer['id']
                    }
                )
            if len(dfd_category['selectables']) > 0:
                dfd_categories.append(dfd_category)
        return dfd_categories

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
                log_error(u'No contact to the configuration at ' + self.settings.value('dfd_qlr_url') + '. Exception: ' + traceback.format_exc())
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

    def get_remote_dfd_qlr(self):
        url = QUrl(self.settings.value('dfd_qlr_url'))
        qnetworkrequest = QNetworkRequest(url)
        request = QgsBlockingNetworkRequest()
        request.get(request=qnetworkrequest, forceRefresh=True)
        reply = request.reply()
        content = reply.content()
        content = str(content, 'utf-8')
        content = self.insert_username_password(content)
        return content

    def write_cached_dfd_qlr(self, contents):
        """We only call this function IF we have a new version downloaded"""
        # Remove old versions file
        for filename in glob.glob(self.settings.value('cache_path') + '*_datafordeler_data.qlr'):
            os.remove(filename)

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
        replace_vars["username"] = self.settings.value('username')
        replace_vars["password"] = self.settings.value('password')
        for i, j in replace_vars.items():
            result = result.replace("{{" + str(i) + "}}", str(j))
        return result



