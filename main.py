import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTableView, QMessageBox
from PySide6.QtCore import QAbstractTableModel, Qt
import pandas as pd
import pyodbc

class DatabaseHandler:
    def __init__(self, databasePath: str):
        self.databasePath = databasePath
        self.connection = None

    def connect(self):
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

        self.tableView = QTableView()
        self.setCentralWidget(self.tableView)
        self.initUI()

    def initUI(self):
        databasePath = './Restaurant.accdb'
        tableName = 'Food'

        dbHandler = DatabaseHandler(databasePath)
        dbHandler.connect()
        try:
            df = dbHandler.readTable(tableName)
            print("here df", df)
            if df.empty:
                QMessageBox.warning(self, "DataFrame Warning", "The DataFrame is empty.")
            else:
                self.displayTable(df)
        except Exception as e:
            QMessageBox.critical(self, "Database Error", str(e))

    def displayTable(self, df: pd.DataFrame):
        model = DataFrameModel(df)
        self.tableView.setModel(model)

def main():
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
