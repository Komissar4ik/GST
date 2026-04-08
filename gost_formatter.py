from pathlib import Path

# Re-export validators' functions for backwards compatibility
from validators.check_alignment import check_alignment
from validators.check_spacing import check_spacing
from validators.check_hyphenation import check_hyphenation
from validators.check_dashes import check_dashes

def run_text_checks(path: str | Path) -> dict[str, Any]:

    path = Path(path)

    return {
        "file": str(path),
        "alignment": check_alignment(path),
        "spacing": check_spacing(path),
        "hyphenation": check_hyphenation(path),
        "dashes": check_dashes(path),
    }
    



