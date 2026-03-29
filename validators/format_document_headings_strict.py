from docx import Document
import re
from .get_chapter_type import get_chapter_type
from .fix_chapter import fix_chapter
from .apply_heading_style import apply_heading_style
from .is_section import is_section
from .get_section_number import get_section_number
from .strict_sequence_check import strict_sequence_check

def format_document_headings_strict(docx_path, output_path):
    """
    Открывает входной docx, проходит по каждому абзацу, и приводит главы/подглавы к ГОСТ-формату.
    """
    doc = Document(docx_path)

    in_main_part = False
    prev_was_chapter = False
    current_chapter = None
    all_section_numbers = []
    expected_chapter_num = 1

    for para in doc.paragraphs:
        text = para.text.strip()
        uptext = text.upper()

        if uptext == "ВВЕДЕНИЕ":
            in_main_part = True
            current_chapter = None
            prev_was_chapter = False
            all_section_numbers.clear()
            expected_chapter_num = 1
            continue
        if uptext == "ЗАКЛЮЧЕНИЕ":
            in_main_part = False

        if in_main_part:
            chapter_type = get_chapter_type(para)

            if chapter_type == "bad" or chapter_type == "no_dot":
                fix_chapter(para, expected_chapter_num, chapter_type)
                current_chapter = expected_chapter_num
                prev_was_chapter = True
                all_section_numbers.clear()
                expected_chapter_num += 1
                continue

            if chapter_type == "gost":
                m = re.match(r'^ГЛАВА\s+(\d+)', uptext)
                if m:
                    corr_num = int(m.group(1))
                    title = re.sub(r'^ГЛАВА\s+\d+\.?', '', para.text, flags=re.IGNORECASE).strip()
                    if corr_num != expected_chapter_num:
                        new_text = f'ГЛАВА {expected_chapter_num}. {title.capitalize()}'
                        apply_heading_style(para, new_text)
                    else:
                        new_text = f'ГЛАВА {expected_chapter_num}. {title.capitalize()}'
                        apply_heading_style(para, new_text)
                    current_chapter = expected_chapter_num
                else:
                    current_chapter = expected_chapter_num
                prev_was_chapter = True
                all_section_numbers.clear()
                expected_chapter_num += 1
                continue

            # 4. Проверяем подзаголовки разделов
            if is_section(para):
                num_str, num_list = get_section_number(para)
                if not num_list:
                    continue
                if prev_was_chapter:
                    if num_list[-1] == 1:
                        apply_heading_style(para, para.text.strip())
                        all_section_numbers.append(num_list)
                    prev_was_chapter = False
                    continue
                if strict_sequence_check(all_section_numbers, num_list):
                    apply_heading_style(para, para.text.strip())
                    all_section_numbers.append(num_list)
                continue

            prev_was_chapter = False

    doc.save(output_path)