# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 2022

@author: Leaundrae Mckinney
"""

from email import header
import math
from daily_data import DailyData
from datetime import datetime
from tabulate import tabulate
import account_class as accounts
from matplotlib import pyplot as plt
import csv,glob,sys
from os import system,name

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
            symbol = input("Enter Ticker Symbol: ").upper()
            companyName = input("Enter Company Name: ").capitalize()
            numShares = float(input("Enter Number of Shares: "))
            newStock = Stock(symbol,companyName,numShares)
            self.stock_list.append(newStock)
            option = input(f'Received {numShares} shares of {companyName} stock -- Press Enter to Add Another Stock or 0 to Stop: ')
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
        _ = input('\t\t--- Press Enter to Continue ---')
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
        print("----------Import historical Stock data from file---------")
        stock_files = glob.glob('./*.csv')
        availableImports = [i.split('.')[1].strip('\\') for i in stock_files]
        symbol = input("Enter data for import: " + str(availableImports) + ": ").upper()
        if symbol not in availableImports:
            print('\nInvalid entry please try again\n')
            return
        dataCount = 0
        foundSymbol = False
        with open(symbol + '.csv','r') as data:
            symbol = data.name.split('.')[0]
            reader = csv.reader(data,delimiter=',')
            for idx,row in enumerate(reader):
                if(idx > 0):
                    date = row[0]
                    close = row[4]
                    volume = row[-1]
                    if len(self.stock_list) <= 0:
                        # If we don't have the selected Stock at to our list
                        self.stock_list.append(Stock(symbol,symbol))
                    for stock in self.stock_list:
                        if stock.symbol == symbol:
                            foundSymbol = True
                            stock.daily_data.append(DailyData(date,close,volume))
                    dataCount = idx
            if foundSymbol:
                print(f'Imported {dataCount} rows of data')
        self.display_report()

                    
    # Function to create stock chart
    def display_stock_chart(self,symbol):
        dates:list[datetime] = []
        prices:list[float] = []
        volumes:list[int] = [] 
        company = ""
        for stock in self.stock_list:
            if(stock.symbol == symbol):
                company = stock.company_name
                for data in stock.daily_data:
                    new_date = datetime.strptime(data.date,'%Y-%m-%d')
                    dates.append(new_date)
                    prices.append(float(data.closing_price))
                    volumes.append(data.volume)
        plt.plot(dates,prices,'g--',linewidth=1)
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.title(company)
        plt.show()
    # Display Chart
    def display_chart(self):
        print("\n----------Display Chart-----------")
        currentStocks = [i.symbol for i in self.stock_list]
        print(f'Stock List: {currentStocks}')
        symbol = input('Which stock to you want to display? ').upper()
        filteredList = list(filter(lambda x:x.symbol == symbol,self.stock_list))
        found = True if len(filteredList) > 0 else False
        if found == True:
            self.display_stock_chart(symbol)
        else:
            print(f'Symbol: {symbol} not found')
            self.delay()
    # Display Report 
    def display_report(self):
        self.clear_screen()
        for stock in self.stock_list:
            
            count = 0
            price_total = 0.0
            volume_total = 0
            lowPrice = sys.maxsize
            highPrice = 0.0
            lowVolume = sys.maxsize
            highVolume = 0.0
            max_date = str(datetime.max).split(' ')[0]
            min_date = str(datetime.min).split(' ')[0]
            earliest_data = DailyData(max_date,0,0)
            latest_data = DailyData(min_date,0,0)
            price_change = 0.0
            profit_loss = 0.0
            # start_price = stock.start_price
            for data in stock.daily_data:
                count += 1
                price_total += float(data.closing_price)
                volume_total += int(data.volume)
                
                lowPrice = min(lowPrice,float(data.closing_price))
                highPrice = max(highPrice,float(data.closing_price))
                lowVolume = min(lowVolume,int(data.volume))
                highVolume = max(highVolume,int(data.volume))
                
                earliest_data = data < earliest_data #Re-wrote __lt__ to return earliest data
                latest_data = data > latest_data #Re-wrote __gt__ to return earliest data
                price_change = float(latest_data.closing_price) - float(earliest_data.closing_price)
                profit_loss = price_change * stock.num_shares
            
            if count > 0:
                header_string = '\n\n\nReport for: {ticker}  Total Shares: {share_amt}'.format(ticker=stock.symbol,share_amt=stock.num_shares)
                data_headers = [['   Date','Closing Price','Volume']] + [[i.date,'${:.2f}'.format(float(i.closing_price)),i.volume] for i in stock.daily_data]
                low_price = '${:.2f}'.format(lowPrice)
                high_price = '${:.2f}'.format(highPrice)
                avg_price = '${:.2f}'.format(price_total / count)
                
                price_headers = [['Low Price','High Price','Average Price']]  
                price_stats = [[low_price,high_price,avg_price]]
                volume_headers = [['Low Volume','High Volume','Average Volume']]
                avg_vol = math.ceil(volume_total / count)
                volume_stats = [[lowVolume,highVolume,avg_vol]]
                
                earning_headers = [['Start','End','$ Change','Profit/Loss']]
                start_price = '${:.2f}'.format(float(earliest_data.closing_price))
                end_price = '${:.2f}'.format(float(latest_data.closing_price))
                earning_stats = [[start_price,end_price,price_change,'{:.2f}'.format(profit_loss)]]
                
                print(header_string,'\n')
                print(tabulate(data_headers,headers='firstrow',numalign='center'))
                print('\n-------------------Summary-------------------\n')
                print(tabulate(price_headers + price_stats,headers='firstrow',numalign='center'))
                print('\n',tabulate(volume_headers + volume_stats,headers='firstrow',numalign='center'))
                print('\n',tabulate(earning_headers+earning_stats,headers='firstrow',numalign='center'))     
            else:
                print('No daily history')

            print('\n\n\n\t\t--- Report Complete ---')       
            self.delay()

    def clear_screen(self):
        if name == 'nt':
            _ = system('cls')
        else:
            _ = system('clear')