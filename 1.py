def format_text(text: str, width: int = 70) -> str:
    words = text.split()
    lines, current = [], ""
    for word in words:
        # +1 — на пробел между словами
        if len(current) + len(word) + (1 if current else 0) <= width:
            current = f"{current} {word}".strip()
        else:
            if current:
                lines.append(current)
            # если слово само длиннее width — оставляем как есть
            current = word
    if current:
        lines.append(current)
    return "\n".join(lines)

if __name__ == '__main__':
    text = input()

    res = format_text(text=text)
    print(res)