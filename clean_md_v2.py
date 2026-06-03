#!/usr/bin/env python3

import re
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext


# Matches any fenced code block line
FENCE_RE = re.compile(
    r'^(`{3,})\s*([a-zA-Z0-9_-]+)?(?:\s+id="[^"]*")?\s*$'
)

# Used only for scan reporting
ID_RE = re.compile(
    r'^(`{3,})\s*[a-zA-Z0-9_-]+\s+id="[^"]*"\s*$'
)

TEXT_RE = re.compile(
    r'^(`{3,})\s*(text|markdown)(?:\s+id="[^"]*")?\s*$'
)


def clean_fences(content: str) -> str:
    """
    Remove:
      ```text          -> ```
      ```markdown      -> ```
      ```python id=... -> ```python
      ```json id=...   -> ```json

    Preserves original line endings.
    """

    lines = []

    for line in content.splitlines(keepends=True):

        stripped = line.rstrip("\r\n")

        m = FENCE_RE.match(stripped)

        if not m:
            lines.append(line)
            continue

        newline = line[len(stripped):]

        fence = m.group(1)
        lang = m.group(2)

        if lang in ("text", "markdown"):
            lines.append(fence + newline)

        elif lang:
            lines.append(f"{fence}{lang}" + newline)

        else:
            lines.append(fence + newline)

    return "".join(lines)


def find_first_match(path: Path):
    """
    Return:
        (line_number, line_text, reason)

    or None if no cleaning needed.
    """

    with open(path, "r", encoding="utf-8") as f:

        for lineno, line in enumerate(f, start=1):

            if TEXT_RE.match(line):
                return (
                    lineno,
                    line.rstrip(),
                    "text/markdown fence"
                )

            if ID_RE.match(line):
                return (
                    lineno,
                    line.rstrip(),
                    "id attribute"
                )

    return None


def find_markdown_files(target: Path):

    if target.is_file():
        return [target] if target.suffix.lower() == ".md" else []

    if target.is_dir():
        return list(target.rglob("*.md"))

    return []


def needs_cleaning(path: Path) -> bool:

    content = path.read_text(encoding="utf-8")
    cleaned = clean_fences(content)

    return cleaned != content


def clean_file(path: Path, create_backup=True):

    content = path.read_text(encoding="utf-8")
    cleaned = clean_fences(content)

    if cleaned != content:

        if create_backup:
            backup = path.with_suffix(path.suffix + ".bak")
            backup.write_text(content, encoding="utf-8")

        path.write_text(cleaned, encoding="utf-8")
        return True

    return False
def find_backup_files(target: Path):

    if target.is_file():

        bak = Path(str(target) + ".bak")

        return [bak] if bak.exists() else []

    if target.is_dir():

        return list(target.rglob("*.md.bak"))

    return []


class CleanerGUI:

    def __init__(self, root):

        self.root = root
        self.root.title("Markdown Fence Cleaner")
        self.root.geometry("900x600")

        self.target = None
        self.files_to_modify = []

        self.build_ui()

    def build_ui(self):

        top = tk.Frame(self.root)
        top.pack(fill="x", padx=10, pady=10)

        self.path_var = tk.StringVar()

        tk.Entry(
            top,
            textvariable=self.path_var
        ).pack(fill="x", pady=(0, 5))

        button_row = tk.Frame(top)
        button_row.pack(fill="x")

        tk.Button(
            button_row,
            text="Select File",
            command=self.select_file
        ).pack(side="left", padx=2)

        tk.Button(
            button_row,
            text="Select Folder",
            command=self.select_folder
        ).pack(side="left", padx=2)

        tk.Button(
            button_row,
            text="Scan",
            command=self.scan_target
        ).pack(side="left", padx=10)

        tk.Button(
            button_row,
            text="Find Backups",
            command=self.find_backups
        ).pack(side="left", padx=2)

        self.clean_button = tk.Button(
            button_row,
            text="Clean",
            state="disabled",
            command=self.clean_files
        )

        tk.Button(
            button_row,
            text="Delete Backups",
            command=self.delete_backups
        ).pack(side="left", padx=2)

        self.backup_var = tk.BooleanVar(value=True)

        tk.Checkbutton(
            button_row,
            text="Create Backups",
            variable=self.backup_var
        ).pack(side="right", padx=10)

        self.clean_button.pack(side="right")

        self.summary_label = tk.Label(
            self.root,
            anchor="w",
            justify="left",
            text="No folder selected."
        )

        self.summary_label.pack(
            fill="x",
            padx=10,
            pady=(0, 5)
        )

        self.results = scrolledtext.ScrolledText(
            self.root,
            wrap=tk.NONE
        )

        self.results.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=(0, 10)
        )

    def select_file(self):

        filename = filedialog.askopenfilename(
            title="Select Markdown File",
            filetypes=[("Markdown files", "*.md")]
        )

        if filename:
            self.target = Path(filename)
            self.path_var.set(filename)
            self.clean_button.config(state="disabled")

    def select_folder(self):

        folder = filedialog.askdirectory(
            title="Select Folder"
        )

        if folder:
            self.target = Path(folder)
            self.path_var.set(folder)
            self.clean_button.config(state="disabled")

    def log(self, text):

        self.results.insert(tk.END, text + "\n")

    def scan_target(self):

        self.results.delete("1.0", tk.END)
        self.clean_button.config(state="disabled")
        self.files_to_modify = []

        if not self.target:

            messagebox.showwarning(
                "No Selection",
                "Select a file or folder first."
            )

            return

        all_files = find_markdown_files(self.target)

        if not all_files:

            self.summary_label.config(
                text="No markdown files found."
            )

            return

        already_clean = []

        for file in all_files:

            try:

                match_info = find_first_match(file)

                if match_info:

                    self.files_to_modify.append(file)

                    lineno, text, reason = match_info

                    self.log(f"MODIFY: {file}")
                    self.log(f"  Reason : {reason}")
                    self.log(f"  Line   : {lineno}")
                    self.log(f"  Match  : {text}")
                    self.log("")

                else:
                    already_clean.append(file)

            except Exception as e:

                self.log(f"ERROR: {file}")
                self.log(f"       {e}")
                self.log("")

        self.summary_label.config(
            text=(
                f"Markdown files found: {len(all_files)}    "
                f"Need cleaning: {len(self.files_to_modify)}    "
                f"Already clean: {len(already_clean)}"
            )
        )

        if self.files_to_modify:
            self.clean_button.config(state="normal")
        else:
            self.log("All markdown files are already clean.")

    def clean_files(self):

        if not self.files_to_modify:
            return

        backup_msg = (
    "Backup files (*.bak) will be created."
    if self.backup_var.get()
    else
    "No backup files will be created."
)

        answer = messagebox.askyesno(
            "Confirm",
            (
                f"Modify {len(self.files_to_modify)} file(s)?\n\n"
                f"{backup_msg}"
            )
        )

        if not answer:
            return

        cleaned_count = 0
        errors = 0

        self.results.delete("1.0", tk.END)

        for file in self.files_to_modify:

            try:

                if clean_file(
                        file,
                        create_backup=self.backup_var.get()
                    ):
                    cleaned_count += 1
                    self.log(f"✓ {file}")

            except Exception as e:

                errors += 1
                self.log(f"✗ {file}")
                self.log(f"    {e}")

        self.log("")
        self.log(
            f"Finished. Modified {cleaned_count} file(s)."
        )

        if errors:
            self.log(f"Errors: {errors}")

        self.clean_button.config(state="disabled")

        messagebox.showinfo(
            "Done",
            f"Modified {cleaned_count} file(s)."
        )

        self.scan_target()

    def find_backups(self):

        self.results.delete("1.0", tk.END)

        if not self.target:
            return

        backups = find_backup_files(self.target)

        if not backups:
            self.log("No backup files found.")
            return

        self.log(f"Found {len(backups)} backup files:")
        self.log("")

        for bak in backups:
            self.log(str(bak))

    def delete_backups(self):

        if not self.target:
            return

        backups = find_backup_files(self.target)

        if not backups:

            messagebox.showinfo(
                "No Backups",
                "No backup files found."
            )

            return

        answer = messagebox.askyesno(
            "Delete Backups",
            (
                f"Delete {len(backups)} backup file(s)?\n\n"
                "This cannot be undone."
            )
        )

        if not answer:
            return

        deleted = 0

        for bak in backups:

            try:
                bak.unlink()
                deleted += 1

            except Exception as e:
                self.log(f"ERROR deleting {bak}: {e}")

        messagebox.showinfo(
            "Done",
            f"Deleted {deleted} backup file(s)."
        )

        self.find_backups();

        self.summary_label.config(
            text=f"Backup files remaining: {len(find_backup_files(self.target))}"
        )


def main():

    root = tk.Tk()
    CleanerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()