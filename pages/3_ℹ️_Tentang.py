# -*- coding: utf-8 -*-
"""
ℹ️ Halaman Tentang
==================

Informasi tentang aplikasi, teori simulasi, dan dokumentasi.
"""

import streamlit as st

st.set_page_config(
    page_title="Tentang - Drive-Thru Simulator",
    page_icon="ℹ️",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    .stApp {
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        padding: 2rem 2.5rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        border: 1px solid rgba(212, 175, 55, 0.3);
        text-align: center;
    }
    
    .main-header h1 {
        color: #ffd700;
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }
    
    .main-header p {
        color: #b8b8b8;
        font-size: 1.1rem;
        margin: 0;
    }
    
    .info-card {
        background: linear-gradient(145deg, #1e1e2f 0%, #252540 100%);
        border-radius: 16px;
        padding: 2rem;
        margin: 1.5rem 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .info-card h3 {
        color: #ffd700;
        margin-bottom: 1rem;
        font-size: 1.3rem;
    }
    
    .info-card p, .info-card li {
        color: #d0d0d0;
        line-height: 1.8;
    }
    
    .tech-badge {
        display: inline-block;
        background: rgba(255, 215, 0, 0.1);
        color: #ffd700;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        margin: 0.2rem;
        font-size: 0.9rem;
        border: 1px solid rgba(255, 215, 0, 0.3);
    }
    
    .golden-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent 0%, #ffd700 50%, transparent 100%);
        margin: 2rem 0;
        border: none;
    }
    
    .formula-box {
        background: rgba(0, 0, 0, 0.3);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid #ffd700;
        font-family: 'Courier New', monospace;
        color: #00d26a;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>ℹ️ Tentang Aplikasi</h1>
    <p>Dashboard Simulasi Sistem Antrean Drive-Thru</p>
</div>
""", unsafe_allow_html=True)

# Overview
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    <div class="info-card">
        <h3>📖 Deskripsi Aplikasi</h3>
        <p>
            Aplikasi ini adalah <strong>Dashboard Simulasi Profesional</strong> untuk menganalisis 
            performa sistem antrean Drive-Thru menggunakan metode <strong>Discrete Event Simulation (DES)</strong>.
        </p>
        <p>
            Dibuat sebagai bagian dari <strong>Tugas Besar Mata Kuliah Pemodelan & Simulasi</strong>,
            aplikasi ini memungkinkan pengguna melakukan analisis <strong>What-If</strong> untuk 
            mengoptimalkan alokasi sumber daya dan mengurangi waktu tunggu pelanggan.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="info-card">
        <h3>🛠️ Teknologi</h3>
        <p>
            <span class="tech-badge">Python 3.10+</span>
            <span class="tech-badge">SimPy 4.0</span>
            <span class="tech-badge">Streamlit</span>
            <span class="tech-badge">Pandas</span>
            <span class="tech-badge">Seaborn</span>
            <span class="tech-badge">Matplotlib</span>
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="golden-divider"></div>', unsafe_allow_html=True)

# Theory Section
st.markdown("## 📚 Teori Sistem Antrean")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="info-card">
        <h3>🔄 Model Sistem Drive-Thru</h3>
        <p>Sistem Drive-Thru dimodelkan sebagai <strong>jaringan antrean tandem</strong> 
        dengan 3 stasiun berurutan:</p>
        <ol>
            <li><strong>Stasiun Pesan</strong> (Order Station) - Kapasitas: 1</li>
            <li><strong>Stasiun Bayar</strong> (Payment Station) - Kapasitas: Dinamis</li>
            <li><strong>Stasiun Ambil</strong> (Pickup Station) - Kapasitas: Dinamis</li>
        </ol>
        <p>Setiap pelanggan harus melewati ketiga stasiun secara berurutan.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="info-card">
        <h3>📊 Distribusi Probabilitas</h3>
        <p>Simulasi menggunakan distribusi <strong>Eksponensial</strong> untuk:</p>
        <ul>
            <li><strong>Waktu Antar-Kedatangan:</strong> Rata-rata 2 menit (default)</li>
            <li><strong>Waktu Layanan Pesan:</strong> Rata-rata 1.5 menit</li>
            <li><strong>Waktu Layanan Bayar:</strong> Rata-rata 1.0 menit</li>
            <li><strong>Waktu Layanan Ambil:</strong> Rata-rata 2.0 menit</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="golden-divider"></div>', unsafe_allow_html=True)

# Formulas
st.markdown("## 📐 Rumus & Metrik")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="info-card">
        <h3>🎯 Utilisasi Resource</h3>
        <div class="formula-box">
            ρ = λ × S / (c × T) × 100%
        </div>
        <p>Dimana:</p>
        <ul>
            <li><strong>ρ</strong> = Utilisasi (%)</li>
            <li><strong>λ</strong> = Jumlah pelanggan</li>
            <li><strong>S</strong> = Rata-rata waktu layanan</li>
            <li><strong>c</strong> = Jumlah server</li>
            <li><strong>T</strong> = Total waktu simulasi</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="info-card">
        <h3>📈 Throughput</h3>
        <div class="formula-box">
            Throughput = N / (T / 60) mobil/jam
        </div>
        <p>Dimana:</p>
        <ul>
            <li><strong>N</strong> = Total pelanggan selesai</li>
            <li><strong>T</strong> = Durasi simulasi (menit)</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="golden-divider"></div>', unsafe_allow_html=True)

# Features
st.markdown("## ✨ Fitur Aplikasi")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="info-card">
        <h3>🏠 Dashboard Utama</h3>
        <ul>
            <li>KPI Scorecard</li>
            <li>Visualisasi waktu tunggu</li>
            <li>Deteksi bottleneck</li>
            <li>Insight otomatis</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="info-card">
        <h3>📊 Analisis Detail</h3>
        <ul>
            <li>Statistik deskriptif</li>
            <li>Matriks korelasi</li>
            <li>Box plot per stasiun</li>
            <li>Statistik antrean</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="info-card">
        <h3>📈 Perbandingan</h3>
        <ul>
            <li>What-If Analysis</li>
            <li>Side-by-side comparison</li>
            <li>Improvement metrics</li>
            <li>Rekomendasi</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="golden-divider"></div>', unsafe_allow_html=True)

# Credits
st.markdown("""
<div class="info-card" style="text-align: center;">
    <h3>📚 Tugas Besar Pemodelan & Simulasi</h3>
    <p style="font-size: 1.1rem; margin-bottom: 1rem;">
        Dibuat untuk memenuhi tugas besar mata kuliah Pemodelan & Simulasi
    </p>
    <p>
        <span class="tech-badge">Semester 5</span>
        <span class="tech-badge">2026</span>
    </p>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    ℹ️ Dibuat dengan ❤️ menggunakan Python & Streamlit
</div>
""", unsafe_allow_html=True)
