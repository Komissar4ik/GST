from pathlib import Path
from typing import Any


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
