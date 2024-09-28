import pandas as pd
from brothers import LightWeightChart

# Example DataFrame
# data = {
#     'Datetime': pd.date_range(start='2023-01-01', periods=5, freq='D'),
#     'Symbol': ['AAPL'] * 5,
#     'Open': [150, 152, 154, 156, 158],
#     'High': [151, 153, 155, 157, 159],
#     'Low': [149, 151, 153, 155, 157],
#     'Close': [150, 152, 154, 156, 158],
#     'Volume': [1000, 1100, 1200, 1300, 1400],
# }
#
# df = pd.DataFrame(data)

def fake_data():
    data = [
            ["Symbol","Close","High","Low","Open","Volume","Datetime","Adj Close"],
            ["ORRF",21, 21, 21, 21, 0   ,"2023-03-13",21.709999084472],
            ["ORRF",21, 21, 21, 21, 333 ,"2023-03-14",21.709999084472],
            ["ORRF",22, 22, 22, 22, 197 ,"2023-03-15",22.092500686645],
            ["ORRF",22, 22, 22, 22, 284 ,"2023-03-16",22.112499237060],
            ["ORRF",22, 22, 22, 22, 426     ,"2023-03-17",22.0],
            ["ORRF",21, 21, 21, 21, 723 ,"2023-03-20",21.780000686645],
            ["ORRF",21, 21, 21, 21, 910 ,"2023-03-21",21.709999084472],
            ["ORRF",21, 21, 21, 21, 370 ,"2023-03-22",21.659999847412],
            ["ORRF",21, 21, 21, 21, 416 ,"2023-03-23",21.370000839233],
            ["ORRF",21, 21, 21, 21, 394 ,"2023-03-24",21.409999847412],
            ["ORRF",21, 21, 21, 21, 156 ,"2023-03-21",21.240900039672],
            ["ORRF",21, 21, 21, 21, 841     ,"2023-03-22",21.200000762939],
            ["ORRF",21, 21, 20, 20, 909 ,"2023-03-23",21.180000305175],
            ["ORRF",20, 20, 20, 20, 645     ,"2023-03-24",20.799999237060],
            ["ORRF",20, 20, 20, 20, 365   ,"2023-03-27",20.780000686645],
            ["ORRF",20, 20, 20, 20, 532    ,"2023-03-28",20.799999237060],
            ["ORRF",20, 20, 20, 20, 335  ,"2023-03-29",20.799999237060],
            ["ORRF",20, 20, 20, 20, 420 ,"2023-03-30",20.809999465942],
            ["ORRF",20, 20, 20, 20, 848 ,"2023-03-31",20.809999465942]
        ]

    df = pd.DataFrame(data[1:], columns=data[0])
    df['Datetime'] = pd.to_datetime(df['Datetime'])
    df.drop(columns='Adj Close', inplace=True)
    #df.set_index('Datetime', inplace=True)    
    return df  





# Create and run the chart
df = fake_data()
df = df[['Datetime', 'Symbol', 'Open', 'High', 'Low', 'Close', 'Volume']]   
df.reset_index()
chart = LightWeightChart(df)
chart.run()
