"""
File: main.py
Deskripsi: Titik masuk utama (entry point) aplikasi Daily Expense Tracker berbasis antarmuka CLI.
Menghubungkan seluruh modul (validation, fileio, processing, report) untuk menyajikan
alur kerja interaktif yang ramah bagi mahasiswa pemula.
"""

import sys
import os
from datetime import datetime

from expense_tracker.processing import ManajerData, AnalisisData
from expense_tracker.validation import cek_tanggal, cek_nominal, cek_kategori, cek_keterangan
from expense_tracker.report import format_rupiah, ekspor_laporan


DEFAULT_DATA_FILE = "data/expenses.csv"
DEFAULT_REPORT_FILE = "data/laporan_pengeluaran.txt"


def clear_screen():
    """Membersihkan tampilan terminal sederhana."""
    # Memberi jarak baris kosong agar tampilan CLI tetap rapi dan nyaman dibaca
    print("\n" + "=" * 60 + "\n")


def cetak_judul():
    """Mencetak banner judul aplikasi."""
    print("=" * 60)
    print("       DAILY EXPENSE TRACKER - PENCATAT PENGELUARAN HARIAN")
    print("              Praktikum Pemrograman Terstruktur")
    print("=" * 60)


def cetak_menu():
    """Menampilkan pilihan menu utama kepada pengguna."""
    print("\n[MENU UTAMA]")
    print("1. Tambah Pengeluaran")
    print("2. Lihat Semua Pengeluaran")
    print("3. Cari Berdasarkan Kategori atau Tanggal")
    print("4. Tampilkan Ringkasan Pengeluaran")
    print("5. Urutkan Pengeluaran Berdasarkan Nominal")
    print("6. Buat Laporan ke File Teks")
    print("7. Keluar")
    print("-" * 60)


def menu_tambah(manager):
    """
    Menangani alur penambahan transaksi pengeluaran baru.
    Menerapkan validasi input dengan blok try/except dan pemanggilan keyword arguments.
    """
    print("\n--- Tambah Pengeluaran Baru ---")
    today_str = datetime.now().strftime("%Y-%m-%d")
    # Input tanggal
    tanggal_input = input(f"Masukkan tanggal (YYYY-MM-DD) [Tekan Enter untuk {today_str}]: ").strip()
    if not tanggal_input:
        tanggal_input = today_str
    try:
        tanggal_valid = cek_tanggal(date_string=tanggal_input)
    except ValueError as err:
        print(f"[Error Validasi] {err}")
        return

    # Input kategori
    kategori_input = input("Masukkan kategori (contoh: Makanan, Transport, Kuliah, Hiburan): ").strip()
    try:
        kategori_valid = cek_kategori(category_string=kategori_input)
    except ValueError as err:
        print(f"[Error Validasi] {err}")
        return

    # Input nominal
    nominal_input = input("Masukkan nominal pengeluaran (contoh: 25000): ").strip()
    try:
        nominal_valid = cek_nominal(amount_input=nominal_input)
    except ValueError as err:
        print(f"[Error Validasi] {err}")
        return

    keterangan_input = input("Masukkan keterangan (opsional, tekan Enter untuk default '-'): ").strip()
    keterangan_valid = cek_keterangan(description_string=keterangan_input)

    record = manager.tambah_data(
        tanggal=tanggal_valid,
        kategori=kategori_valid,
        nominal=nominal_valid,
        keterangan=keterangan_valid,
    )

    print("\n[Berhasil] Transaksi baru berhasil dicatat dan disimpan ke file CSV!")
    print(f"-> Tanggal    : {record['tanggal']}")
    print(f"-> Kategori   : {record['kategori']}")
    print(f"-> Nominal    : {format_rupiah(record['nominal'])}")
    print(f"-> Keterangan : {record['keterangan']}")


def cetak_tabel(expenses, title="Daftar Pengeluaran"):
    """
    Menampilkan daftar transaksi dalam format tabel teks yang rapi.
    """
    print(f"\n--- {title} ---")
    if not expenses:
        print("Belum ada data transaksi yang dapat ditampilkan.")
        return

    garis = "-" * 75
    print(garis)
    print(f"{'No':<4} {'Tanggal':<12} {'Kategori':<16} {'Nominal':<18} {'Keterangan'}")
    print(garis)

    for i, exp in enumerate(expenses, start=1):
        print(f"{i:<4} {exp['tanggal']:<12} {exp['kategori']:<16} {format_rupiah(exp['nominal']):<18} {exp['keterangan']}")

    print(garis)
    print(f"Total baris: {len(expenses)} transaksi")


def menu_lihat(manager):
    """Menampilkan seluruh catatan pengeluaran."""
    expenses = manager.ambil_semua()
    cetak_tabel(expenses=expenses, title="Semua Pengeluaran")


def menu_cari(manager):
    """Menangani pencarian data berdasarkan kategori atau tanggal."""
    print("\n--- Cari Pengeluaran ---")
    print("1. Cari berdasarkan Kategori")
    print("2. Cari berdasarkan Tanggal")
    print("3. Cari berdasarkan Kategori dan Tanggal")
    pilihan = input("Pilih metode pencarian (1-3): ").strip()

    kategori_cari = None
    tanggal_cari = None

    if pilihan == "1":
        kategori_cari = input("Masukkan kata kunci kategori: ").strip()
    elif pilihan == "2":
        tanggal_input = input("Masukkan tanggal (YYYY-MM-DD): ").strip()
        try:
            tanggal_cari = cek_tanggal(date_string=tanggal_input)
        except ValueError as err:
            print(f"[Error Validasi] {err}")
            return
    elif pilihan == "3":
        kategori_cari = input("Masukkan kata kunci kategori: ").strip()
        tanggal_input = input("Masukkan tanggal (YYYY-MM-DD): ").strip()
        try:
            tanggal_cari = cek_tanggal(date_string=tanggal_input)
        except ValueError as err:
            print(f"[Error Validasi] {err}")
            return
    else:
        print("[Peringatan] Pilihan tidak valid.")
        return

    # Pemanggilan fungsi saring_data dengan keyword arguments
    hasil = manager.saring_data(kategori=kategori_cari, tanggal=tanggal_cari)
    cetak_tabel(expenses=hasil, title="Hasil Pencarian Pengeluaran")


def menu_ringkasan(manager):
    """Menampilkan analisis statistik pengeluaran menggunakan AnalisisData."""
    expenses = manager.ambil_semua()
    if not expenses:
        print("\n[Info] Data masih kosong. Tambahkan transaksi terlebih dahulu untuk melihat ringkasan.")
        return

    analyzer = AnalisisData(expenses=expenses)
    summary = analyzer.rangkuman()

    print("\n" + "=" * 55)
    print("             RINGKASAN DAN ANALISIS PENGELUARAN")
    print("=" * 55)
    print(f"Jumlah Total Transaksi   : {summary['jumlah_transaksi']}")
    print(f"Total Nominal Pengeluaran : {format_rupiah(summary['total_pengeluaran'])}")
    print(f"Rata-rata per Transaksi  : {format_rupiah(summary['rata_rata'])}")
    print("-" * 55)
    print("Rincian Pengeluaran per Kategori:")
    for kat, total_kat in summary["per_kategori"].items():
        persen = (total_kat / summary["total_pengeluaran"]) * 100 if summary["total_pengeluaran"] > 0 else 0
        print(f"  * {kat:<18} : {format_rupiah(total_kat):>16} ({persen:.1f}%)")
    print("-" * 55)
    if summary["terendah"]:
        t_min = summary["terendah"]
        print(f"Transaksi Terendah       : {format_rupiah(t_min['nominal'])} ({t_min['kategori']} - {t_min['tanggal']})")
    if summary["tertinggi"]:
        t_max = summary["tertinggi"]
        print(f"Transaksi Tertinggi      : {format_rupiah(t_max['nominal'])} ({t_max['kategori']} - {t_max['tanggal']})")
    print("=" * 55)


def menu_urutkan(manager):
    """Mengurutkan pengeluaran berdasarkan nominal (lambda pada sorted)."""
    print("\n--- Urutkan Pengeluaran Berdasarkan Nominal ---")
    print("1. Nominal Terbesar ke Terkecil (Descending)")
    print("2. Nominal Terkecil ke Terbesar (Ascending)")
    pilihan = input("Pilihan Anda (1-2) [Default 1]: ").strip()

    desc = True
    if pilihan == "2":
        desc = False

    # Mengurutkan menggunakan metode yang mengimplementasikan ekspresi lambda
    sorted_expenses = manager.urutkan(descending=desc)
    tipe_urut = "Terbesar ke Terkecil" if desc else "Terkecil ke Terbesar"
    cetak_tabel(expenses=sorted_expenses, title=f"Pengeluaran Diurutkan ({tipe_urut})")


def menu_laporan(manager):
    """Mengekspor laporan teks komprehensif ke file teks."""
    expenses = manager.ambil_semua()
    if not expenses:
        print("\n[Peringatan] Belum ada data transaksi untuk dibuatkan laporan.")
        return

    analyzer = AnalisisData(expenses=expenses)
    summary = analyzer.rangkuman()

    custom_path = input(f"Masukkan jalur file laporan [Tekan Enter untuk '{DEFAULT_REPORT_FILE}']: ").strip()
    target_path = custom_path if custom_path else DEFAULT_REPORT_FILE

    try:
        ekspor_laporan(filepath=target_path, summary=summary, expenses=expenses)
        print(f"\n[Berhasil] Laporan pengeluaran berhasil disimpan ke: '{os.path.abspath(target_path)}'")
    except Exception as err:
        print(f"[Error] Gagal menyimpan laporan: {err}")


def main():
    """Fungsi utama untuk menjalankan antarmuka CLI aplikasi."""
    cetak_judul()

    # Inisialisasi manajer data pengeluaran
    manager = ManajerData(filepath=DEFAULT_DATA_FILE)
    print(f"[Inisialisasi] Penyimpanan data terhubung: '{DEFAULT_DATA_FILE}'")

    while True:
        cetak_menu()
        pilihan = input("Pilih menu (1-7): ").strip()

        try:
            if pilihan == "1":
                menu_tambah(manager=manager)
            elif pilihan == "2":
                menu_lihat(manager=manager)
            elif pilihan == "3":
                menu_cari(manager=manager)
            elif pilihan == "4":
                menu_ringkasan(manager=manager)
            elif pilihan == "5":
                menu_urutkan(manager=manager)
            elif pilihan == "6":
                menu_laporan(manager=manager)
            elif pilihan == "7":
                print("\nTerima kasih telah menggunakan Daily Expense Tracker. Sampai jumpa kembali!")
                break
            else:
                print("\n[Peringatan] Pilihan tidak valid. Silakan pilih menu antara 1 sampai 7.")
        except KeyboardInterrupt:
            print("\n\n[Info] Program dihentikan oleh pengguna. Sampai jumpa!")
            break
        except Exception as error:
            print(f"\n[Terjadi Kesalahan Tak Terduga]: {error}")


if __name__ == "__main__":
    main()