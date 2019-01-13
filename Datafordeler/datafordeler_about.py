# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DatafordelerAboutDialog
                                 A QGIS plugin
 Easy access to webservices from Datafordeler
                             -------------------
        begin                : 2019-01-02
        git sha              : $Format:%H$
        copyright            : (C) 2019 Septima
        email                : kontakt@septima.dk
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog

FORM_CLASS, _ = uic.loadUiType(
    os.path.join(os.path.dirname(__file__), 'aboutKortforsyningen.ui')
)


class KFAboutDialog(QDialog, FORM_CLASS):
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)
