from tabulate import tabulate

class ReportGenerator:
    def __init__(self, report_type):
        self.report_type = report_type
        self.report_generators = {
            'average': self._generate_average_report,
            # Здесь можно добавлять новые генераторы отчетов
            # 'top_slow': self._generate_top_slow_report,
            # 'errors': self._generate_errors_report,
            # 'report1': lambda...
        }
    
    def generate(self, stats):
        """Генерация отчета на основе статистики"""
        generator = self.report_generators.get(self.report_type)
        if generator is None:
            raise ValueError(
                f"Неизвестный тип отчета: {self.report_type}. "
                f"Доступные типы: {list(self.report_generators.keys())}"
            )
        return generator(stats)
    
    def _generate_average_report(self, stats):
        """Генерация отчета со средним временем ответа"""
        # сортировка по убыванию количества запросов
        sorted_stats = sorted(
            stats.items(),
            key=lambda x: x[1]['total'],
            reverse=True
        )
        
        # подготовка данных для таблички
        table_data = []
        for idx, (url, data) in enumerate(sorted_stats):
            table_data.append([
                idx,
                url,
                data['total'],
                round(data['avg_response_time'], 3)
            ])
        
        # формирование таблички
        headers = ["#", "handler", "total", "avg_response_time"]
        return tabulate(table_data, headers=headers, tablefmt="plain")
    
    # # пример добавления нового генератора отчетов:
    # def _generate_top_slow_report(self, stats):
    #     """Генерация отчета с самыми медленными эндпоинтами"""
    #     sorted_stats = sorted(
    #         stats.items(),
    #         key=lambda x: x[1]['avg_response_time'],
    #         reverse=True
    #     )
    #     ...