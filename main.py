import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QTableView, QMessageBox,
    QPushButton, QFileDialog, QComboBox, QHBoxLayout, QLabel
)
from PySide6.QtCore import QAbstractTableModel, Qt
import pandas as pd
import pyodbc

class DatabaseHandler:
    def __init__(self, databasePath: str = None):
        self.databasePath = databasePath
        self.connection = None

    def setDatabasePath(self, databasePath: str):
        self.databasePath = databasePath

    def connect(self):
        if not self.databasePath:
            raise Exception("Database path not set.")
        
        try:
            connStr = (
                r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
                f'DBQ={self.databasePath};'
            )
            self.connection = pyodbc.connect(connStr)
            print("Connected to the database successfully")
        except pyodbc.Error as e:
            print(f"Error connecting to database: {e}")
            self.connection = None

    def getTables(self):
        if self.connection is None:
            raise Exception("No database connection. Please connect first.")
        
        try:
            cursor = self.connection.cursor()
            tables = [table.table_name for table in cursor.tables(tableType='TABLE')]
            return tables
        except pyodbc.Error as e:
            print(f"Fetching tables failed: {e}")
            return []

    def readTable(self, tableName: str) -> pd.DataFrame:
        if self.connection is None:
            raise Exception("No database connection. Please connect first.")
        
        query = f"SELECT * FROM {tableName}"
        try:
            df = pd.read_sql(query, self.connection)
            return df
        except Exception as e:
            print(f"Error reading table {tableName}: {e}")
            return pd.DataFrame()

class DataFrameModel(QAbstractTableModel):
    def __init__(self, df: pd.DataFrame):
        QAbstractTableModel.__init__(self)
        self._df = df

    def rowCount(self, parent=None):
        return self._df.shape[0]

    def columnCount(self, parent=None):
        return self._df.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid() and role == Qt.DisplayRole:
            return str(self._df.iloc[index.row(), index.column()])
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self._df.columns[section]
            elif orientation == Qt.Vertical:
                return str(self._df.index[section])
        return None

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Database Table Viewer")
        self.setGeometry(100, 100, 800, 600)
        
        self.dbHandler = DatabaseHandler()

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.layout = QVBoxLayout()
        self.centralWidget.setLayout(self.layout)

        self.selectButton = QPushButton("Select Database")
        self.selectButton.clicked.connect(self.selectDatabase)
        self.layout.addWidget(self.selectButton, alignment=Qt.AlignCenter)

        self.tableCombo = QComboBox()
        self.tableCombo.setEnabled(False)
        self.tableCombo.currentIndexChanged.connect(self.tableSelected)

        self.layout.addWidget(self.tableCombo, alignment=Qt.AlignCenter)

        self.tableView = QTableView()
        self.layout.addWidget(self.tableView)

    def selectDatabase(self):
        fileDialog = QFileDialog()
        fileDialog.setFileMode(QFileDialog.ExistingFile)
        fileDialog.setNameFilter("Access Database Files (*.accdb *.mdb)")
        if fileDialog.exec_():
            databasePath = fileDialog.selectedFiles()[0]
            self.dbHandler.setDatabasePath(databasePath)
            try:
                self.dbHandler.connect()
                tables = self.dbHandler.getTables()


                if tables:
                    self.tableCombo.clear()
                    self.tableCombo.addItems(tables)
                    self.tableCombo.setEnabled(True)
                    QMessageBox.information(self, "Database Connected", "Connected to database successfully!")
                else:
                    QMessageBox.warning(self, "No Tables Found", "The selected database has no tables.")
            except Exception as e:
                QMessageBox.critical(self, "Connection Error", str(e))

    def tableSelected(self):
        tableName = self.tableCombo.currentText()
        if tableName:
            try:
                df = self.dbHandler.readTable(tableName)
                if df.empty:
                    QMessageBox.warning(self, "DataFrame Warning", "The selected table is empty.")
                else:
                    self.displayTable(df)

            except Exception as e:
                QMessageBox.critical(self, "Error Reading Table", str(e))

    def displayTable(self, df: pd.DataFrame):
        model = DataFrameModel(df)
        self.tableView.setModel()

def main():
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
