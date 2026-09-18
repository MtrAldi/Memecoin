# Solana Pump.fun & GMGN Memecoin Rugpull Detector

Tool berbasis Python untuk mendeteksi potensi *rugpull* (penipuan developer), analisis konsentrasi *holder*, dan memindai token *trending* di ekosistem Solana (Pump.fun & Raydium).

## Fitur Utama
1. **Pump Analyzer (`pump_analyzer.py`)**: Menganalisis token spesifik berdasarkan alamat kontrak (*Mint Address*), memeriksa porsi kepemilikan *dev*, konsentrasi *top holders*, dan status *freeze authority*.
2. **Trending Scanner (`trending_pump_scanner.py`)**: Memindai token *hot/trending* di ekosistem Solana secara otomatis dan menghitung *Safety Score* (0–100) untuk meminimalisir risiko tersangkut *rugpull*.

## Cara Instalasi
Pastikan Anda memiliki Python 3 dan pustaka `requests` terinstal:
```bash
pip install requests
```

## Cara Penggunaan

### 1. Analisis Token Spesifik
Jalankan skrip analisis dengan memasukkan alamat kontrak Solana token yang ingin Anda periksa:
```bash
python3 pump_analyzer.py <CONTRACT_ADDRESS>
```

### 2. Pindai Token Trending / Hot
Jalankan skrip pemindai untuk melihat daftar token yang sedang aktif beserta skor keamanannya:
```bash
python3 trending_pump_scanner.py
```

## Disclaimer
Perdagangan memecoin memiliki risiko kerugian finansial yang sangat tinggi. Tool ini hanya membantu membaca metrik on-chain dan **bukan** merupakan saran keuangan (*NFA - Not Financial Advice*). Selalu gunakan dana dingin (*risk capital*) Anda sendiri.
