import re
from collections import Counter


def find_chords(text: str) -> None:
    """
    Знаходить музичні акорди у тексті.
    Наприклад: C, Am, F#m7, Bb, Gsus4.
    """
    pattern = r"\b[A-G][#b]?(?:m|maj|min|sus|dim|aug)?[0-9]{0,2}(?:#[0-5])?(?:\/[A-G][#b]?)?\b"
    chords = re.findall(pattern, text)

    counts = Counter(chords)
    for chord, count in sorted(counts.items()):
        print(f"{chord} ---------- {count} раз(и)")


if __name__ == '__main__':
    with open('hw9_10_2_song.txt', 'r', encoding='utf-8') as file:
        text_from_file = file.read()
    find_chords(text_from_file)
