import yfinance as yf

def get_options(symbol):
    tk = yf.Ticker(symbol)
    try:
        exp = tk.options[0]
        chain = tk.option_chain(exp)
        return chain.calls, chain.puts
    except:
        return None, None