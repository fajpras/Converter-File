"""Aplikasi GUI File Converter berbasis CustomTkinter dan TkinterDnD2."""

import os
import sys
from tkinter import messagebox

import customtkinter as ctk
from tkinterdnd2 import DND_FILES, TkinterDnD

from app.convert import SUPPORTED_CONVERSIONS, convert_file
from app.file import file_out, pilih_file

DEFAULT_FORMAT_OPTIONS = ["PDF", "DOCX", "JPG", "PNG"]


class DnDCTk(ctk.CTk, TkinterDnD.DnDWrapper):
    """Root window CustomTkinter dengan dukungan drag-and-drop."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TkdndVersion = TkinterDnD._require(self)


class FileConverterApp(DnDCTk):
    """Jendela utama aplikasi File Converter."""

    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.title("File Converter")
        self.geometry("500x600")
        self.resizable(False, False)

        icon_path = os.path.join(
            getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__))),
            "icon.ico",
        )
        if os.path.isfile(icon_path):
            self.iconbitmap(icon_path)

        self._build_ui()
        self._bind_events()

    def _build_ui(self) -> None:
        """Membangun komponen antarmuka pengguna."""
        # Area drag and drop
        self.drop_bg = ctk.CTkFrame(
            self,
            width=400,
            height=200,
            corner_radius=10,
            border_width=2,
            border_color="#3B8ED0",
        )
        self.drop_bg.pack(pady=30, padx=10)

        self.drop_label = ctk.CTkLabel(
            self.drop_bg,
            text="Taruh file di sini",
            font=("Monospace", 20),
        )
        self.drop_label.place(relx=0.5, rely=0.5, anchor="center")

        # Input file asal
        frame_input = ctk.CTkFrame(self, fg_color="transparent")
        frame_input.pack(pady=10)

        self.input_entry = ctk.CTkEntry(
            frame_input,
            width=300,
            height=40,
            border_width=1,
            border_color="#85BCEA",
            placeholder_text="Pilih file asal...",
            font=("Monospace", 14),
            corner_radius=5,
        )
        self.input_entry.grid(row=0, column=0)

        self.btn_file = ctk.CTkButton(
            frame_input,
            width=75,
            height=40,
            corner_radius=5,
            text="Pilih",
            command=self.select_input_file,
        )
        self.btn_file.grid(row=0, column=1, padx=(15, 0))

        # Pilihan format tujuan
        self.label_convert = ctk.CTkLabel(
            self,
            width=200,
            height=30,
            text="Konversi ke",
            font=("Monospace", 16, "bold"),
        )
        self.label_convert.pack(pady=10, padx=10, anchor="center")

        self.dropdown = ctk.CTkOptionMenu(
            self,
            height=40,
            width=200,
            font=("Monospace", 18),
            values=DEFAULT_FORMAT_OPTIONS,
        )
        self.dropdown.pack(pady=5, anchor="center")

        # Input lokasi output
        frame_output = ctk.CTkFrame(self, fg_color="transparent")
        frame_output.pack(pady=20)

        self.output_entry = ctk.CTkEntry(
            frame_output,
            width=300,
            height=40,
            placeholder_text="Lokasi simpan...",
            font=("Monospace", 14),
        )
        self.output_entry.grid(row=0, column=0)

        self.btn_dest = ctk.CTkButton(
            frame_output,
            width=75,
            height=40,
            text="Simpan",
            command=self.select_output_file,
        )
        self.btn_dest.grid(row=0, column=1, padx=(15, 0))

        # Tombol mulai konversi
        self.btn_konversi = ctk.CTkButton(
            self,
            text="MULAI KONVERSI",
            width=300,
            height=50,
            fg_color="#10b981",
            hover_color="#059669",
            font=("Monospace", 18, "bold"),
            command=self.start_conversion,
        )
        self.btn_konversi.pack(padx=10, pady=10, anchor="center")

    def _bind_events(self) -> None:
        """Mengatur event drag-and-drop pada area target."""
        self.drop_bg.drop_target_register(DND_FILES)
        self.drop_bg.dnd_bind("<<Drop>>", self.on_file_drop)

    def _set_input_file(self, path_file: str) -> None:
        """Memvalidasi file input, memperbarui UI, dan menyesuaikan format tujuan."""
        if not path_file or not os.path.isfile(path_file):
            messagebox.showwarning("Peringatan", "File tidak valid atau tidak ditemukan.")
            return

        ext = os.path.splitext(path_file)[1].lower()
        pilihan_baru = SUPPORTED_CONVERSIONS.get(ext)
        if not pilihan_baru:
            messagebox.showwarning(
                "Format Tidak Didukung",
                f"Ekstensi '{ext or 'tanpa ekstensi'}' belum didukung.\n"
                "Format yang didukung: PDF, DOCX, JPG, JPEG, PNG.",
            )
            return

        nama_file = os.path.basename(path_file)
        self.drop_label.configure(text=f"File:\n{nama_file}", text_color="#10b981")
        self.drop_bg.configure(border_color="#4ade80", fg_color="#14532d")

        self.input_entry.delete(0, "end")
        self.input_entry.insert(0, path_file)

        self.dropdown.configure(values=pilihan_baru)
        self.dropdown.set(pilihan_baru[0])

    def select_input_file(self) -> None:
        """Membuka dialog untuk memilih file sumber."""
        path_file = pilih_file()
        if path_file:
            self._set_input_file(path_file)

    def select_output_file(self) -> None:
        """Membuka dialog untuk memilih lokasi file tujuan."""
        ext = self.dropdown.get().lower()
        path_file = file_out(ext)
        if path_file:
            self.output_entry.delete(0, "end")
            self.output_entry.insert(0, path_file)

    def on_file_drop(self, event) -> None:
        """Menangani file yang dijatuhkan ke area drag-and-drop."""
        dropped_files = self.tk.splitlist(event.data)
        if dropped_files:
            self._set_input_file(dropped_files[0])

    def start_conversion(self) -> None:
        """Memvalidasi input dan menjalankan proses konversi."""
        file_asal = self.input_entry.get().strip()
        file_tujuan = self.output_entry.get().strip()
        target_format = self.dropdown.get().strip()

        if not file_asal or not file_tujuan:
            messagebox.showwarning(
                "Input Belum Lengkap",
                "Pilih file asal dan lokasi penyimpanan terlebih dahulu.",
            )
            return

        if not os.path.isfile(file_asal):
            messagebox.showerror("Error", f"File asal tidak ditemukan:\n{file_asal}")
            return

        expected_ext = f".{target_format.lower()}"
        if not file_tujuan.lower().endswith(expected_ext):
            file_tujuan = f"{file_tujuan}{expected_ext}"

        try:
            saved_paths = convert_file(file_asal, file_tujuan, target_format)
        except Exception as exc:
            messagebox.showerror("Error", f"Gagal mengonversi file:\n{exc}")
            return

        hasil_teks = "\n".join(saved_paths)
        messagebox.showinfo("Berhasil", f"File berhasil dikonversi:\n{hasil_teks}")
        self.reset_form()

    def reset_form(self) -> None:
        """Mengembalikan seluruh field form ke kondisi awal."""
        self.input_entry.delete(0, "end")
        self.output_entry.delete(0, "end")

        self.drop_label.configure(text="Taruh file di sini", text_color="white")
        self.drop_bg.configure(border_color="#3B8ED0", fg_color="transparent")

        self.dropdown.configure(values=DEFAULT_FORMAT_OPTIONS)
        self.dropdown.set(DEFAULT_FORMAT_OPTIONS[0])


if __name__ == "__main__":
    app = FileConverterApp()
    app.mainloop()
