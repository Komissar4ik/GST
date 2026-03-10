import re

def fix_dashes(text):

    # диапазоны чисел
    text = re.sub(r'(?<=\d)-(?=\d)', '–', text)

    # тире между словами
    text = re.sub(r'\s-\s', ' — ', text)

    return text