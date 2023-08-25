import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import datetime
import quantstats as qs
from pypfopt.expected_returns import mean_historical_return
from pypfopt.risk_models import CovarianceShrinkage
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import objective_functions
from pypfopt import HRPOpt
from pypfopt.efficient_frontier import EfficientCVaR
import tempfile

# Setting stock data collector 
def get_stock(ticker, start, end):
    data = yf.Ticker(ticker).history(start=start, end=end)
    data[ticker] = data["Close"]
    return data[[ticker]]

@st.cache_data
def combine_stocks(tickers, start, end):
    data_frames = [get_stock(ticker, start, end) for ticker in tickers]
    df_merged = pd.concat(data_frames, axis=1)
    return df_merged

def generate_maxsharpe_portfolio(portfolio, gamma_sharpe):
    mu = mean_historical_return(portfolio)
    Sigma = CovarianceShrinkage(portfolio).ledoit_wolf()
    ef = EfficientFrontier(mu, Sigma)
    ef.add_objective(objective_functions.L2_reg, gamma=gamma_sharpe)
    weights = ef.max_sharpe()
    clean_weights = ef.clean_weights()
    return clean_weights

def generate_tearsheet(returns, benchmark, rf, title):
    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmpfile:
        filepath = tmpfile.name

    qs.reports.html(returns, benchmark=benchmark, rf=rf, title=title, download_filename=filepath, output="Save")
    return filepath

def get_tickers_from_csv(filename):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(filename, delimiter=';')
    # Combine 'Name' and 'Ticker' columns, and return as a list
    return (df['name'] + ' (' + df['yfinance_ticker'] + ')').tolist()

combined_tickers = get_tickers_from_csv('assets.csv')

def main():
    st.title("Portfolio Optimization with qiip")

    # User Input
    selected_combined_tickers = st.multiselect("Select Tickers", combined_tickers)
    start = st.date_input("Start Date", datetime.datetime(2020, 2, 5))
    end = st.date_input("End Date", datetime.datetime(2023, 4, 6))

    if len(selected_combined_tickers) >= 2:
        selected_tickers = [item.split('(')[1].replace(')', '') for item in selected_combined_tickers]
        portfolio = combine_stocks(selected_tickers, start, end)
    
        if st.button("Generate Data"):
            st.write(portfolio)

        if st.button("Generate Max Sharpe Portfolio"):
            maxsharpe_weights = generate_maxsharpe_portfolio(portfolio, 2.0)
    
            # Convert dictionary to DataFrame for nice table display
            weights_df = pd.DataFrame(list(maxsharpe_weights.items()), columns=['Tickers', 'Weights'])
            st.table(weights_df.set_index('Tickers'))


            # Calculate portfolio returns using the weights
            returns = portfolio.pct_change().dropna()
            portfolio_returns = (returns * list(maxsharpe_weights.values())).sum(axis=1)

            html_report_path = generate_tearsheet(portfolio_returns, benchmark='SPY', rf=0.0, title="Maximum Sharpe Portfolio")
            st.components.v1.html(open(html_report_path, 'r').read(), height=8000)
    else:
        st.warning('Please select at least two tickers to proceed.')

if __name__ == "__main__":
    main()