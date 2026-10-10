"""
Modul: processing.py
Deskripsi: Berisi kelas dan fungsi pemrosesan serta analisis data pengeluaran harian.
Memenuhi ketentuan:
- Minimal dua class: `ManajerData` dan `AnalisisData`.
- Menggunakan `*args` untuk perhitungan beberapa nominal.
- Menggunakan `**kwargs` untuk pembuatan record transaksi.
- Menggunakan `lambda` pada `sorted()` untuk mengurutkan transaksi berdasarkan nominal.
- Pemanggilan fungsi menggunakan keyword arguments.
"""

import os
import sys
from expense_tracker.validation import cek_tanggal, cek_nominal, cek_kategori, cek_keterangan
from expense_tracker.fileio import buat_file, simpan_data, muat_data


def hitung_total(*amounts):
    """
    Menghitung total menggunakan *args.
    Menerima sejumlah nominal, menjumlahkannya sebagai float, lalu mengembalikan
    hasilnya dibulatkan 2 desimal.
    """
    total = 0.0
    for nilai in amounts:
        total += float(nilai)
    return round(total, 2)


def buat_record(**kwargs):
    """
    Membuat dictionary record transaksi menggunakan **kwargs.
    Alur: ambil tiap field dari kwargs (dengan nilai bawaan), validasi lewat
    modul validation, lalu kembalikan sebagai satu dictionary.
    """
    raw_date = kwargs.get("tanggal", "")
    raw_category = kwargs.get("kategori", "")
    raw_amount = kwargs.get("nominal", 0)
    raw_desc = kwargs.get("keterangan", "-")

    valid_date = cek_tanggal(raw_date)
    valid_category = cek_kategori(raw_category)
    valid_amount = cek_nominal(raw_amount)
    valid_desc = cek_keterangan(raw_desc)

    return {
        "tanggal": valid_date,
        "kategori": valid_category,
        "nominal": valid_amount,
        "keterangan": valid_desc,
    }


class ManajerData:
    """
    Kelas pengelola daftar pengeluaran.
    Bertugas memuat, menambah, menyaring, dan mengurutkan data transaksi.
    """

    def __init__(self, filepath="data/expenses.csv"):
        """
        Menyimpan lokasi file, memastikan file CSV ada (mode 'x'),
        lalu memuat isi file ke memori.
        """
        self.filepath = filepath
        buat_file(self.filepath)
        self.expenses = self.muat_ulang()

    def muat_ulang(self):
        """Membaca ulang seluruh data dari file CSV ke list di memori."""
        self.expenses = muat_data(filepath=self.filepath)
        return self.expenses

    def tambah_data(self, tanggal, kategori, nominal, keterangan="-"):
        """
        Membuat record baru (tervalidasi), menambahkannya ke list di memori,
        lalu menyimpannya ke file CSV. Mengembalikan record yang dibuat.
        """
        new_record = buat_record(
            tanggal=tanggal,
            kategori=kategori,
            nominal=nominal,
            keterangan=keterangan
        )

        self.expenses.append(new_record)
        simpan_data(filepath=self.filepath, expense=new_record)

        return new_record

    def ambil_semua(self):
        """Mengembalikan salinan list seluruh transaksi agar data asli tidak terubah."""
        return list(self.expenses)

    def saring_data(self, kategori=None, tanggal=None):
        """
        Menyaring transaksi berdasarkan kategori (mengandung kata kunci,
        tidak peka huruf besar/kecil) dan/atau tanggal (harus sama persis).
        Filter yang kosong diabaikan.
        """
        hasil = []
        for item in self.expenses:
            cocok_kategori = True
            cocok_tanggal = True

            # Cek kategori hanya jika kata kunci diisi
            if kategori is not None and kategori.strip():
                cocok_kategori = kategori.strip().lower() in item["kategori"].lower()

            # Cek tanggal hanya jika tanggal diisi
            if tanggal is not None and tanggal.strip():
                cocok_tanggal = item["tanggal"] == tanggal.strip()

            # Transaksi dimasukkan jika lolos semua filter yang aktif
            if cocok_kategori and cocok_tanggal:
                hasil.append(item)

        return hasil

    def urutkan(self, descending=True):
        """
        Mengurutkan transaksi berdasarkan nominal menggunakan lambda sebagai key.
        descending=True berarti dari terbesar ke terkecil.
        """
        return sorted(self.expenses, key=lambda item: item["nominal"], reverse=descending)


class AnalisisData:
    """
    Kelas untuk analisis statistik pengeluaran.
    Menerima list transaksi lalu menghitung total, rata-rata, rincian, dan nilai ekstrem.
    """

    def __init__(self, expenses):
        """Menyimpan list transaksi yang akan dianalisis."""
        self.expenses = expenses

    def total_semua(self):
        """
        Menghitung total seluruh pengeluaran.
        List nominal dibuka dengan tanda * agar masuk ke hitung_total(*args).
        Mengembalikan 0.0 jika data kosong.
        """
        if not self.expenses:
            return 0.0

        daftar_nominal = [item["nominal"] for item in self.expenses]
        return hitung_total(*daftar_nominal)

    def rata_rata(self):
        """
        Menghitung rata-rata pengeluaran per transaksi (total dibagi jumlah transaksi).
        Mengembalikan 0.0 jika data kosong supaya tidak terjadi pembagian dengan nol.
        """
        if not self.expenses:
            return 0.0

        total_pengeluaran = self.total_semua()
        jumlah_transaksi = len(self.expenses)
        rata_rata = total_pengeluaran / jumlah_transaksi
        return round(rata_rata, 2)

    def rincian_kat(self):
        """
        Menghitung total pengeluaran untuk tiap kategori.
        Mengembalikan dictionary {kategori: total}.
        """
        breakdown = {}
        for item in self.expenses:
            kat = item["kategori"]
            # Tambahkan nominal ke total kategori (mulai dari 0.0 jika kategori baru)
            breakdown[kat] = round(breakdown.get(kat, 0.0) + item["nominal"], 2)
        return breakdown

    def cek_ekstrem(self):
        """
        Mencari transaksi dengan nominal terendah dan tertinggi.
        Memakai lambda sebagai key pada min() dan max().
        """
        if not self.expenses:
            return {"terendah": None, "tertinggi": None}

        terendah = min(self.expenses, key=lambda x: x["nominal"])
        tertinggi = max(self.expenses, key=lambda x: x["nominal"])

        return {
            "terendah": terendah,
            "tertinggi": tertinggi
        }

    def rangkuman(self):
        """
        Menggabungkan seluruh hasil analisis (total, jumlah, rata-rata,
        rincian kategori, terendah, tertinggi) dalam satu dictionary
        yang siap dipakai untuk tampilan dan laporan.
        """
        total = self.total_semua()
        rata_rata = self.rata_rata()
        breakdown = self.rincian_kat()
        min_max = self.cek_ekstrem()

        return {
            "total_pengeluaran": total,
            "jumlah_transaksi": len(self.expenses),
            "rata_rata": rata_rata,
            "per_kategori": breakdown,
            "terendah": min_max["terendah"],
            "tertinggi": min_max["tertinggi"],
        }


if __name__ == "__main__":
    # Blok ini hanya berjalan saat processing.py dijalankan langsung (uji lokal)
    _ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if _ROOT not in sys.path:
        sys.path.insert(0, _ROOT)

    print("=== PENGUJIAN LOKAL MODUL PROCESSING.PY ===")
    test_total = hitung_total(15000.0, 35000.0, 50000.0)
    print(f"1. Uji fungsi hitung_total(*args) : Total = Rp {test_total}")
    assert test_total == 100000.0, "Pengujian hitung_total gagal"

    test_rec = buat_record(
        tanggal="2026-10-09",
        kategori="Makanan",
        nominal=25000,
        keterangan="Uji lokal record"
    )
    print(f"2. Uji fungsi buat_record(**kwargs): {test_rec}")
    assert test_rec["kategori"] == "Makanan", "Pengujian buat_record gagal"

    dummy_analyzer = AnalisisData(expenses=[test_rec])
    print(f"3. Uji AnalisisData (Rata-rata): Rp {dummy_analyzer.rata_rata()}")
    assert dummy_analyzer.rata_rata() == 25000.0

    print("[BERHASIL] Seluruh pengujian lokal pada modul processing.py lulus!\n")
