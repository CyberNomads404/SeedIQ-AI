import importlib
from typing import Dict, Any
from .analyze_types.base_ai import BaseAnalyze

class AnalyzerLoader:

    @staticmethod
    def load(seed_category: str) -> BaseAnalyze:
        module_name = f"src.drivers.analyze.analyze_types.{seed_category}_ai"
        class_name = f"{seed_category.capitalize()}Analyzer"

        try:
            module = importlib.import_module(module_name)
            analyzer_class = getattr(module, class_name)
            return analyzer_class()
        except ModuleNotFoundError:
            raise ValueError(f"No analyzer found for seed type '{seed_category}'")
        except AttributeError:
            raise ValueError(f"Analyzer class for '{seed_category}' not implemented correctly")
