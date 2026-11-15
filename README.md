# File Converter

Aplikasi desktop GUI sederhana berbasis Python untuk mengonversi file dokumen dan gambar dengan dukungan **drag-and-drop**.

## Fitur Utama

- **Drag-and-Drop**: Tarik dan jatuhkan file langsung ke area aplikasi.
- **Deteksi Format Otomatis**: Opsi format tujuan otomatis menyesuaikan jenis file yang dipilih.
- **Konversi yang Didukung**:
  - **PDF → DOCX**
  - **PDF → JPG / PNG** (mendukung PDF satu halaman maupun banyak halaman; multi-halaman disimpan sebagai `*_page_1`, `*_page_2`, dst.)
  - **DOCX → PDF**
  - **JPG / JPEG / PNG → PDF**

## Prasyarat

- **Python 3.10+**
- **Poppler** (diperlukan oleh `pdf2image` untuk konversi PDF ke gambar):
  - **Windows**: Unduh Poppler for Windows, ekstrak, lalu tambahkan folder `bin` ke `PATH`.
  - **Linux (Ubuntu/Debian)**: `sudo apt install poppler-utils`
  - **macOS**: `brew install poppler`
- **Microsoft Word** (diperlukan oleh `docx2pdf` di Windows/macOS untuk konversi DOCX ke PDF).

## Instalasi

1. Masuk ke direktori proyek:
   ```bash
   cd file-converter
   ```

2. (Opsional) Buat dan aktifkan virtual environment:
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # Linux/macOS
   source .venv/bin/activate
   ```

3. Pasang dependensi:
   ```bash
   pip install -r requirements.txt
   ```

## Cara Menjalankan

```bash
python main.py
```

### Langkah Penggunaan

1. Tarik file ke area **"Taruh file di sini"** atau klik tombol **Pilih** untuk memilih file.
2. Pilih format tujuan pada dropdown **Konversi ke**.
3. Klik tombol **Simpan** untuk menentukan lokasi dan nama file hasil konversi.
4. Klik **MULAI KONVERSI**.

## Struktur Proyek

```text
file-converter/
├── app/
│   ├── __init__.py      # Inisialisasi package app
│   ├── convert.py       # Logika konversi file (PDF, DOCX, gambar)
│   └── file.py          # Dialog pemilihan file input dan output
├── dok/
│   ├── alproo.drawio    # Diagram alur proyek
│   └── package.txt      # Catatan daftar dependensi awal
├── main.py              # Antarmuka GUI utama (CustomTkinter + TkinterDnD2)
├── requirements.txt     # Daftar dependensi Python
├── .gitignore           # Daftar file/folder yang diabaikan Git
└── README.md            # Dokumentasi proyek
```
