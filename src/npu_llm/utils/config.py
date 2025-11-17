"""Configuration management."""

import os
from pathlib import Path
from typing import Any, Dict, Optional

import yaml


class Config:
    """Configuration manager for NPU-LLM."""

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize configuration.

        Args:
            config_path: Path to YAML config file
        """
        self.config_path = config_path
        self._config: Dict[str, Any] = {}

        if config_path:
            self.load(config_path)
        else:
            self._load_defaults()

    def _load_defaults(self) -> None:
        """Load default configuration."""
        self._config = {
            'model': {
                'cache_dir': str(Path.home() / '.cache' / 'npu_llm'),
                'default_backend': 'openvino',
                'default_device': 'NPU',
            },
            'inference': {
                'max_length': 512,
                'temperature': 0.7,
                'top_p': 0.9,
                'top_k': 50,
            },
            'logging': {
                'level': 'INFO',
                'file': None,
            },
        }

    def load(self, config_path: str) -> None:
        """
        Load configuration from YAML file.

        Args:
            config_path: Path to YAML config file
        """
        path = Path(config_path)
        if not path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")

        with open(path, 'r') as f:
            self._config = yaml.safe_load(f)

    def save(self, config_path: str) -> None:
        """
        Save configuration to YAML file.

        Args:
            config_path: Path to save config file
        """
        path = Path(config_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, 'w') as f:
            yaml.dump(self._config, f, default_flow_style=False)

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value using dot notation.

        Args:
            key: Configuration key (e.g., 'model.cache_dir')
            default: Default value if key not found

        Returns:
            Configuration value
        """
        keys = key.split('.')
        value = self._config

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    def set(self, key: str, value: Any) -> None:
        """
        Set configuration value using dot notation.

        Args:
            key: Configuration key (e.g., 'model.cache_dir')
            value: Value to set
        """
        keys = key.split('.')
        config = self._config

        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]

        config[keys[-1]] = value

    def update_from_env(self) -> None:
        """Update configuration from environment variables."""
        # Model settings
        if 'NPU_LLM_CACHE_DIR' in os.environ:
            self.set('model.cache_dir', os.environ['NPU_LLM_CACHE_DIR'])

        if 'NPU_LLM_DEVICE' in os.environ:
            self.set('model.default_device', os.environ['NPU_LLM_DEVICE'])

        if 'NPU_LLM_BACKEND' in os.environ:
            self.set('model.default_backend', os.environ['NPU_LLM_BACKEND'])

        # Logging
        if 'NPU_LLM_LOG_LEVEL' in os.environ:
            self.set('logging.level', os.environ['NPU_LLM_LOG_LEVEL'])

    def to_dict(self) -> Dict[str, Any]:
        """
        Get configuration as dictionary.

        Returns:
            Configuration dictionary
        """
        return self._config.copy()

    def __repr__(self) -> str:
        """String representation of configuration."""
        return f"Config({self._config})"
