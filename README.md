# About
This is a simple PySide6 application to show the data from a MSAccess database. It allows you to select your Mircosoft Access database, load, see the tables and data inside it    
# Requirements
- Python 3.x
- PySide6
- pandas
- pyodbc
# Installation
Clone the repo:
```
git clone https://github.com/mostafa-binesh/Datall-Interview-Question
cd Datall-Interview-Question
```
Create and activate venv:
```
python -m venv venv
.\venv\Scripts\activate
```
Install the requirements:
```
pip install -r ./requirements.txt  
```
# How To Work
After passing Installation section, just run the main python file:  
```
python main.py   
```
Click on the "Select Database" button and choose your access database. for your convenience there is a demo access file in the repo.
After connecting to the database successfully, you can see the database's tables in the dropdown. Select a table and data will be shown in a dataframe
# Demo
![Main_page](https://github.com/user-attachments/assets/5d78ce90-baba-4943-9355-02086f4be184)
![ShowData](https://github.com/user-attachments/assets/c312d599-0f0f-4f9d-a5e8-0b65e0c8a4e3)
