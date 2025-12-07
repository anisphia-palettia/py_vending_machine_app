import requests
from PIL import Image
from io import BytesIO
import customtkinter as ctk


def load_image_url(url, size=(150, 150)):
    try:
        response = requests.get(url)
        response.raise_for_status()

        img_data = response.content
        pil_image = Image.open(BytesIO(img_data))

        # Resize
        pil_image = pil_image.resize(size, Image.LANCZOS)

        # CTkImage untuk tampil otomatis dark/light mode
        return ctk.CTkImage(light_image=pil_image, dark_image=pil_image, size=size)

    except Exception as e:
        print("Gagal memuat gambar:", e)
        return None
