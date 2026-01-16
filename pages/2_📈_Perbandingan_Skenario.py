# -*- coding: utf-8 -*-
"""
📈 Halaman Perbandingan Skenario
================================

Halaman untuk membandingkan beberapa skenario simulasi (What-If Analysis).
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
    page_title="Perbandingan Skenario - Drive-Thru Simulator",
    page_icon="📈",
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
    
    .scenario-card {
        background: linear-gradient(145deg, #1e1e2f 0%, #252540 100%);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .scenario-card h4 {
        color: #ffd700;
        font-size: 1.1rem;
        font-weight: 600;
        margin: 0 0 0.75rem 0;
    }
    
    .scenario-card p {
        color: #d0d0d0;
        margin: 0.25rem 0;
    }
    
    .vs-badge {
        background: linear-gradient(135deg, #ffd700 0%, #ffaa00 100%);
        color: #1a1a2e;
        font-weight: 800;
        padding: 0.75rem 1.25rem;
        border-radius: 50%;
        display: inline-block;
        font-size: 1.2rem;
    }
    
    .golden-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent 0%, #ffd700 50%, transparent 100%);
        margin: 2rem 0;
        border: none;
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
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>📈 Perbandingan Skenario What-If</h1>
    <p>Bandingkan dampak perubahan konfigurasi terhadap performa sistem</p>
</div>
""", unsafe_allow_html=True)

# Sidebar Configuration
with st.sidebar:
    st.markdown("# ⚙️ Konfigurasi Skenario")
    
    st.markdown("### 📍 Parameter Tetap")
    
    laju_kedatangan = st.slider(
        "Interval Kedatangan (menit)",
        min_value=0.5,
        max_value=5.0,
        value=2.0,
        step=0.1,
        help="Rata-rata waktu antar kedatangan mobil"
    )
    
    durasi = st.slider(
        "Durasi Simulasi (menit)",
        min_value=60,
        max_value=480,
        value=240,
        step=30,
        help="Berapa lama simulasi akan berjalan"
    )
    
    st.markdown("---")
    st.markdown("### 🅰️ Skenario A (Baseline)")
    
    kasir_a = st.number_input("Jumlah Kasir A", min_value=1, max_value=5, value=1)
    staff_a = st.number_input("Jumlah Staff Ambil A", min_value=1, max_value=5, value=1)
    
    st.markdown("---")
    st.markdown("### 🅱️ Skenario B (Optimasi)")
    
    kasir_b = st.number_input("Jumlah Kasir B", min_value=1, max_value=5, value=2)
    staff_b = st.number_input("Jumlah Staff Ambil B", min_value=1, max_value=5, value=2)
    
    st.markdown("---")
    
    run_comparison = st.button(
        "🔄 JALANKAN PERBANDINGAN",
        use_container_width=True,
        type="primary"
    )

# Main Content
if run_comparison:
    with st.spinner("🔄 Menjalankan simulasi Skenario A & B..."):
        # Run both scenarios
        df_a, df_q_a, util_a, stats_a = jalankan_simulasi(
            laju_kedatangan=laju_kedatangan,
            durasi_simulasi=durasi,
            jumlah_kasir=kasir_a,
            jumlah_staff_ambil=staff_a,
            random_seed=42
        )
        
        df_b, df_q_b, util_b, stats_b = jalankan_simulasi(
            laju_kedatangan=laju_kedatangan,
            durasi_simulasi=durasi,
            jumlah_kasir=kasir_b,
            jumlah_staff_ambil=staff_b,
            random_seed=42
        )
        
        st.session_state.comparison_run = True
        st.session_state.scenario_a = {'df': df_a, 'util': util_a, 'stats': stats_a, 'kasir': kasir_a, 'staff': staff_a}
        st.session_state.scenario_b = {'df': df_b, 'util': util_b, 'stats': stats_b, 'kasir': kasir_b, 'staff': staff_b}

if 'comparison_run' in st.session_state and st.session_state.comparison_run:
    scen_a = st.session_state.scenario_a
    scen_b = st.session_state.scenario_b
    
    st.markdown('<div class="golden-divider"></div>', unsafe_allow_html=True)
    
    # Scenario Cards
    col1, col2, col3 = st.columns([2, 1, 2])
    
    with col1:
        st.markdown(f"""
        <div class="scenario-card">
            <h4>🅰️ Skenario A (Baseline)</h4>
            <p><strong>Kasir:</strong> {scen_a['kasir']} | <strong>Staff Ambil:</strong> {scen_a['staff']}</p>
            <p><strong>Total Mobil:</strong> {scen_a['stats']['total_mobil']}</p>
            <p><strong>Avg. Tunggu:</strong> {scen_a['stats']['rata_waktu_tunggu']:.1f} menit</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 2rem;">
            <span class="vs-badge">VS</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="scenario-card">
            <h4>🅱️ Skenario B (Optimasi)</h4>
            <p><strong>Kasir:</strong> {scen_b['kasir']} | <strong>Staff Ambil:</strong> {scen_b['staff']}</p>
            <p><strong>Total Mobil:</strong> {scen_b['stats']['total_mobil']}</p>
            <p><strong>Avg. Tunggu:</strong> {scen_b['stats']['rata_waktu_tunggu']:.1f} menit</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Improvement Metrics
    wait_improvement = ((scen_a['stats']['rata_waktu_tunggu'] - scen_b['stats']['rata_waktu_tunggu']) 
                       / scen_a['stats']['rata_waktu_tunggu'] * 100) if scen_a['stats']['rata_waktu_tunggu'] > 0 else 0
    
    st.markdown("""
    <div class="section-header">
        <h2>📊 Perbandingan Metrik</h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        delta_wait = scen_b['stats']['rata_waktu_tunggu'] - scen_a['stats']['rata_waktu_tunggu']
        st.metric("⏱️ Waktu Tunggu", f"{scen_b['stats']['rata_waktu_tunggu']:.1f} min", 
                 f"{delta_wait:+.1f} menit", delta_color="inverse")
    
    with col2:
        delta_throughput = scen_b['stats']['throughput'] - scen_a['stats']['throughput']
        st.metric("📈 Throughput", f"{scen_b['stats']['throughput']:.0f}/jam", 
                 f"{delta_throughput:+.0f} mobil")
    
    with col3:
        max_util_b = max(scen_b['util'].values()) if scen_b['util'] else 0
        max_util_a = max(scen_a['util'].values()) if scen_a['util'] else 0
        st.metric("🎯 Max Utilisasi", f"{max_util_b:.1f}%", 
                 f"{max_util_b - max_util_a:+.1f}%", delta_color="inverse")
    
    with col4:
        extra_staff = (scen_b['kasir'] - scen_a['kasir']) + (scen_b['staff'] - scen_a['staff'])
        st.metric("👥 Tambahan Resource", f"+{extra_staff} staff", 
                 f"Hemat {abs(wait_improvement):.0f}%" if wait_improvement > 0 else "")
    
    # Improvement Summary
    if wait_improvement > 10:
        st.success(f"✅ **Skenario B menghemat {wait_improvement:.1f}% waktu tunggu!** Penambahan resource sangat efektif.")
    elif wait_improvement > 0:
        st.info(f"ℹ️ **Skenario B menghemat {wait_improvement:.1f}% waktu tunggu.** Peningkatan moderat.")
    else:
        st.warning(f"⚠️ **Penambahan resource tidak efektif** ({wait_improvement:.1f}%). Bottleneck mungkin di stasiun lain.")
    
    st.markdown('<div class="golden-divider"></div>', unsafe_allow_html=True)
    
    # Boxplot Comparison
    st.markdown("""
    <div class="section-header">
        <h2>📦 Perbandingan Distribusi</h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig, ax = plt.subplots(figsize=(10, 6))
        plt.style.use('dark_background')
        fig.patch.set_facecolor('#1a1a2e')
        ax.set_facecolor('#1a1a2e')
        
        bp = ax.boxplot(
            [scen_a['df']['Total_Waktu_Tunggu'], scen_b['df']['Total_Waktu_Tunggu']],
            labels=[f"Skenario A\n({scen_a['kasir']}K, {scen_a['staff']}S)", 
                   f"Skenario B\n({scen_b['kasir']}K, {scen_b['staff']}S)"],
            patch_artist=True
        )
        
        colors = ['#00d2ff', '#ffd700']
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
        
        ax.set_ylabel('Total Waktu Tunggu (Menit)', fontsize=12, color='white')
        ax.set_title('Perbandingan Distribusi Waktu Tunggu', fontsize=14, color='#ffd700', fontweight='bold')
        ax.tick_params(colors='white')
        ax.grid(True, alpha=0.2, axis='y')
        sns.despine(ax=ax, top=True, right=True)
        ax.spines['bottom'].set_color('#666')
        ax.spines['left'].set_color('#666')
        
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)
    
    with col2:
        st.markdown("#### 📊 Statistik Ringkas")
        
        comparison_data = pd.DataFrame({
            'Metrik': ['Median', 'Mean', 'Max', 'Std Dev'],
            'Skenario A': [
                f"{scen_a['df']['Total_Waktu_Tunggu'].median():.2f}",
                f"{scen_a['df']['Total_Waktu_Tunggu'].mean():.2f}",
                f"{scen_a['df']['Total_Waktu_Tunggu'].max():.2f}",
                f"{scen_a['df']['Total_Waktu_Tunggu'].std():.2f}"
            ],
            'Skenario B': [
                f"{scen_b['df']['Total_Waktu_Tunggu'].median():.2f}",
                f"{scen_b['df']['Total_Waktu_Tunggu'].mean():.2f}",
                f"{scen_b['df']['Total_Waktu_Tunggu'].max():.2f}",
                f"{scen_b['df']['Total_Waktu_Tunggu'].std():.2f}"
            ]
        })
        
        st.dataframe(comparison_data, use_container_width=True, hide_index=True)
    
    # Recommendation
    st.markdown('<div class="golden-divider"></div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="section-header">
        <h2>💡 Rekomendasi</h2>
    </div>
    """, unsafe_allow_html=True)
    
    if wait_improvement > 15:
        st.success(f"""
        ### ✅ Implementasikan Skenario B
        
        Dengan menambah resource, Anda dapat mengurangi waktu tunggu sebesar **{wait_improvement:.1f}%**.
        ROI positif jika biaya staff sebanding dengan kepuasan pelanggan.
        """)
    elif wait_improvement > 5:
        st.info(f"""
        ### ℹ️ Pertimbangkan Skenario B
        
        Peningkatan {wait_improvement:.1f}% mungkin layak jika volume pelanggan tinggi.
        """)
    else:
        bottleneck_a, _ = identifikasi_bottleneck(scen_a['util'])
        st.warning(f"""
        ### ⚠️ Jangan Tambah Resource
        
        Penambahan staff tidak efektif. Fokus perbaiki proses di stasiun **{bottleneck_a}**.
        """)

else:
    # Initial state
    st.markdown("""
    <div style="text-align: center; padding: 3rem; background: linear-gradient(145deg, #1e1e2f 0%, #252540 100%); 
                border-radius: 20px; margin: 2rem 0; border: 1px solid rgba(212, 175, 55, 0.2);">
        <h2 style="color: #ffd700; margin-bottom: 1rem;">🎯 Siap untuk Membandingkan?</h2>
        <p style="color: #b8b8b8; font-size: 1.1rem; max-width: 600px; margin: 0 auto;">
            Konfigurasi dua skenario berbeda di <strong style="color: #ffd700;">Panel Konfigurasi</strong>, 
            kemudian klik <strong style="color: #00d26a;">JALANKAN PERBANDINGAN</strong>.
        </p>
        <div style="margin-top: 2rem; padding: 1.5rem; background: rgba(255, 215, 0, 0.1); border-radius: 12px; border: 1px solid rgba(255, 215, 0, 0.3);">
            <h4 style="color: #ffd700; margin-bottom: 0.75rem;">💡 Tips:</h4>
            <ul style="color: #d0d0d0; text-align: left; list-style-type: none; padding: 0; margin: 0;">
                <li>🅰️ <strong>Skenario A</strong> - Konfigurasi baseline (kondisi saat ini)</li>
                <li>🅱️ <strong>Skenario B</strong> - Konfigurasi yang ingin diuji</li>
                <li>📊 <strong>Perbandingan</strong> - Lihat dampak perubahan resource</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    📈 Halaman Perbandingan Skenario • Dashboard Simulasi Drive-Thru
</div>
""", unsafe_allow_html=True)
