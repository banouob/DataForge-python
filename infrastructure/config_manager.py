import os


class ConfigManager:
    def __init__(self):
        self._props: dict[str, str] = {
            'output.json.enabled': 'false',
            'output.json.path': 'output',
        }
        self._load()
        self._validate()

    def _load(self):
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config_path = os.path.join(root, 'config.properties')
        if not os.path.exists(config_path):
            return
        with open(config_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' in line:
                    key, _, val = line.partition('=')
                    self._props[key.strip()] = val.strip()

    def _validate(self):
        if self.is_json_output_enabled() and not self.get_json_output_path():
            raise ValueError("output.json.enabled=true 但 output.json.path 為空")

    def is_json_output_enabled(self) -> bool:
        return self._props.get('output.json.enabled', 'false').lower() == 'true'

    def get_json_output_path(self) -> str:
        path = self._props.get('output.json.path', 'output')
        if not os.path.isabs(path):
            root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            path = os.path.join(root, path)
        return path
