def check_alignment(path: str | Path) -> dict[str, Any]:
    """
    Проверка выравнивания текста: должно быть по ширине.
    """

    try:
        doc = _open_document(path)
    except (ValueError, FileNotFoundError) as e:
        return {"ok": False, "error": str(e)}

    violations = []

    for para_idx, paragraph, page in _iter_all_paragraphs_with_page(doc):

        if _is_heading(paragraph):
            continue

        alignment = paragraph.paragraph_format.alignment

        if alignment is None:
            continue

        if alignment != WD_ALIGN_PARAGRAPH.JUSTIFY:

            violations.append({
                "page": page,
                "value": str(alignment),
                "required": "JUSTIFY",
                "text": _snippet(paragraph.text)
            })

    if not violations:
        return {"ok": True, "message": "Выравнивание соблюдено."}

    return {
        "ok": False,
        "message": "Нарушено выравнивание.",
        "violations": violations
    }

def check_spacing(path: str | Path) -> dict[str, Any]:
    """
    Проверка интервалов между абзацами.
    Требование: line_spacing = 1.5, space_before = 0, space_after = 0
    """

    try:
        doc = _open_document(path)
    except (ValueError, FileNotFoundError) as e:
        return {"ok": False, "error": str(e)}

    violations = []

    for para_idx, paragraph, page in _iter_all_paragraphs_with_page(doc):

        fmt = paragraph.paragraph_format

        if fmt.line_spacing and abs(fmt.line_spacing - 1.5) > 0.01:

            violations.append({
                "page": page,
                "value": fmt.line_spacing,
                "required": "1.5",
                "text": _snippet(paragraph.text)
            })

        if fmt.space_before and fmt.space_before.pt != 0:

            violations.append({
                "page": page,
                "value": fmt.space_before.pt,
                "required": "0",
                "text": _snippet(paragraph.text)
            })

        if fmt.space_after and fmt.space_after.pt != 0:

            violations.append({
                "page": page,
                "value": fmt.space_after.pt,
                "required": "0",
                "text": _snippet(paragraph.text)
            })

    if not violations:
        return {"ok": True, "message": "Интервалы между абзацами соблюдены."}

    return {
        "ok": False,
        "message": "Нарушены интервалы между абзацами.",
        "violations": violations
    }

def check_hyphenation(path: str | Path) -> dict[str, Any]:
    """
    Проверка наличия переносов слов.
    """

    try:
        doc = _open_document(path)
    except (ValueError, FileNotFoundError) as e:
        return {"ok": False, "error": str(e)}

    violations = []

    for para_idx, paragraph, page in _iter_all_paragraphs_with_page(doc):

        if "\u00AD" in paragraph.text:

            violations.append({
                "page": page,
                "value": "перенос",
                "required": "без ручных переносов",
                "text": _snippet(paragraph.text)
            })

    if not violations:
        return {"ok": True, "message": "Переносы слов отсутствуют."}

    return {
        "ok": False,
        "message": "Обнаружены переносы слов.",
        "violations": violations
    }

import re

def check_dashes(path: str | Path) -> dict[str, Any]:
    """
    Проверка дефисов и тире.
    Если используется ' - ' вместо ' — ' → ошибка.
    """

    try:
        doc = _open_document(path)
    except (ValueError, FileNotFoundError) as e:
        return {"ok": False, "error": str(e)}

    violations = []

    for para_idx, paragraph, page in _iter_all_paragraphs_with_page(doc):

        text = paragraph.text

        if re.search(r"\s-\s", text):

            violations.append({
                "page": page,
                "value": "-",
                "required": "—",
                "text": _snippet(text)
            })

    if not violations:
        return {"ok": True, "message": "Дефисы и тире используются корректно."}

    return {
        "ok": False,
        "message": "Найдены дефисы вместо тире.",
        "violations": violations
    }

def run_text_checks(path: str | Path) -> dict[str, Any]:

    path = Path(path)

    return {
        "file": str(path),
        "alignment": check_alignment(path),
        "spacing": check_spacing(path),
        "hyphenation": check_hyphenation(path),
        "dashes": check_dashes(path),
    }
    



