from pathlib import Path

from context_collector.utils import read_file_list, filter_files, get_all_files


def build_context(include_path: Path = None, output_path: Path = None, exclude_path: Path = None):
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
    if include_path is None:
        include_paths = get_all_files()
    else:
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
    contents = []
    for file in sorted(all_files):
        if file.is_file():
            try:
                rel_path = file.relative_to(Path.cwd())
            except ValueError:
                # На всякий случай, если файл вне cwd (маловероятно)
                rel_path = file
            content = f"=== {rel_path} ===\n"

            try:
                content += file.read_text(encoding="utf-8")
            except Exception as e:
                content += f"[Ошибка чтения файла: {e}]"
            
            contents.append(content)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write('\n'.join(contents))
        
    print(f"[SUCCESS] Контекст успешно записан в {output_path}")
