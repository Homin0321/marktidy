# MarkTidy 🪄

MarkTidy is a web-based Markdown text processing tool built with Streamlit that helps you clean and format your Markdown content.

## Features

- 🧹 **Clean Up Operations**
  - Clear all formatting
  - Remove blank lines in lists
  - Remove links while preserving link text
  - Remove images
  - Remove bold formatting
  - Fix bold-ending symbols
  - Fix strikethrough formatting
  - Remove horizontal rules

- 🔠 **Document Structure & Headings**
  - Extract headings only
  - Remove plain text
  - Shift heading levels up or down (±3 levels)
  - Automatic heading numbering (1., 1.1., 2., etc.)

## Installation

1. Clone this repository
2. Install dependencies:
```bash
pip install streamlit
```
3. Run the application:
```bash
streamlit run app.py
```

## Usage

1. Enter or paste your Markdown text in the sidebar text area
2. Select desired cleanup operations:
   - Toggle "Clear all formatting" to remove all markdown syntax
   - Toggle "Remove blank lines in list" to eliminate empty lines within lists
   - Toggle "🔗 Remove links" to keep only link text
   - Toggle "🖼️ Remove images" to remove image elements
   - Toggle "Remove **bold** formatting" to remove bold formatting
   - Toggle "**Fix bold** formatting issues" to fix bold text ending with symbols
   - Toggle "Fix ~~strikethrough~~ formatting" to standardise strikethrough syntax
   - Toggle "Remove horizontal rules" to delete horizontal lines
3. Structure options:
   - Toggle "Extract headings only" to keep only headings
   - Toggle "Remove plain text" to keep structure but remove content
   - Toggle "🔢 Auto-number headings" for automatic section numbering
   - Use the slider to adjust heading levels (±3 levels)

The results will update automatically as you type or change options.

## Output

The application displays two columns:
- Left: Rendered Markdown preview
- Right: Processed Markdown source code

## Example

Input:
```markdown
# My Document

This is a **test!**

[Link](https://example.com)
![Image](image.jpg)
```

Output (with all cleanup options enabled):
```markdown
# My Document
This is a test!
Link
```

## License

MIT License

## Contributing

Feel free to open issues and pull requests!
