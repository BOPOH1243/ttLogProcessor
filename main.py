import argparse
import sys
from log_processor import LogProcessor
from report_generator import ReportGenerator

def parse_args():
    """Парсинг аргументов командной строки"""
    parser = argparse.ArgumentParser(description='Анализатор лог-файлов')
    parser.add_argument('--file', nargs='+', required=True, help='Лог-файлы для анализа')
    parser.add_argument('--report', choices=['average'], required=True, help='Тип отчета')
    parser.add_argument('--date', help='Фильтрация по дате (YYYY-MM-DD)')
    return parser.parse_args()

def main():
    try:
        args = parse_args()
        
        # Обработка логов
        processor = LogProcessor(files=args.file, date_filter=args.date)
        stats = processor.process()
        
        # Генерация отчета
        generator = ReportGenerator(report_type=args.report)
        report = generator.generate(stats)
        
        # Вывод результата
        print(report)
        
    except Exception as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()