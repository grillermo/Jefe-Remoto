from PyQt4.QtCore import *
from PyQt4.QtGui import *

CONNECTION_STATE, NAME, IPADRESSS, TRANSFER_STATE = range(4)

class machinesTableModel(QAbstractTableModel):
    def __init__(self, machines = {}):
        super(machinesTableModel, self).__init__()
        self.machines = machines

    def headerData(self, section,orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return 'Nombre'
            else:
                return 'Compu'

    def data(self, index, role=Qt.DisplayRole):
        if (not index.isValid() or
            not (0 <= index.row() < len(self.machines))):
            return None

        if role == Qt.DecorationRole:
            value = "00fff000"
            pixmap = QtGui.QPixmap(24,24)
            pixmap.fill(value)
            icon = QtGui.QIcon(pixmap)
            return icon

        if role == Qt.DisplayRole:
            if colum == NAME:
                return QVariant('PC01IP23')
            if column == IPADRESSS:
                return QVariant(machine['PC01IP23'])


    def rowCount(self, parent):
        return len(self.machines)

    def columnCount(self, index=QModelIndex()):
        return 4 # connection State, Name, IP Address, File transfer state
##    def headerData(self):
##        pass
##    def flags(self):
##        pass
##    def setData(self):
##        pass
##    def insertRows(self):
##        pass
##    def removeRows(self):
##        pass


def main():
    pass

if __name__ == '__main__':
    main()
