# trading-util

Experimental Python utilities for running indicator-based backtesting workflows on market data.

## Status
This is a hobby project and a work in progress.

## Features
- Download historical market/fundamental data per ticker via `yfinance`
- Generate signal-driven trades using:
  - Bollinger Bands
  - Keltner Channel
  - RSI combinations
- Produce aggregate trade analysis outputs

## Requirements
- Python 3.10+
- [TA-Lib](https://github.com/mrjbq7/ta-lib/) installed on your system

Install Python dependencies:

```bash
pip install -r requirements.txt
```

## Quickstart
1. Clone the repo.
2. Install dependencies.
3. Download ticker data:

```bash
python -m src.dataUtils.downloadData
```

4. Run analysis:

```bash
python -m src.analysis.analysis
```

## Project layout
- `src/dataUtils/downloadData.py` — downloads and stores market data
- `src/dataUtils/PriceDataUtil.py` — loads ticker/history data
- `src/dataUtils/TradesDataUtil.py` — persists generated trades/analysis
- `src/analysis/` — indicators, strategy logic, and analysis orchestration
- `resources/` — input ticker list and generated outputs

## Data source & compliance
This project fetches market/fundamental data using `yfinance` (which accesses Yahoo Finance data sources).

Important:
- Data provider terms can restrict use, redistribution, and commercial usage.
- You are responsible for verifying and complying with applicable Terms of Service/licensing for your usage.
- This repository is intended to share code, not bulk redistribute downloaded market datasets.

## Contributing
Contributions are welcome—see [CONTRIBUTING.md](CONTRIBUTING.md).

## Security
See [SECURITY.md](SECURITY.md) for reporting guidance.

## License
MIT — see [LICENSE](LICENSE).
