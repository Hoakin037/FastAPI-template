import os
import pkgutil
from pathlib import Path


def get_subfolders_paths(folder_path: Path) -> list:
    subfolders = []

    for item in os.listdir(folder_path):  # noqa: PTH208
        item_path = os.path.join(folder_path, item)  # noqa: PTH118
        subfolders.append(item_path)

    return subfolders


def load_all_models() -> None:
    path = "app.modules"
    modules_folder = "models"

    modules = []
    modules_path = Path("app/modules").resolve()
    subfolders = get_subfolders_paths(modules_path)

    for subfolder in subfolders:
        seperator = "/"

        if "/" not in subfolder:
            seperator = "\\"

        module = subfolder.split(seperator)[-1]
        walked_modules = pkgutil.walk_packages(
            path=[f"{subfolder}/models"], prefix=f"{path}.{module}.{modules_folder}."
        )

        modules.extend(module_info.name for module_info in walked_modules)

    for module in modules:
        __import__(module)
