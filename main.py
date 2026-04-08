import sys
from pathlib import Path
from pprint import pprint

from validators.check_alignment import check_alignment
from validators.check_spacing import check_spacing
from validators.check_hyphenation import check_hyphenation
from validators.check_dashes import check_dashes


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <path-to-docx>")
        return

    path = Path(sys.argv[1])

    print("Running check_alignment...")
    pprint(check_alignment(path))

    print("\nRunning check_spacing...")
    pprint(check_spacing(path))

    print("\nRunning check_hyphenation...")
    pprint(check_hyphenation(path))

    print("\nRunning check_dashes...")
    pprint(check_dashes(path))


if __name__ == '__main__':
    main()
