from nautobot_tools import get_built_in_yang_modules_path
from yangson import DataModel


def get_model(path, name: str, mod_path=None, description: str = None):
    default_path = get_built_in_yang_modules_path()
    if mod_path:
        mod_path = list(mod_path)
        mod_path.append(default_path)
    else:
        mod_path = [path, default_path]

    data_model = DataModel.from_file(path + name, tuple(mod_path), description)
    return data_model.schema
