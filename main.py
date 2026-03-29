import sys
from validators.format_document_headings_strict import format_document_headings_strict

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Использование: python main.py <входной_файл.docx> <выходной_файл.docx>")
        sys.exit(1)
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    format_document_headings_strict(input_file, output_file)
    print(f"Готово! Результат сохранён в {output_file}")