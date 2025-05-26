import os
import importlib.util
from os.path import join
from app.utils.logger import logger

def load_handlers(bot, handlers_dir="app/telegram/handlers"):
    """
    Dynamically imports all Python files in the handlers directory and its subdirectories.
    Ensures that `none_handler.py` is always loaded last.
    """
    handler_files = []

    for root, _, files in os.walk(handlers_dir):
        for filename in files:
            if filename.endswith(".py") and not filename.startswith("_"):
                file_path = join(root, filename)
                if filename == "none_handler.py":
                    continue  # defer loading this one
                handler_files.append(file_path)

    # Load all except none_handler.py
    for file_path in handler_files:
        module_name = os.path.splitext(os.path.basename(file_path))[0]
        try:
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            logger.info(f"✅ Loaded handler: {file_path}")
        except Exception as e:
            logger.error(f"❌ Failed to load handler {file_path}: {e}")

    # Load none_handler.py last
    none_handler_path = join(handlers_dir, "none_handler.py")
    if os.path.isfile(none_handler_path):
        try:
            spec = importlib.util.spec_from_file_location("none_handler", none_handler_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            logger.info(f"✅ Loaded final handler: {none_handler_path}")
        except Exception as e:
            logger.error(f"❌ Failed to load final handler {none_handler_path}: {e}")
