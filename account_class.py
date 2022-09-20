# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 2022

@author: Leaundrae Mckinney
"""

class Retirement_Account:
    def __init__(self,balance:float=0,acctNumber:str=''):
        self.balance = balance
        self.acctNumber = acctNumber

class Traditional(Retirement_Account):
    def __init__(self,stock_list,balance:int=0,acctNumber:str=0):
        Retirement_Account.__init__(self,balance,acctNumber)
        self.stock_list = stock_list
    
    def add_stock(self,stock_data):
        pass

class Robo(Retirement_Account):
    def __init__(self,balance:float=0.0,acctNumber:str=0,years:float=0.0):
        Retirement_Account.__init__(self,balance,acctNumber)
        self.years = years
    
    def investment_return(self):
        return (self.years * self.balance * 1.05)



