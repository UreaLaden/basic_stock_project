from datetime import datetime
import matplotlib.pyplot as plt

class DailyData():    
    """"Parameters: date,closing_price,volume"""
    def __init__(self,date:datetime,closing_price:float,volume:int):
        self.date = date
        self.closing_price = closing_price
        self.volume = volume
        
    # Display Report 
    def display_report(self):
        print("This method is under construction")

    


