from pathlib import Path
from pathspec import PathSpec
from pathspec.patterns import GitWildMatchPattern

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
    Фильтрует список файлов по шаблонам .gitignore с помощью pathspec.
    Поддерживает все стандартные правила gitignore.
    """
    spec = PathSpec.from_lines(GitWildMatchPattern, patterns)
    # Преобразуем абсолютные пути в относительные (относительно текущей директории)
    current_dir = Path.cwd()
    filtered = []
    for file in files:
        try:
            rel_path = file.relative_to(current_dir)
        except ValueError:
            # Если файл вне текущей директории — оставляем его без изменений
            rel_path = file
        if not spec.match_file(rel_path):
            filtered.append(file)
    return filtered


def get_all_files() -> list[str]:
    """
    Возвращает список абсолютных путей ко всем файлам в текущей директории и поддиректориях.
    """
    print("[INFO] Файл с включениями не указан — собираем все файлы проекта")
    return [str(p) for p in Path.cwd().rglob("*") if p.is_file()]
