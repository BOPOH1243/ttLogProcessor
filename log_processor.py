import json
from datetime import datetime
from collections import defaultdict
import sys
import os

class LogProcessor:
    def __init__(self, files, date_filter=None):
        self.files = files
        self.date_filter = date_filter
        self.url_stats = defaultdict(lambda: {'total': 0, 'total_time': 0.0})
        
    def process(self):
        """Обработка лог-файлов и сбор статистики"""
        for file_path in self.files:
            self._process_file(file_path)
        return self._calculate_results()
    
    def _process_file(self, file_path):
        """Обработка одного лог-файла"""
        if os.path.exists(file_path): #надо заменить на pathlib FIXME
            with open(file_path, 'r') as f:
                for line in f:
                    self._process_line(line.strip())
        else: raise FileNotFoundError(f"Ошибка. файл {file_path} не найден")
    
    def _process_line(self, line):
        """Обработка одной строки лога"""
        try:
            log_entry = json.loads(line)
            if not self._should_process(log_entry):
                return
            self._update_stats(log_entry)
            
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            print(f"Ошибка обработки записи: {e}", file=sys.stderr)
    
    def _should_process(self, log_entry):
        """Проверка, нужно ли обрабатывать запись"""
        if self.date_filter is None:
            return True
            
        try:
            log_date = datetime.fromisoformat(log_entry['@timestamp']).date()
            filter_date = datetime.fromisoformat(self.date_filter).date()
            return log_date == filter_date
        except (KeyError, ValueError):
            return False
    
    def _update_stats(self, log_entry):
        """Обновление статистики на основе записи"""
        url = log_entry['url']
        response_time = float(log_entry['response_time'])
        
        self.url_stats[url]['total'] += 1
        self.url_stats[url]['total_time'] += response_time
    
    def _calculate_results(self):
        """Расчет финальных результатов"""
        return {
            url: {
                'total': stats['total'],
                'avg_response_time': stats['total_time'] / stats['total']
            }
            for url, stats in self.url_stats.items()
        }