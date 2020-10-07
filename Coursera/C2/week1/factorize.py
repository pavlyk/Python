# import unittest

class TestFactorize(unittest.TestCase):


    def test_wrong_types_raise_exception(self):
        '''
        Проверяет, что передаваемый в функцию аргумент
        типа float или str вызывает исключение TypeError. 
        Тестовый набор входных данных:  'string',  1.5
        '''
        cases = ('string', 1.5)
        for x in cases:
            with self.subTest(case=x):
                self.assertRaises(TypeError, factorize, x)

    def test_negative(self):
        cases = (-1, -10, -100)
        for x in cases:
            with self.subTest(case=x):
                self.assertRaises(ValueError, factorize, x)
        
    def test_zero_and_one_cases(self):
        cases = ({'x': 0,'output': (0,)},{'x': 1,'output': (1,)})
        for i in cases:
            x = i['x']
            output = i['output']
            with self.subTest(case=i['x']):
                # print(factorize(i['x']),)
                self.assertEqual(factorize(x), output)

    def test_simple_numbers(self):
        cases = ({'x': 3,'output': (3,)},{'x': 13,'output': (13,)},{'x': 29,'output': (29,)})
        for i in cases:
            x = i['x']
            output = i['output']
            with self.subTest(case=i['x']):
                # print(factorize(i['x']),)
                self.assertEqual(factorize(x), output)

    def test_two_simple_multipliers(self):
        cases = ({'x': 6,'output': (2, 3)},{'x': 26,'output': (2, 13)},{'x': 121,'output': (11, 11)})
        for i in cases:
            x = i['x']
            output = i['output']
            with self.subTest(case=i['x']):
                # print(factorize(i['x']),)
                self.assertEqual(factorize(x), output)

    def test_many_multipliers(self):
        cases = ({'x': 1001,'output': (7, 11, 13)},{'x': 9699690,'output': (2, 3, 5, 7, 11, 13, 17, 19)})
        for i in cases:
            x = i['x']
            output = i['output']
            with self.subTest(case=i['x']):
                # print(factorize(i['x']),)
                self.assertEqual(factorize(x), output)


# def factorize(x):
#     """ 
#     Factorize positive integer and return its factors.
#     :type x: int,>=0
#     :rtype: tuple[N],N>0
#     """
#     pass


# if __name__ == "__main__":
#     unittest.main()