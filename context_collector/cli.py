import argparse
from pathlib import Path
from context_collector import core


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

    core.build_context(args.include, args.output, args.exclude)


if __name__ == '__main__':
    main()