import streamlit as st
import re

st.set_page_config(page_title="MarkTidy", layout="wide")

st.sidebar.header("🪄 MarkTidy")

# --- Sidebar inputs ---
# The app will rerun every time the input text is changed.
input_text = st.sidebar.text_area("Enter text", height=250, placeholder="Enter markdown text here...", label_visibility="collapsed")

# Removed the 'Convert' button.

# --- Cleanup Options ---
# The app will rerun every time an option is changed.
remove_blank_lines = st.sidebar.checkbox("Remove blank lines in list", value=True)
remove_links = st.sidebar.checkbox("🔗 Remove links", value=True)
remove_images = st.sidebar.checkbox("🖼️ Remove images", value=True)
fix_bold_symbols = st.sidebar.checkbox("**Fix bold** formatting", value=True)
remove_bold = st.sidebar.checkbox("**Remove bold** formatting")

# --- Structure Options ---
auto_number_headings = st.sidebar.checkbox("🔢 Auto-number headings", value=False)
heading_shift = st.sidebar.slider("🔠 Adjust heading level", min_value=-3, max_value=3, value=0)

# --- Helper functions ---

def shift_headings(md_text: str, direction: str) -> str:
    """Adjusts heading levels. direction = '+1' or '-1'"""
    lines = md_text.splitlines()
    new_lines = []
    for line in lines:
        if line.strip().startswith("#"):
            match = re.match(r"^(#+)(\s*)(.*)", line)
            if match:
                hashes, space, content = match.groups()
                level = len(hashes)
                if direction == "+1" and level < 6:
                    level += 1
                elif direction == "-1" and level > 1:
                    level -= 1
                line = "#" * level + space + content
        new_lines.append(line)
    return "\n".join(new_lines)


def fix_bold_symbol_issue(md_text: str) -> str:
    """
    If **bold text** ends with a symbol (!, %, ), ., ?, :, ;, etc.,
    add a space after ** to prevent rendering issues.
    """
    # Pattern: **content(symbol)** → **content(symbol)**␣
    return re.sub(r"(\*\*[^\*]*[\W]\*\*)(?!\s)", r"\1 ", md_text)

def number_headings(md_text: str) -> str:
    """
    Automatically adds numbers (e.g., 1., 1.1, 2.) based on heading hierarchy.
    H1(#) is left unchanged, numbering starts from H2(##).
    Ignores content within code blocks.
    """
    lines = md_text.splitlines()
    new_lines = []

    # Track current numbers (H2 ~ H6)
    # Index = heading level - 2 (0: H2, 4: H6)
    counters = [0] * 5
    in_code_block = False

    for line in lines:
        stripped_line = line.strip()

        # Toggle code block
        if stripped_line.startswith("```"):
            in_code_block = not in_code_block
            new_lines.append(line)
            continue

        if in_code_block:
            new_lines.append(line)
            continue

        match = re.match(r"^(#+)(\s*)(.*)", line)
        if match:
            hashes, space, content = match.groups()
            level = len(hashes)  # 1 (H1) to 6 (H6)

            if level == 1:
                # Reset all counters when a new H1 is encountered
                counters = [0] * 5
                new_lines.append(line)  # Keep H1 unchanged
                continue

            if 2 <= level <= 6:
                # 1. Reset all counters lower than the current level
                for i in range(level-1, 5):
                    counters[i] = 0

                # 2. Increment the current level counter
                counters[level-2] += 1

                # 3. Generate number string (e.g., 1.2.3.)
                number_parts = [str(c) for c in counters[:level-1] if c > 0]
                number_prefix = ".".join(number_parts) + "."

                # 4. Remove existing numbers and add new numbers
                content_clean = re.sub(r"^(\d+\.)+\s*", "", content.strip())
                new_line = f"{'#' * level}{space}{number_prefix} {content_clean.strip()}"
                new_lines.append(new_line)
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)

    return "\n".join(new_lines)


# --- Processing logic ---
output_text = input_text

# Execute the conversion logic only if there is input text.
if input_text.strip():
    # 1. Basic cleanup tasks
    lines = output_text.splitlines()

    if remove_blank_lines:
        # Apply blank line removal only within lists
        new_lines = []
        in_list = False
        last_list_index = -1
        
        # First pass: find the last list item
        for i, line in enumerate(lines):
            if line.strip().startswith("- ") or line.strip().startswith("* "):
                last_list_index = i

        # Second pass: process lines
        for i, line in enumerate(lines):
            if line.strip().startswith("- ") or line.strip().startswith("* "):
                in_list = True
                new_lines.append(line)
            elif in_list and line.strip() == "":
                # Keep blank line if it's after the last list item
                if i > last_list_index:
                    new_lines.append(line)
                # Skip blank lines within the list
                continue
            else:
                in_list = False
                new_lines.append(line)
        lines = new_lines

    if remove_bold:
        lines = [re.sub(r"\*\*(.*?)\*\*", r"\1", line) for line in lines]

    if remove_links:
        lines = [re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", line) for line in lines]

    if remove_images:
        lines = [re.sub(r"!\[.*?\]\([^)]+\)", "", line) for line in lines]

    output_text = "\n".join(lines)

    # Fix bold formatting issues
    if fix_bold_symbols:
        output_text = fix_bold_symbol_issue(output_text)

    # Adjust heading levels
    if heading_shift != 0:
        direction = "+1" if heading_shift > 0 else "-1"
        for _ in range(abs(heading_shift)):
            output_text = shift_headings(output_text, direction)

    # Auto-number headings (best applied last)
    if auto_number_headings:
        output_text = number_headings(output_text)

# --- Main layout ---
col1, col2 = st.columns(2)  # Create two columns

with col1:
    st.markdown(output_text, unsafe_allow_html=True)

with col2:
    st.code(output_text, language="markdown")

# Initial state guidance message
if not input_text.strip():
    st.info("Enter markdown text in the left sidebar to see the results displayed here automatically.")
