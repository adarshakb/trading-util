from pathlib import Path

import yfinance as yf

from src.dataUtils.PriceDataUtil import PriceData


def download_all_ticker_data():
    df = PriceData.get_all_tickers()
    resources_root = Path(__file__).resolve().parents[2] / "resources" / "tickerList"

    for _, row in df.iterrows():
        ticker = row["Ticker"]
        company = yf.Ticker(ticker)
        print(f"Downloading data for {ticker}")

        output_directory = resources_root / ticker
        output_directory.mkdir(parents=True, exist_ok=True)

        company.history(period="max").to_csv(output_directory / "history.csv")
        company.actions.to_csv(output_directory / "actions.csv")
        company.dividends.to_csv(output_directory / "dividends.csv")
        company.splits.to_csv(output_directory / "splits.csv")
        company.major_holders.to_csv(output_directory / "major_holders.csv")
        company.institutional_holders.to_csv(output_directory / "institutional_holders.csv")
        company.financials.to_csv(output_directory / "financials.csv")
        company.quarterly_financials.to_csv(output_directory / "quarterly_financials.csv")
        company.balance_sheet.to_csv(output_directory / "balance_sheet.csv")
        company.quarterly_balance_sheet.to_csv(output_directory / "quarterly_balance_sheet.csv")
        company.cashflow.to_csv(output_directory / "cashflow.csv")
        company.quarterly_cashflow.to_csv(output_directory / "quarterly_cashflow.csv")
        company.earnings.to_csv(output_directory / "earnings.csv")
        company.quarterly_earnings.to_csv(output_directory / "quarterly_earnings.csv")

        sustainability = company.sustainability
        if sustainability is not None:
            sustainability.to_csv(output_directory / "sustainability.csv")

        recommendations = company.recommendations
        if recommendations is not None:
            recommendations.to_csv(output_directory / "recommendations.csv")


if __name__ == "__main__":
    download_all_ticker_data()
