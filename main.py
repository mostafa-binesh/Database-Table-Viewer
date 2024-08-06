import sys
from PySide6.QtWidgets import QApplication, QMessageBox
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
        query = f"SELECT * FROM {tableName}"
        try:
            df = pd.read_sql(query, self.connection)
            return df
        except Exception as e:
            print(f"Error reading table {tableName}: {e}")
            return pd.DataFrame()

def main():
    app = QApplication(sys.argv)
    
    databasePath = 'Restaurant.accdb'
    tableName = 'Food'
    
    dbHandler = DatabaseHandler(databasePath)
    dbHandler.connect()
    
    try:
        df = dbHandler.readTable(tableName)
        print(df)
    except Exception as e:
        QMessageBox.critical(None, "Database Error: ", str(e))
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
