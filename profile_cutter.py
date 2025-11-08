import math
from itertools import product
import numpy as np

class Cutter:
    def __init__(self, user_input):
        self._stock, self._demand = self._to_dictionaries(user_input)
        self._priority = self._priority_stock()

    def _to_dictionaries(self, user_input):
        """Преобразует входные данные в словари вида 'длина: количество'"""
        stock, demand = dict(), dict()
        for key, value in user_input.items():
            if key.startswith("qty") and int(value) != 0:
                length_key = "len" + key[-1]
                corresponding_length = float(user_input[length_key])
                stock[corresponding_length] = int(value)
            elif key == "demand_qty":
                length_key = "demand_len"
                corresponding_length = float(user_input[length_key])
                demand[corresponding_length] = int(value)
        return stock, demand
    
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
            message = ""
            for err in errors:
                message += err + '\n'
            return message
        answer = self._process()   
        return self._format_output(answer)

    def _validate_data(self):
        errors = []      
        for l, qty in self._stock.items():
            if qty < 0:
                errors.append(f"Отрицательное количество профиля длины {l}: {qty}")
        for l, qty in self._demand.items():
            if qty == 0:
                errors.append(f"Количество заказанного профиля должно быть больше 0")
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
    
    def _process(self):
        """Находит решение по приоритетам:
            1. Минимизация остатков
            2. Максимально равномерное решение (x1≈x2≈...≈xn)"""
        total_demand = sum(l * qty for l, qty in self._demand.items())
        solutions = self._solve_equation(self._stock.keys(), total_demand)
        best_answer = self._find_uniform_solution(solutions)
        return best_answer
    
    def _solve_equation(self, coefficients, target):
        """
        Решает линейное уравнение вида c1x1 + c2x2 + ... + cnxn = target,
        где c1, c2, ..., cn - длины профилей, а x1, x2, ..., xn - количества профилей, то, что мы находим.
        Если нет точного решения, считает приближенное: 
        c1x1 + c2x2 + ... + cnxn > target, где x1, x2, ..., xn - наименьшие
        """
        total_priority = sum(l * qty for l, qty in self._priority.items())
        if total_priority < target:
            solution = {l: 0 for l in self._stock.keys()}
            sorted_by_waste = [l for l in self._stock.keys()]
            demand_prof = list(self._demand.keys())[0]
            sorted_by_waste.sort(key=lambda l: l % demand_prof)
            for l in sorted_by_waste:
                if target <= 0:
                    break
                
                qty_per_profile = l // demand_prof
                fill_qty = qty_per_profile * self._stock[l]
                fill_length = demand_prof * fill_qty
                if fill_length > target:
                    used_qty = math.ceil(target / qty_per_profile / demand_prof)
                    solution[l] = used_qty
                    target -= l * used_qty
                else:
                    solution[l] = self._stock[l]
                    target -= fill_length
            return [list(solution.values())]   
        else:
            coefficients = list(self._priority.keys())
            clean_solutions = []
            waste_solutions = []
            best_diff = float('inf')
            coeffs = np.array(coefficients)
            ranges = self._get_var_ranges(target)

            for values in product(*ranges):
                left = np.dot(values, coeffs)
                diff = left - target
                if abs(diff) < 1e-8:
                    waste_solutions = None
                    clean_solutions.append(values)
                elif waste_solutions is not None and diff > 0:
                    if diff < best_diff:
                        waste_solutions.clear()
                        waste_solutions.append(values)
                        best_diff = diff
                    elif diff == best_diff:
                        waste_solutions.append(values)
            
            if waste_solutions is not None:
                return waste_solutions
            return clean_solutions
        
    def _get_var_ranges(self, target):
        """Находит диапазоны допустимых значений для каждой переменной x1, x2 и т.д. в уравнении"""
        ranges = []
        for l, qty in self._priority.items():
            ranges.append(range(0, min(qty, math.ceil(target / l)) + 1))
        return ranges
    
    def _find_uniform_solution(self, solutions):
        """Возвращает самое равномерное решение из всех найденнных решений, используя дисперсию"""
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
            return "Решение не найдено"
        
        output = ""
        demand_prof = list(self._demand.keys())[0]
        if len(answer) == len(self._priority):
            for l, qty in zip(self._priority.keys(), answer):
                qty_per_stock_profile = int(l / demand_prof)
                combination = [demand_prof for _ in range(qty_per_stock_profile)]
                output += f"Используйте разбиение {l} ⟶ {combination} {qty} раз(а)\n"
        else:
            for l, qty in zip(self._stock.keys(), answer):
                if qty == 0:
                    continue
                qty_per_stock_profile = int(l / demand_prof)
                waste = l % demand_prof
                combination = "["
                for i in range(qty_per_stock_profile):
                    if i == qty_per_stock_profile - 1:
                        combination += f"{demand_prof}]"
                        break
                    combination += f"{demand_prof}, "
                if waste != 0:
                    combination += f" + {waste}"
                output += f"Используйте разбиение {l} ⟶ {combination}  {qty} раз(а)\n"
        return output