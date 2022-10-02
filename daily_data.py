from datetime import datetime, date
import matplotlib.pyplot as plt

class DailyData():    
    """"Parameters: date,closing_price,volume"""
    def __init__(self,date:datetime,closing_price:float,volume:int):
        self.date = date
        self.closing_price = closing_price
        self.volume = volume
    
    def __str__(self):
        return (f'DailyData({self.date},{self.closing_price},{self.volume})')
    
    def __lt__(self,other):
        myStrDate = str(self.date)
        oStrDate = str(other.date)
        
        mySplitDate = myStrDate.split('-')
        oSplitDate = oStrDate.split('-')
        
        mYear = int(mySplitDate[0])
        mMonth = int(mySplitDate[1])
        mDay = int(mySplitDate[2])
        mDate = date(mYear,mMonth,mDay)
        
        oYear = int(oSplitDate[0])
        oMonth = int(oSplitDate[1])
        oDay = oSplitDate[2] if len(oSplitDate) < 4 else int(oSplitDate[2].split(' ')[0])
        oDate = date(oYear,oMonth,int(oDay))

        return self if mDate < oDate else other
    
    def __gt__(self,other):
        myStrDate = str(self.date)
        oStrDate = str(other.date)
        
        mySplitDate = myStrDate.split('-')
        oSplitDate = oStrDate.split('-')
        
        mYear = int(mySplitDate[0])
        mMonth = int(mySplitDate[1])
        mDay = int(mySplitDate[2])
        mDate = date(mYear,mMonth,mDay)
        
        oYear = int(oSplitDate[0])
        oMonth = int(oSplitDate[1])
        oDay = oSplitDate[2] if len(oSplitDate) < 4 else int(oSplitDate[2].split(' ')[0])
        oDate = date(oYear,oMonth,int(oDay))

        return self if mDate > oDate else other
        


    


