# -*- coding: utf-8 -*-
"""
📊 Halaman Analisis Detail
==========================

Halaman untuk analisis mendalam hasil simulasi Drive-Thru.
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from simulation import jalankan_simulasi, identifikasi_bottleneck

# Page Config
st.set_page_config(
    page_title="Analisis Detail - Drive-Thru Simulator",
    page_icon="📊",
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
        padding: 1.5rem 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        border: 1px solid rgba(212, 175, 55, 0.3);
    }
    
    .main-header h1 {
        color: #ffd700;
        font-size: 2rem;
        font-weight: 800;
        margin: 0;
    }
    
    .main-header p {
        color: #b8b8b8;
        margin: 0.5rem 0 0 0;
    }
    
    .golden-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent 0%, #ffd700 50%, transparent 100%);
        margin: 2rem 0;
        border: none;
    }
    
    .stat-card {
        background: linear-gradient(145deg, #1e1e2f 0%, #252540 100%);
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>📊 Analisis Detail Simulasi</h1>
    <p>Statistik dan visualisasi mendalam dari hasil simulasi</p>
</div>
""", unsafe_allow_html=True)

# Check if simulation data exists
if 'simulation_run' in st.session_state and st.session_state.simulation_run:
    df_hasil = st.session_state.df_hasil
    df_antrean = st.session_state.df_antrean
    utilisasi = st.session_state.utilisasi
    statistik = st.session_state.statistik
    
    if len(df_hasil) > 0:
        # =====================================================================
        # STATISTIK DESKRIPTIF
        # =====================================================================
        st.markdown("## 📈 Statistik Deskriptif")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Ringkasan Waktu Tunggu")
            stats_tunggu = df_hasil['Total_Waktu_Tunggu'].describe()
            
            fig, ax = plt.subplots(figsize=(8, 6))
            plt.style.use('dark_background')
            fig.patch.set_facecolor('#1a1a2e')
            ax.set_facecolor('#1a1a2e')
            
            metrics = ['Min', '25%', '50%', '75%', 'Max']
            values = [stats_tunggu['min'], stats_tunggu['25%'], stats_tunggu['50%'], 
                     stats_tunggu['75%'], stats_tunggu['max']]
            colors = ['#00d26a', '#00d26a', '#ffd700', '#ffa502', '#ff4757']
            
            bars = ax.bar(metrics, values, color=colors, edgecolor='white', linewidth=0.5)
            
            for bar, val in zip(bars, values):
                ax.text(bar.get_x() + bar.get_width()/2, val + 0.2, f'{val:.1f}', 
                       ha='center', fontsize=11, color='white', fontweight='bold')
            
            ax.set_ylabel('Waktu (Menit)', fontsize=12, color='white')
            ax.set_title('Distribusi Persentil Waktu Tunggu', fontsize=14, color='#ffd700', fontweight='bold')
            ax.tick_params(colors='white')
            sns.despine(ax=ax, top=True, right=True)
            ax.spines['bottom'].set_color('#666')
            ax.spines['left'].set_color('#666')
            
            plt.tight_layout()
            st.pyplot(fig)
            plt.close(fig)
        
        with col2:
            st.markdown("### Box Plot per Stasiun")
            
            fig, ax = plt.subplots(figsize=(8, 6))
            plt.style.use('dark_background')
            fig.patch.set_facecolor('#1a1a2e')
            ax.set_facecolor('#1a1a2e')
            
            data_to_plot = [
                df_hasil['Waktu_Tunggu_Pesan'],
                df_hasil['Waktu_Tunggu_Bayar'],
                df_hasil['Waktu_Tunggu_Ambil']
            ]
            
            bp = ax.boxplot(data_to_plot, labels=['Pesan', 'Bayar', 'Ambil'], patch_artist=True)
            
            colors = ['#00d2ff', '#ffd700', '#ff4757']
            for patch, color in zip(bp['boxes'], colors):
                patch.set_facecolor(color)
                patch.set_alpha(0.7)
            
            for whisker in bp['whiskers']:
                whisker.set_color('white')
            for cap in bp['caps']:
                cap.set_color('white')
            for median in bp['medians']:
                median.set_color('#00d26a')
                median.set_linewidth(2)
            
            ax.set_ylabel('Waktu Tunggu (Menit)', fontsize=12, color='white')
            ax.set_title('Distribusi Waktu Tunggu per Stasiun', fontsize=14, color='#ffd700', fontweight='bold')
            ax.tick_params(colors='white')
            ax.grid(True, alpha=0.2, axis='y')
            sns.despine(ax=ax, top=True, right=True)
            ax.spines['bottom'].set_color('#666')
            ax.spines['left'].set_color('#666')
            
            plt.tight_layout()
            st.pyplot(fig)
            plt.close(fig)
        
        st.markdown('<div class="golden-divider"></div>', unsafe_allow_html=True)
        
        # =====================================================================
        # ANALISIS KORELASI
        # =====================================================================
        st.markdown("## 🔗 Analisis Korelasi")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            corr_cols = ['Waktu_Datang', 'Waktu_Tunggu_Pesan', 'Waktu_Tunggu_Bayar', 
                        'Waktu_Tunggu_Ambil', 'Total_Waktu_Tunggu', 'Total_Waktu_Sistem']
            corr_matrix = df_hasil[corr_cols].corr()
            
            fig, ax = plt.subplots(figsize=(10, 8))
            plt.style.use('dark_background')
            fig.patch.set_facecolor('#1a1a2e')
            
            sns.heatmap(corr_matrix, annot=True, cmap='RdYlGn', center=0,
                       square=True, linewidths=0.5, ax=ax, fmt='.2f',
                       annot_kws={'size': 9, 'color': 'white'})
            
            ax.set_title('Matriks Korelasi Waktu', fontsize=14, color='#ffd700', fontweight='bold', pad=15)
            ax.tick_params(colors='white', labelsize=8)
            
            plt.tight_layout()
            st.pyplot(fig)
            plt.close(fig)
        
        with col2:
            st.markdown("### Interpretasi Korelasi")
            
            st.info("""
            **📈 Korelasi Positif Tinggi (> 0.7):**
            - Menunjukkan hubungan searah yang kuat
            - Jika satu variabel naik, yang lain cenderung naik
            """)
            
            st.warning("""
            **📉 Korelasi Negatif (< -0.3):**
            - Menunjukkan hubungan berlawanan
            - Jika satu naik, yang lain turun
            """)
            
            st.success("""
            **⚪ Korelasi Rendah (-0.3 s/d 0.3):**
            - Tidak ada hubungan signifikan
            """)
            
            corr_arrival_total = corr_matrix.loc['Waktu_Datang', 'Total_Waktu_Tunggu']
            if corr_arrival_total > 0.3:
                st.error(f"⚠️ Korelasi waktu kedatangan vs total tunggu: **{corr_arrival_total:.2f}** - Antrean memburuk seiring waktu!")
            else:
                st.success(f"✅ Korelasi waktu kedatangan vs total tunggu: **{corr_arrival_total:.2f}** - Sistem cukup stabil")
        
        st.markdown('<div class="golden-divider"></div>', unsafe_allow_html=True)
        
        # =====================================================================
        # STATISTIK ANTREAN
        # =====================================================================
        st.markdown("## 📉 Statistik Panjang Antrean")
        
        col1, col2 = st.columns(2)
        
        with col1:
            avg_queues = {
                'Pesan': df_antrean['Antrean_Pesan'].mean(),
                'Bayar': df_antrean['Antrean_Bayar'].mean(),
                'Ambil': df_antrean['Antrean_Ambil'].mean()
            }
            
            fig, ax = plt.subplots(figsize=(8, 5))
            plt.style.use('dark_background')
            fig.patch.set_facecolor('#1a1a2e')
            ax.set_facecolor('#1a1a2e')
            
            colors = ['#00d2ff', '#ffd700', '#ff4757']
            bars = ax.bar(avg_queues.keys(), avg_queues.values(), color=colors, 
                         edgecolor='white', linewidth=0.5)
            
            for bar, val in zip(bars, avg_queues.values()):
                ax.text(bar.get_x() + bar.get_width()/2, val + 0.05, f'{val:.2f}', 
                       ha='center', fontsize=12, color='white', fontweight='bold')
            
            ax.set_ylabel('Rata-rata Jumlah Mobil', fontsize=12, color='white')
            ax.set_title('Rata-rata Panjang Antrean', fontsize=14, color='#ffd700', fontweight='bold')
            ax.tick_params(colors='white')
            sns.despine(ax=ax, top=True, right=True)
            ax.spines['bottom'].set_color('#666')
            ax.spines['left'].set_color('#666')
            ax.grid(True, alpha=0.2, axis='y')
            
            plt.tight_layout()
            st.pyplot(fig)
            plt.close(fig)
        
        with col2:
            max_queues = {
                'Pesan': df_antrean['Antrean_Pesan'].max(),
                'Bayar': df_antrean['Antrean_Bayar'].max(),
                'Ambil': df_antrean['Antrean_Ambil'].max()
            }
            
            fig, ax = plt.subplots(figsize=(8, 5))
            plt.style.use('dark_background')
            fig.patch.set_facecolor('#1a1a2e')
            ax.set_facecolor('#1a1a2e')
            
            colors = ['#00d2ff', '#ffd700', '#ff4757']
            bars = ax.bar(max_queues.keys(), max_queues.values(), color=colors, 
                         edgecolor='white', linewidth=0.5)
            
            for bar, val in zip(bars, max_queues.values()):
                ax.text(bar.get_x() + bar.get_width()/2, val + 0.1, f'{int(val)}', 
                       ha='center', fontsize=12, color='white', fontweight='bold')
            
            ax.set_ylabel('Jumlah Mobil Maksimum', fontsize=12, color='white')
            ax.set_title('Panjang Antrean Maksimum', fontsize=14, color='#ffd700', fontweight='bold')
            ax.tick_params(colors='white')
            sns.despine(ax=ax, top=True, right=True)
            ax.spines['bottom'].set_color('#666')
            ax.spines['left'].set_color('#666')
            ax.grid(True, alpha=0.2, axis='y')
            
            plt.tight_layout()
            st.pyplot(fig)
            plt.close(fig)
    else:
        st.warning("Data simulasi kosong.")
else:
    st.warning("""
    ⚠️ **Belum Ada Data Simulasi**
    
    Silakan jalankan simulasi terlebih dahulu di halaman utama (🏠 Dashboard Utama).
    """)
    
    if st.button("Kembali ke Dashboard Utama"):
        st.switch_page("app.py")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    📊 Halaman Analisis Detail • Dashboard Simulasi Drive-Thru
</div>
""", unsafe_allow_html=True)
