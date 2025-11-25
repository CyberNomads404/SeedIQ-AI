import importlib
from .analyze_types.base_ai import BaseAnalyze
from src.services.image_service import ImageService

class AnalyzeLoader:
    @staticmethod
    def load(seed_category: str) -> BaseAnalyze:
        module_name = f"src.drivers.analyze.analyze_types.{seed_category}_ai"
        class_name = f"{seed_category.capitalize()}Analyze"

        try:
            module = importlib.import_module(module_name)
            analyze_class = getattr(module, class_name)
            return analyze_class(ImageService())
        except ModuleNotFoundError:
            raise ValueError(f"No analyzer found for seed type '{seed_category}'")
        except AttributeError:
            raise ValueError(f"Analyze class for '{seed_category}' not implemented correctly")
