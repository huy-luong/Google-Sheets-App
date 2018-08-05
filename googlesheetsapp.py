import pyodbc
import sys
from collections import defaultdict

# Begin application in pickState
state = "pickState"
# List of all states
states = ["A", "B", "C", "D"]

print("Fetching spreadsheet data . . .")
# Creating connection to ODBC Driver
cnxn = pyodbc.connect('DSN=CData GoogleSheets Source Sys;')
cursor = cnxn.cursor()
# store of all data from Products sheet
cursor.execute("SELECT * FROM Northwind_Products")
products = cursor.fetchall()
#  store all data from Suppliers sheet
cursor.execute("SELECT * From Northwind_Suppliers")
suppliers = cursor.fetchall()
# store all data from Orders sheet
cursor.execute("SELECT * From Northwind_Orders")
orders = cursor.fetchall()
cnxn.close()

# Fetch all of the countries of the suppliers
countries = []
for country in suppliers:
    if country.Country not in countries:
        countries.append(country.Country)

# Method to return list of producsts available in a country
def productsByCountry(x):
    print("The products available from suppliers within " + x + " are:")
    for supplier in suppliers:
        # Matching country to user_input country
        if supplier.Country == x:
            for product in products:
                # Checks for matching supplierID as well as if the product is not discontinued
                if product.SupplierID == supplier.SupplierID and not product.Discontinued:
                    print(product.ProductName)

# Method to return list of products that are less than or equal to specified price
def productsByMaxLimit(n):
    print("The products available that are less than or equal to " +
          str(n) + " per unit price:")
    for product in products:
        if product.UnitPrice <= n:
            print(product.ProductName + " , per unit Price: " +
                  str(product.UnitPrice))

# Method to return list of discontinued products
def discontinued():
    print("The products that have been discontinued are:\n")
    for product in products:
        if product.Discontinued:
            print(product.ProductName)

# Method to return list of average order prices per country, sorted alphabetically
def avgOrderPrice():
    print("Average order prices per country: ")
    d = defaultdict(list)
    for a in orders:
        if a.ShipCountry == "":
            continue
        else:
            # Map each country in dict and add OrderPrices into list of values
            d[a.ShipCountry].append(a.OrderPrice)
    for k, v in d.items():
        # v is the list of orderPrices for country k
        # round average to 2 decimals
        d[k] = round((sum(v) / len(v)), 2)
    # sort results alphabetically
    for a in sorted(d.items()):
        print(a)


# Enter state machine until 'exit' is typed at any moment which will stop the program
while True:
    # First state, prompts customer to explore one of many options of viewing data from spreadsheet
    if state == "pickState":
        print("Hello, please type the letter(case sensitive) corresponding to the type of search you would like to perform: (type 'exit' at any point to stop program)")
        print("A: To search a country and return all products offered by suppliers in that country")
        print("B: To search for products, per unit, that cost less than or equal to specified price")
        print("C: To view all products that have been discontinued")
        print("D: To view the average order price per country")
        picker = input()
        if picker == "exit":
            quit()
        elif picker not in states:
            print("Invalid input")
            state == "pickState"
        else:
            state = picker

    # State A, lets user look up products offered by a specified country
    if state == "A":
        # List out the available countries to search
        for x in countries:
            print(x)
        user_input = input(
            "Hello, please enter one of the countries specified to see a list of all the products offered by suppliers in that country:\n")
        # Validating user input
        if user_input == "exit":
            quit()
        elif user_input in countries:
            productsByCountry(user_input)
            state = "pickState"
        else:
            while True:
                print(
                    "Country entered is invalid or does not have any available products.")
                user_input = input(
                    "Please enter a valid country specified above:\n")
                if user_input in countries:
                    productsByCountry(user_input)
                    break
        state = "pickState"
    # State B, lists items that are equal to or less than specified value
    if state == "B":
        while True:
            print("Please enter a unit max price value rounded to 2 decimals:")
            user_input = input()
            if user_input == "exit":
                quit()
            try:
                if "." in user_input:
                    maxPrice = float(user_input)
                else:
                    maxPrice = int(user_input)
                # Checking if value does not exceed 2 decimal values
                if type(maxPrice) is float:
                    if len(user_input.rsplit('.')[-1]) > 2:
                        print("Value has too many decimals")
                        state == "B"
                    else:
                        productsByMaxLimit(maxPrice)
                        break
                else:
                    productsByMaxLimit(maxPrice)
                    break
            # Catches the error if input is not an integer/float
            except ValueError:
                if user_input == "exit":
                    quit()
                print("Invalid response")
        state = "pickState"

    # State C, lists items that have been Discontinued
    if state == "C":
        discontinued()
        state = "pickState"

    # State D, lists average order price per country, sorted alphabetically
    if state == "D":
        avgOrderPrice()
        state = "pickState"
