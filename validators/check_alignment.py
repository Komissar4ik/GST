from pathlib import Path
from typing import Any
from docx.enum.text import WD_ALIGN_PARAGRAPH


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
