import pandas
import yfinance as yf
import os

df = pandas.read_csv("../../resources/tickerList/NASDAQ-100-Stock-Tickers-List.csv")

for index, row in df.iterrows():
    company = yf.Ticker(row['Ticker'])
    print(row)
    outputDirectory = "../../resources/tickerList/" + row['Ticker']
    if not os.path.exists(outputDirectory):
        os.mkdir(outputDirectory)
    company.history(period="max").to_csv(outputDirectory + "/history.csv");
    company.actions.to_csv(outputDirectory + "/actions.csv");
    company.dividends.to_csv(outputDirectory + "/dividends.csv");
    company.splits.to_csv(outputDirectory + "/splits.csv");
    company.major_holders.to_csv(outputDirectory + "/major_holders.csv");
    company.institutional_holders.to_csv(outputDirectory + "/institutional_holders.csv");
    company.financials.to_csv(outputDirectory + "/financials.csv");
    company.quarterly_financials.to_csv(outputDirectory + "/quarterly_financials.csv");
    company.balance_sheet.to_csv(outputDirectory + "/balance_sheet.csv");
    company.quarterly_balance_sheet.to_csv(outputDirectory + "/quarterly_balance_sheet.csv");
    company.cashflow.to_csv(outputDirectory + "/cashflow.csv");
    company.quarterly_cashflow.to_csv(outputDirectory + "/quarterly_cashflow.csv");
    company.earnings.to_csv(outputDirectory + "/earnings.csv");
    company.quarterly_earnings.to_csv(outputDirectory + "/quarterly_earnings.csv");
    sustainability = company.sustainability
    if sustainability is not None:
        sustainability.to_csv(outputDirectory + "/sustainability.csv");
    recommendations = company.recommendations
    if recommendations is not None:
        recommendations.to_csv(outputDirectory + "/recommendations.csv");
