import math
from itertools import product
import numpy as np

class Cutter:
    def __init__(self, stock: dict, demand: dict):
        self._stock = stock
        self._demand = demand
        self._priority = self._priority_stock()
    
    def _priority_stock(self):
        """Находит те длины профиля на складе, которые нацело делятся на длину заказанного профиля"""
        stock_list = self._stock.keys()
        demanded_profile = list(self._demand.keys())[0]
        result = dict()
        for stock_prof in stock_list:
            if stock_prof % demanded_profile == 0:
                result[stock_prof] = self._stock[stock_prof]
        return result

    def calculate(self):
        """Находит решение и выводит ответ в понятном формате"""
        errors = self._validate_data()
        if errors:
            return self._error_handle(errors)
        answer = self._process()   
        return self._format_output(answer)

    def _validate_data(self):
        errors = []      
        for l, qty in self._stock.items():
            if qty < 0:
                errors.append(f"Отрицательное количество профиля длины {l}: {qty}")
        for l, qty in self._demand.items():
            if qty < 0:
                errors.append(f"Отрицательное количество заказанного профиля: {qty}")
        
        if errors:
            return errors
        
        total_stock = sum(l * qty for l, qty in self._stock.items())
        total_demand = sum(l * qty for l, qty in self._demand.items())
        if total_stock < total_demand:
            errors.append(
                f"Недостаточно профиля на складе! Есть {total_stock} метров, надо {total_demand}")
        return errors if errors else None
    
    def _error_handle(self, errors):
        message = ""
        for err in errors:
            message += err + '\n'
        return message
    
    def _process(self):
        """Находит решение"""
        total_demand = sum(l * qty for l, qty in self._demand.items())
        solutions = self._solve_equation(list(self._priority.keys()), total_demand)
        best_answer = self._choose_best_solution(solutions)
        return best_answer
    
    def _solve_equation(self, coefficients, target):
        """Решает линейное уравнение вида c1x1 + c2x2 + ... + cnxn = target"""
        solutions = []
        coeffs = np.array(coefficients)
        ranges = self._get_var_ranges(target)
        for values in product(*ranges):
            total = np.dot(values, coeffs)
            if abs(total - target) < 1e-8:
                solutions.append(values)
        return solutions
        
    def _get_var_ranges(self, target):
        """Находит диапазоны допустимых значений для каждой переменной x1, x2 и т.д. в уравнении"""
        ranges = []
        for l, qty in self._priority.items():
            ranges.append(range(0, min(qty, math.ceil(target / l)) + 1))
        return ranges
    
    def _choose_best_solution(self, solutions):
        """Возвращает лучшее решение из всех решений"""
        result = tuple()
        best_variance = float('inf')
        for sol in solutions:
            curr = np.var(sol)
            if curr < best_variance:
                best_variance = curr
                result = sol
        return result
    
    def _format_output(self, answer):
        """Выводит полученный результат понятным текстом"""
        if len(answer) == 0:
            return "Решения без остатков не найдено"
        
        output = ""
        priority_keys = self._priority.keys()
        for l, qty in zip(priority_keys, answer):
            demanded_profile = list(self._demand.keys())[0]
            qty_per_stock_profile = int(l / demanded_profile)
            combination = [demanded_profile for _ in range(qty_per_stock_profile)]
            output += f"Используйте разбиение {l} ⟶ {combination} {qty} раз(а)\n"
        return output