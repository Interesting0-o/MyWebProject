import re

_CJK_PATTERN = re.compile(r"[\u4e00-\u9fff]")
_WORD_PATTERN = re.compile(r"[A-Za-z0-9]+")


def estimate_reading_time(blocks: list[dict]) -> int:
    parts: list[str] = []

    for block in blocks:
        block_type = block.get("type")
        if block_type == "list":
            parts.extend(str(item) for item in block.get("items", []))
        elif block_type == "code":
            parts.append(str(block.get("code", "")))
        else:
            parts.append(str(block.get("text", "")))

    text = " ".join(parts)
    cjk_count = len(_CJK_PATTERN.findall(text))
    word_count = len(_WORD_PATTERN.findall(text))

    return max(1, round(cjk_count / 300 + word_count / 200))
