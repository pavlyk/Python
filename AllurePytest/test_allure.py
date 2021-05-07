import allure
import time
import pytest

def capital_case(x):
    return x.capitalize()

@allure.feature('Первый тест')
@allure.story('Проводим первое тестирование')
@allure.severity('critical') # critical trivial blocker normal minor
def test_capital_case1():
    assert capital_case('semaphore') == 'Semaphore'

@allure.feature('Второй тест')
@allure.story('Проводим второе тестирование')
@allure.severity('trivial')
def test_capital_case2():
    assert capital_case("semaphore") == 'SEmaphore'

@allure.feature('Третий тест')
@allure.story('Проводим третье тестирование')
@allure.severity('blocker')
def test_capital_case3():
    assert capital_case('hello') == 'Hello'

# pytest --alluredir results
# allure serve results