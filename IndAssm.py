import yfinance as yf
import pandas as pd

stocks = [
    "1155.KL",
    "1295.KL",
    "1023.KL",
    "5347.KL",
    "5225.KL"
]


stock_names = {
    "1155.KL": "Maybank",
    "1295.KL": "Public Bank",
    "1023.KL": "CIMB Group",
    "5347.KL": "Tenaga Nasional",
    "5225.KL": "IHH Healthcare"
}


def analyze_stock(stock):

    data = yf.Ticker(stock).history(period="1mo")

    # clean data (IMPORTANT)
    data = data.dropna(subset=["Close"])

    if len(data) < 2:
        return [stock, None, None, None, None, None, None]

    yesterday_close = data["Close"].iloc[-2]
    today_close = data["Close"].iloc[-1]

    daily_return = today_close - yesterday_close

    shares = 1000 / yesterday_close
    total_return = daily_return * shares
    return_pct = (total_return / 1000) * 100

    return [
        stock,
        round(yesterday_close, 2),
        round(today_close, 2),
        round(daily_return, 2),
        int(shares),
        round(total_return, 2),
        round(return_pct, 2)
    ]


results = [analyze_stock(stock) for stock in stocks]

df = pd.DataFrame(results, columns=[
    "Ticker",
    "Yesterday Close",
    "Today Close",
    "Daily Return",
    "Shares Purchasable",
    "Estimated Total Return",
    "Return Percentage"
])


df["Company"] = df["Ticker"].map(stock_names)


df = df[
    [
        "Company",
        "Ticker",
        "Yesterday Close",
        "Today Close",
        "Daily Return",
        "Shares Purchasable",
        "Estimated Total Return",
        "Return Percentage"
    ]
]


print("\nQUESTION 1: RESULT")
print(df.to_string(index=False))



df = df.rename(columns={
    "Yesterday Close": "Previous Closing Price",
    "Today Close": "Latest Closing Price"
})




portfolio_summary = df[
    [
        "Ticker",
        "Previous Closing Price",
        "Latest Closing Price",
        "Estimated Total Return",
        "Return Percentage"
    ]
]

print("QUESTION 2(a): PORTFOLIO SUMMARY")
print(portfolio_summary)




def classify_performance(x):
    if x < 0:
        return "Negative Return"
    elif x <= 2:
        return "Moderate Return"
    else:
        return "High Return"


df["Performance Category"] = df["Return Percentage"].apply(classify_performance)

grouped_result = df.groupby("Performance Category", as_index=False)["Estimated Total Return"].mean()

grouped_result = grouped_result.rename(columns={
    "Estimated Total Return": "Average Estimated Total Return"
})

print("\nQUESTION 2(b): GROUPED RESULT")
print(grouped_result)



import matplotlib.pyplot as plt

plt.figure(figsize=(12,6))

for stock in stocks:
    data = yf.Ticker(stock).history(period="1mo")
    plt.plot(data.index, data["Close"], label=stock)

plt.title("Closing Price Trend")
plt.xlabel("Date")
plt.ylabel("Closing Price (RM)")
plt.legend()
plt.grid(True)

plt.show()



plt.figure(figsize=(8,5))

plt.bar(df["Ticker"], df["Return Percentage"])

plt.title("Portfolio Performance Comparison")
plt.xlabel("Stock")
plt.ylabel("Return Percentage (%)")

plt.grid(True)
plt.show()