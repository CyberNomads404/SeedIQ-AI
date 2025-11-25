from abc import ABC, abstractmethod
from typing import Dict, Any
from src.services.image_service import ImageService
import cv2
import numpy as np

class BaseAnalyze(ABC):
    def __init__(self, image_service: ImageService):
        self.image_service = image_service
        self.cv2 = cv2
        self.np = np

    def analyze(self, payload: Dict[str, Any]) -> tuple:
        image_url = payload["image_url"]
        save_path = None

        try:
            save_path = self.image_service.download_image_from_url(image_url)
            result, params_ai = self.ai(payload, save_path)
            return (result, params_ai)

        except Exception as e:
            raise RuntimeError(f"Error processing analysis: {str(e)}")

        finally:
            if save_path:
                self.image_service.delete(save_path)

    @abstractmethod
    def ai(self, payload: Dict[str, Any], save_path: str) -> tuple:
        pass
