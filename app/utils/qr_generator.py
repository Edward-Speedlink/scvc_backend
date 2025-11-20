import qrcode
import os

def generate_qr_code(data, output_dir='qrcodes'):
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, f"{data}.png")

    qr = qrcode.QRCode(box_size=10, border=2)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")
    img.save(path)
    return path
