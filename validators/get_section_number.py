import re

def get_section_number(paragraph):
    # Возвращает номер раздела в виде строки и списка целых чисел
    m = re.match(r'^((\d+(?:\.\d+)+))\s+\S', paragraph.text.strip())
    num_str = m.group(1) if m else None
    num_list = list(map(int, num_str.split('.'))) if num_str else None
    return num_str, num_list