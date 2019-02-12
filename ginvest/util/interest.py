import math

def year_to_day(yearlyrate):
    return math.pow(1.0 + float(yearlyrate) / 100.0, 1.0/365.0) - 1.0

def year_to_month(yearlyrate):
    return math.pow(1.0 + float(yearlyrate) / 100.0, 1.0/12.0) - 1.0

def day_to_month(dailyrate):
    return math.pow(1.0 + float(dailyrate) / 100.0, 30) - 1.0

def day_to_year(monthlyrate):
    return math.pow(1.0 + float(monthlyrate) / 100.0, 365) - 1.0

def month_to_year(monthlyrate):
    return math.pow(1.0 + float(monthlyrate) / 100.0, 12) - 1.0
