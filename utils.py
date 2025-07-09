from pathlib import Path


def read_file_list(path: Path) -> list[str]:
    """
    Читает список путей из файла.
    """
    result = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()
            if stripped and not stripped.startswith("#"):
                result.append(stripped)
    return result