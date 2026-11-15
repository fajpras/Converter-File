"""Modul fungsi konversi dokumen dan gambar."""

import os
from typing import Callable

from PIL import Image

SUPPORTED_CONVERSIONS: dict[str, list[str]] = {
    ".pdf": ["DOCX", "JPG", "PNG"],
    ".docx": ["PDF"],
    ".jpg": ["PDF"],
    ".jpeg": ["PDF"],
    ".png": ["PDF"],
}


def pdf_to_docx(source_path: str, target_path: str) -> list[str]:
    """Mengonversi file PDF menjadi dokumen DOCX."""
    from pdf2docx import Converter

    cv = Converter(source_path)
    try:
        cv.convert(target_path)
    finally:
        cv.close()
    return [target_path]


def docx_to_pdf(source_path: str, target_path: str) -> list[str]:
    """Mengonversi dokumen DOCX menjadi file PDF."""
    from docx2pdf import convert

    convert(source_path, target_path)
    return [target_path]


def pdf_to_images(source_path: str, target_path: str, dpi: int = 200) -> list[str]:
    """Mengonversi halaman PDF menjadi gambar JPG atau PNG."""
    from pdf2image import convert_from_path

    pages = convert_from_path(source_path, dpi=dpi)
    if not pages:
        raise ValueError("File PDF tidak memiliki halaman untuk dikonversi.")

    ext = os.path.splitext(target_path)[1].lstrip(".").upper()
    img_format = "JPEG" if ext == "JPG" else ext
    if img_format not in ("JPEG", "PNG"):
        raise ValueError(f"Format gambar tidak didukung: {ext}")

    output_dir = os.path.dirname(os.path.abspath(target_path))
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    saved_paths: list[str] = []
    if len(pages) == 1:
        page = pages[0]
        if img_format == "JPEG" and page.mode != "RGB":
            page = page.convert("RGB")
        page.save(target_path, img_format)
        saved_paths.append(target_path)
    else:
        stem, orig_ext = os.path.splitext(target_path)
        for idx, page in enumerate(pages, start=1):
            out_path = f"{stem}_page_{idx}{orig_ext}"
            if img_format == "JPEG" and page.mode != "RGB":
                page = page.convert("RGB")
            page.save(out_path, img_format)
            saved_paths.append(out_path)

    return saved_paths


def image_to_pdf(source_path: str, target_path: str) -> list[str]:
    """Mengonversi gambar (JPG/JPEG/PNG) menjadi file PDF."""
    source_abs = os.path.abspath(source_path)
    target_abs = os.path.abspath(target_path)

    output_dir = os.path.dirname(target_abs)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    with Image.open(source_abs) as image:
        if image.mode != "RGB":
            image = image.convert("RGB")
        image.save(target_abs, "PDF", resolution=100.0)

    return [target_abs]


_CONVERTER_DISPATCH: dict[tuple[str, str], Callable[[str, str], list[str]]] = {
    (".pdf", "DOCX"): pdf_to_docx,
    (".pdf", "JPG"): pdf_to_images,
    (".pdf", "PNG"): pdf_to_images,
    (".docx", "PDF"): docx_to_pdf,
    (".jpg", "PDF"): image_to_pdf,
    (".jpeg", "PDF"): image_to_pdf,
    (".png", "PDF"): image_to_pdf,
}


def convert_file(source_path: str, target_path: str, target_format: str) -> list[str]:
    """Menjalankan konversi berdasarkan ekstensi asal dan format tujuan."""
    if not os.path.isfile(source_path):
        raise FileNotFoundError(f"File asal tidak ditemukan:\n{source_path}")

    source_ext = os.path.splitext(source_path)[1].lower()
    normalized_format = target_format.strip().upper()
    handler = _CONVERTER_DISPATCH.get((source_ext, normalized_format))

    if handler is None:
        raise ValueError(
            f"Konversi dari '{source_ext or 'tanpa ekstensi'}' ke '{normalized_format}' tidak didukung."
        )

    return handler(source_path, target_path)
