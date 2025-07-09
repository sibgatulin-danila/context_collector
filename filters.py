from pathlib import Path
from fnmatch import fnmatch


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