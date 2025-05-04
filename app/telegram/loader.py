import os
import importlib.util
from os.path import join

def load_handlers(bot, handlers_dir="app/telegram/handlers"):
    """
    Dynamically imports all Python files in the handlers directory and its subdirectories.
    Each file should contain bot handlers that register upon import.
    """
    for root, _, files in os.walk(handlers_dir):
        for filename in files:
            if filename.endswith(".py") and not filename.startswith("_"):
                module_name = filename[:-3]
                file_path = join(root, filename)

                spec = importlib.util.spec_from_file_location(module_name, file_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                print(f"✅ Loaded handler: {file_path}")
