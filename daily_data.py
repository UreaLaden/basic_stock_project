from datetime import datetime

class DailyData():    
    
    def __init__(self,date:datetime,closing_price:float,volume:int):
        self.date = date
        self.closing_price = closing_price
        self.volume = volume
        
    # Display Report 
    def display_report(self):
        print("This method is under construction")
    
    # Function to create stock chart
    def display_stock_chart(self,symbol):
        print("This method is under construction")

    # Display Chart
    def display_chart(self):
        print("This method is under construction")


