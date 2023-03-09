import yfinance as yf
import pandas as pd
import pandas_market_calendars as mcal

pd.set_option("display.precision", 12)


def get_returns(ticker: str, start_date: pd.Timestamp = pd.Timestamp("2015-01-02")):
    """Given a symbol and yfinance period, returns a series of daily returns (1 + %age) of the symbol over the course
    of the period"""
    returns = (
        yf.Ticker(ticker).history(period="max")["Close"][start_date:].pct_change() + 1
    )
    returns.index = returns.index.date
    index_range = mcal.date_range(
        mcal.get_calendar("NYSE").schedule(
            start_date=start_date, end_date=pd.Timestamp.today().floor("1D")
        ),
        frequency="1D",
    )
    returns = returns.reindex(index_range.date).fillna(1) # fill_value argument has issues with different NaNs lol
    return returns


def weights(
    ticker_weights: list[str], start_date: pd.Timestamp = pd.Timestamp("2015-01-02")
):
    """Given a dictionary of symbols and initial weights, returns a dataframe of all the adjusted weights of
    the portfolio over time. That is, the percentage of the portfolio each security takes over the course of
    daily returns.

    .. code-block:: python
        weights({"AAPL": 0.25, "WBA": 0.25, "CBOE": 0.5}, period="1y")

    Note this is NOT fixed/rebalanced weights as most daily target indices pursue. This is to highlight the change in
    weights of an untouched portfolio

    Parameters:
        ticker_weights (dict): a dictionary where keys are strings, and values are floating point weights. sum(values)
        should approach 1.0 start_date: A pandas timestamp with the start date of portfolio. This day will yield the
        starting weights

    Returns:
        A dataframe of daily portfolio weights, weight the initial weights designated at the start of the period
        provided
    """
    df = pd.DataFrame()
    for ticker in ticker_weights:
        df[ticker] = get_returns(ticker, start_date)
        df[ticker].iloc[0] = ticker_weights[ticker]
    for i in range(1, len(df)):  # can't do with rolling.agg :(
        df.iloc[i] = df.iloc[i - 1] * df.iloc[i]
        df.iloc[i] /= df.iloc[i].sum()
    return df


def etf_returns(
    ticker_weights: dict,
    start_date: pd.Timestamp = pd.Timestamp("2015-01-02"),
    index_base: float = 100.0,
):
    """Given a dictionary of symbols and FIXED weights, a period, and the start value of the Index, returns a dataframe
    with weighted daily returns of the index ('ER' for 'Excess Returns'), weighted returns of each index component,
    and the index value for each day from the base.

    Note that this is under the behavior of daily targetted returns, and supports leverage. This does NOT account
    for dividend re-investment"""
    df = pd.DataFrame()
    for ticker in ticker_weights:
        df[ticker] = get_returns(ticker, start_date) * ticker_weights[ticker]
    df["ER"] = df.sum(axis=1)
    df["ER"][0] = index_base
    df["Index"] = (
        df["ER"].rolling(window=len(df), min_periods=1).apply(pd.Series.product)
    )
    return df


print(etf_returns({"RIVN": 0.5, "AAPL": 0.5}))
