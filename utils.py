from pathlib import Path
from fnmatch import fnmatch

def read_file_list(path: Path) -> list[str]:
    """
    Читает список путей из файла.
    Не должен использоваться для получения всех файлов проекта.
    """
    result = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()
            if stripped and not stripped.startswith("#"):
                result.append(stripped)
    return result


def filter_files(files: list[Path], patterns: list[str]) -> list[Path]:
    """
    Фильтрует список файлов по шаблонам.
    """
    result = []
    for file in files:
        should_include = True
        for pattern in patterns:
            if fnmatch(str(file), pattern):
                should_include = False
                break
        if should_include:
            result.append(file)
    return result


def get_all_files() -> list[str]:
    """
    Возвращает список абсолютных путей ко всем файлам в текущей директории и поддиректориях.
    """
    print("[INFO] Файл с включениями не указан — собираем все файлы проекта")
    return [str(p) for p in Path.cwd().rglob("*") if p.is_file()]
