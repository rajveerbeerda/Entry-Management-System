import pandas as pd
from datetime import datetime

def checkOut(name, phone):
    df = pd.read_csv('visitor.csv')
    ind = -1
    for i in range(len(df)):
        lst = list(df.iloc[i])
        if lst[0]==name and str(lst[2])==phone and int(lst[5])==1:
            ind = i
            break

    new_column = pd.Series([0], name='status', index=[ind])
    df.update(new_column)
    curTime = datetime.now()
    checkoutTime = str(curTime.strftime("%I:%M %p"))
    new_column = pd.Series([checkoutTime], name='checkout', index=[ind])
    df.update(new_column)
    df.to_csv('visitor.csv',mode='w', index=False, header=list(df.columns))

    lst = list(df.iloc[ind])
    return lst