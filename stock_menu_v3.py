# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 2022

@author: Leaundrae Mckinney
"""
from stock_class import StockData

def main_menu():
    option = ""
    stock_data = StockData()
    while True:
        print("Stock Analyzer ---")
        print("1 - Add Stock")
        print("2 - Delete Stock")
        print("3 - List stocks")
        print("4 - Add Daily Stock Data (Date, Price, Volume)")
        print("5 - Show Chart")
        print("6 - Investor Type")
        print("7 - Load Data")
        print("0 - Exit Program")
        option = input("Enter Menu Option: ")
        if option =="0":
            print("Goodbye")
            break
        
        if option == "1":
            stock_data.add_stock()
        elif option == "2":
            stock_data.delete_stock()
        elif option == "3":
            stock_data.list_stocks()
        elif option == "4":
           stock_data.add_stock_data() 
        elif option == "5":
            stock_data.display_chart()
        elif option == "6":
            stock_data.investment_type()
        elif option == "7":
            stock_data.import_stock_csv()
        else:
            
            print("Goodbye")

# Begin program
def main():
    main_menu()


# Program Starts Here
if __name__ == "__main__":
    # execute only if run as a stand-alone script
    main()