import os
from pdf2image import convert_from_path

def pdf_to_image(pdf_path, output_dir="images"):
    os.makedirs(output_dir, exist_ok=True)

    pages = convert_from_path(pdf_path, dpi=150)
    image_path = os.path.join(output_dir, pdf_path.split("/")[-1].replace(".pdf", ".png"))

    pages[0].save(image_path, "PNG")
    return image_path
