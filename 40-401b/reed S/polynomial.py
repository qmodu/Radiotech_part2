# -*- coding:utf-8 -*-

from StringIO import StringIO

class Polynomial(object):
    """Класс полинома.
    
    Полиномиальные объекты являются неизменными.
    
    Примечание: в то время как класс не зависит от типа используемых
    коэффициентов (при условии что они поддерживаю обычные математические
    операции), полиномальный класс предполагет идентичную адитивность и
    мультипликативность для 0 и 1 соответственно. Если вы делаете какие нибуть
    математические операции за областью переменных или используете не номера
    в качестве коэффициентов, этот класс необходимо изменить.
    """
    def __init__(self, coefficients=(), **sparse):
        """
        Есть три способа инициализации полиномиального объекта.
        1) With a list, tuple, or other iterable, creates a polynomial using
        the items as coefficients in order of decreasing power

        2) С аргументами ключевого слова например x3=5, устанавливает
        коэффициент x^3 равный 5

        3) При вызове без аргументов, создает пустой полином, что эквивалентно
        Polynomial((0,))

        >>> print Polynomial((5, 0, 0, 0, 0, 0))
        5x^5

        >>> print Polynomial(x32=5, x64=8)
        8x^64 + 5x^32

        >>> print Polynomial(x5=5, x9=4, x0=2) 
        4x^9 + 5x^5 + 2
        """
        if coefficients and sparse:
            raise TypeError("Укажите список коэффициентов /или/ ключевые слова, не"
                    " оба")
        if coefficients:
            # Polynomial((1, 2, 3, ...))
            c = list(coefficients)
            # Стираем все ведущие нулевые коэффициенты
            while c and c[0] == 0:
                c.pop(0)
            if not c:
                c.append(0)

            self.coefficients = tuple(c)
        elif sparse:
            # Polynomial(x32=...)
            powers = sparse.keys()
            powers.sort(reverse=1)
            highest = int(powers[0][1:])
            coefficients = [0] * (highest+1)

            for power, coeff in sparse.iteritems():
                power = int(power[1:])
                coefficients[highest - power] = coeff

            self.coefficients = tuple(coefficients)
        else:
            # Polynomial()
            self.coefficients = (0,)

    def __len__(self):
        """Возвращает число членов в полином"""
        return len(self.coefficients)
    def degree(self):
        """Возвращает степень полинома"""
        return len(self.coefficients) - 1

    def __add__(self, other):
        diff = len(self) - len(other)
        if diff > 0:
            t1 = self.coefficients
            t2 = (0,) * diff + other.coefficients
        else:
            t1 = (0,) * (-diff) + self.coefficients
            t2 = other.coefficients

        return self.__class__(x+y for x,y in zip(t1, t2))

    def __neg__(self):
        return self.__class__(-x for x in self.coefficients)
    def __sub__(self, other):
        return self + -other
            
    def __mul__(self, other):
        terms = [0] * (len(self) + len(other))

        for i1, c1 in enumerate(reversed(self.coefficients)):
            if c1 == 0:
                # Оптимизация
                continue
            for i2, c2 in enumerate(reversed(other.coefficients)):
                terms[i1+i2] += c1*c2

        return self.__class__(reversed(terms))

    def __floordiv__(self, other):
        return divmod(self, other)[0]
    def __mod__(self, other):
        return divmod(self, other)[1]

    def __divmod__(dividend, divisor):
        """Осуществляет полиномиальное рекурсивное разделение."""
        class_ = dividend.__class__

        # Посмотрите колько раз старший член делителя 
        # может перейти в старший порядок dividend
        
        dividend_power = dividend.degree()
        dividend_coefficient = dividend.coefficients[0]

        divisor_power = divisor.degree()
        divisor_coefficient = divisor.coefficients[0]

        quotient_power = dividend_power - divisor_power
        if quotient_power < 0:
            # Не делим все,возвращаем 0 для частного и всей
            # dividend как остаток
            return class_((0,)), dividend

        # Вычисляем сколько раз старший член порядка делителя переходит 
        # в dividend
        quotient_coefficient = dividend_coefficient / divisor_coefficient
        quotient = class_( (quotient_coefficient,) + (0,) * quotient_power )

        remander = dividend - quotient * divisor

        if remander.coefficients == (0,):
            # Идем равномерно без остатака, получим
            return quotient, remander

        # Был остаток, смотрим сколько раз остаток уходит в делитель
        morequotient, remander = divmod(remander, divisor)
        return quotient + morequotient, remander

    def __eq__(self, other):
        return self.coefficients == other.coefficients
    def __ne__(self, other):
        return self.coefficients != other.coefficients
    def __hash__(self):
        return hash(self.coefficients)

    def __repr__(self):
        n = self.__class__.__name__
        return "%s(%r)" % (n, self.coefficients)
    def __str__(self):
        buf = StringIO()
        l = len(self) - 1
        for i, c in enumerate(self.coefficients):
            if not c and i > 0:
                continue
            power = l - i
            if c == 1 and power != 0:
                c = ""
            if power > 1:
                buf.write("%sx^%s" % (c, power))
            elif power == 1:
                buf.write("%sx" % c)
            else:
                buf.write("%s" % c)
            buf.write(" + ")
        return buf.getvalue()[:-3]

    def evaluate(self, x):
        "Оцениваем этот полином при значениях х, возвращая результат."
        # Содержит сумму каждого члена полинома
        c = 0

        # Удерживает текущую мощность х. Это умножается на x после каждый член
        # в многочлене суммируется. Инициализация x^0 = 1
        p = 1

        for term in reversed(self.coefficients):
            c = c + term * p

            p = p * x

        return c

    def get_coefficient(self, degree):
        """Возвращает коэффициент указанного члена"""
        if degree > self.degree():
            return 0
        else:
            return self.coefficients[-(degree+1)]
