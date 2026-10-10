"""
Package: expense_tracker
Deskripsi: Paket aplikasi Daily Expense Tracker untuk pencatatan dan analisis pengeluaran harian.
Modul:
- validation: Validasi data input pengguna dan baris CSV.
- fileio: Operasi berkas CSV dan berkas teks dengan penanganan error.
- processing: Pengelolaan dan analisis data (ExpenseManager dan ExpenseAnalyzer).
- report: Pembuatan dan ekspor laporan ringkasan.
- testing: Pengujian unit otomatis (unittest).
"""

from .validation import cek_tanggal, cek_nominal, cek_kategori, ExpenseValidationError
from .fileio import buat_file, simpan_data, muat_data, simpan_teks
from .processing import ManajerData, AnalisisData, buat_record, hitung_total
from .report import format_rupiah, susun_teks, ekspor_laporan

__all__ = [
    "ExpenseValidationError",
    "cek_tanggal",
    "cek_nominal",
    "cek_kategori",
    "buat_file",
    "simpan_data",
    "muat_data",
    "simpan_teks",
    "ManajerData",
    "AnalisisData",
    "buat_record",
    "hitung_total",
    "format_rupiah",
    "susun_teks",
    "ekspor_laporan",
]
