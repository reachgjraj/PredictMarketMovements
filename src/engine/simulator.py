def simulate_pl(symbol, entry, exit, direction):
    mult = 20 if "NQ" in symbol else 50 if "ES" in symbol else 1
    points = exit - entry if direction == "Bullish" else entry - exit
    return round(points * mult, 2)