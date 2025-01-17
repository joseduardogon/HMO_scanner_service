import os
import cv2
from pyzbar.pyzbar import decode
from reportlab.pdfgen import canvas
from PIL import Image


def detect_barcode(image):
    # Detect image barcode
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    barcodes = decode(gray)
    return barcodes


def save_as_pdf(images, output_path):
    # Save Tiff as an PDF file
    pil_images = [Image.open(img).convert('RGB') for img in images]
    pil_images[0].save(output_path, save_all=True, append_images=pil_images[1:])


def process_tiff_folder(folder_path, output_folder):
    # Processing all tiff files in a folder and separating then in PDFs
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    current_images = []
    batch_number = 1

    for root, _, files in os.walk(folder_path):
        for file in sorted(files):
            if file.lower().endswith('.tiff'):
                file_path = os.path.join(root, file)

                # Load image
                image = cv2.imread(file_path)

                # Barcode verification
                barcodes = detect_barcode(image)

                if barcodes:
                    # Save current batch as PDF
                    if current_images:
                        output_path = os.path.join(output_folder, f"batch_{batch_number}.pdf")
                        save_as_pdf(current_images, output_path)
                        print(f"Lote {batch_number} salvo em {output_path}")
                        batch_number += 1
                        current_images = []

                # Add image to current batch
                current_images.append(file_path)

    # Save last batch as PDF
    if current_images:
        output_path = os.path.join(output_folder, f"batch_{batch_number}.pdf")
        save_as_pdf(current_images, output_path)
        print(f"Lote {batch_number} salvo em {output_path}")


# Config
input_folder = "caminho/para/pasta_tiff"
output_folder = "caminho/para/pasta_output"

process_tiff_folder(input_folder, output_folder)
