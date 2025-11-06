import streamlit as st
import re

# Configure the Streamlit page layout
st.set_page_config(page_title="MarkTidy", layout="wide")

# Create the sidebar header
st.sidebar.header("🪄 MarkTidy")

# --- Sidebar Configuration Section ---
# Text input area for markdown content
input_text = st.sidebar.text_area("Enter text", height=250, placeholder="Enter markdown text here...", label_visibility="collapsed")

# --- Cleanup Options Section ---
# Toggle switches for various markdown cleanup operations
clear_formatting = st.sidebar.checkbox("Clear all formatting")
remove_blank_lines = st.sidebar.checkbox("Remove blank lines in list", value=True)
remove_links = st.sidebar.checkbox("🔗 Remove links")
remove_images = st.sidebar.checkbox("🖼️ Remove images", value=True)
remove_bold = st.sidebar.checkbox("**Remove bold** formatting")
fix_bold_symbols = st.sidebar.checkbox("**Fix bold** formatting issues", value=True)
remove_strikethrough = st.sidebar.checkbox("~~Remove strikethrough~~ formatting")
remove_horizontal = st.sidebar.checkbox("Remove horizontal rules")

# --- Document Structure Options Section ---
extract_heading = st.sidebar.checkbox("Extract headings only")
remove_plain_text = st.sidebar.checkbox("Remove plain text")
auto_number_headings = st.sidebar.checkbox("🔢 Auto-number headings", value=False)
heading_shift = st.sidebar.slider("🔠 Adjust heading level", min_value=-3, max_value=3, value=0)

# --- Helper Functions ---

def shift_headings(md_text: str, direction: str) -> str:
    """
    Adjusts the level of markdown headings up or down.
    
    Args:
        md_text: Input markdown text
        direction: Either '+1' to increase or '-1' to decrease heading level
    
    Returns:
        Modified markdown text with adjusted heading levels
    """
    lines = md_text.splitlines()
    new_lines = []
    for line in lines:
        if line.strip().startswith("#"):
            match = re.match(r"^(#+)(\s*)(.*)", line)
            if match:
                hashes, space, content = match.groups()
                level = len(hashes)
                # Ensure heading level stays within valid range (1-6)
                if direction == "+1" and level < 6:
                    level += 1
                elif direction == "-1" and level > 1:
                    level -= 1
                line = "#" * level + space + content
        new_lines.append(line)
    return "\n".join(new_lines)

def fix_bold_symbol_issue(md: str) -> str:
    """
    Fixes markdown bold formatting issues by ensuring proper spacing.
    
    Args:
        md: Input markdown text
    
    Returns:
        Markdown text with corrected bold symbol spacing
    """
    pattern = re.compile(r'\*\*(.+?)\*\*(\s*)', re.DOTALL)

    def repl(m):
        inner = m.group(1)
        after = m.group(2)
        # Add space after ** if content contains symbols and no space exists
        if re.search(r'[^0-9A-Za-z\s]', inner) and after == '':
            return f'**{inner}** '
        return m.group(0)

    return pattern.sub(repl, md)

def remove_paragraph(md_text: str) -> str:
    """
    Removes paragraphs, blockquotes, and code blocks from markdown text.
    It preserves headings, lists, horizontal rules, and blank lines.

    Args:
        md_text: Input markdown text.

    Returns:
        Markdown text with specified elements removed.
    """
    lines = md_text.splitlines()
    new_lines = []
    in_code_block = False

    for line in lines:
        stripped_line = line.strip()

        if stripped_line.startswith("```"):
            in_code_block = not in_code_block
            continue

        if in_code_block:
            continue

        # Preserve headings, lists, horizontal rules, and blank lines
        if (stripped_line.startswith("#") or
            stripped_line.startswith(("- ", "* ")) or
            re.match(r"^\d+\.\s", stripped_line) or
            re.match(r"^\s*([-*_]){3,}\s*$", stripped_line) or
            not stripped_line):
            new_lines.append(line)

    return "\n".join(new_lines)

def number_headings(md_text: str) -> str:
    """
    Automatically numbers markdown headings hierarchically.
    H1 headings are preserved without numbers, numbering starts from H2.
    
    Args:
        md_text: Input markdown text
    
    Returns:
        Markdown text with numbered headings
    """
    lines = md_text.splitlines()
    new_lines = []
    
    # Initialize counters for heading levels H2-H6
    counters = [0] * 5
    in_code_block = False

    for line in lines:
        stripped_line = line.strip()

        # Handle code block boundaries
        if stripped_line.startswith("```"):
            in_code_block = not in_code_block
            new_lines.append(line)
            continue

        # Skip processing within code blocks
        if in_code_block:
            new_lines.append(line)
            continue

        # Process headings
        match = re.match(r"^(#+)(\s*)(.*)", line)
        if match:
            hashes, space, content = match.groups()
            level = len(hashes)

            if level == 1:
                # Reset counters for H1 and keep unchanged
                counters = [0] * 5
                new_lines.append(line)
                continue

            if 2 <= level <= 6:
                # Reset lower level counters
                for i in range(level-1, 5):
                    counters[i] = 0

                # Increment current level counter
                counters[level-2] += 1

                # Generate heading number
                number_parts = [str(c) for c in counters[:level-1] if c > 0]
                number_prefix = ".".join(number_parts) + "."

                # Apply new heading format
                content_clean = re.sub(r"^(\d+\.)+\s*", "", content.strip())
                new_line = f"{'#' * level}{space}{number_prefix} {content_clean.strip()}"
                new_lines.append(new_line)
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)

    return "\n".join(new_lines)

def remove_blank_lines_between_list_items(lines: list[str]) -> list[str]:
    """
    Removes empty lines between list items while preserving other blank lines.
    
    Args:
        lines: List of strings representing markdown text lines
        
    Returns:
        List of strings with unnecessary blank lines removed
    """
    new_lines = []
    is_list_item_flags = []
    
    # First pass: mark all list items
    for line in lines:
        is_list_item_flags.append(
            line.strip().startswith("- ") or 
            line.strip().startswith("* ") or 
            re.match(r"^\d+\.\s", line.strip())
        )
    
    # Second pass: remove blank lines between list items
    for i, line in enumerate(lines):
        prev_line_was_list_item = is_list_item_flags[i-1] if i > 0 else False
        current_line_is_blank = line.strip() == ""
        next_line_is_list_item = is_list_item_flags[i+1] if i < len(lines) - 1 else False
        
        # Skip blank lines only between list items
        if current_line_is_blank and prev_line_was_list_item and next_line_is_list_item:
            continue
            
        new_lines.append(line)
    
    return new_lines

def clear_markdown_format(md_text: str) -> str:
    """
    Removes all common markdown formatting from the text.

    Args:
        md_text: Input markdown text.

    Returns:
        Text with markdown formatting removed.
    """
    # 1. Remove images, keeping alt text
    md_text = re.sub(r"!\[([^\]]*)\]\([^)]+\)", r"\1", md_text)
    # 2. Remove links, keeping link text
    md_text = re.sub(r"\[([^\]]*)\]\([^)]+\)", r"\1", md_text)
    # 3. Remove bold, italic, strikethrough, and inline code
    md_text = re.sub(r"\*\*(.*?)\*\*", r"\1", md_text)  # Bold
    md_text = re.sub(r"__(.*?)__", r"\1", md_text)    # Bold
    md_text = re.sub(r"\*(.*?)\*", r"\1", md_text)      # Italic
    md_text = re.sub(r"_(.*?)_", r"\1", md_text)      # Italic
    md_text = re.sub(r"~~(.*?)~~", r"\1", md_text)    # Strikethrough
    md_text = re.sub(r"`(.*?)`", r"\1", md_text)        # Inline code

    lines = md_text.splitlines()
    new_lines = []
    for line in lines:
        # 4. Remove headings
        line = re.sub(r"^#+\s*", "", line)
        # 5. Remove list markers
        line = re.sub(r"^\s*([\*\-\+]|\d+\.)\s+", "", line)
        # 6. Remove blockquotes
        line = re.sub(r"^\s*>\s?", "", line)
        # 7. Remove horizontal rules
        if re.match(r"^\s*([-*_]){3,}\s*$", line):
            continue
        new_lines.append(line)

    return "\n".join(new_lines)


def extract_headings(md_text: str) -> str:
    """
    Extracts only the heading lines from markdown text.

    Args:
        md_text: Input markdown text.

    Returns:
        String containing only the heading lines.
    """
    lines = md_text.splitlines()
    heading_lines = []
    in_code_block = False

    for line in lines:
        stripped_line = line.strip()

        if stripped_line.startswith("```"):
            in_code_block = not in_code_block
            continue

        if in_code_block:
            continue

        # Preserve headings
        if stripped_line.startswith("#"):
            heading_lines.append(line)

    return "\n".join(heading_lines)


# --- Main Processing Logic ---
output_text = input_text

if input_text.strip():
    if extract_heading:
        output_text = extract_headings(output_text)

    # Convert input to lines for processing
    lines = output_text.splitlines()

    # Apply selected cleanup operations
    if remove_blank_lines:
        lines = remove_blank_lines_between_list_items(lines)

    if remove_bold:
        lines = [re.sub(r"\*\*(.*?)\*\*", r"\1", line) for line in lines]

    if remove_links:
        lines = [re.sub(r"\[([^\]]*)\]\([^)]+\)", r"\1", line) for line in lines]

    if remove_images:
        lines = [re.sub(r"!\[.*?\]\([^)]+\)", "", line) for line in lines]

    if remove_strikethrough:
        lines = [re.sub(r"~~(.*?)~~", r"\1", line) for line in lines]

    # Reconstruct text from processed lines
    output_text = "\n".join(lines)

    # Apply formatting fixes
    if fix_bold_symbols:
        output_text = fix_bold_symbol_issue(output_text)

    if remove_horizontal:
        output_text = re.sub(r"^\s*([-*_]){3,}\s*$", "", output_text, flags=re.MULTILINE)

    # Apply heading modifications
    if heading_shift != 0:
        direction = "+1" if heading_shift > 0 else "-1"
        for _ in range(abs(heading_shift)):
            output_text = shift_headings(output_text, direction)

    if remove_plain_text:
        output_text = remove_paragraph(output_text)

    # Apply heading numbers last to ensure correct numbering
    if auto_number_headings:
        output_text = number_headings(output_text)

    if clear_formatting:
        # Clear all other formatting if this option is selected
        output_text = clear_markdown_format(output_text)

# --- Display Section ---
if not input_text.strip():
    st.info("Enter markdown text in the left sidebar to see the results displayed here automatically.")
else:
    # Create side-by-side view of rendered and raw markdown
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(output_text, unsafe_allow_html=True)
    with col2:
        st.code(output_text, language="markdown")
