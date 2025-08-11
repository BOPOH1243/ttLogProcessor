import pytest
from unittest.mock import patch, MagicMock
from main import parse_args, main

def test_parse_args():
    '''парсинг аргументов'''
    with patch('sys.argv', ['main.py', '--file', 'test.log', '--report', 'average']):
        args = parse_args()
        assert args.file == ['test.log']
        assert args.report == 'average'
        assert args.date is None

    with patch('sys.argv', ['main.py', '--file', 'f1.log', 'f2.log', '--report', 'average', '--date', '2025-06-22']):
        args = parse_args()
        assert args.file == ['f1.log', 'f2.log']
        assert args.date == '2025-06-22'

@patch('main.LogProcessor')
@patch('main.ReportGenerator')
def test_main_success(MockReportGenerator, MockLogProcessor):
    '''успешное выполнение'''
    mock_processor = MockLogProcessor.return_value
    mock_processor.process.return_value = {'/test': {'total': 1, 'avg_response_time': 0.1}}
    
    mock_generator = MockReportGenerator.return_value
    mock_generator.generate.return_value = "test report"
    
    with patch('sys.argv', ['main.py', '--file', 'test.log', '--report', 'average']):
        main()
    
    MockLogProcessor.assert_called_once_with(files=['test.log'], date_filter=None)
    mock_processor.process.assert_called_once()
    mock_generator.generate.assert_called_once_with({'/test': {'total': 1, 'avg_response_time': 0.1}})
