# MarkTidy 🪄

MarkTidy is a web-based Markdown text processing tool built with Streamlit that helps you clean and format your Markdown content.

## Features

- 🧹 **Clean Up Operations**
  - Remove blank lines in lists
  - Remove links while preserving link text
  - Remove images
  - Remove bold formatting
  - Fix bold-ending symbols

- 🔠 **Heading Management**
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
   - Toggle "Remove blank lines in list" to eliminate empty lines within lists
   - Toggle "🔗 Remove links" to keep only link text
   - Toggle "🖼️ Remove images" to remove image elements
   - Toggle "Fix **bold** formatting" to fix bold text ending with symbols
   - Toggle "Remove **bold** formatting" to remove bold formatting
3. Structure options:
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
