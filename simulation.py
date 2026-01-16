# -*- coding: utf-8 -*-
"""
Modul Backend Simulasi Drive-Thru Queue System
===============================================

Modul ini berisi logika simulasi menggunakan SimPy untuk sistem antrean Drive-Thru
dengan 3 stasiun layanan: Pesan, Bayar, dan Ambil.

Author: Simulation Dashboard
Version: 1.0.0
"""

import simpy
import random
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class KonfigurasiSimulasi:
    """Kelas untuk menyimpan konfigurasi parameter simulasi."""
    laju_kedatangan: float = 2.0  # Rata-rata menit antar kedatangan
    durasi_simulasi: int = 240    # Durasi simulasi dalam menit
    kapasitas_kasir: int = 1      # Jumlah kasir di stasiun bayar
    kapasitas_ambil: int = 1      # Jumlah staff di stasiun ambil
    waktu_layanan_pesan: float = 1.5  # Rata-rata waktu layanan pesan (menit)
    waktu_layanan_bayar: float = 1.0  # Rata-rata waktu layanan bayar (menit)
    waktu_layanan_ambil: float = 2.0  # Rata-rata waktu layanan ambil (menit)
    random_seed: Optional[int] = 42   # Seed untuk reproduksibilitas


class DriveThru:
    """
    Representasi sistem Drive-Thru dengan 3 stasiun layanan.
    
    Attributes:
        env: SimPy Environment
        stasiun_pesan: Resource untuk stasiun pemesanan
        stasiun_bayar: Resource untuk stasiun pembayaran
        stasiun_ambil: Resource untuk stasiun pengambilan
        config: Konfigurasi simulasi
    """
    
    def __init__(self, env: simpy.Environment, config: KonfigurasiSimulasi):
        """
        Inisialisasi sistem Drive-Thru.
        
        Args:
            env: SimPy Environment
            config: Konfigurasi parameter simulasi
        """
        self.env = env
        self.config = config
        
        # Definisi Resource dengan kapasitas dari konfigurasi
        self.stasiun_pesan = simpy.Resource(env, capacity=1)
        self.stasiun_bayar = simpy.Resource(env, capacity=config.kapasitas_kasir)
        self.stasiun_ambil = simpy.Resource(env, capacity=config.kapasitas_ambil)
    
    def layanan_pesan(self) -> float:
        """Generator waktu layanan stasiun pesan."""
        waktu = random.expovariate(1.0 / self.config.waktu_layanan_pesan)
        yield self.env.timeout(waktu)
        return waktu
    
    def layanan_bayar(self) -> float:
        """Generator waktu layanan stasiun bayar."""
        waktu = random.expovariate(1.0 / self.config.waktu_layanan_bayar)
        yield self.env.timeout(waktu)
        return waktu
    
    def layanan_ambil(self) -> float:
        """Generator waktu layanan stasiun ambil."""
        waktu = random.expovariate(1.0 / self.config.waktu_layanan_ambil)
        yield self.env.timeout(waktu)
        return waktu


class SimulasiDriveThru:
    """
    Kelas utama untuk menjalankan simulasi Drive-Thru.
    
    Mengumpulkan data log setiap pelanggan dan monitoring antrean.
    """
    
    def __init__(self, config: KonfigurasiSimulasi):
        """
        Inisialisasi simulasi.
        
        Args:
            config: Konfigurasi parameter simulasi
        """
        self.config = config
        self.log_data: List[Dict] = []
        self.queue_data: List[Dict] = []
        self.utilisasi_data: Dict[str, float] = {}
        
        # Set random seed jika tersedia
        if config.random_seed is not None:
            random.seed(config.random_seed)
            np.random.seed(config.random_seed)
    
    def _proses_pelanggan(
        self, 
        env: simpy.Environment, 
        nama_mobil: str, 
        drivethru: DriveThru
    ):
        """
        Proses alur pelanggan dari datang hingga selesai.
        
        Mencatat timestamp untuk setiap tahap layanan.
        """
        # 1. Datang ke sistem
        waktu_datang = env.now
        
        # 2. Proses di Stasiun Pesan
        waktu_mulai_pesan = env.now
        with drivethru.stasiun_pesan.request() as request:
            yield request
            waktu_mulai_layanan_pesan = env.now
            waktu_tunggu_pesan = waktu_mulai_layanan_pesan - waktu_mulai_pesan
            yield env.process(drivethru.layanan_pesan())
            waktu_selesai_pesan = env.now
        
        # 3. Proses di Stasiun Bayar
        waktu_mulai_bayar = env.now
        with drivethru.stasiun_bayar.request() as request:
            yield request
            waktu_mulai_layanan_bayar = env.now
            waktu_tunggu_bayar = waktu_mulai_layanan_bayar - waktu_mulai_bayar
            yield env.process(drivethru.layanan_bayar())
            waktu_selesai_bayar = env.now
        
        # 4. Proses di Stasiun Ambil
        waktu_mulai_ambil = env.now
        with drivethru.stasiun_ambil.request() as request:
            yield request
            waktu_mulai_layanan_ambil = env.now
            waktu_tunggu_ambil = waktu_mulai_layanan_ambil - waktu_mulai_ambil
            yield env.process(drivethru.layanan_ambil())
            waktu_selesai = env.now
        
        # 5. Hitung total waktu
        total_waktu = waktu_selesai - waktu_datang
        total_tunggu = waktu_tunggu_pesan + waktu_tunggu_bayar + waktu_tunggu_ambil
        total_layanan = total_waktu - total_tunggu
        
        # 6. Simpan data log
        self.log_data.append({
            'ID_Mobil': nama_mobil,
            'Waktu_Datang': round(waktu_datang, 2),
            'Waktu_Selesai': round(waktu_selesai, 2),
            'Waktu_Tunggu_Pesan': round(waktu_tunggu_pesan, 2),
            'Waktu_Tunggu_Bayar': round(waktu_tunggu_bayar, 2),
            'Waktu_Tunggu_Ambil': round(waktu_tunggu_ambil, 2),
            'Total_Waktu_Tunggu': round(total_tunggu, 2),
            'Total_Waktu_Layanan': round(total_layanan, 2),
            'Total_Waktu_Sistem': round(total_waktu, 2)
        })
    
    def _generator_pelanggan(
        self, 
        env: simpy.Environment, 
        drivethru: DriveThru
    ):
        """Generator pelanggan berdasarkan distribusi eksponensial."""
        id_mobil = 0
        while True:
            # Waktu antar kedatangan mengikuti distribusi eksponensial
            yield env.timeout(random.expovariate(1.0 / self.config.laju_kedatangan))
            id_mobil += 1
            env.process(
                self._proses_pelanggan(env, f'Mobil_{id_mobil:03d}', drivethru)
            )
    
    def _monitor_antrean(
        self, 
        env: simpy.Environment, 
        drivethru: DriveThru
    ):
        """Monitor panjang antrean setiap menit."""
        while True:
            self.queue_data.append({
                'Waktu': round(env.now, 2),
                'Antrean_Pesan': len(drivethru.stasiun_pesan.queue),
                'Antrean_Bayar': len(drivethru.stasiun_bayar.queue),
                'Antrean_Ambil': len(drivethru.stasiun_ambil.queue),
                'Total_Antrean': (
                    len(drivethru.stasiun_pesan.queue) +
                    len(drivethru.stasiun_bayar.queue) +
                    len(drivethru.stasiun_ambil.queue)
                )
            })
            yield env.timeout(1)  # Cek setiap 1 menit
    
    def jalankan(self) -> pd.DataFrame:
        """
        Menjalankan simulasi dan mengembalikan hasil.
        
        Returns:
            DataFrame berisi log setiap pelanggan
        """
        # Reset data
        self.log_data = []
        self.queue_data = []
        
        # Setup environment
        env = simpy.Environment()
        drivethru = DriveThru(env, self.config)
        
        # Aktifkan proses
        env.process(self._generator_pelanggan(env, drivethru))
        env.process(self._monitor_antrean(env, drivethru))
        
        # Jalankan simulasi
        env.run(until=self.config.durasi_simulasi)
        
        # Hitung utilisasi
        self._hitung_utilisasi()
        
        return pd.DataFrame(self.log_data)
    
    def _hitung_utilisasi(self):
        """Menghitung persentase utilisasi setiap stasiun."""
        if not self.log_data:
            self.utilisasi_data = {
                'Pesan': 0.0,
                'Bayar': 0.0,
                'Ambil': 0.0
            }
            return
        
        jumlah_mobil = len(self.log_data)
        waktu_simulasi = self.config.durasi_simulasi
        
        # Estimasi waktu sibuk berdasarkan rata-rata layanan
        busy_pesan = jumlah_mobil * self.config.waktu_layanan_pesan
        busy_bayar = jumlah_mobil * self.config.waktu_layanan_bayar
        busy_ambil = jumlah_mobil * self.config.waktu_layanan_ambil
        
        # Hitung persentase utilisasi (mempertimbangkan kapasitas)
        util_pesan = min((busy_pesan / (waktu_simulasi * 1)) * 100, 100)
        util_bayar = min((busy_bayar / (waktu_simulasi * self.config.kapasitas_kasir)) * 100, 100)
        util_ambil = min((busy_ambil / (waktu_simulasi * self.config.kapasitas_ambil)) * 100, 100)
        
        self.utilisasi_data = {
            'Pesan': round(util_pesan, 2),
            'Bayar': round(util_bayar, 2),
            'Ambil': round(util_ambil, 2)
        }
    
    def get_dataframe_antrean(self) -> pd.DataFrame:
        """Mendapatkan DataFrame panjang antrean."""
        return pd.DataFrame(self.queue_data)
    
    def get_utilisasi(self) -> Dict[str, float]:
        """Mendapatkan data utilisasi setiap stasiun."""
        return self.utilisasi_data


def jalankan_simulasi(
    laju_kedatangan: float = 2.0,
    durasi_simulasi: int = 240,
    jumlah_kasir: int = 1,
    jumlah_staff_ambil: int = 1,
    random_seed: Optional[int] = 42
) -> Tuple[pd.DataFrame, pd.DataFrame, Dict[str, float], Dict[str, float]]:
    """
    Fungsi utama untuk menjalankan simulasi Drive-Thru.
    
    Args:
        laju_kedatangan: Rata-rata menit antar kedatangan pelanggan
        durasi_simulasi: Durasi simulasi dalam menit
        jumlah_kasir: Jumlah kasir di stasiun pembayaran
        jumlah_staff_ambil: Jumlah staff di stasiun pengambilan
        random_seed: Seed untuk reproduksibilitas hasil
    
    Returns:
        Tuple berisi:
        - DataFrame log pelanggan
        - DataFrame monitoring antrean
        - Dictionary utilisasi setiap stasiun
        - Dictionary statistik KPI
    """
    # Buat konfigurasi
    config = KonfigurasiSimulasi(
        laju_kedatangan=laju_kedatangan,
        durasi_simulasi=durasi_simulasi,
        kapasitas_kasir=jumlah_kasir,
        kapasitas_ambil=jumlah_staff_ambil,
        random_seed=random_seed
    )
    
    # Jalankan simulasi
    simulasi = SimulasiDriveThru(config)
    df_log = simulasi.jalankan()
    df_antrean = simulasi.get_dataframe_antrean()
    utilisasi = simulasi.get_utilisasi()
    
    # Hitung statistik KPI
    statistik = hitung_statistik(df_log, durasi_simulasi)
    
    return df_log, df_antrean, utilisasi, statistik


def hitung_statistik(df: pd.DataFrame, durasi_simulasi: int) -> Dict[str, float]:
    """
    Menghitung statistik KPI dari hasil simulasi.
    
    Args:
        df: DataFrame hasil simulasi
        durasi_simulasi: Durasi simulasi dalam menit
    
    Returns:
        Dictionary berisi statistik KPI
    """
    if df.empty:
        return {
            'total_mobil': 0,
            'rata_waktu_tunggu': 0.0,
            'max_waktu_tunggu': 0.0,
            'min_waktu_tunggu': 0.0,
            'rata_waktu_sistem': 0.0,
            'throughput': 0.0,
            'std_waktu_tunggu': 0.0
        }
    
    return {
        'total_mobil': len(df),
        'rata_waktu_tunggu': round(df['Total_Waktu_Tunggu'].mean(), 2),
        'max_waktu_tunggu': round(df['Total_Waktu_Tunggu'].max(), 2),
        'min_waktu_tunggu': round(df['Total_Waktu_Tunggu'].min(), 2),
        'rata_waktu_sistem': round(df['Total_Waktu_Sistem'].mean(), 2),
        'throughput': round(len(df) / (durasi_simulasi / 60), 2),  # Mobil per jam
        'std_waktu_tunggu': round(df['Total_Waktu_Tunggu'].std(), 2)
    }


def identifikasi_bottleneck(utilisasi: Dict[str, float]) -> Tuple[str, str]:
    """
    Mengidentifikasi bottleneck dari data utilisasi.
    
    Args:
        utilisasi: Dictionary utilisasi setiap stasiun
    
    Returns:
        Tuple (nama_stasiun_bottleneck, status_sistem)
    """
    if not utilisasi:
        return "Tidak Diketahui", "Data Tidak Tersedia"
    
    # Cari stasiun dengan utilisasi tertinggi
    bottleneck = max(utilisasi, key=utilisasi.get)
    nilai_tertinggi = utilisasi[bottleneck]
    
    # Tentukan status sistem
    if nilai_tertinggi >= 95:
        status = "KRITIS - Overload"
    elif nilai_tertinggi >= 85:
        status = "PERINGATAN - Hampir Penuh"
    elif nilai_tertinggi >= 70:
        status = "SIBUK - Perlu Perhatian"
    else:
        status = "STABIL - Berjalan Baik"
    
    return bottleneck, status


def generate_insight(
    statistik: Dict[str, float], 
    utilisasi: Dict[str, float],
    jumlah_kasir: int,
    jumlah_staff_ambil: int
) -> str:
    """
    Menghasilkan insight otomatis berdasarkan hasil simulasi.
    
    Args:
        statistik: Dictionary statistik KPI
        utilisasi: Dictionary utilisasi
        jumlah_kasir: Jumlah kasir
        jumlah_staff_ambil: Jumlah staff ambil
    
    Returns:
        String insight dalam Bahasa Indonesia
    """
    if not statistik or statistik['total_mobil'] == 0:
        return "⚠️ Tidak ada data untuk dianalisis. Jalankan simulasi terlebih dahulu."
    
    bottleneck, status = identifikasi_bottleneck(utilisasi)
    rata_tunggu = statistik['rata_waktu_tunggu']
    throughput = statistik['throughput']
    
    # Build insight
    insight_parts = []
    
    # Status sistem
    if "KRITIS" in status:
        insight_parts.append(
            f"🔴 **Status Sistem: {status}**\n\n"
            f"Dengan {jumlah_kasir} kasir dan {jumlah_staff_ambil} staff pengambilan, "
            f"sistem mengalami kemacetan serius."
        )
    elif "PERINGATAN" in status:
        insight_parts.append(
            f"🟠 **Status Sistem: {status}**\n\n"
            f"Sistem bekerja mendekati kapasitas maksimum. "
            f"Pertimbangkan untuk menambah resource."
        )
    else:
        insight_parts.append(
            f"🟢 **Status Sistem: {status}**\n\n"
            f"Sistem berjalan dengan baik dengan konfigurasi saat ini."
        )
    
    # Bottleneck analysis
    insight_parts.append(
        f"\n\n📍 **Bottleneck Utama:** Stasiun **{bottleneck}** "
        f"(Utilisasi: {utilisasi.get(bottleneck, 0):.1f}%)"
    )
    
    # Wait time analysis
    if rata_tunggu > 10:
        insight_parts.append(
            f"\n\n⏱️ **Waktu Tunggu:** Rata-rata {rata_tunggu:.1f} menit - "
            f"**TERLALU LAMA!** Pelanggan mungkin akan meninggalkan antrean."
        )
    elif rata_tunggu > 5:
        insight_parts.append(
            f"\n\n⏱️ **Waktu Tunggu:** Rata-rata {rata_tunggu:.1f} menit - "
            f"Perlu perbaikan untuk kepuasan pelanggan."
        )
    else:
        insight_parts.append(
            f"\n\n⏱️ **Waktu Tunggu:** Rata-rata {rata_tunggu:.1f} menit - "
            f"Sangat baik! Pelanggan tidak lama menunggu."
        )
    
    # Throughput analysis
    insight_parts.append(
        f"\n\n📊 **Throughput:** {throughput:.0f} mobil/jam terlayani dengan baik."
    )
    
    # Recommendations
    rekomendasi = []
    if utilisasi.get('Bayar', 0) > 85 and jumlah_kasir < 3:
        rekomendasi.append("• Tambah 1 kasir untuk mengurangi kemacetan di pembayaran")
    if utilisasi.get('Ambil', 0) > 85 and jumlah_staff_ambil < 3:
        rekomendasi.append("• Tambah 1 staff pengambilan untuk mempercepat layanan")
    if utilisasi.get('Pesan', 0) > 90:
        rekomendasi.append("• Pertimbangkan sistem pre-order via aplikasi")
    
    if rekomendasi:
        insight_parts.append("\n\n💡 **Rekomendasi:**\n" + "\n".join(rekomendasi))
    
    return "".join(insight_parts)


if __name__ == "__main__":
    # Test simulasi
    print("Menjalankan test simulasi...")
    df, df_q, util, stats = jalankan_simulasi(
        laju_kedatangan=2.0,
        durasi_simulasi=240,
        jumlah_kasir=1,
        jumlah_staff_ambil=1
    )
    
    print(f"\nHasil Simulasi:")
    print(f"- Total mobil terlayani: {stats['total_mobil']}")
    print(f"- Rata-rata waktu tunggu: {stats['rata_waktu_tunggu']:.2f} menit")
    print(f"- Throughput: {stats['throughput']:.2f} mobil/jam")
    print(f"\nUtilisasi:")
    for stasiun, nilai in util.items():
        print(f"- {stasiun}: {nilai:.2f}%")
    
    bottleneck, status = identifikasi_bottleneck(util)
    print(f"\nBottleneck: {bottleneck} ({status})")