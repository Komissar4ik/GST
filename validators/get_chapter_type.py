import re

def get_chapter_type(paragraph):
    """
    Определяет тип главы:
    - "gost": правильная глава ("ГЛАВА 1. ...")
    - "bad": глава без слова "ГЛАВА" (например, "1 ТЕКСТ")
    - "no_dot": глава без точки ("ГЛАВА 1 Анализ ...")
    - None: не глава
    """
    text = paragraph.text.strip()
    uptext = text.upper()
    if re.match(r'^ГЛАВА\s+\d+\.\s+.+', uptext):
        return "gost"
    elif re.match(r'^\d+\s+[A-ZА-ЯЁ]', uptext) and not re.match(r'^\d+\.\d+', uptext):
        return "bad"
    elif re.match(r'^ГЛАВА\s+\d+\s+[^\d\W]', text, re.IGNORECASE):
        return "no_dot"
    else:
        return None