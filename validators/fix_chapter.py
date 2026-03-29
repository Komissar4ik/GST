import re
from .apply_heading_style import apply_heading_style

def fix_chapter(paragraph, num, chapter_type):
    """
    Приводит разные типы глав к формату ГОСТ.
    """
    text = paragraph.text.strip()
    if chapter_type == "bad":
        m = re.match(r'^(\d+)\s+(.+)$', text)
        if m:
            title = m.group(2).capitalize()
            new_text = f'ГЛАВА {num}. {title}'
            apply_heading_style(paragraph, new_text)
    elif chapter_type == "no_dot":
        m = re.match(r'^(ГЛАВА)\s+(\d+)\s+(.+)$', text, re.IGNORECASE)
        if m:
            title = m.group(3).capitalize()
            new_text = f'ГЛАВА {num}. {title}'
            apply_heading_style(paragraph, new_text)