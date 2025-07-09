from pathlib import Path


def read_file_list(path: Path) -> list[str]:
    """
    Читает список путей из файла.
    Если path == None, возвращает все файлы в текущей директории.
    """
    if path is None:
        print("[INFO] Файл с включениями не указан — собираем все файлы проекта")
        return [str(p) for p in Path.cwd().rglob("*") if p.is_file()]

    result = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()
            if stripped and not stripped.startswith("#"):
                result.append(stripped)
    return result