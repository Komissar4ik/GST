# -*- coding: utf-8 -*-
"""
Проверки .docx на соответствие ГОСТ 7.32 (библиотека python-docx).
Вход: путь к файлу .docx.
Выход: либо параметр соблюдён, либо список нарушений с указанием параграфа (и при необходимости run).
"""

from pathlib import Path
from typing import Any

from docx import Document
from docx.document import Document as DocumentType
from docx.text.paragraph import Paragraph
from docx.table import Table
from docx.shared import Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH

# ГОСТ 7.32: требуемые значения
FONT_REQUIRED = "Times New Roman"
FONT_SIZE_PT = 14  # pt
FIRST_LINE_INDENT_CM = 1.25  # см
ALIGNMENT_REQUIRED = WD_ALIGN_PARAGRAPH.JUSTIFY  # по ширине


def _open_document(path: str | Path) -> DocumentType:
    """Открывает .docx через python-docx."""
    path = Path(path)
    if path.suffix.lower() != ".docx":
        raise ValueError("Ожидается файл с расширением .docx")
    if not path.exists():
        raise FileNotFoundError(f"Файл не найден: {path}")
    return Document(path)


def _paragraph_has_page_break_before_next(paragraph: Paragraph) -> bool:
    """Есть ли в параграфе разрыв страницы (после него следующая страница)."""
    try:
        for run in paragraph.runs:
            r = run._r  # lxml element w:r
            for child in r:
                tag = child.tag if hasattr(child, "tag") else ""
                if "lastRenderedPageBreak" in tag or (
                    "}br" in tag and child.get("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}type") == "page"
                ):
                    return True
    except Exception:
        pass
    return False


def _iter_all_paragraphs_with_page(doc: DocumentType) -> list[tuple[int, Paragraph, int]]:
    """
    Обходит документ в порядке появления. Возвращает (индекс_1-based, параграф, страница).
    Страница вычисляется по разрывам страниц в документе (lastRenderedPageBreak); если их нет — везде 1.
    """
    result: list[tuple[int, Paragraph, int]] = []
    idx = 0
    page = 1
    for block in doc.iter_inner_content():
        if isinstance(block, Paragraph):
            idx += 1
            result.append((idx, block, page))
            if _paragraph_has_page_break_before_next(block):
                page += 1
        elif isinstance(block, Table):
            for row in block.rows:
                for cell in row.cells:
                    for p in cell.paragraphs:
                        idx += 1
                        result.append((idx, p, page))
                        if _paragraph_has_page_break_before_next(p):
                            page += 1
    return result


def _iter_all_paragraphs(doc: DocumentType) -> list[tuple[int, Paragraph]]:
    """Обходит документ, возвращает (индекс, параграф) для обратной совместимости."""
    return [(i, p) for i, p, _ in _iter_all_paragraphs_with_page(doc)]


# Максимальная длина фрагмента текста в отчёте
_TEXT_SNIPPET_LEN = 80

def _is_heading(paragraph: Paragraph) -> bool:
    """Параграф считается заголовком и не проверяется на размер шрифта/выравнивание."""
    name = (paragraph.style.name or "").strip()
    if not name:
        return False
    if name in ("Title", "Subtitle"):
        return True
    return name.startswith("Heading ") or name.startswith("Заголовок ")


def _snippet(text: str, max_len: int = _TEXT_SNIPPET_LEN) -> str:
    """Обрезает текст до max_len символов, добавляет … при обрезке."""
    text = (text or "").strip().replace("\n", " ")
    if len(text) <= max_len:
        return text
    return text[: max_len - 1].rstrip() + "…"


def check_font(path: str | Path) -> dict[str, Any]:
    """
    Проверка шрифта: должен быть Times New Roman (ГОСТ 7.32).
    На вход — путь к .docx. На выход — либо соблюдение, либо список нарушений (страница, текст).
    """
    try:
        doc = _open_document(path)
    except (ValueError, FileNotFoundError) as e:
        return {"ok": False, "error": str(e)}
    violations: list[dict[str, Any]] = []
    for para_idx, paragraph, page in _iter_all_paragraphs_with_page(doc):
        for run_idx, run in enumerate(paragraph.runs, start=1):
            if not run.text.strip():
                continue
            font_name = run.font.name
            if font_name is None:
                continue
            if font_name != FONT_REQUIRED:
                violations.append({
                    "page": page,
                    "value": font_name,
                    "required": FONT_REQUIRED,
                    "text": _snippet(run.text),
                })
    if not violations:
        return {"ok": True, "message": "Шрифт соблюдён: везде указан Times New Roman."}
    return {
        "ok": False,
        "message": "Шрифт не соблюдён.",
        "violations": violations,
    }


def check_font_size(path: str | Path) -> dict[str, Any]:
    """
    Проверка размера шрифта: 14 pt по ГОСТ 7.32.
    На вход — путь к .docx. На выход — либо соблюдение, либо список нарушений (страница, текст).
    """
    try:
        doc = _open_document(path)
    except (ValueError, FileNotFoundError) as e:
        return {"ok": False, "error": str(e)}
    violations: list[dict[str, Any]] = []
    for para_idx, paragraph, page in _iter_all_paragraphs_with_page(doc):
        if _is_heading(paragraph):
            continue
        for run_idx, run in enumerate(paragraph.runs, start=1):
            if not run.text.strip():
                continue
            size = run.font.size
            if size is None:
                continue
            size_pt = size.pt
            if abs(size_pt - FONT_SIZE_PT) > 0.01:
                violations.append({
                    "page": page,
                    "value_pt": round(size_pt, 1),
                    "required_pt": FONT_SIZE_PT,
                    "text": _snippet(run.text),
                })
    if not violations:
        return {"ok": True, "message": f"Размер шрифта соблюдён: {FONT_SIZE_PT} pt."}
    return {
        "ok": False,
        "message": "Размер шрифта не соблюдён.",
        "violations": violations,
    }


def check_paragraph_indent(path: str | Path) -> dict[str, Any]:
    """
    Проверка абзацного отступа первой строки: 1,25 см по ГОСТ 7.32.
    На вход — путь к .docx. На выход — либо соблюдение, либо список нарушений с номером параграфа.
    """
    try:
        doc = _open_document(path)
    except (ValueError, FileNotFoundError) as e:
        return {"ok": False, "error": str(e)}
    violations: list[dict[str, Any]] = []
    required_pt = Cm(FIRST_LINE_INDENT_CM).pt
    for para_idx, paragraph, page in _iter_all_paragraphs_with_page(doc):
        try:
            indent = paragraph.paragraph_format.first_line_indent
        except (ValueError, TypeError):
            continue
        if indent is None:
            continue
        indent_pt = indent.pt
        if abs(indent_pt - required_pt) > 0.1:
            violations.append({
                "page": page,
                "value_cm": round(indent.cm, 2),
                "required_cm": FIRST_LINE_INDENT_CM,
                "text": _snippet(paragraph.text),
            })
    if not violations:
        return {"ok": True, "message": "Абзацный отступ соблюдён: 1,25 см для первой строки."}
    return {
        "ok": False,
        "message": "Абзацный отступ не соблюдён.",
        "violations": violations,
    }


def check_alignment(path: str | Path) -> dict[str, Any]:
    """
    Проверка выравнивания: по ГОСТ 7.32 основной текст — по ширине (JUSTIFY).
    На вход — путь к .docx. На выход — либо соблюдение, либо список параграфов с другим выравниванием.
    """
    try:
        doc = _open_document(path)
    except (ValueError, FileNotFoundError) as e:
        return {"ok": False, "error": str(e)}
    violations: list[dict[str, Any]] = []
    for para_idx, paragraph, page in _iter_all_paragraphs_with_page(doc):
        if _is_heading(paragraph):
            continue
        alignment = paragraph.paragraph_format.alignment
        if alignment is None:
            continue
        if alignment != ALIGNMENT_REQUIRED:
            violations.append({
                "page": page,
                "value": str(alignment),
                "required": "JUSTIFY (по ширине)",
                "text": _snippet(paragraph.text),
            })
    if not violations:
        return {"ok": True, "message": "Выравнивание соблюдено: по ширине."}
    return {
        "ok": False,
        "message": "Выравнивание не соблюдено.",
        "violations": violations,
    }


def run_all_checks(path: str | Path) -> dict[str, Any]:
    """Запуск всех четырёх проверок. Возвращает сводку по каждой."""
    path = Path(path)
    return {
        "file": str(path),
        "font": check_font(path),
        "font_size": check_font_size(path),
        "paragraph_indent": check_paragraph_indent(path),
        "alignment": check_alignment(path),
    }


def _format_violation(x: dict[str, Any]) -> str:
    """Одна строка нарушения: фрагмент текста с ошибкой."""
    text = (x.get("text") or "").strip()
    if text:
        snippet = f"«{text}»"
    else:
        snippet = "(нет текста)"
    detail_parts = []
    if "value" in x:
        detail_parts.append(f"значение: {x['value']}")
    if "value_pt" in x:
        detail_parts.append(f"{x['value_pt']} pt (требуется {x.get('required_pt', 14)} pt)")
    if "value_cm" in x:
        detail_parts.append(f"{x['value_cm']} см (требуется {x.get('required_cm', 1.25)} см)")
    detail = f" — {', '.join(detail_parts)}" if detail_parts else ""
    return f"  {snippet}{detail}"


def _format_check_block(name: str, result: dict[str, Any]) -> list[str]:
    """Список строк для одной проверки: заголовок и при ошибках — текст по каждому нарушению."""
    lines = []
    if result.get("error"):
        lines.append(f"{name} — ошибка ({result['error']})")
        return lines
    if result.get("ok"):
        lines.append(f"{name} — все хорошо")
        return lines
    v = result.get("violations", [])
    if not v:
        lines.append(f"{name} — все хорошо")
        return lines
    lines.append(f"{name} — ошибка:")
    for x in v:
        lines.append(_format_violation(x))
    return lines


def write_report(docx_path: str | Path, report_path: str | Path | None = None) -> str:
    """
    Запускает все проверки и записывает отчёт в файл.
    Формат: каждая строка — «Проверка — все хорошо» или «Проверка — ошибка (...)»
    Возвращает путь к созданному файлу отчёта.
    """
    docx_path = Path(docx_path)
    if report_path is None:
        report_path = docx_path.with_suffix(".report.txt")
    report_path = Path(report_path)

    result = run_all_checks(docx_path)
    lines = [
        f"Отчёт по файлу: {result['file']}",
        "",
    ]
    for block in [
        ("Шрифт", result["font"]),
        ("Размер шрифта", result["font_size"]),
        ("Абзацный отступ", result["paragraph_indent"]),
        ("Выравнивание", result["alignment"]),
    ]:
        lines.extend(_format_check_block(block[0], block[1]))
        lines.append("")
    text = "\n".join(lines).rstrip()
    report_path.write_text(text, encoding="utf-8")
    return str(report_path)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Использование: python gost_checks.py <путь к .docx> [путь к отчёту]")
        sys.exit(1)
    docx_file = sys.argv[1]
    report_file = sys.argv[2] if len(sys.argv) > 2 else None
    report_path = write_report(docx_file, report_file)
    print(f"Отчёт сохранён: {report_path}")
