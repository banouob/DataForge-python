import os
os.environ["DOTNET_SYSTEM_GLOBALIZATION_INVARIANT"] = "1"

import sys
import tkinter as tk

# 確保專案根目錄在 sys.path
ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from infrastructure.config_manager import ConfigManager
from infrastructure import error_logger
from controller.processing_controller import ProcessingController
from ui.file_chooser_service import FileChooserService


def main():
    try:
        config = ConfigManager()
    except ValueError as e:
        import tkinter.messagebox as mb
        root = tk.Tk()
        root.withdraw()
        mb.showerror("設定錯誤", str(e))
        return

    controller = ProcessingController(config)

    root = tk.Tk()
    FileChooserService(root, controller.process_files)

    error_logger.log_info("DataForge Python 啟動")
    root.mainloop()


if __name__ == "__main__":
    main()
