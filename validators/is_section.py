import re

def is_section(paragraph):
    # Проверяет: это подзаголовок раздела ("1.1 ...", "1.2.1 ...", и т.д.)
    return re.match(r'^(\d+(\.\d+)+)\s+\S', paragraph.text.strip()) is not None