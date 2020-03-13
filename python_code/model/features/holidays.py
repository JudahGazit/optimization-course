import pandas as pd

from python_code.config import PATH


def add_holidays(df):
    df = df.copy()
    usa_holidays = pd.read_csv(PATH + 'usholidays.csv')
    usa_holidays.columns = [c.upper() for c in usa_holidays.columns]
    usa_holidays = usa_holidays[['DATE', 'HOLIDAY']]
    df = df.merge(usa_holidays, on=['DATE'], how='left')
    df.HOLIDAY = df.HOLIDAY.apply(lambda v: 1 if isinstance(v, str) else 0)
    return df
