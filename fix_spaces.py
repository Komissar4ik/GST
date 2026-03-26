import re

_UNITS = (
    'кг', 'г', 'т', 'мг',
    'км', 'м', 'см', 'мм', 'нм',
    'л', 'мл',
    'кВт', 'Вт', 'МВт',
    'А', 'мА', 'В', 'мВ', 'кВ',
    'Гц', 'кГц', 'МГц', 'ГГц',
    'ч', 'мин', 'с', 'мс',
    'руб', 'тыс', 'млн', 'млрд',
    'шт', 'экз',
)
_UNITS_RE = '|'.join(re.escape(u) for u in sorted(_UNITS, key=len, reverse=True))


def fix_multiple_spaces(text: str) -> str:
    return re.sub(r'[ \t]{2,}', ' ', text)


def fix_space_before_punct(text: str) -> str:
    return re.sub(r'\s+([,\.;:!?])', r'\1', text)


def fix_space_after_punct(text: str) -> str:
    return re.sub(r'([,;:!?])(?=[^\s])', r'\1 ', text)


def fix_bracket_spaces(text: str) -> str:
    text = re.sub(r'\(\s+', '(', text)
    text = re.sub(r'\s+\)', ')', text)
    return text


def fix_percent_degree_space(text: str) -> str:
    text = re.sub(r'(\d)\s+%', r'\1%', text)
    text = re.sub(r'(\d)\s+°', r'\1°', text)
    return text


def fix_nbsp_before_units(text: str) -> str:
    return re.sub(rf'(\d)\s+({_UNITS_RE})(?=\b)', lambda m: m.group(1) + '\u00a0' + m.group(2), text)


def fix_strip_lines(text: str) -> str:
    return '\n'.join(line.strip() for line in text.splitlines())


def fix_spaces(text: str) -> str:
    text = fix_strip_lines(text)
    text = fix_multiple_spaces(text)
    text = fix_space_before_punct(text)
    text = fix_space_after_punct(text)
    text = fix_bracket_spaces(text)
    text = fix_percent_degree_space(text)
    text = fix_nbsp_before_units(text)
    return text
