"""Tarik harga harian saham IDX dari Yahoo Finance dan simpan sebagai CSV.

Tiap file berisi:
  close      : harga penutupan apa adanya (seperti di Stockbit)
  adj_close  : harga yang sudah disesuaikan dividen & aksi korporasi (dipakai untuk backtest)
  volume
"""
import os
import time

import pandas as pd
import yfinance as yf

TICKERS = [
    "ADRO", "ANTM", "ASII", "AUTO", "BRIS", "INDF", "IPCC",
    "PGAS", "POWR", "SIDO", "TLKM", "TOTL", "TOTO", "UNTR",
]
BENCHMARK = {"JKSE": "^JKSE"}  # IHSG
START = "2010-01-01"
OUT = "data"
os.makedirs(OUT, exist_ok=True)


def fetch(symbol):
    df = yf.download(symbol, start=START, auto_adjust=False, actions=False, progress=False)
    if df.empty:
        raise ValueError("data kosong")
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    out = pd.DataFrame({
        "close": df["Close"],
        "adj_close": df["Adj Close"],
        "volume": df["Volume"],
    })
    out = out.dropna(subset=["close"])
    out.index.name = "date"
    return out


jobs = {t: f"{t}.JK" for t in TICKERS}
jobs.update(BENCHMARK)

failed = []
for name, symbol in jobs.items():
    for attempt in range(3):
        try:
            df = fetch(symbol)
            df.round(4).to_csv(f"{OUT}/{name}.csv")
            print(f"{name}: {len(df)} baris, {df.index[0].date()} s.d. {df.index[-1].date()}")
            break
        except Exception as e:
            print(f"{name}: percobaan {attempt + 1} gagal ({e})")
            time.sleep(5)
    else:
        failed.append(name)
    time.sleep(1)

if failed:
    print("Gagal:", ", ".join(failed))
    # Jangan gagalkan seluruh job; file lama tetap dipakai.
