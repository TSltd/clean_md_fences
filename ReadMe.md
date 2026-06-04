![Platform](https://img.shields.io/badge/platform-linux-blue)
![License](https://img.shields.io/badge/license-MIT-green)

# clean-md-fences

A desktop utility for cleaning ChatGPT-style Markdown code fences.

It removes unwanted `id="..."` attributes from fenced code blocks and normalizes `text` / `markdown` fences while preserving all other language identifiers.

Available as:

- Python source
- Standalone Linux AppImage
- PyInstaller executable

---

## Features

- Recursive folder scanning
- Processes entire Markdown documentation repositories
- Preview files before modification
- Shows the first matching fence that triggered detection
- Optional backup creation (`.bak` files)
- Backup discovery and cleanup tools
- Supports:
  - ` ```text `
  - ` ```markdown `
  - ` ```python id="..." `
  - ` ```json id="..." `
  - Any other fenced language

- Preserves original line endings
- Standalone GUI application (Tkinter)
- Linux AppImage distribution

---

## What It Does

Transforms:

````markdown
```text id="a1b2c3"
hello
```
````

Into:

````markdown
```
hello
```
````

And transforms:

````markdown
```json id="cdctex"
{
  "hello": "world"
}
```
````

Into:

````markdown
```json
{
  "hello": "world"
}
```
````

---

## Rules

### `text` and `markdown`

Language identifiers are removed entirely.

Example:

````markdown
```text id="abc"
example
```
````

becomes:

````markdown
```
example
```
````

And:

````markdown
```markdown id="xyz"
example
```
````

becomes:

````markdown
```
example
```
````

---

### Other Languages

The language identifier is preserved.

Only the `id="..."` attribute is removed.

Example:

````markdown
```python id="abc123"
print("hello")
```
````

becomes:

````markdown
```python
print("hello")
```
````

---

## GUI Usage

Launch the application:

```bash
python clean_md_v2.py
```

### Workflow

1. Select a file or folder.
2. Click **Scan**.
3. Review files that will be modified.
4. Click **Clean**.
5. Optionally create backups.
6. Optionally remove backups after verification.

### Backup Management

When enabled, backups are created as:

```text
README.md.bak
guide.md.bak
api.md.bak
```

The application can:

- Find backup files
- Display backup files
- Delete backup files

---

## Linux AppImage

A standalone AppImage is available from the GitHub Releases page:

https://github.com/TSltd/clean_md_fences/releases/tag/v1.0.0

Download:

```text
MarkdownFenceCleaner-x86_64.AppImage
```

Make executable:

```bash
chmod +x MarkdownFenceCleaner-x86_64.AppImage
```

Run:

```bash
./MarkdownFenceCleaner-x86_64.AppImage
```

No Python installation is required.

---

## Building from Source

Create a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install build tools:

```bash
pip install pyinstaller
```

Build:

```bash
pyinstaller \
  --onefile \
  --windowed \
  --name MarkdownFenceCleaner \
  clean_md_v2.py
```

Result:

```text
dist/MarkdownFenceCleaner
```

---

## Example

### Input

````markdown
```text id="a1b2c3"
Define runtime semantic contracts
```

```json id="cdctex"
{
  "capability": "reassure"
}
```
````

### Output

````markdown
```
Define runtime semantic contracts
```

```json
{
  "capability": "reassure"
}
```
````

---

## Requirements

### Running from Source

- Python 3.8+

### Standalone AppImage

No dependencies required.

---

## License

MIT
