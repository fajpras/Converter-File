"""Modul dialog pemilihan file input dan lokasi penyimpanan output."""

import os
from tkinter import filedialog


def pilih_file() -> str:
    """Membuka dialog untuk memilih file sumber yang akan dikonversi."""
    filetypes = [
        ("Semua Format Didukung", "*.pdf *.docx *.jpg *.jpeg *.png"),
        ("Dokumen PDF", "*.pdf"),
        ("Dokumen Word", "*.docx"),
        ("Gambar (JPG/PNG)", "*.jpg *.jpeg *.png"),
        ("Semua File", "*.*"),
    ]
    filename = filedialog.askopenfilename(
        title="Pilih File",
        initialdir=os.path.expanduser("~"),
        filetypes=filetypes,
    )
    return filename.strip("{}") if filename else ""


def file_out(ext: str) -> str:
    """Membuka dialog untuk menentukan lokasi penyimpanan file hasil konversi."""
    clean_ext = ext.lstrip(".").lower()
    path_tujuan = filedialog.asksaveasfilename(
        title="Pilih Lokasi Penyimpanan File",
        initialdir=os.path.expanduser("~"),
        defaultextension=f".{clean_ext}",
        filetypes=[
            (f"File {clean_ext.upper()}", f"*.{clean_ext}"),
            ("Semua File", "*.*"),
        ],
    )
    return path_tujuan or ""
