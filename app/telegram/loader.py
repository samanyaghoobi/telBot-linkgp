import os
import importlib.util
from os.path import join

def load_handlers(bot, handlers_dir="app/telegram/handlers"):
    """
    Dynamically imports all Python files in the handlers directory and its subdirectories.
    Ensures that 'none_handler.py' is loaded last.
    """
    none_handler_path = "app/telegram/handlers/none_handler.py"

    for root, _, files in os.walk(handlers_dir):
        for filename in files:
            if filename.endswith(".py") and not filename.startswith("_"):
                file_path = join(root, filename)

                if filename == "none_handler.py":
                    none_handler_path = file_path
                    continue  # skip for now

                # normal handler
                module_name = filename[:-3]
                spec = importlib.util.spec_from_file_location(module_name, file_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                print(f"✅ Loaded handler: {file_path}")

    # load none_handler.py last
    if none_handler_path:
        module_name = "none_handler"
        spec = importlib.util.spec_from_file_location(module_name, none_handler_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        print(f"✅ Loaded handler (last): {none_handler_path}")
