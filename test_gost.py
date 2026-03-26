from fix_spaces import fix_spaces
from fix_special_headings import fix_special_headings_text, is_special, canonical_form

RESET  = '\033[0m'
GREEN  = '\033[92m'
RED    = '\033[91m'
YELLOW = '\033[93m'
BOLD   = '\033[1m'

passed = 0
failed = 0


def check(label: str, result: str, expected: str):
    global passed, failed
    if result == expected:
        print(f'{GREEN}OK{RESET}  {label}')
        passed += 1
    else:
        print(f'{RED}FAIL{RESET} {label}')
        print(f'     ожидалось: {expected!r}')
        print(f'     получено:  {result!r}')
        failed += 1


print(f'\n{BOLD}=== fix_spaces ==={RESET}\n')

check('двойные пробелы',
      fix_spaces('Текст  с   пробелами'),
      'Текст с пробелами')

check('пробел перед точкой',
      fix_spaces('Конец .'),
      'Конец.')

check('пробел перед запятой',
      fix_spaces('один , два'),
      'один, два')

check('пробел перед двоеточием',
      fix_spaces('итого :'),
      'итого:')

check('пробел после запятой',
      fix_spaces('один,два'),
      'один, два')

check('пробел внутри скобок',
      fix_spaces('( текст )'),
      '(текст)')

check('пробел перед %',
      fix_spaces('50 %'),
      '50%')

check('пробел перед °',
      fix_spaces('90 °'),
      '90°')

check('неразрывный пробел перед кг',
      fix_spaces('5 кг'),
      '5\u00a0кг')

check('неразрывный пробел перед мм',
      fix_spaces('10 мм'),
      '10\u00a0мм')

check('strip строки',
      fix_spaces('  текст  '),
      'текст')

check('комплексный случай',
      fix_spaces('Масса  детали ( с покрытием )  равна 5 кг .'),
      'Масса детали (с покрытием) равна 5\u00a0кг.')


print(f'\n{BOLD}=== fix_special_headings ==={RESET}\n')

check('is_special: введение',
      str(is_special('введение')),
      'True')

check('is_special: Введение с точкой',
      str(is_special('Введение.')),
      'True')

check('is_special: 1. Введение.',
      str(is_special('1. Введение.')),
      'True')

check('is_special: обычный заголовок',
      str(is_special('Методология исследования')),
      'False')

check('is_special: Приложение А',
      str(is_special('Приложение А')),
      'True')

check('canonical_form: введение',
      canonical_form('введение'),
      'ВВЕДЕНИЕ')

check('canonical_form: 1. Заключение.',
      canonical_form('1. Заключение.'),
      'ЗАКЛЮЧЕНИЕ')

check('canonical_form: Список литературы.',
      canonical_form('Список литературы.'),
      'СПИСОК ЛИТЕРАТУРЫ')

check('canonical_form: Приложение б',
      canonical_form('Приложение б'),
      'ПРИЛОЖЕНИЕ Б')

check('text: убирает номер и точку',
      fix_special_headings_text('# 1. Введение.'),
      '# ВВЕДЕНИЕ')

check('text: нижний регистр',
      fix_special_headings_text('# заключение'),
      '# ЗАКЛЮЧЕНИЕ')

check('text: обычный заголовок не трогает',
      fix_special_headings_text('# 2 Методология'),
      '# 2 Методология')

check('text: несколько строк',
      fix_special_headings_text('# 1. Введение.\n## 1.1 Общие положения\n# Заключение.'),
      '# ВВЕДЕНИЕ\n## 1.1 Общие положения\n# ЗАКЛЮЧЕНИЕ')

check('text: без uppercase',
      fix_special_headings_text('# Введение', force_uppercase=False),
      '# Введение')


print(f'\n{BOLD}Итого: {GREEN}{passed} OK{RESET}{BOLD}  {RED}{failed} FAIL{RESET}\n')
