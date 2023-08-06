from pathlib import Path

from nautobot.extras.plugins import PluginConfig


class NautobotYangConfig(PluginConfig):
    name = 'nautobot_tools'
    verbose_name = 'Nautobot Yang'
    description = 'Nautobot Yang'
    version = '0.1'
    author = 'Dimas Ari'
    author_email = 'dimas.ari@dataductus.com'
    base_url = 'yang'
    required_settings = []
    default_settings = {
        'loud': False
    }


config = NautobotYangConfig

_ROOT = Path(__file__).resolve().parent


def get_built_in_yang_modules_path():
    return _ROOT / 'yang'
