import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from typing import List, Callable


class FileChooserService:
    def __init__(self, root: tk.Tk, on_files_selected: Callable[[List[str]], List[str]]):
        self._root = root
        self._on_files_selected = on_files_selected
        self._build_ui()

    def _build_ui(self):
        self._root.title("DataForge - 交通事故案件處理")
        self._root.geometry("800x600")

        btn_frame = tk.Frame(self._root)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)

        select_btn = tk.Button(
            btn_frame,
            text="選取 .doc 檔案",
            command=self._select_and_process,
            font=("Microsoft JhengHei", 12),
            bg="#0078D4",
            fg="white",
            padx=10,
            pady=5,
        )
        select_btn.pack(side=tk.LEFT)

        clear_btn = tk.Button(
            btn_frame,
            text="清除",
            command=self._clear,
            font=("Microsoft JhengHei", 12),
            padx=10,
            pady=5,
        )
        clear_btn.pack(side=tk.LEFT, padx=5)

        self._text_area = scrolledtext.ScrolledText(
            self._root,
            font=("Microsoft JhengHei", 11),
            wrap=tk.WORD,
            state=tk.DISABLED,
        )
        self._text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    def _select_and_process(self):
        paths = filedialog.askopenfilenames(
            title="選取交通事故 .doc 檔案",
            filetypes=[("Word 97-2003 文件", "*.doc"), ("所有檔案", "*.*")],
        )
        if not paths:
            return

        results = self._on_files_selected(list(paths))
        self._display_results(list(paths), results)

    def _display_results(self, paths: List[str], results: List[str]):
        self._text_area.config(state=tk.NORMAL)
        for path, result in zip(paths, results):
            import os
            filename = os.path.basename(path)
            self._text_area.insert(tk.END, f"【{filename}】\n{result}\n\n")
        self._text_area.config(state=tk.DISABLED)

    def _clear(self):
        self._text_area.config(state=tk.NORMAL)
        self._text_area.delete("1.0", tk.END)
        self._text_area.config(state=tk.DISABLED)

    def show_error(self, title: str, message: str):
        messagebox.showerror(title, message)
