# 🚗 Dashboard Simulasi Drive-Thru Queue System

Aplikasi web profesional untuk analisis **What-If** pada sistem antrean Drive-Thru menggunakan **Discrete Event Simulation (SimPy)**.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![SimPy](https://img.shields.io/badge/SimPy-4.0+-green.svg)

## 📋 Deskripsi

Aplikasi ini mensimulasikan sistem antrean Drive-Thru dengan 3 stasiun layanan:
1. **Stasiun Pemesanan** (Kapasitas: 1)
2. **Stasiun Pembayaran** (Kapasitas: Dinamis)
3. **Stasiun Pengambilan** (Kapasitas: Dinamis)

## ✨ Fitur

- **Dashboard Utama**: KPI scorecard, visualisasi waktu tunggu, deteksi bottleneck
- **Analisis Detail**: Statistik deskriptif, matriks korelasi, box plot
- **Perbandingan Skenario**: What-If analysis untuk optimasi resource
- **Insight Otomatis**: Rekomendasi berbasis hasil simulasi

## 🚀 Demo

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://tugasbesar-pemodelan.streamlit.app)

## 📁 Struktur Project

```
├── app.py                 # Dashboard Utama
├── simulation.py          # Backend SimPy
├── requirements.txt       # Dependencies
└── pages/
    ├── 1_📊_Analisis_Detail.py
    ├── 2_📈_Perbandingan_Skenario.py
    └── 3_ℹ️_Tentang.py
```

## 🛠️ Instalasi

```bash
# Clone repository
git clone https://github.com/atepginzo/TugasBesar_Pemodelan.git
cd TugasBesar_Pemodelan

# Install dependencies
pip install -r requirements.txt

# Jalankan aplikasi
streamlit run app.py
```

## 📦 Dependencies

- streamlit >= 1.28.0
- simpy >= 4.0.0
- pandas >= 2.0.0
- numpy >= 1.24.0
- matplotlib >= 3.7.0
- seaborn >= 0.12.0

## 🎓 Tugas Besar

**Mata Kuliah**: Pemodelan & Simulasi  
**Semester**: 5  
**Tahun**: 2026

## 📄 License

MIT License
