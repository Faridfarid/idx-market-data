# idx-market-data

Harga harian 14 saham IDX dan IHSG, diperbarui otomatis tiap hari bursa pukul ±18:23 WIB lewat GitHub Actions. Dipakai untuk backtest strategi momentum.

Saham: ADRO, ANTM, ASII, AUTO, BRIS, INDF, IPCC, PGAS, POWR, SIDO, TLKM, TOTL, TOTO, UNTR. Benchmark: IHSG (`JKSE.csv`).

Kolom tiap file di `data/`:
- `close`: harga penutupan apa adanya
- `adj_close`: harga yang disesuaikan dividen dan aksi korporasi (untuk backtest)
- `volume`

Sumber: Yahoo Finance. Menambah saham cukup dengan mengubah daftar `TICKERS` di `scripts/fetch_prices.py`.
