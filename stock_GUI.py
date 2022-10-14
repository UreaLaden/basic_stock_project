# Summary: This module contains the user interface and logic for a graphical user interface version of the stock manager program.add()
# Author: Leaundrae Mckinney
# Date: 13 October 2022

from datetime import datetime
from stock_class import Stock,DailyData
from os import path
from tkinter import *
from tkinter import ttk
from tkinter import messagebox,simpledialog,filedialog
import csv
import matplotlib.pyplot as plt
import json

class StockApp:
    def __init__(self):
        self.stock_list:list[Stock] = []

        # Create Window
        self.root = Tk()
        self.root.title('Stock Manager')

        # Add Menu 
        self.menubar = Menu(self.root)

        self.filemenu = Menu(self.menubar,tearoff = 0)

        self.webmenu = Menu(self.menubar,tearoff=0)
        self.webmenu.add_command(label = "Import CSV from Yahoo! Finance...",command=self.importCSV_web_data)
        self.menubar.add_cascade(label="Web",menu=self.webmenu)
        
        self.chartmenu = Menu(self.menubar,tearoff=0)
        self.chartmenu.add_command(label="Display Stock Chart",command = self.display_chart)
        self.menubar.add_cascade(label="Chart",menu=self.chartmenu)
        
        self.root.config(menu=self.menubar)

        # Add heading information
        self.headingLabel = Label(self.root,text="No Stock Selected")
        self.headingLabel.grid(column=0,row=0,columnspan=3,padx=5,pady=10)

        # Add stock list
        self.stockLabel = Label(self.root,text="Stocks")
        self.stockLabel.grid(column=0,row=1,padx=5,pady=10,stick=(N))

        self.stockList = Listbox(self.root)
        self.stockList.grid(column=0,row=2,padx=5,pady=5,sticky=(N,S))
        self.stockList.bind('<<ListboxSelect>>',self.update_data)

        # Add tabs
        self.notebook = ttk.Notebook(self.root,padding="5 5 5 5")

        self.notebook.grid(column=2,row=2,sticky=(N,W,E,S))
        self.mainFrame = ttk.Frame(self.notebook)
        self.stockDataFrame = ttk.Frame(self.notebook)
        self.reportFrame = ttk.Frame(self.notebook)
        self.notebook.add(self.mainFrame,text='Manage')
        self.notebook.add(self.stockDataFrame,text='History')
        self.notebook.add(self.reportFrame,text='Report')

        # Set Up Main Tab
        self.addStockGroup = LabelFrame(self.mainFrame,text="Add Stock",padx=5,pady=5)
        self.addStockGroup.grid(column=0,row=0,padx=5,pady=5,sticky=(W,E))

        self.addSymbolLabel = Label(self.addStockGroup,text="Symbol")
        self.addSymbolLabel.grid(column=0,row=0,padx=5,pady=5,sticky=(W))
        self.addSymbolEntry = Entry(self.addStockGroup)
        self.addSymbolEntry.grid(column=1,row=0,padx=5,pady=5)

        self.addNameLabel = Label(self.addStockGroup,text="Name")
        self.addNameLabel.grid(column=0,row=1,padx=5,pady=5,sticky=(W))
        self.addNameEntry = Entry(self.addStockGroup)
        self.addNameEntry.grid(column=1,row=1,padx=5,pady=5)

        self.addSharesLabel = Label(self.addStockGroup,text="Shares")
        self.addSharesLabel.grid(column=0,row=2,padx=5,pady=5,sticky=(W))
        self.addSharesEntry = Entry(self.addStockGroup)
        self.addSharesEntry.grid(column=1,row=2,padx=5,pady=5)

        self.addStockButton = Button(self.addStockGroup,text="New Stock",command = self.add_stock)
        self.addStockButton.grid(column=0,row=3,columnspan=2,padx=5,pady=5)
        
        self.deleteGroup = LabelFrame(self.mainFrame,text="Delete Stock")
        self.deleteGroup.grid(column=0,row=2,padx=5,pady=5)

        self.deleteStockButton = Button(self.deleteGroup,text="Delete Selected Stock",command=self.delete_stock)
        self.deleteStockButton.grid(column=0,row=0,padx=5,pady=5)

        # Setup History Tab
        self.dailyDataList = Text(self.stockDataFrame,width=40)
        self.dailyDataList.grid(column=0,row=0,padx=5,pady=5)

        # Setup Report Tab
        self.stockReport = Text(self.reportFrame,width=40)
        self.stockReport.grid(column=0,row=0,padx=5,pady=5)

        self.root.mainloop()
    
    def update_data(self,evt):
        """Refresh history and report tabs"""
        self.display_stock_data()

    def display_stock_data(self):
        """Display stock price and volume history"""
        if(self.stockList.curselection()):
            symbol:str = self.stockList.get(self.stockList.curselection())

            for stock in self.stock_list:
                self.headingLabel['text'] = stock.company_name + " - " + str(stock.num_shares) + " Shares"
                self.dailyDataList.delete("1.0",END)
                self.stockReport.delete("1.0",END)
                self.dailyDataList.insert(END,"-Date-  -Price- -Volume-\n")
            
            self.dailyDataList.insert(END,"========================================\n")
            for daily_data in stock.daily_data:
                close = daily_data.closing_price
                row = daily_data.date + "  " + '${:.2}'.format(close) + "  " + str(daily_data.volume) + "\n"
                self.dailyDataList.insert(END,row)
            
            #display report
            count = 0
            price_total = 0.00
            volume_total = 0.00
            lowPrice = 999999.999
            highPrice = 0.00
            lowVolume = 999999999999
            highVolume = 0

            for daily_data in stock.daily_data:
                count = count + 1
                price_total = price_total + float(daily_data.closing_price)
                volume_total = volume_total + float(daily_data.volume)
                lowPrice = min(float(daily_data.closing_price),lowPrice)
                lowVolume = min(float(daily_data.volume),lowVolume)
                highVolume = max(float(daily_data.volume),highVolume)
                highPrice = max(float(daily_data.closing_price),highPrice)
                priceChange = lowPrice - highPrice

            if count > 0:
                self.stockReport.insert(END,"Summary Data--\n\n")
                self.stockReport.insert(END,"Low Price: " + "${:,.2f}".format(lowPrice) + "\n")
                self.stockReport.insert(END,"High Price: " + "${:,.2f}".format(highPrice) + "\n")
                self.stockReport.insert(END,"Average Price: " + "${:,.2f}".format(price_total/count) + "\n")
                self.stockReport.insert(END,"Low Volume: " + str(lowVolume) + "\n")
                self.stockReport.insert(END,"High Volume: " + str(highVolume) + "\n")
                self.stockReport.insert(END,"Average Volume: " + str(volume_total/count) + "\n\n")
                self.stockReport.insert(END,"Change in Price: " + "${:,.2f}".format(priceChange) + "\n")
                self.stockReport.insert(END,"Profit/Loss: " + "${:,.2f}".format(priceChange * stock.num_shares) + "\n")
            else:
                self.stockReport.insert(END,"*** No daily history.")

    def add_stock(self):
        """Add new stock to track"""
        for stock in self.stock_list:
            if stock.symbol == self.addSymbolEntry.get():
                messagebox.showinfo("Invalid Operation",f"{stock.symbol} is already in the collection")
                return
        new_stock = Stock(self.addSymbolEntry.get(),self.addNameEntry.get(),float(self.addSharesEntry.get()))
        self.stock_list.append(new_stock)
        self.stockList.insert(END,self.addSymbolEntry.get())
        self.addSymbolEntry.delete(0,END)
        self.addNameEntry.delete(0,END)
        self.addSharesEntry.delete(0,END)

    def delete_stock(self):
        """Remove stock and all history from being tracked"""
        symbol = self.stockList.curselection()
        idx = 0
        for stock in self.stock_list:
            if stock.symbol == symbol:
                self.stock_list.pop(idx)
            idx += 1
        self.display_stock_data()
        self.stockList.delete(0,END)
        for stock in self.stock_list:
            if stock.symbol == symbol:
                self.stockList.insert(END,stock.symbol)

        messagebox.showinfo("Stock Deleted", symbol + " Removed")

    # Get price and volume history from Yahoo! Finance using CSV import
    def import_stock_csv(self,stock_list:list[Stock],symbol:str,filename:str):
        for stock in stock_list:
            if stock.symbol == symbol:
                with open(filename,'r') as data:
                    symbol = data.name.split('.')[0]                    
                    reader = csv.reader(data,delimiter=',')
                    next(reader)
                    dataCount = 0
                    for idx,row in enumerate(reader):
                        date = row[0]
                        close = row[4]
                        volume = row[-1]
                        if len(self.stock_list) <= 0:
                            # If we don't have the selected Stock at to our list
                            self.stockList.insert(END,symbol)
                            self.stock_list.append(Stock(symbol,symbol))
                        for stock in self.stock_list:
                            if stock.symbol == symbol.split('/')[-1]:
                                dailyData = DailyData(date,close,volume)
                                print(dailyData)
                                stock.add_data(dailyData)
                            dataCount = idx
                    print(f'Imported {dataCount} rows of data')

    def importCSV_web_data(self):
        """Import CSV stock history file"""
        symbol = self.stockList.get(self.stockList.curselection())
        filename = filedialog.askopenfilename(title=f"Select " + symbol +" File to Import",filetypes=[('Yahoo Finance! CSV','*.csv')])
        if filename != '':
            self.import_stock_csv(self.stock_list,symbol,filename)
            self.display_stock_data()
            messagebox.showinfo("Import Complete",symbol + " Import Complete")

    def display_chart(self):
        """Display stock price chart"""
        messagebox.showinfo("This module is under construction")

def main():
    app = StockApp()

if __name__ == '__main__':
    main()