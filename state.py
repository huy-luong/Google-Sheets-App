import pyodbc
from collections import defaultdict

cnxn = pyodbc.connect('DSN=CData GoogleSheets Source Sys')

cursor = cnxn.cursor()
#store of all data from Products sheet
#user_input = input("Please enter the country name to see all products offered by suppliers from that country:")
cursor.execute("SELECT p.ShipCountry, ROUND(AVG(CAST(p.OrderPrice AS FLOAT)), 2) From Northwind_Orders p WHERE p.ShipCountry != '' GROUP BY p.ShipCountry ORDER BY p.ShipCountry")
orders = cursor.fetchall()
cursor.close()

for order in orders:
    print(order)
