"""
Modul: validation.py
Deskripsi: Menyediakan fungsi-fungsi untuk validasi data input pengguna maupun data transaksi.
Memenuhi ketentuan: Menggunakan pernyataan `raise` untuk memvalidasi data dan memastikan keabsahan tipe & nilai.
"""

from datetime import datetime


class ExpenseValidationError(ValueError):
    """
    Exception buatan sendiri untuk menangani error validasi data pengeluaran.
    """
    pass


def cek_tanggal(date_string):
    """
    Memvalidasi format tanggal harus YYYY-MM-DD.
    """
    if not isinstance(date_string, str):
        raise ExpenseValidationError("Tanggal harus berupa teks.")
        
    clean_date = date_string.strip()
    if not clean_date:
        raise ExpenseValidationError("Tanggal tidak boleh kosong.")

    try:
        datetime.strptime(clean_date, "%Y-%m-%d")
    except ValueError:
        raise ExpenseValidationError("Format tanggal harus YYYY-MM-DD (contoh: 2026-10-09).")

    return clean_date


def cek_nominal(amount_input):
    """
    Memvalidasi nominal harus angka positif (>0).
    """
    try:
        amount = float(amount_input)
    except (TypeError, ValueError):
        raise ExpenseValidationError(f"Nominal '{amount_input}' bukan angka yang valid.")

    if amount <= 0:
        raise ExpenseValidationError("Nominal pengeluaran harus lebih besar dari 0.")

    return round(amount, 2)


def cek_kategori(category_string):
    """
    Memvalidasi kategori agar tidak kosong.
    """
    if not isinstance(category_string, str):
        raise ExpenseValidationError("Kategori harus berupa teks.")
        
    clean_category = category_string.strip()
    if not clean_category:
        raise ExpenseValidationError("Kategori pengeluaran tidak boleh kosong.")

    return clean_category.title()


def cek_keterangan(description_string):
    """
    Memvalidasi keterangan. Jika kosong diberi nilai default '-'.
    """
    if description_string is None:
        return "-"
        
    clean_desc = str(description_string).strip()
    return clean_desc if clean_desc else "-"
