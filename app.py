# -*- coding: utf-8 -*-
"""
🚗 Dashboard Simulasi Drive-Thru Queue System
==============================================

Aplikasi Streamlit untuk analisis What-If pada sistem antrean Drive-Thru
menggunakan simulasi diskrit (SimPy).

Author: Simulation Dashboard  
Version: 1.0.0
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from simulation import (
    jalankan_simulasi, 
    identifikasi_bottleneck, 
    generate_insight
)

# =====================================================================
# KONFIGURASI HALAMAN
# =====================================================================
st.set_page_config(
    page_title="Dashboard Simulasi Drive-Thru",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': """
        ## 🚗 Dashboard Simulasi Drive-Thru
        
        Aplikasi ini dibuat untuk Tugas Besar Pemodelan & Simulasi.
        Menggunakan SimPy untuk simulasi antrean diskrit.
        """
    }
)

# =====================================================================
# CUSTOM CSS - PREMIUM DARK THEME
# =====================================================================
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Global Styles */
    .stApp {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main Header */
    .main-header {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        padding: 2rem 2.5rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        border: 1px solid rgba(212, 175, 55, 0.3);
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
    }
    
    .main-header h1 {
        color: #ffd700;
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 10px rgba(255, 215, 0, 0.3);
    }
    
    .main-header p {
        color: #b8b8b8;
        font-size: 1.1rem;
        margin: 0;
    }
    
    /* KPI Cards */
    .kpi-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .kpi-card {
        background: linear-gradient(145deg, #1e1e2f 0%, #252540 100%);
        border-radius: 16px;
        padding: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .kpi-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(212, 175, 55, 0.15);
    }
    
    .kpi-value {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #ffd700 0%, #ffaa00 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .kpi-value.green {
        background: linear-gradient(135deg, #00d26a 0%, #00a854 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .kpi-value.red {
        background: linear-gradient(135deg, #ff4757 0%, #ff3838 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .kpi-label {
        color: #888;
        font-size: 0.9rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-top: 0.5rem;
    }
    
    .kpi-delta {
        font-size: 0.85rem;
        margin-top: 0.3rem;
    }
    
    .kpi-delta.positive {
        color: #00d26a;
    }
    
    .kpi-delta.negative {
        color: #ff4757;
    }
    
    /* Section Headers */
    .section-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.75rem;
        border-bottom: 2px solid rgba(212, 175, 55, 0.3);
    }
    
    .section-header h2 {
        color: #ffffff;
        font-size: 1.4rem;
        font-weight: 700;
        margin: 0;
    }
    
    .section-header .icon {
        font-size: 1.5rem;
    }
    
    /* Insight Box */
    .insight-box {
        background: linear-gradient(145deg, #1a2744 0%, #1e3a5f 100%);
        border-radius: 16px;
        padding: 1.75rem;
        margin: 1.5rem 0;
        border-left: 4px solid #ffd700;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
    }
    
    .insight-box h3 {
        color: #ffd700;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .insight-box p {
        color: #d0d0d0;
        font-size: 0.95rem;
        line-height: 1.7;
        margin: 0;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f0f1a 0%, #1a1a2e 100%);
    }
    
    section[data-testid="stSidebar"] .stMarkdown h1 {
        color: #ffd700;
        font-size: 1.4rem;
        font-weight: 700;
        border-bottom: 2px solid rgba(212, 175, 55, 0.3);
        padding-bottom: 0.75rem;
    }
    
    section[data-testid="stSidebar"] .stMarkdown h3 {
        color: #ffffff;
        font-size: 1rem;
        font-weight: 600;
        margin-top: 1.5rem;
    }
    
    /* Button Styling */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #ffd700 0%, #ffaa00 100%);
        color: #1a1a2e;
        font-weight: 700;
        font-size: 1rem;
        padding: 0.75rem 1.5rem;
        border-radius: 12px;
        border: none;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #ffcc00 0%, #ff9900 100%);
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(255, 215, 0, 0.4);
    }
    
    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: rgba(30, 30, 50, 0.5);
        padding: 0.5rem;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: #888;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #ffd700 0%, #ffaa00 100%);
        color: #1a1a2e;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 800;
    }
    
    /* DataFrame Styling */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
    }
    
    /* Divider */
    .golden-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent 0%, #ffd700 50%, transparent 100%);
        margin: 2rem 0;
        border: none;
    }
    
    /* Chart Container */
    .chart-container {
        background: rgba(30, 30, 50, 0.3);
        border-radius: 16px;
        padding: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
</style>
""", unsafe_allow_html=True)

# =====================================================================
# HELPER FUNCTIONS
# =====================================================================
def create_wait_time_line_chart(df: pd.DataFrame):
    """Membuat line chart waktu tunggu vs waktu kedatangan."""
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # Set style
    sns.set_theme(style="darkgrid", palette="viridis")
    plt.style.use('dark_background')
    fig.patch.set_facecolor('#1a1a2e')
    ax.set_facecolor('#1a1a2e')
    
    # Plot
    ax.plot(
        df['Waktu_Datang'], 
        df['Total_Waktu_Tunggu'], 
        color='#ffd700', 
        linewidth=2, 
        marker='o', 
        markersize=4,
        alpha=0.8
    )
    
    # Average line
    avg_wait = df['Total_Waktu_Tunggu'].mean()
    ax.axhline(
        avg_wait, 
        color='#ff4757', 
        linestyle='--', 
        linewidth=2, 
        label=f'Rata-rata: {avg_wait:.1f} menit'
    )
    
    # Styling
    ax.set_xlabel('Waktu Kedatangan (Menit)', fontsize=12, color='white', fontweight='bold')
    ax.set_ylabel('Waktu Tunggu (Menit)', fontsize=12, color='white', fontweight='bold')
    ax.set_title('📈 Tren Waktu Tunggu Pelanggan', fontsize=14, color='#ffd700', fontweight='bold', pad=15)
    ax.tick_params(colors='white')
    ax.legend(loc='upper left', facecolor='#1a1a2e', edgecolor='#ffd700', labelcolor='white')
    
    # Remove spines
    sns.despine(ax=ax, top=True, right=True)
    ax.spines['bottom'].set_color('#666')
    ax.spines['left'].set_color('#666')
    
    plt.tight_layout()
    return fig


def create_wait_time_histogram(df: pd.DataFrame):
    """Membuat histogram distribusi waktu tunggu."""
    fig, ax = plt.subplots(figsize=(10, 5))
    
    plt.style.use('dark_background')
    fig.patch.set_facecolor('#1a1a2e')
    ax.set_facecolor('#1a1a2e')
    
    # Histogram with KDE
    sns.histplot(
        data=df, 
        x='Total_Waktu_Tunggu', 
        kde=True, 
        color='#00d26a',
        alpha=0.7,
        ax=ax,
        edgecolor='white',
        linewidth=0.5
    )
    
    # Mean line
    mean_val = df['Total_Waktu_Tunggu'].mean()
    ax.axvline(mean_val, color='#ffd700', linestyle='--', linewidth=2, label=f'Mean: {mean_val:.1f}')
    
    # Styling
    ax.set_xlabel('Waktu Tunggu (Menit)', fontsize=12, color='white', fontweight='bold')
    ax.set_ylabel('Frekuensi', fontsize=12, color='white', fontweight='bold')
    ax.set_title('📊 Distribusi Waktu Tunggu', fontsize=14, color='#ffd700', fontweight='bold', pad=15)
    ax.tick_params(colors='white')
    ax.legend(loc='upper right', facecolor='#1a1a2e', edgecolor='#ffd700', labelcolor='white')
    
    sns.despine(ax=ax, top=True, right=True)
    ax.spines['bottom'].set_color('#666')
    ax.spines['left'].set_color('#666')
    
    plt.tight_layout()
    return fig


def create_utilization_chart(utilisasi: dict):
    """Membuat horizontal bar chart utilisasi dengan highlighting bottleneck."""
    fig, ax = plt.subplots(figsize=(10, 4))
    
    plt.style.use('dark_background')
    fig.patch.set_facecolor('#1a1a2e')
    ax.set_facecolor('#1a1a2e')
    
    stations = list(utilisasi.keys())
    values = list(utilisasi.values())
    
    # Dynamic colors based on utilization
    colors = []
    for v in values:
        if v >= 90:
            colors.append('#ff4757')  # Red - critical
        elif v >= 70:
            colors.append('#ffa502')  # Orange - warning
        else:
            colors.append('#00d26a')  # Green - OK
    
    # Horizontal bar chart
    bars = ax.barh(stations, values, color=colors, height=0.6, edgecolor='white', linewidth=0.5)
    
    # Add value labels
    for bar, value in zip(bars, values):
        ax.text(
            value + 2, 
            bar.get_y() + bar.get_height()/2, 
            f'{value:.1f}%', 
            va='center', 
            fontsize=12, 
            color='white',
            fontweight='bold'
        )
    
    # Capacity line
    ax.axvline(100, color='#ff4757', linestyle='--', linewidth=2, alpha=0.7, label='Batas Kapasitas')
    ax.axvline(80, color='#ffa502', linestyle=':', linewidth=1.5, alpha=0.5, label='Zona Peringatan (80%)')
    
    # Styling
    ax.set_xlabel('Utilisasi (%)', fontsize=12, color='white', fontweight='bold')
    ax.set_title('🎯 Utilisasi Setiap Stasiun', fontsize=14, color='#ffd700', fontweight='bold', pad=15)
    ax.set_xlim(0, 120)
    ax.tick_params(colors='white')
    ax.legend(loc='upper right', facecolor='#1a1a2e', edgecolor='#ffd700', labelcolor='white')
    
    # Invert y-axis for better reading
    ax.invert_yaxis()
    
    sns.despine(ax=ax, top=True, right=True)
    ax.spines['bottom'].set_color('#666')
    ax.spines['left'].set_color('#666')
    
    plt.tight_layout()
    return fig


def create_queue_dynamics_chart(df_queue: pd.DataFrame):
    """Membuat line chart dinamika panjang antrean."""
    fig, ax = plt.subplots(figsize=(10, 5))
    
    plt.style.use('dark_background')
    fig.patch.set_facecolor('#1a1a2e')
    ax.set_facecolor('#1a1a2e')
    
    # Plot each station
    ax.plot(df_queue['Waktu'], df_queue['Antrean_Pesan'], label='Stasiun Pesan', 
            color='#00d2ff', linewidth=2, alpha=0.8)
    ax.plot(df_queue['Waktu'], df_queue['Antrean_Bayar'], label='Stasiun Bayar', 
            color='#ffd700', linewidth=2, alpha=0.8)
    ax.plot(df_queue['Waktu'], df_queue['Antrean_Ambil'], label='Stasiun Ambil', 
            color='#ff4757', linewidth=2.5)
    
    # Fill area under the curves
    ax.fill_between(df_queue['Waktu'], df_queue['Antrean_Ambil'], alpha=0.2, color='#ff4757')
    
    # Styling
    ax.set_xlabel('Waktu Simulasi (Menit)', fontsize=12, color='white', fontweight='bold')
    ax.set_ylabel('Jumlah Mobil Mengantre', fontsize=12, color='white', fontweight='bold')
    ax.set_title('📉 Dinamika Panjang Antrean Real-Time', fontsize=14, color='#ffd700', fontweight='bold', pad=15)
    ax.tick_params(colors='white')
    ax.legend(loc='upper right', facecolor='#1a1a2e', edgecolor='#ffd700', labelcolor='white')
    ax.set_ylim(bottom=0)
    
    sns.despine(ax=ax, top=True, right=True)
    ax.spines['bottom'].set_color('#666')
    ax.spines['left'].set_color('#666')
    
    # Grid
    ax.grid(True, alpha=0.2, linestyle='--')
    
    plt.tight_layout()
    return fig


# =====================================================================
# SIDEBAR - CONTROL PANEL
# =====================================================================
with st.sidebar:
    st.markdown("# 🎛️ Panel Konfigurasi")
    
    st.markdown("### ⏱️ Pengaturan Waktu")
    
    laju_kedatangan = st.slider(
        "Interval Kedatangan (menit)",
        min_value=0.5,
        max_value=5.0,
        value=2.0,
        step=0.1,
        help="Rata-rata waktu antar kedatangan mobil"
    )
    
    durasi_simulasi = st.slider(
        "Durasi Simulasi (menit)",
        min_value=60,
        max_value=480,
        value=240,
        step=30,
        help="Berapa lama simulasi akan berjalan"
    )
    
    st.markdown("### 👥 Sumber Daya Sistem")
    
    jumlah_kasir = st.slider(
        "Jumlah Kasir",
        min_value=1,
        max_value=5,
        value=1,
        help="Jumlah kasir di stasiun pembayaran"
    )
    
    jumlah_staff_ambil = st.slider(
        "Jumlah Staff Pengambilan",
        min_value=1,
        max_value=5,
        value=1,
        help="Jumlah staff di stasiun pengambilan"
    )
    
    st.markdown("### 🎲 Pengaturan Lanjutan")
    
    use_random_seed = st.checkbox("Gunakan Seed Tetap", value=True)
    random_seed = None
    if use_random_seed:
        random_seed = st.number_input("Random Seed", min_value=1, max_value=9999, value=42)
    
    st.markdown("---")
    
    # Run Simulation Button
    run_simulation = st.button(
        "🚀 JALANKAN SIMULASI",
        use_container_width=True,
        type="primary"
    )

# =====================================================================
# MAIN CONTENT
# =====================================================================

# Hero Header
st.markdown("""
<div class="main-header">
    <h1>🚗 Dashboard Simulasi Drive-Thru</h1>
    <p>Analisis What-If untuk Optimasi Sistem Antrean menggunakan SimPy Discrete Event Simulation</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if 'simulation_run' not in st.session_state:
    st.session_state.simulation_run = False
if 'df_hasil' not in st.session_state:
    st.session_state.df_hasil = None

# Run simulation if button clicked
if run_simulation:
    with st.spinner("🔄 Menjalankan simulasi..."):
        df_hasil, df_antrean, utilisasi, statistik = jalankan_simulasi(
            laju_kedatangan=laju_kedatangan,
            durasi_simulasi=durasi_simulasi,
            jumlah_kasir=jumlah_kasir,
            jumlah_staff_ambil=jumlah_staff_ambil,
            random_seed=random_seed
        )
        
        # Store in session state
        st.session_state.simulation_run = True
        st.session_state.df_hasil = df_hasil
        st.session_state.df_antrean = df_antrean
        st.session_state.utilisasi = utilisasi
        st.session_state.statistik = statistik
        st.session_state.jumlah_kasir = jumlah_kasir
        st.session_state.jumlah_staff_ambil = jumlah_staff_ambil

# Display content
if st.session_state.simulation_run and st.session_state.df_hasil is not None:
    df_hasil = st.session_state.df_hasil
    df_antrean = st.session_state.df_antrean
    utilisasi = st.session_state.utilisasi
    statistik = st.session_state.statistik
    
    # Check if we have data
    if len(df_hasil) == 0:
        st.warning("⚠️ Simulasi tidak menghasilkan data. Coba tingkatkan durasi atau turunkan interval kedatangan.")
    else:
        # =====================================================================
        # KPI SECTION
        # =====================================================================
        st.markdown('<div class="golden-divider"></div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="section-header">
            <span class="icon">📊</span>
            <h2>Metrik Kinerja Utama</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # KPI Row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="🚗 Total Mobil Dilayani",
                value=f"{statistik['total_mobil']:,}",
                delta=f"{statistik['throughput']:.0f} mobil/jam"
            )
        
        with col2:
            avg_wait = statistik['rata_waktu_tunggu']
            delta_color = "normal" if avg_wait <= 5 else "inverse"
            st.metric(
                label="⏱️ Rata-rata Waktu Tunggu",
                value=f"{avg_wait:.1f} menit",
                delta=f"Max: {statistik['max_waktu_tunggu']:.1f}",
                delta_color=delta_color
            )
        
        with col3:
            bottleneck, status = identifikasi_bottleneck(utilisasi)
            max_util = max(utilisasi.values()) if utilisasi else 0
            st.metric(
                label="🎯 Utilisasi Tertinggi",
                value=f"{max_util:.1f}%",
                delta=f"Stasiun {bottleneck}"
            )
        
        with col4:
            st.metric(
                label="📈 Throughput",
                value=f"{statistik['throughput']:.0f}",
                delta="mobil per jam"
            )
        
        # Status Alert
        _, status = identifikasi_bottleneck(utilisasi)
        if "KRITIS" in status:
            st.error(f"⚠️ **Status Sistem: {status}** - Diperlukan penambahan resource segera!")
        elif "PERINGATAN" in status:
            st.warning(f"⚡ **Status Sistem: {status}** - Sistem mendekati kapasitas maksimum")
        else:
            st.success(f"✅ **Status Sistem: {status}** - Performa sistem optimal")
        
        st.markdown('<div class="golden-divider"></div>', unsafe_allow_html=True)
        
        # =====================================================================
        # VISUALIZATION TABS
        # =====================================================================
        tab1, tab2, tab3 = st.tabs([
            "📈 Analisis Waktu",
            "🎯 Deteksi Bottleneck", 
            "📋 Data Mentah"
        ])
        
        with tab1:
            st.markdown("""
            <div class="section-header">
                <span class="icon">⏱️</span>
                <h2>Analisis Efisiensi Waktu</h2>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig_line = create_wait_time_line_chart(df_hasil)
                st.pyplot(fig_line)
                plt.close(fig_line)
            
            with col2:
                fig_hist = create_wait_time_histogram(df_hasil)
                st.pyplot(fig_hist)
                plt.close(fig_hist)
            
            # Queue Dynamics
            st.markdown("""
            <div class="section-header">
                <span class="icon">📉</span>
                <h2>Dinamika Antrean Sepanjang Waktu</h2>
            </div>
            """, unsafe_allow_html=True)
            
            fig_queue = create_queue_dynamics_chart(df_antrean)
            st.pyplot(fig_queue)
            plt.close(fig_queue)
        
        with tab2:
            st.markdown("""
            <div class="section-header">
                <span class="icon">🎯</span>
                <h2>Analisis Bottleneck & Utilisasi</h2>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                fig_util = create_utilization_chart(utilisasi)
                st.pyplot(fig_util)
                plt.close(fig_util)
            
            with col2:
                st.markdown("#### 📊 Detail Utilisasi")
                
                for station, value in utilisasi.items():
                    color = "🔴" if value >= 90 else "🟠" if value >= 70 else "🟢"
                    st.markdown(f"{color} **{station}:** {value:.1f}%")
                
                st.markdown("---")
                st.markdown("#### 📖 Legenda:")
                st.markdown("🟢 Aman (< 70%)")
                st.markdown("🟠 Sibuk (70-90%)")
                st.markdown("🔴 Kritis (> 90%)")
        
        with tab3:
            st.markdown("""
            <div class="section-header">
                <span class="icon">📋</span>
                <h2>Data Detail Simulasi</h2>
            </div>
            """, unsafe_allow_html=True)
            
            # Data Statistics
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 📈 Ringkasan Statistik")
                stat_df = df_hasil[['Total_Waktu_Tunggu', 'Total_Waktu_Sistem']].describe()
                st.dataframe(stat_df.style.format("{:.2f}"), use_container_width=True)
            
            with col2:
                st.markdown("#### ⏱️ Statistik Per Stasiun")
                station_stats = pd.DataFrame({
                    'Stasiun': ['Pesan', 'Bayar', 'Ambil'],
                    'Rata-rata Tunggu': [
                        df_hasil['Waktu_Tunggu_Pesan'].mean(),
                        df_hasil['Waktu_Tunggu_Bayar'].mean(),
                        df_hasil['Waktu_Tunggu_Ambil'].mean()
                    ],
                    'Max Tunggu': [
                        df_hasil['Waktu_Tunggu_Pesan'].max(),
                        df_hasil['Waktu_Tunggu_Bayar'].max(),
                        df_hasil['Waktu_Tunggu_Ambil'].max()
                    ]
                })
                st.dataframe(station_stats.style.format("{:.2f}", subset=['Rata-rata Tunggu', 'Max Tunggu']), 
                           use_container_width=True)
            
            # Full Data Table
            st.markdown("#### 📋 Data Lengkap (10 Teratas)")
            st.dataframe(
                df_hasil.head(10).style.format({
                    'Waktu_Datang': '{:.1f}',
                    'Waktu_Selesai': '{:.1f}',
                    'Waktu_Tunggu_Pesan': '{:.2f}',
                    'Waktu_Tunggu_Bayar': '{:.2f}',
                    'Waktu_Tunggu_Ambil': '{:.2f}',
                    'Total_Waktu_Tunggu': '{:.2f}',
                    'Total_Waktu_Layanan': '{:.2f}',
                    'Total_Waktu_Sistem': '{:.2f}'
                }),
                use_container_width=True
            )
            
            # Download button
            csv = df_hasil.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Data CSV",
                data=csv,
                file_name="hasil_simulasi_drive_thru.csv",
                mime="text/csv"
            )
        
        # =====================================================================
        # INSIGHT BOX
        # =====================================================================
        st.markdown('<div class="golden-divider"></div>', unsafe_allow_html=True)
        
        insight = generate_insight(
            statistik, 
            utilisasi, 
            st.session_state.jumlah_kasir, 
            st.session_state.jumlah_staff_ambil
        )
        
        st.markdown(f"""
        <div class="insight-box">
            <h3>💡 Insight & Rekomendasi Otomatis</h3>
            <p>{insight.replace(chr(10), '<br>')}</p>
        </div>
        """, unsafe_allow_html=True)

else:
    # Initial state - no simulation run yet
    st.markdown("""
    <div style="text-align: center; padding: 3rem; background: linear-gradient(145deg, #1e1e2f 0%, #252540 100%); border-radius: 20px; margin: 2rem 0;">
        <h2 style="color: #ffd700; margin-bottom: 1rem;">🎯 Siap untuk Memulai?</h2>
        <p style="color: #b8b8b8; font-size: 1.1rem; max-width: 600px; margin: 0 auto;">
            Atur parameter simulasi di <strong style="color: #ffd700;">Panel Konfigurasi</strong> di sebelah kiri, 
            kemudian klik tombol <strong style="color: #00d26a;">JALANKAN SIMULASI</strong> untuk melihat hasil analisis.
        </p>
        <div style="margin-top: 2rem; padding: 1.5rem; background: rgba(255, 215, 0, 0.1); border-radius: 12px; border: 1px solid rgba(255, 215, 0, 0.3);">
            <h4 style="color: #ffd700; margin-bottom: 0.75rem;">💡 Tips:</h4>
            <ul style="color: #d0d0d0; text-align: left; list-style-type: none; padding: 0; margin: 0;">
                <li>📍 <strong>Interval Kedatangan</strong> - Semakin kecil = antrean semakin padat</li>
                <li>👥 <strong>Jumlah Staff</strong> - Tambah untuk mengurangi bottleneck</li>
                <li>⏱️ <strong>Durasi</strong> - Simulasi lebih lama = hasil lebih akurat</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align: center; padding: 2rem; margin-top: 2rem; color: #666;">
    <p>Dibuat dengan ❤️ untuk Tugas Besar Pemodelan & Simulasi</p>
    <p style="font-size: 0.8rem;">Menggunakan SimPy • Streamlit • Seaborn</p>
</div>
""", unsafe_allow_html=True)
