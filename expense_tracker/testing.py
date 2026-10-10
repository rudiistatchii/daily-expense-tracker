"""
Modul: testing.py
Deskripsi: Pengujian unit otomatis untuk aplikasi Daily Expense Tracker menggunakan framework bawaan `unittest`.
Memenuhi ketentuan:
- Menggunakan `unittest` dengan minimal satu class pengujian dan minimal lima metode pengujian.
- Menguji:
  1. Penambahan transaksi.
  2. Perhitungan total pengeluaran.
  3. Perhitungan rata-rata.
  4. Penolakan nominal tidak valid.
  5. Penanganan data rusak atau file yang belum tersedia.
- Menggunakan pernyataan `assert` minimal sekali dalam pengujian.
- Menggunakan folder/file sementara (TemporaryDirectory) agar data riil tidak tercampur/terhapus.
- Menggunakan `if __name__ == "__main__":` untuk pengujian lokal langsung.
"""

import os
import sys
import shutil
import tempfile
import unittest

# Menambahkan root direktori proyek ke sys.path agar modul dapat dijalankan langsung
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from expense_tracker.validation import (
    cek_tanggal as valid_tanggal,
    cek_nominal as valid_nominal,
    cek_kategori as valid_kategori,
)
from expense_tracker.fileio import (
    buat_file as buat_file_local,
    muat_data as baca_data,
    simpan_data as simpan_data_local,
    simpan_teks as simpan_teks_local,
)
from expense_tracker.processing import (
    ManajerData as DataManager,
    AnalisisData as Analisis,
    hitung_total as total_nominal,
    buat_record as buat_rekam,
)


class TestDailyExpenseTracker(unittest.TestCase):
    """
    Kelas pengujian unit untuk seluruh alur bisnis Daily Expense Tracker.
    """

    def setUp(self):
        """
        Menyiapkan direktori dan file CSV sementara sebelum setiap pengujian dijalankan.
        Menjamin isolasi total terhadap data pengguna asli.
        """
        self.test_dir = tempfile.mkdtemp()
        self.test_csv_path = os.path.join(self.test_dir, "test_expenses.csv")
        self.manager = DataManager(filepath=self.test_csv_path)

    def tearDown(self):
        """
        Membersihkan seluruh file dan direktori sementara setelah pengujian selesai.
        """
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def tambah_data(self, **kwargs):
        """Metode bantuan singkat dalam bahasa Indonesia."""
        return self.manager.tambah_data(**kwargs)

    def lihat_data(self):
        """Metode bantuan singkat dalam bahasa Indonesia."""
        return self.manager.ambil_semua()

    def urut_data(self):
        """Metode bantuan singkat dalam bahasa Indonesia."""
        return self.manager.urutkan(descending=True)

    def filter_kategori(self, category):
        """Metode bantuan singkat dalam bahasa Indonesia."""
        return self.manager.saring_data(kategori=category)

    def test_tambah_data(self):
        """
        1. Pengujian penambahan transaksi baru.
        Memverifikasi transaksi tersimpan dengan benar di memori dan file CSV.
        """
        record = self.tambah_data(
            tanggal="2026-10-09",
            kategori="Makanan",
            nominal=25000.0,
            keterangan="Makan siang soto ayam"
        )

        all_expenses = self.lihat_data()

        # Menggunakan pernyataan assert eksplisit (memenuhi ketentuan wajib)
        assert len(all_expenses) == 1, "Jumlah transaksi harus 1 setelah penambahan"
        assert all_expenses[0]["nominal"] == 25000.0, "Nominal transaksi harus sesuai"

        # Pengujian assertions bawaan unittest
        self.assertEqual(record["kategori"], "Makanan")
        self.assertEqual(record["tanggal"], "2026-10-09")
        self.assertEqual(record["keterangan"], "Makan siang soto ayam")

        # Verifikasi muat ulang langsung dari file CSV
        reloaded = baca_data(self.test_csv_path)
        self.assertEqual(len(reloaded), 1)
        self.assertEqual(reloaded[0]["kategori"], "Makanan")

    def test_total(self):
        """
        2. Pengujian perhitungan total pengeluaran.
        Memverifikasi keakuratan akumulasi nominal dan penggunaan *args pada hitung_total.
        """
        # Uji fungsi dengan parameter *args langsung
        total_args = total_nominal(10000.0, 20000.0, 35000.0)
        self.assertEqual(total_args, 65000.0)
        # Penggunaan pernyataan assert eksplisit
        assert total_args == 65000.0, "Fungsi hitung_total(*args) gagal menjumlahkan nominal"

        # Tambahkan transaksi ke manajer
        self.tambah_data(tanggal="2026-10-09", kategori="Makanan", nominal=15000.0, keterangan="Sarapan")
        self.tambah_data(tanggal="2026-10-09", kategori="Transportasi", nominal=10000.0, keterangan="Bensin")
        self.tambah_data(tanggal="2026-10-09", kategori="Hiburan", nominal=25000.0, keterangan="Buku")

        analyzer = Analisis(expenses=self.lihat_data())
        total = analyzer.total_semua()
        self.assertEqual(total, 50000.0)

    def test_rata_rata(self):
        """
        3. Pengujian perhitungan rata-rata pengeluaran.
        Memverifikasi rata-rata saat ada data dan saat data kosong.
        """
        # Pengujian saat data masih kosong
        empty_analyzer = Analisis(expenses=[])
        self.assertEqual(empty_analyzer.rata_rata(), 0.0)

        # Pengujian saat terisi data
        self.tambah_data(tanggal="2026-10-09", kategori="Pendidikan", nominal=40000.0, keterangan="Fotokopi")
        self.tambah_data(tanggal="2026-10-09", kategori="Pendidikan", nominal=60000.0, keterangan="Buku Teks")

        analyzer = Analisis(expenses=self.lihat_data())
        rata_rata = analyzer.rata_rata()

        # (40.000 + 60.000) / 2 = 50.000
        self.assertEqual(rata_rata, 50000.0)

    def test_nominal_salah(self):
        """
        4. Pengujian penolakan nominal tidak valid.
        Memverifikasi bahwa sistem membangkitkan ValueError untuk nominal negatif, 0, atau non-angka.
        """
        # Nominal nol harus ditolak
        with self.assertRaises(ValueError):
            valid_nominal(0)

        # Nominal negatif harus ditolak
        with self.assertRaises(ValueError):
            valid_nominal(-15000)

        # Nominal berupa string teks non-angka harus ditolak
        with self.assertRaises(ValueError):
            valid_nominal("gratis")

        # Format tanggal salah juga harus ditolak dengan ValueError
        with self.assertRaises(ValueError):
            valid_tanggal("09-10-2026")  # Format bukan YYYY-MM-DD

        with self.assertRaises(ValueError):
            valid_tanggal("2026-02-31")  # Tanggal kalender tidak ada

    def test_data_rusak(self):
        """
        5. Pengujian penanganan data rusak atau file yang belum tersedia.
        Memverifikasi bahwa file yang belum ada tidak memicu crash, dan baris CSV yang cacat dilewati secara aman.
        """
        # Skenario 1: File belum tersedia sama sekali
        non_existent_path = os.path.join(self.test_dir, "file_fiktif.csv")
        expenses_missing = baca_data(filepath=non_existent_path)
        self.assertEqual(expenses_missing, [])
        assert isinstance(expenses_missing, list)

        # Skenario 2: File CSV berisi campuran baris valid dan baris rusak/cacat
        corrupt_csv_path = os.path.join(self.test_dir, "corrupt_data.csv")
        with open(corrupt_csv_path, "w", encoding="utf-8") as f:
            f.write("tanggal,kategori,nominal,keterangan\n")
            f.write("2026-10-09,Makanan,12000,Nasi Goreng\n")        # Baris VALID
            f.write("baris-rusak-tanpa-koma-yang-benar\n")           # Baris RUSAK (kurang kolom)
            f.write("2026-10-09,Minuman,bukan_angka,Kopi\n")         # Baris RUSAK (nominal bukan angka)
            f.write("99-99-9999,Lainnya,5000,Snack\n")               # Baris RUSAK (format tanggal salah)
            f.write("2026-10-09,Transport,8000,Ongkos Busway\n")     # Baris VALID

        # Memuat file CSV yang mengandung baris rusak
        loaded_data = baca_data(filepath=corrupt_csv_path)

        # Hanya 2 baris valid yang harus terbaca tanpa membuat program crash
        self.assertEqual(len(loaded_data), 2)
        self.assertEqual(loaded_data[0]["kategori"], "Makanan")
        self.assertEqual(loaded_data[0]["nominal"], 12000.0)
        self.assertEqual(loaded_data[1]["kategori"], "Transport")
        self.assertEqual(loaded_data[1]["nominal"], 8000.0)

    def test_urut_filter(self):
        """
        Pengujian tambahan: Memverifikasi pengurutan berbasis lambda dan penyaringan transaksi.
        """
        self.tambah_data(tanggal="2026-10-01", kategori="Makanan", nominal=10000.0, keterangan="Snack")
        self.tambah_data(tanggal="2026-10-02", kategori="Hiburan", nominal=50000.0, keterangan="Tiket")
        self.tambah_data(tanggal="2026-10-03", kategori="Makanan", nominal=20000.0, keterangan="Siang")

        # Uji pengurutan terbesar ke terkecil
        sorted_desc = self.urut_data()
        self.assertEqual(sorted_desc[0]["nominal"], 50000.0)
        self.assertEqual(sorted_desc[-1]["nominal"], 10000.0)

        # Uji filter kategori
        filtered_food = self.filter_kategori("Makanan")
        self.assertEqual(len(filtered_food), 2)


if __name__ == "__main__":
    # Menjalankan pengujian unit lokal saat modul dieksekusi langsung
    unittest.main()
