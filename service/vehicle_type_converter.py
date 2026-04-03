import os
from infrastructure import error_logger


class VehicleTypeConverter:
    def __init__(self):
        self._mappings: dict[str, str] = {}
        self._load()

    def _load(self):
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        prop_path = os.path.join(root, 'vehicle-types.properties')

        if not os.path.exists(prop_path):
            error_logger.log_warning(f"找不到車種對應表: {prop_path}")
            return

        with open(prop_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' in line:
                    key, _, val = line.partition('=')
                    self._mappings[key.strip()] = val.strip()

        error_logger.log_info(f"載入車種對應表，共 {len(self._mappings)} 條規則")

    def convert(self, vehicle_type: str) -> str:
        if not vehicle_type:
            return vehicle_type
        result = self._mappings.get(vehicle_type, vehicle_type)
        if result != vehicle_type:
            error_logger.log_info(f"車種轉換: [{vehicle_type}] → [{result}]")
        return result

    def mapping_count(self) -> int:
        return len(self._mappings)
