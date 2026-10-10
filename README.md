# Daily Expense Tracker (Pencatat Pengeluaran Harian)

Aplikasi pencatat dan analisis pengeluaran harian berbasis terminal (CLI) menggunakan bahasa pemrograman Python. Proyek ini dikembangkan untuk memenuhi tugas praktikum **Pemrograman Terstruktur**, dirancang dengan arsitektur modular yang rapi, mudah dipahami oleh mahasiswa pemula, serta menerapkan prinsip-prinsip *clean code* dan penanganan galat (*error handling*).

---

## Daftar Fitur

Aplikasi menyediakan menu interaktif berbasis CLI dengan 7 opsi utama:
1. **Tambah Pengeluaran**: Mencatat transaksi baru dengan tanggal (YYYY-MM-DD), kategori, nominal, dan keterangan. Data divalidasi dan disimpan secara permanen ke file CSV.
2. **Lihat Semua Pengeluaran**: Menampilkan seluruh riwayat transaksi dalam format tabel teks yang rapi beserta format mata uang Rupiah.
3. **Cari Berdasarkan Kategori atau Tanggal**: Memfilter transaksi berdasarkan kata kunci kategori, tanggal transaksi tertentu, atau kombinasi keduanya.
4. **Tampilkan Ringkasan Pengeluaran**: Menyajikan analisis statistik komprehensif, mencakup total transaksi, total nominal, rata-rata pengeluaran per transaksi, rincian per kategori dengan persentase kontribusi, serta transaksi nominal terendah dan tertinggi.
5. **Urutkan Pengeluaran Berdasarkan Nominal**: Mengurutkan daftar transaksi dari yang terbesar ke terkecil (*descending*) atau terkecil ke terbesar (*ascending*) memanfaatkan ekspresi `lambda`.
6. **Buat Laporan ke File Teks**: Mengekspor ringkasan statistik dan daftar transaksi ke dalam berkas teks (.txt) siap cetak/baca.
7. **Keluar**: Menutup aplikasi dengan aman.

---

## Struktur Folder Proyek

```text
pengeluaranHarian_petruk/
├── data/
│   ├── expenses.csv             # Penyimpanan data transaksi permanen (dibuat otomatis)
│   └── laporan_pengeluaran.txt  # Berkas laporan hasil ekspor (dibuat saat menu 6 dipilih)
├── docs/
│   └── refactoring.md           # Catatan tabel refactoring kode
├── expense_tracker/
│   ├── __init__.py              # Inisialisasi package expense_tracker
│   ├── validation.py            # Validasi input tanggal, nominal (raise), dan kategori
│   ├── fileio.py                # Operasi file (mode 'x', 'a', 'r', 'w' dengan with open)
│   ├── processing.py            # Kelas ExpenseManager & ExpenseAnalyzer (*args, **kwargs, lambda)
│   ├── report.py                # Pemformatan mata uang dan pembuatan laporan teks
│   └── testing.py               # Pengujian unit otomatis (unittest & assert)
├── main.py                      # Titik masuk utama aplikasi (CLI interactive loop)
└── README.md                    # Dokumentasi lengkap proyek
```

### Penjelasan Fungsi Setiap File:
- **`main.py`**: Berfungsi sebagai antarmuka pengguna berbasis terminal (CLI), mengelola alur menu 1–7 dan menangani masukan pengguna.
- **`expense_tracker/__init__.py`**: Menandai direktori sebagai *package* Python dan mengekspos modul-modul utama.
- **`expense_tracker/validation.py`**: Memusatkan logika verifikasi data; menggunakan `raise ValueError` untuk menolak format tanggal salah, nominal `<= 0`, atau kategori kosong.
- **`expense_tracker/fileio.py`**: Mengelola pembacaan dan penulisan berkas menggunakan pernyataan aman `with open()` dengan mode `'x'` (inisialisasi), `'a'` (tambah data), `'r'` (baca baris per baris), dan `'w'` (tulis laporan). Menangani `FileExistsError`, `FileNotFoundError`, serta baris CSV rusak.
- **`expense_tracker/processing.py`**: Mengimplementasikan dua kelas inti (`ExpenseManager` dan `ExpenseAnalyzer`), penggunaan `*args` untuk akumulasi nominal, `**kwargs` untuk pembuatan *record*, serta `lambda` untuk pengurutan.
- **`expense_tracker/report.py`**: Mengonversi angka ke format Rupiah (`format_currency`) dan menyusun tata letak teks laporan harian.
- **`expense_tracker/testing.py`**: Berisi pengujian unit otomatis dengan `unittest.TestCase` dan pernyataan `assert` untuk menguji fungsionalitas secara terisolasi.
- **`docs/refactoring.md`**: Mendokumentasikan tabel riwayat perbaikan kode (*Extract Function*, *Rename Variable*, *Remove Duplicate Code*).

---

## Pemenuhan Ketentuan Pemrograman

| No | Ketentuan Wajib | Implementasi dalam Kode |
| :---: | :--- | :--- |
| 1 | Minimal 2 Class | `ExpenseManager` dan `ExpenseAnalyzer` di [`processing.py`](file:///c:/Users/Rudhi/Documents/pengeluaranHarian_petruk/expense_tracker/processing.py) |
| 2 | Minimal 5 fungsi/metode buatan sendiri | `add_expense`, `get_all_expenses`, `filter_expenses`, `sort_by_amount`, `calculate_total`, `calculate_average`, `get_summary`, `format_currency` |
| 3 | Penggunaan `*args` | Fungsi `calculate_sum(*amounts)` di [`processing.py`](file:///c:/Users/Rudhi/Documents/pengeluaranHarian_petruk/expense_tracker/processing.py) |
| 4 | Penggunaan `**kwargs` | Fungsi `create_expense_record(**kwargs)` di [`processing.py`](file:///c:/Users/Rudhi/Documents/pengeluaranHarian_petruk/expense_tracker/processing.py) |
| 5 | Penggunaan `lambda` | Digunakan pada fungsi `sorted(..., key=lambda item: item['nominal'])` di [`processing.py`](file:///c:/Users/Rudhi/Documents/pengeluaranHarian_petruk/expense_tracker/processing.py) |
| 6 | Keyword argument pada pemanggilan | Digunakan pada pemanggilan fungsi/metode, misalnya `add_expense(tanggal=..., kategori=...)` |
| 7 | Pemisahan tanggung jawab modul | Dibagi menjadi `validation`, `fileio`, `processing`, `report`, dan `testing` |
| 8 | Operasi berkas dengan `with open()` | Seluruh operasi pembacaan dan penulisan berkas di [`fileio.py`](file:///c:/Users/Rudhi/Documents/pengeluaranHarian_petruk/expense_tracker/fileio.py) menggunakan `with open()` |
| 9 | Mode berkas `'x'`, `'a'`, `'r'`, `'w'` | Mode `'x'` untuk inisialisasi awal CSV, `'a'` untuk menambah data transaksi, `'r'` untuk membaca baris CSV, dan `'w'` untuk menyimpan laporan teks |
| 10 | Penanganan `FileExistsError` | Ditangani di `init_csv_file` saat membuat berkas awal dengan mode `'x'` |
| 11 | Penanganan `FileNotFoundError` | Ditangani di `load_expenses_from_csv` dengan pesan informatif jika berkas belum ada |
| 12 | Perulangan `for` membaca baris file | Menggunakan `for line in file:` pada fungsi `load_expenses_from_csv` |
| 13 | Penanganan baris rusak dengan `try/except` | Melewati baris cacat tanpa menghentikan pemrosesan baris valid di `load_expenses_from_csv` |
| 14 | Penggunaan `raise` untuk validasi | Menerapkan `raise ValueError` di [`validation.py`](file:///c:/Users/Rudhi/Documents/pengeluaranHarian_petruk/expense_tracker/validation.py) untuk nominal `<= 0` atau tanggal salah |
| 15 | Penggunaan `assert` dalam pengujian | Digunakan pernyataan `assert` eksplisit di [`testing.py`](file:///c:/Users/Rudhi/Documents/pengeluaranHarian_petruk/expense_tracker/testing.py) |
| 16 | `unittest` minimal 1 kelas & 5 metode | Kelas `TestDailyExpenseTracker` dengan 6 metode pengujian di [`testing.py`](file:///c:/Users/Rudhi/Documents/pengeluaranHarian_petruk/expense_tracker/testing.py) |
| 17 | `if __name__ == "__main__":` | Terdapat di [`main.py`](file:///c:/Users/Rudhi/Documents/pengeluaranHarian_petruk/main.py) dan [`testing.py`](file:///c:/Users/Rudhi/Documents/pengeluaranHarian_petruk/expense_tracker/testing.py) |
| 18 | Dokumentasi & Komentar | Seluruh fungsi memiliki docstring dan komentar bahasa Indonesia yang jelas |

---

## Cara Menjalankan Program

### Prasyarat
- Python versi 3.8 atau lebih baru terpasang di sistem.

### Menjalankan Aplikasi Utama (CLI)
Buka terminal di direktori proyek, lalu jalankan perintah:

```powershell
python main.py
```

---

## Contoh Input dan Output

### 1. Menambah Pengeluaran Baru (Menu 1)
**Input:**
```text
Pilih menu (1-7): 1

--- Tambah Pengeluaran Baru ---
Masukkan tanggal (YYYY-MM-DD) [Tekan Enter untuk 2026-10-09]: 2026-10-09
Masukkan kategori (contoh: Makanan, Transport, Kuliah, Hiburan): Makanan
Masukkan nominal pengeluaran (contoh: 25000): 25000
Masukkan keterangan (opsional, tekan Enter untuk default '-'): Nasi Padang Siang
```

**Output:**
```text
[Berhasil] Transaksi baru berhasil dicatat dan disimpan ke file CSV!
-> Tanggal    : 2026-10-09
-> Kategori   : Makanan
-> Nominal    : Rp 25.000,00
-> Keterangan : Nasi Padang Siang
```

---

### 2. Tampilkan Ringkasan Pengeluaran (Menu 4)
**Output:**
```text
=======================================================
             RINGKASAN DAN ANALISIS PENGELUARAN
=======================================================
Jumlah Total Transaksi   : 2
Total Nominal Pengeluaran : Rp 40.000,00
Rata-rata per Transaksi  : Rp 20.000,00
-------------------------------------------------------
Rincian Pengeluaran per Kategori:
  * Makanan            :     Rp 25.000,00 (62.5%)
  * Transport          :     Rp 15.000,00 (37.5%)
-------------------------------------------------------
Transaksi Terendah       : Rp 15.000,00 (Transport - 2026-10-09)
Transaksi Tertinggi      : Rp 25.000,00 (Makanan - 2026-10-09)
=======================================================
```

---

### 3. Buat Laporan ke File Teks (Menu 6)
**Input:**
```text
Pilih menu (1-7): 6
Masukkan jalur file laporan [Tekan Enter untuk 'data/laporan_pengeluaran.txt']: 
```

**Output:**
```text
[Berhasil] Laporan pengeluaran berhasil disimpan ke: 'C:\...\data\laporan_pengeluaran.txt'
```

Isi berkas `data/laporan_pengeluaran.txt` yang dihasilkan:
```text
=================================================================
           LAPORAN RINGKASAN PENGELUARAN HARIAN
                  DAILY EXPENSE TRACKER
=================================================================
Waktu Pembuatan Laporan : 2026-10-09 22:01:29
Total Seluruh Transaksi : 2 transaksi
Total Nominal Pengeluaran: Rp 40.000,00
Rata-rata per Transaksi : Rp 20.000,00
-----------------------------------------------------------------
RINGKASAN BERDASARKAN KATEGORI:
  - Makanan              :     Rp 25.000,00 (62.5%)
  - Transport            :     Rp 15.000,00 (37.5%)
-----------------------------------------------------------------
TRANSAKSI EKSTREM (TERENDAH & TERTINGGI):
  - Terendah  : Rp 15.000,00 [Transport] (2026-10-09 - Bensin Motor)
  - Tertinggi : Rp 25.000,00 [Makanan] (2026-10-09 - Nasi Padang Siang)
-----------------------------------------------------------------
DAFTAR SELURUH TRANSAKSI:
No   Tanggal      Kategori         Nominal          Keterangan
-----------------------------------------------------------------
1    2026-10-09   Makanan          Rp 25.000,00     Nasi Padang Siang
2    2026-10-09   Transport        Rp 15.000,00     Bensin Motor
=================================================================
                   AKHIR DARI LAPORAN
=================================================================
```

---

## Cara Menjalankan Pengujian Unit (Testing)

Pengujian unit menggunakan pustaka bawaan `unittest`. Pengujian menggunakan direktori sementara (*temporary directory*) sehingga tidak akan mengubah atau menghapus data pengeluaran asli di `data/expenses.csv`.

Dapat dijalankan melalui dua cara:

### Cara 1: Eksekusi Langsung Modul Testing
```powershell
python expense_tracker/testing.py
```

### Cara 2: Menjalankan Lewat Modul Unittest Runner
```powershell
python -m unittest expense_tracker/testing.py
```

### Hasil Pengujian yang Diharapkan:
```text
......
----------------------------------------------------------------------
Ran 6 tests in 0.062s

OK
```
Semua 6 pengujian berhasil dilewati (*OK*) tanpa kegagalan.
