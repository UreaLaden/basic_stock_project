# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 2022

@author: Leaundrae Mckinney
"""

from daily_data import DailyData
from datetime import datetime
from tabulate import tabulate
import account_class as accounts

class Stock:

    def __init__(self,symbol:str='',company_name:str='',num_shares:float=0,daily_data:list[DailyData]=[]):
        self.symbol = symbol
        self.company_name = company_name
        self.num_shares = num_shares
        self.daily_data = daily_data

class StockData:

    def __init__(self,stock_list:list[Stock]=[]):
        self.stock_list = stock_list

    def add_stock(self):
        print("--- Add Stock ---")
        while True:
            symbol = input("Enter Ticker Symbol: ")
            companyName = input("Enter Company Name: ")
            numShares = float(input("Enter Number of Shares: "))
            newStock = Stock(symbol,companyName,numShares)
            self.stock_list.append(newStock)
            option = input(f'Received {numShares} shares of {companyName.capitalize()} stock -- Press Enter to Add Another Stock or 0 to Stop: ')
            if option == '0':
                return
    # Remove stock and all daily data
    def delete_stock(self):
        print("\n------ Delete Stock ------")
        currentStocks = [i.symbol for i in self.stock_list]
        print(f'Stock List: {currentStocks}')
        symbol = input("Which stock to you want to delete? ")
        deletedStock = 0
        for i in self.stock_list:
            if i.symbol == symbol:
                self.stock_list.remove(i)
                print(f'Deleted {i.num_shares} shares of {i.company_name} stock\n')
                deletedStock += 1
        if deletedStock < 1:
            _ = input(f'Symbol: {symbol} could not be found. Please try again')
    # List stocks being tracked
    def list_stocks(self):
        print("\n------ Recorded Stocks ------")
        stocks = self.stock_list
        nestedStocks = [['SYMBOL','NAME','SHARES']] + [[i.symbol.upper(),i.company_name.capitalize(),i.num_shares] for i in stocks]
        print('\n',tabulate(nestedStocks,headers='firstrow'),end='\n\n')

        self.delay()
    # Add Daily Stock Data
    def add_stock_data(self):
        print("\n------ Add Daily Stock Data ------\n")
        currentStocks = [i.symbol.upper() for i in self.stock_list]
        print(f'Stock List: {currentStocks}')
        symbol = input("Which stock to you want to use? ")
        try:
            stock = [i for i in self.stock_list if i.symbol.upper() == symbol.upper()][0]
        except IndexError:
            print("Symbol Not Found ***")
            self.delay()
            return

        print(f'Targeting: {stock.symbol}')
        print("""
                    Enter Data Seperated by Commas - Do Not use Spaces
                    Enter a Blank Line to Quit  
                    Enter Date,Price,Volume
            """)
        while True:
            command = input('''Example: 8/28/22,47.85,10550:  ''')
            if command != '' and stock != None:
                input_data = command.split(',')
                stock.daily_data.append(
                    DailyData(
                        datetime.strptime(input_data[0],"%m/%d/%y"),
                        float(input_data[1]),
                        float(input_data[2])
                    ))
            else:
                if stock != None:
                    print("Date Entry Complete")   
                else:
                    self.delay()
                return
    # Pause for user confirmation to continue
    def delay(self):
        _ = input('Press Enter to Continue ***')
    # Instantiate Traditional or Robo account depending on user inputq
    def investment_type(self):
        print("Investment Account ---")
        balance = float(input("What is your initial balance: "))
        number = input("What is your account number: ")
        acct= input("Do you want a Traditional (t) or Robo (r) account: ")
        if acct.lower() == "r":
            years = float(input("How many years until retirement: "))
            robo_acct = accounts.Robo(balance, number, years)
            print("Your investment return is ",robo_acct.investment_return())
            print("\n\n")
        elif acct.lower() == "t":
            trad_acct = accounts.Traditional(balance, number)
            temp_list=[]
            print("Choose stocks from the list below: ")
            while True:
                currentStocks = [i.symbol.upper() for i in self.stock_list]
                print(f'Stock List: {currentStocks}')
                symbol = input("Which stock do you want to purchase, 0 to quit: ").upper()
                if symbol =="0":
                    break
                shares = float(input("How many shares do you want to buy?: "))
                found = False
                for stock in self.stock_list:
                    if stock.symbol.upper() == symbol:
                        found = True
                        current_stock = stock
                if found == True:
                    current_stock.num_shares += shares 
                    temp_list.append(current_stock)
                    print("Bought ",shares,"of",symbol)
                else:
                    print("Symbol Not Found ***")
            trad_acct.add_stock(temp_list)
    # Get price and volume history from Yahoo! Finance using CSV import.
    def import_stock_csv(self):
        print("This method is under construction")

