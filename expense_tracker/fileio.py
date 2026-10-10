"""
Modul: fileio.py
Deskripsi: Mengelola seluruh operasi input/output berkas (CSV dan teks) untuk Daily Expense Tracker.
Memenuhi ketentuan:
- Menggunakan `with open()` untuk seluruh operasi berkas.
- Menggunakan mode 'x' (pembuatan awal CSV), 'a' (menambah transaksi), 'r' (membaca data baris per baris), dan 'w' (menulis laporan teks).
- Menangani `FileExistsError` secara aman saat mode 'x'.
- Menangani `FileNotFoundError` dengan pesan yang jelas saat mode 'r'.
- Menggunakan perulangan `for` untuk membaca setiap baris file.
- Menggunakan `try/except` untuk menangkap baris CSV rusak dan melewatinya (skip) tanpa menghentikan pembacaan baris valid lainnya.
"""

import os
from expense_tracker.validation import cek_tanggal, cek_nominal, cek_kategori, cek_keterangan

CSV_HEADER = "tanggal,kategori,nominal,keterangan\n"


def baca_baris(line):
    """
    Menguraikan (parsing) satu baris data CSV menjadi dictionary transaksi yang valid.
    Jika baris cacat, fungsi mengabaikannya secara aman.
    """
    clean_line = line.strip()
    if not clean_line:
        return None

    # Pisahkan kolom
    parts = clean_line.split(",", 3)
    if len(parts) != 4:
        return None

    raw_date, raw_cat, raw_amount, raw_desc = parts

    try:
        valid_date = cek_tanggal(raw_date)
        valid_cat = cek_kategori(raw_cat)
        valid_amount = cek_nominal(raw_amount)
        valid_desc = cek_keterangan(raw_desc)

        return {
            "tanggal": valid_date,
            "kategori": valid_cat,
            "nominal": valid_amount,
            "keterangan": valid_desc,
        }
    except Exception:
        # Baris data rusak dilewati (skip)
        return None


def buat_file(filepath):
    """
    Membuat file CSV baru dengan header kolom menggunakan mode 'x'.
    """
    folder = os.path.dirname(filepath)
    if folder and not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)

    try:
        with open(filepath, "x", encoding="utf-8") as f:
            f.write(CSV_HEADER)
        return True
    except FileExistsError:
        return False


def simpan_data(filepath, expense):
    """
    Menambahkan satu record pengeluaran ke dalam file CSV menggunakan mode 'a'.
    """
    if not os.path.exists(filepath):
        buat_file(filepath)

    csv_line = f"{expense['tanggal']},{expense['kategori']},{expense['nominal']},{expense['keterangan']}\n"
    
    with open(filepath, "a", encoding="utf-8") as f:
        f.write(csv_line)


def muat_data(filepath):
    """
    Membaca semua transaksi dari file CSV menggunakan mode 'r'.
    Membaca baris demi baris secara iteratif.
    """
    expenses = []

    try:
        with open(filepath, "r", encoding="utf-8") as file:
            is_header = True
            
            for line in file:
                if is_header:
                    is_header = False
                    if "tanggal,kategori,nominal" in line.lower():
                        continue

                try:
                    record = baca_baris(line)
                    if record is not None:
                        expenses.append(record)
                except Exception:
                    continue

    except FileNotFoundError:
        print(f"[Info] File data '{filepath}' belum ditemukan.")
        return []

    return expenses


def simpan_teks(filepath, content):
    """
    Menyimpan teks laporan ke dalam file teks menggunakan mode 'w'.
    """
    folder = os.path.dirname(filepath)
    if folder and not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)

    with open(filepath, "w", encoding="utf-8") as file:
        file.write(content)
