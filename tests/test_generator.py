import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from report_generator import ReportGenerator

def test_generate_average_report():
    stats = {
        '/api/homeworks/': {'total': 10, 'avg_response_time': 0.1},
        '/api/other/': {'total': 5, 'avg_response_time': 0.2}
    }
    
    generator = ReportGenerator(report_type='average')
    report = generator.generate(stats)
    
    assert 'handler' in report
    assert 'total' in report
    assert 'avg_response_time' in report
    assert '/api/homeworks/' in report
    assert '/api/other/' in report
    assert '10' in report
    assert '0.1' in report
    assert '0.2' in report

def test_unknown_report_type():
    '''обработка неизвестного типа отчета'''
    with pytest.raises(ValueError) as exc_info:
        generator = ReportGenerator(report_type='unknown')
        generator.generate({})
    
    assert "Неизвестный тип отчета" in str(exc_info.value)
    assert "average" in str(exc_info.value)  # выводится список доступных отчетов