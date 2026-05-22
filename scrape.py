import os
import json
import yfinance as yf

# Takip etmek istediğiniz popüler hisselerin listesi
symbols = ["IBM", "AAPL", "MSFT", "TSLA", "NVDA", "AMZN"]

# Çıktıların kaydedileceği klasör
os.makedirs("data", exist_ok=True)

for symbol in symbols:
    try:
        # yfinance ile hissenin son 100 günlük verilerini çekiyoruz
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="100d")
        
        # Günlük kapanış fiyatlarını alıp virgülden sonra 2 basamağa yuvarlıyoruz
        prices = hist['Close'].round(2).tolist()
        
        data = {
            "symbol": symbol,
            "history": prices
        }
        
        # Veriyi data/HISSE.json olarak kaydediyoruz
        with open(f"data/{symbol}.json", "w") as f:
            json.dump(data, f, indent=2)
            
        print(f"Başarıyla güncellendi: {symbol} (Gün sayısı: {len(prices)})")
    except Exception as e:
        print(f"Hata oluştu ({symbol}): {e}")
