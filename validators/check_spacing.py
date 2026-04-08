from pathlib import Path
from typing import Any


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
