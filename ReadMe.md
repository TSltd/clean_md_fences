# clean-md-fences

Small utility script for cleaning ChatGPT-style Markdown code fences.

It removes unwanted `id="..."` attributes from fenced code blocks and normalizes `text` / `markdown` fences.

---

## What It Does

Transforms code fences like this:

````
```text id="a1b2c3"
hello
```
````

Into:

````
```
hello
```
````

And transforms:

````
```json id="cdctex"
{
"hello": "world"
}
```
````

Into:

````
```json
{
"hello": "world"
}
```
````

---

## Rules

### `text` and `markdown`

These language tags are removed completely.

Examples:

````
```text id="abc"

```

```
````

→

````
```
```
````

````
```markdown id="xyz"

```
````

→

````
```

```
````

---

### Other Languages

The language is preserved, but the `id="..."` attribute is removed.

Example:

````
```json id="123"

```
````

→

````
```json

```
````

---

## Installation

Clone the repository:

```bash
git clone https://github.com/yourname/clean-md-fences.git
cd clean-md-fences
```

Make the script executable (optional):

```bash
chmod +x clean_md.py
```

---

## Usage

### Process a File

```bash
python clean_md.py input.md > output.md
```

### Pipe Input

```bash
cat input.md | python clean_md.py
```

### In-place Editing (Linux/macOS)

```bash
python clean_md.py input.md > tmp.md && mv tmp.md input.md
```

---

## Example

### Input

````
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

````
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

- Python 3.7+

No external dependencies required.

---

## License

MIT
