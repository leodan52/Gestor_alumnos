# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ventana_directorios.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Ventana_Directorios(object):
    def setupUi(self, Ventana_Directorios):
        Ventana_Directorios.setObjectName("Ventana_Directorios")
        Ventana_Directorios.resize(672, 198)
        Ventana_Directorios.setMinimumSize(QtCore.QSize(672, 198))
        Ventana_Directorios.setMaximumSize(QtCore.QSize(672, 198))
        self.verticalLayout = QtWidgets.QVBoxLayout(Ventana_Directorios)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(Ventana_Directorios)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.widget = QtWidgets.QWidget(self.frame)
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.Entrada_BaseDatos = QtWidgets.QLineEdit(self.widget)
        self.Entrada_BaseDatos.setObjectName("Entrada_BaseDatos")
        self.horizontalLayout.addWidget(self.Entrada_BaseDatos)
        self.Boton_BaseDatos = QtWidgets.QToolButton(self.widget)
        self.Boton_BaseDatos.setObjectName("Boton_BaseDatos")
        self.horizontalLayout.addWidget(self.Boton_BaseDatos)
        self.verticalLayout_2.addWidget(self.widget)
        self.widget_2 = QtWidgets.QWidget(self.frame)
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget_2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_3 = QtWidgets.QLabel(self.widget_2)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.Entrada_BasePDF = QtWidgets.QLineEdit(self.widget_2)
        self.Entrada_BasePDF.setObjectName("Entrada_BasePDF")
        self.horizontalLayout_2.addWidget(self.Entrada_BasePDF)
        self.Boton_BasePDF = QtWidgets.QToolButton(self.widget_2)
        self.Boton_BasePDF.setObjectName("Boton_BasePDF")
        self.horizontalLayout_2.addWidget(self.Boton_BasePDF)
        self.verticalLayout_2.addWidget(self.widget_2)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.verticalLayout.addWidget(self.frame)
        self.buttonBox = QtWidgets.QDialogButtonBox(Ventana_Directorios)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Ventana_Directorios)
        self.buttonBox.accepted.connect(Ventana_Directorios.accept)
        self.buttonBox.rejected.connect(Ventana_Directorios.reject)
        QtCore.QMetaObject.connectSlotsByName(Ventana_Directorios)

    def retranslateUi(self, Ventana_Directorios):
        _translate = QtCore.QCoreApplication.translate
        Ventana_Directorios.setWindowTitle(_translate("Ventana_Directorios", "Elige tus directorios"))
        self.label.setText(_translate("Ventana_Directorios", "<html><head/><body><p>Elige donde estarán las carpetas de trabajo:</p></body></html>"))
        self.label_2.setText(_translate("Ventana_Directorios", "<html><head/><body><p>¿Dónde está tu base de datos?</p></body></html>"))
        self.Boton_BaseDatos.setText(_translate("Ventana_Directorios", "..."))
        self.label_3.setText(_translate("Ventana_Directorios", "<html><head/><body><p>¿Dónde guardas los PDF de los alumnos?</p></body></html>"))
        self.Boton_BasePDF.setText(_translate("Ventana_Directorios", "..."))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Ventana_Directorios = QtWidgets.QDialog()
    ui = Ui_Ventana_Directorios()
    ui.setupUi(Ventana_Directorios)
    Ventana_Directorios.show()
    sys.exit(app.exec_())
