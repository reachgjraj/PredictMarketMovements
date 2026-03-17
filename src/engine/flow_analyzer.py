def find_unusual(df):
    if df is None: return None
    return df[df['volume'] > (df['openInterest'] * 1.5)].sort_values('volume', ascending=False).head(5)