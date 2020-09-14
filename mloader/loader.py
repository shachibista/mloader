import importlib
from typing import Optional, Any, List

class Loader:
    config: Optional[dict] = None

    def __init__(self, _config: dict):
        self.config = _config

    def _get_value(self, compound_key: str) -> Any:
        keys = compound_key.split(".")

        anchor: Any = self.config

        while len(keys) > 0:
            key = keys.pop(0)
            anchor = anchor[key]
        
        return anchor

    def load(self, key, as_class=False, package=None) -> Any:
        obj = self._get_value(key)

        if as_class:
            if isinstance(obj, str):
                class_path = obj
                params = {}
            elif isinstance(obj, dict):
                class_path_key = f"{key}_name"

                if class_path_key not in obj:
                    raise Exception(f"please specify {key}_name for instantiation")

                class_path = obj.pop(class_path_key)
                params = obj
        
            class_parts = class_path.split(".")
            class_name = class_parts.pop()
            
            module: Any = globals()
            if len(class_parts) > 0:
                module = importlib.import_module(".".join(class_parts))
            elif package is not None:
                module = importlib.import_module(package)
            
            class_instantiator = getattr(module, class_name)

            return class_instantiator(**params)

        return obj