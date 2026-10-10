"""
Modul: report.py
Deskripsi: Bertanggung jawab memformat nilai mata uang serta membuat dan mengekspor
laporan ringkasan pengeluaran dalam bentuk teks terstruktur.
"""

import os
from datetime import datetime
from expense_tracker.fileio import simpan_teks


def format_rupiah(amount):
    """
    Memformat angka float menjadi string mata uang Rupiah yang rapi.
    Contoh: 150000 -> 'Rp 150.000,00'
    """
    try:
        val = float(amount)
        formatted = f"{val:,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")
        return f"Rp {formatted}"
    except (ValueError, TypeError):
        return f"Rp {amount}"


def susun_teks(summary, expenses):
    """
    Menyusun teks laporan lengkap yang rapi dan terstruktur untuk pengeluaran harian.
    """
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    garis_tebal = "=" * 65
    garis_tipis = "-" * 65

    lines = [
        garis_tebal,
        "           LAPORAN RINGKASAN PENGELUARAN HARIAN",
        "                  DAILY EXPENSE TRACKER",
        garis_tebal,
        f"Waktu Pembuatan Laporan : {now_str}",
        f"Total Seluruh Transaksi : {summary['jumlah_transaksi']} transaksi",
        f"Total Nominal Pengeluaran: {format_rupiah(summary['total_pengeluaran'])}",
        f"Rata-rata per Transaksi : {format_rupiah(summary['rata_rata'])}",
        garis_tipis,
        "RINGKASAN BERDASARKAN KATEGORI:",
    ]

    total_pengeluaran = summary["total_pengeluaran"]
    breakdown = summary.get("per_kategori", {})
    if breakdown and total_pengeluaran > 0:
        for kat, nominal in breakdown.items():
            persentase = (nominal / total_pengeluaran) * 100
            lines.append(f"  - {kat:<20} : {format_rupiah(nominal):>16} ({persentase:.1f}%)")
    else:
        lines.append("  (Belum ada data pengeluaran berdasarkan kategori)")

    lines.append(garis_tipis)
    lines.append("TRANSAKSI EKSTREM (TERENDAH & TERTINGGI):")
    terendah = summary.get("terendah")
    tertinggi = summary.get("tertinggi")

    if terendah:
        lines.append(
            f"  - Terendah  : {format_rupiah(terendah['nominal'])} "
            f"[{terendah['kategori']}] ({terendah['tanggal']} - {terendah['keterangan']})"
        )
    else:
        lines.append("  - Terendah  : -")

    if tertinggi:
        lines.append(
            f"  - Tertinggi : {format_rupiah(tertinggi['nominal'])} "
            f"[{tertinggi['kategori']}] ({tertinggi['tanggal']} - {tertinggi['keterangan']})"
        )
    else:
        lines.append("  - Tertinggi : -")

    lines.append(garis_tipis)
    lines.append("DAFTAR SELURUH TRANSAKSI:")
    lines.append(f"{'No':<4} {'Tanggal':<12} {'Kategori':<16} {'Nominal':<16} {'Keterangan'}")
    lines.append(garis_tipis)

    if expenses:
        for idx, item in enumerate(expenses, start=1):
            lines.append(
                f"{idx:<4} {item['tanggal']:<12} {item['kategori']:<16} "
                f"{format_rupiah(item['nominal']):<16} {item['keterangan']}"
            )
    else:
        lines.append("  (Tidak ada transaksi yang tercatat)")

    lines.append(garis_tebal)
    lines.append("                   AKHIR DARI LAPORAN")
    lines.append(garis_tebal)

    return "\n".join(lines) + "\n"


def ekspor_laporan(filepath, summary, expenses):
    """
    Membuat string laporan dan menyimpannya ke berkas teks.
    """
    report_content = susun_teks(summary=summary, expenses=expenses)
    simpan_teks(filepath=filepath, content=report_content)
    return report_content
