# Validators and helpers for secure file uploads

import os
import uuid
import imghdr
from typing import BinaryIO

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from PIL import Image

# Default limits and allowed types
MAX_UPLOAD_SIZE = 5 * 1024 * 1024  # 5 MB
ALLOWED_MIME_TYPES = {
    "image/png",
    "image/jpeg",
    "application/pdf",
}

# Simple file signature checks for common types
_SIGNATURES = {
    "image/png": [b"\x89PNG\r\n\x1a\n"],
    "image/jpeg": [b"\xff\xd8\xff"],
    "application/pdf": [b"%PDF-"],
}


def _get_file_start(fp: BinaryIO, num_bytes: int = 16) -> bytes:
    fp.seek(0)
    chunk = fp.read(num_bytes)
    fp.seek(0)
    return chunk


def validate_file_size(file_obj):
    try:
        size = file_obj.size
    except AttributeError:
        # fallback: read to determine size
        file_obj.seek(0, os.SEEK_END)
        size = file_obj.tell()
        file_obj.seek(0)

    if size > MAX_UPLOAD_SIZE:
        raise ValidationError(f"File too large (>{MAX_UPLOAD_SIZE} bytes)")


def detect_mime_from_signature(file_obj):
    start = _get_file_start(file_obj, 16)
    for mime, sigs in _SIGNATURES.items():
        for sig in sigs:
            if start.startswith(sig):
                return mime
    # try image heuristics
    file_obj.seek(0)
    kind = imghdr.what(file_obj)
    file_obj.seek(0)
    if kind == "png":
        return "image/png"
    if kind in ("jpeg", "jpg"):
        return "image/jpeg"
    return None


def validate_mime_and_signature(file_obj, content_type: str = None):
    detected = detect_mime_from_signature(file_obj)
    if content_type:
        if content_type not in ALLOWED_MIME_TYPES:
            raise ValidationError(f"Content-Type '{content_type}' is not allowed")
        # If detected exists, require it to match declared content type for extra safety
        if detected and detected != content_type:
            raise ValidationError(
                f"File signature does not match declared Content-Type ({detected} != {content_type})"
            )
    else:
        if not detected or detected not in ALLOWED_MIME_TYPES:
            raise ValidationError("File type not allowed or could not be detected from signature")


def validate_image_open(file_obj):
    # Use Pillow to verify image integrity for image types
    try:
        file_obj.seek(0)
        img = Image.open(file_obj)
        img.verify()
        file_obj.seek(0)
    except Exception as exc:
        raise ValidationError("Invalid image file") from exc


def validate_upload(file_obj, content_type: str = None):
    """Top-level validator to run in model fields, forms, or upload endpoints.

    - Checks size
    - Checks MIME/content-type vs file signature
    - If image, ensures Pillow can open and verify it
    """
    validate_file_size(file_obj)
    validate_mime_and_signature(file_obj, content_type=content_type)

    # If it's an image type (either declared or detected), run image verification
    mime = content_type or detect_mime_from_signature(file_obj)
    if mime and mime.startswith("image/"):
        validate_image_open(file_obj)
