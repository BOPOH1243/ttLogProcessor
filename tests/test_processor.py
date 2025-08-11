import pytest
import json
import tempfile
import os
import sys
from datetime import datetime
# Добавляем корень проекта в PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from log_processor import LogProcessor

@pytest.fixture
def sample_log_file():
    """Создание временного лог-файла для тестов"""
    logs = [
        {
            "@timestamp": "2025-06-22T20:08+00:00",
            "status": 200,
            "url": "/api/homeworks/",
            "request_method": "GET",
            "response_time": 0.02,
            "http_user_agent": "test"
        },
        {
            "@timestamp": "2025-06-22T21:08+00:00",
            "status": 200,
            "url": "/api/homeworks/",
            "request_method": "GET",
            "response_time": 0.04,
            "http_user_agent": "test"
        },
        {
            "@timestamp": "2025-06-23T20:08+00:00",
            "status": 200,
            "url": "/api/other/",
            "request_method": "GET",
            "response_time": 0.01,
            "http_user_agent": "test"
        }
    ]
    
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.log', delete=False) as f:
        for log in logs:
            f.write(json.dumps(log) + '\n')
        f.flush()
        yield f.name
        try:
            os.unlink(f.name)
        except FileNotFoundError:
            pass

def test_process_logs(sample_log_file):
    '''база работы процессора'''
    processor = LogProcessor(files=[sample_log_file])
    stats = processor.process()
    
    assert len(stats) == 2
    assert stats['/api/homeworks/']['total'] == 2
    assert stats['/api/homeworks/']['avg_response_time'] == 0.03
    assert stats['/api/other/']['total'] == 1
    assert stats['/api/other/']['avg_response_time'] == 0.01

def test_date_filter(sample_log_file):
    '''фильтрация по дате'''
    processor = LogProcessor(files=[sample_log_file], date_filter="2025-06-22")
    stats = processor.process()
    
    assert len(stats) == 1
    assert '/api/homeworks/' in stats
    assert '/api/other/' not in stats

def test_process_invalid_file():
    '''обработка несуществующего файла'''
    with pytest.raises(Exception) as exc_info:
        processor = LogProcessor(files=["nonexistent.log"])
        processor.process()
    
    assert "Ошибка" in str(exc_info.value)

def test_calculate_results_empty():
    '''расчет результатов при пустой статистике'''
    processor = LogProcessor(files=[])
    processor.url_stats = {}
    result = processor._calculate_results()
    assert result == {}

def test_date_filter_invalid():
    '''обработка невалидной даты в логе'''
    logs = [{
        "@timestamp": "invalid-date",
        "url": "/test",
        "response_time": 0.1
    }]
    
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.log') as f:
        for log in logs:
            f.write(json.dumps(log) + '\n')
        f.flush()
        
        processor = LogProcessor(files=[f.name], date_filter="2025-06-22")
        stats = processor.process()
        assert stats == {}  # Запись с неправильной датой должна быть пропущена