import argparse
from pathlib import Path

from utils import read_file_list
from filters import filter_files


def collect_context(include_path: Path = None, output_path: Path = None, exclude_path: Path = None):
    """
    Собирает контекст из указанных файлов и папок.
    Если include_path не указан — берутся все файлы в текущей директории.
    """
    # Автоматически генерируем имя выходного файла, если не задано
    if output_path is None:
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = Path(f"context_{timestamp}.txt")

    print(f"[INFO] Считываем список включаемых путей {'(по умолчанию)' if include_path is None else ''}")
    include_paths = read_file_list(include_path)

    print("[INFO] Преобразуем пути к абсолютным")
    abs_include_paths = [Path(p).resolve() for p in include_paths]

    print("[INFO] Сканируем файлы...")
    all_files = []
    for path in abs_include_paths:
        if path.is_dir():
            all_files.extend(path.rglob("*"))
        elif path.is_file():
            all_files.append(path)

    # Убираем дубликаты
    all_files = list(set(all_files))

    # Фильтруем по exclude, если указан
    if exclude_path:
        print(f"[INFO] Применяем фильтр исключения из {exclude_path}")
        exclude_patterns = read_file_list(exclude_path)
        all_files = filter_files(all_files, exclude_patterns)

    # Записываем в выходной файл
    print(f"[INFO] Записываем результат в {output_path}")
    with open(output_path, "w", encoding="utf-8") as f:
        for file in sorted(all_files):
            if file.is_file():
                f.write(f"\n\n=== {file} ===\n")
                try:
                    f.write(file.read_text(encoding="utf-8"))
                except Exception as e:
                    f.write(f"[Ошибка чтения файла: {e}]")

    print(f"[SUCCESS] Контекст успешно записан в {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Сборщик контекста для ИИ")
    parser.add_argument("-i", "--include", type=Path, help="Файл со списком файлов/папок для включения", default=None)
    parser.add_argument("-o", "--output", type=Path, help="Выходной файл контекста", default=None)
    parser.add_argument("-e", "--exclude", type=Path, help="Файл со списком файлов/папок для исключения", default=None)

    args = parser.parse_args()

    if args.include and not args.include.exists():
        print(f"[ERROR] Файл с включениями не найден: {args.include}")
        return

    if args.exclude and not args.exclude.exists():
        print(f"[ERROR] Файл с исключениями не найден: {args.exclude}")
        return

    if args.output is None:
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        args.output = Path(f"context_{timestamp}.txt")

    collect_context(args.include, args.output, args.exclude)


if __name__ == '__main__':
    main()