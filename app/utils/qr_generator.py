import qrcode
import json
import os
from datetime import datetime


def generate_certificate_qr(student_name, course_name, certificate_number, issued_at, folder="static/qrcodes"):
    os.makedirs(folder, exist_ok=True)

    # Handle both date objects and strings for issued_at
    if hasattr(issued_at, 'isoformat'):
        # It's a datetime/date object - use isoformat
        issued_at_str = issued_at.isoformat()
    elif isinstance(issued_at, str):
        # It's already a string - use as is
        issued_at_str = issued_at
    else:
        # Fallback: use current date
        issued_at_str = datetime.now().date().isoformat()

    qr_data = {
        "student_name": student_name,
        "course_name": course_name,
        "certificate_number": certificate_number,
        "issued_at": issued_at.isoformat(),
        "verify_url": f"https://speedlinktraining.com/verify/{certificate_number}"
    }

    json_str = json.dumps(qr_data)

    filename = f"{certificate_number.replace('/', '_')}.png"
    filepath = os.path.join(folder, filename)

    img = qrcode.make(json_str)
    img.save(filepath)

    return filepath

