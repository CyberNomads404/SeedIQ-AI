import os
import requests
import mimetypes
import random
from urllib.parse import urlparse


class ImageService:

    def __init__(self, base_path: str = "storage/downloads"):
        self.base_path = base_path
        os.makedirs(self.base_path, exist_ok=True)

    def generate_filename(self, url: str) -> str:
        filename = os.path.basename(urlparse(url).path)

        if not filename or "." not in filename:
            filename = f"imagem_baixada_{random.randint(1000, 9999)}.jpg"

        return filename

    def validate_mime(self, response):
        mime = response.headers.get("Content-Type", "")
        if not mime.startswith("image/"):
            raise Exception(f"URL não é uma imagem válida. MIME: {mime}")

    def download_image_from_url(self, url: str) -> str:
        filename = self.generate_filename(url)
        save_path = os.path.join(self.base_path, filename)

        response = requests.get(url, stream=True)

        if response.status_code != 200:
            raise Exception(f"Falha ao baixar imagem. HTTP {response.status_code}")

        self.validate_mime(response)

        with open(save_path, "wb") as file:
            file.write(response.content)

        return save_path

    def delete(self, path: str) -> bool:
        if os.path.exists(path):
            os.remove(path)
            return True

        return False
