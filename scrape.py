import os
import json
import yfinance as yf

# Takip edilecek en büyük 12 hisse senedi
symbols = ["MSFT", "AAPL", "NVDA", "GOOG", "AMZN", "META", "TSLA", "NFLX", "AMD", "IBM", "INTC", "PYPL"]
os.makedirs("data", exist_ok=True)
summary = []

for symbol in symbols:
    try:
        ticker = yf.Ticker(symbol)
        
        # Son 100 günlük kapanış geçmişini çekip kaydediyoruz
        hist = ticker.history(period="100d")
        prices = hist['Close'].round(2).tolist()
        
        with open(f"data/{symbol}.json", "w") as f:
            json.dump({"symbol": symbol, "history": prices}, f, indent=2)
            
        # Şirket bilgilerini (Piyasa Değeri ve Şirket Adı) çekiyoruz
        info = ticker.info
        market_cap = info.get('marketCap', 0) / 1e9  # Milyar Dolar cinsinden
        company_name = info.get('longName', symbol)
        
        # Günlük yüzde değişimi (Son gün kapanışı vs Bir önceki gün kapanışı)
        change_percent = 0.0
        if len(prices) > 1:
            change_percent = round(((prices[-1] - prices[-2]) / prices[-2]) * 100, 2)
        
        summary.append({
            "symbol": symbol,
            "name": company_name,
            "changePercent": change_percent,
            "marketCap": market_cap
        })
        print(f"Başarıyla kazındı: {symbol} | Değer: {market_cap:.2f}B$ | Günlük Değişim: {change_percent}%")
    except Exception as e:
        print(f"Hata oluştu ({symbol}): {e}")

# Tüm hisselerin özet bilgisini data/summary.json olarak kaydediyoruz
with open("data/summary.json", "w") as f:
    json.dump(summary, f, indent=2)
