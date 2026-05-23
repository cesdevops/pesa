# ── Standard Library ──────────────────────────────────────
import os
import re
import base64
import datetime
import uuid
# ── Third-Party ───────────────────────────────────────────
import requests
from PIL import Image
from PyPDF2 import PdfReader

# ── Django ────────────────────────────────────────────────
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import redirect
import re
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

import re

# ── Internal / Locani==========================================
# AD ID ENCODING / DECODING
# ============================================================

def encode_ad_id(ad_id):
    """Encode advertisement ID to base64."""
    try:
        return base64.urlsafe_b64encode(str(ad_id).encode()).decode()
    except Exception:
        return None


def decode_ad_id(encoded_id):
    """Decode base64 advertisement ID, adding padding if needed."""
    try:
        padding_needed = 4 - (len(encoded_id) % 4)
        if padding_needed:
            encoded_id += "=" * padding_needed
        decoded_bytes = base64.urlsafe_b64decode(encoded_id.encode())
        return int(decoded_bytes.decode())
    except Exception:
        return None

# ============================================================
# FILE VALIDATION
# ============================================================

def validate_file(file, request, max_size_mb=2, allowed_extensions=None):
    """
    Validates an uploaded file for:
      - File size limit
      - Allowed extensions
      - Magic byte check for images and PDFs
      - Image integrity via Pillow
      - PDF readability via PyPDF2
    Returns True if valid, False otherwise (adds error message to request).
    """
    if not file:
        return True

    # 1. File size check
    limit = max_size_mb * 1024 * 1024
    if file.size > limit:
        messages.error(request, f"File size should not exceed {max_size_mb} MB.")
        return False

    # 2. Extension check
    if allowed_extensions is None:
        allowed_extensions = ["jpg", "jpeg", "png", "pdf"]

    ext = os.path.splitext(file.name)[1][1:].lower()
    if ext not in allowed_extensions:
        messages.error(request, f"Only {', '.join(allowed_extensions)} files allowed.")
        return False

    file_bytes = file.read()
    file.seek(0)

    # 3. Image validation (magic bytes + Pillow verify)
    if ext in ["jpg", "jpeg", "png"]:
        if ext in ["jpg", "jpeg"] and not file_bytes.startswith(b"\xFF\xD8"):
            messages.error(request, "Invalid JPEG file.")
            return False

        if ext == "png" and not file_bytes.startswith(b"\x89PNG"):
            messages.error(request, "Invalid PNG file.")
            return False

        try:
            with Image.open(file) as img:
                img.verify()
        except Exception:
            messages.error(request, "Corrupted or invalid image file.")
            return False
        finally:
            file.seek(0)

    # 4. PDF validation (magic bytes + PyPDF2 readability)
    if ext == "pdf":
        if not file_bytes.startswith(b"%PDF"):
            messages.error(request, "Invalid PDF file.")
            return False

        try:
            reader = PdfReader(file)
            text_content = ""
            for page in reader.pages:
                text_content += (page.extract_text() or "")
            text_content = text_content.lower()
        except Exception:
            messages.error(request, "Unreadable PDF file.")
            return False
        finally:
            file.seek(0)

    return True


# ============================================================
# TEXT / FIELD VALIDATORS
# ============================================================

def validate_text_field(value, field_name="Field"):
    """
    Validates a basic text field.
    Allows only letters, numbers, spaces, hyphens, and underscores.
    Raises ValidationError if invalid characters are found.
    """
    if not value:
        return  # Empty handled by required field setting

    if not re.match(r'^[a-zA-Z0-9 _-]+$', value):
        raise ValidationError(
            f"{field_name} contains invalid characters. "
            "Only letters, numbers, spaces, '-' and '_' are allowed."
        )

def validate_email_field(value, field_name="Email"):
    """
    Validates email format.
    Raises ValidationError if invalid.
    """

    if not value:
        return

    try:
        validate_email(value)
    except ValidationError:
        raise ValidationError(f"Invalid {field_name} format.")
    

def validate_mobile_number(value):
    """
    Validates an Indian mobile number.
    Must be 10 digits and start with 6–9.
    Raises ValidationError if invalid.
    """
    if not re.match(r'^[6-9]\d{9}$', value):
        raise ValidationError(
            "Invalid mobile number. Must be 10 digits and start with 6–9."
        )


def validate_decimal_number(value):
    """
    Validates that the value is a valid integer or decimal number.
    Examples: 3, 3.45, 0.5, 10.0
    Raises ValidationError if invalid.
    """
    if not re.match(r'^\d+(\.\d+)?$', str(value)):
        raise ValidationError("Enter a valid number (e.g., 3, 3.45, 0.5).")

def validate_clean_text(value, field_name="This field"):
    """
    Generic validator for text fields:
    - Blocks HTML/script tags
    - Allows Marathi (Devanagari) and English letters
    - Allows numbers, spaces, dots, slashes, parentheses, and hyphens
    - Allows blank values
    """
    if value is None:
        return  # Treat None as allowed when field is blank=True

    value = str(value).strip()

    # Allow blank string ("") when blank=True in model
    if value == "":
        return

    # Block HTML or script content
    if re.search(r'<|>|script|onerror|onload', value, re.IGNORECASE):
        raise ValidationError(f"{field_name}: HTML or script tags are not allowed.")

    # Allow Marathi (Devanagari) + English letters + digits + safe symbols
    allowed_pattern = r'^[\u0900-\u097F A-Za-z0-9.,/()\-]+$'

    if not re.fullmatch(allowed_pattern, value):
        raise ValidationError(
            f"{field_name}: Invalid characters found. Only Marathi/English letters, numbers, spaces, '.', '/', '(', ')' and '-' are allowed."
        )

    return value














