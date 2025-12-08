"""
Polynomial Math Library

A comprehensive library for polynomial operations including arithmetic,
calculus operations, and various utility functions.
"""

from typing import List, Union, Tuple
import math


class Polynomial:
    """
    Represents a polynomial with real coefficients.
    
    Coefficients are stored in ascending order of powers:
    [a0, a1, a2, ...] represents a0 + a1*x + a2*x^2 + ...
    """
    
    def __init__(self, coefficients: List[float]):
        """
        Initialize a polynomial with given coefficients.
        
        Args:
            coefficients: List of coefficients in ascending order of powers
                         [a0, a1, a2] represents a0 + a1*x + a2*x^2
        """
        if not coefficients:
            self.coefficients = [0.0]
        else:
            # Remove leading zeros but keep at least one coefficient
            self.coefficients = list(coefficients)
            while len(self.coefficients) > 1 and abs(self.coefficients[-1]) < 1e-10:
                self.coefficients.pop()
    
    @property
    def degree(self) -> int:
        """Return the degree of the polynomial."""
        if len(self.coefficients) == 1 and abs(self.coefficients[0]) < 1e-10:
            return 0
        return len(self.coefficients) - 1
    
    def __repr__(self) -> str:
        """Return a string representation of the polynomial."""
        if not self.coefficients or all(abs(c) < 1e-10 for c in self.coefficients):
            return "0"
        
        terms = []
        for i, coef in enumerate(self.coefficients):
            if abs(coef) < 1e-10:
                continue
            
            # Format coefficient
            if i == 0:
                terms.append(f"{coef:g}")
            elif abs(coef - 1.0) < 1e-10:
                if i == 1:
                    terms.append("x")
                else:
                    terms.append(f"x^{i}")
            elif abs(coef + 1.0) < 1e-10:
                if i == 1:
                    terms.append("-x")
                else:
                    terms.append(f"-x^{i}")
            else:
                if i == 1:
                    terms.append(f"{coef:g}x")
                else:
                    terms.append(f"{coef:g}x^{i}")
        
        if not terms:
            return "0"
        
        # Join terms with proper signs
        result = terms[0]
        for term in terms[1:]:
            if term[0] == '-':
                result += f" - {term[1:]}"
            else:
                result += f" + {term}"
        
        return result
    
    def __str__(self) -> str:
        """Return a string representation of the polynomial."""
        return self.__repr__()
    
    def __eq__(self, other) -> bool:
        """Check if two polynomials are equal."""
        if not isinstance(other, Polynomial):
            return False
        
        if len(self.coefficients) != len(other.coefficients):
            return False
        
        return all(abs(a - b) < 1e-10 for a, b in zip(self.coefficients, other.coefficients))
    
    def __add__(self, other: Union['Polynomial', float]) -> 'Polynomial':
        """Add two polynomials or add a constant to a polynomial."""
        if isinstance(other, (int, float)):
            other = Polynomial([other])
        
        if not isinstance(other, Polynomial):
            raise TypeError("Can only add Polynomial or number")
        
        # Determine the length of the result
        max_len = max(len(self.coefficients), len(other.coefficients))
        result = [0.0] * max_len
        
        for i in range(len(self.coefficients)):
            result[i] += self.coefficients[i]
        
        for i in range(len(other.coefficients)):
            result[i] += other.coefficients[i]
        
        return Polynomial(result)
    
    def __radd__(self, other: Union['Polynomial', float]) -> 'Polynomial':
        """Right addition."""
        return self.__add__(other)
    
    def __sub__(self, other: Union['Polynomial', float]) -> 'Polynomial':
        """Subtract two polynomials or subtract a constant from a polynomial."""
        if isinstance(other, (int, float)):
            other = Polynomial([other])
        
        if not isinstance(other, Polynomial):
            raise TypeError("Can only subtract Polynomial or number")
        
        max_len = max(len(self.coefficients), len(other.coefficients))
        result = [0.0] * max_len
        
        for i in range(len(self.coefficients)):
            result[i] += self.coefficients[i]
        
        for i in range(len(other.coefficients)):
            result[i] -= other.coefficients[i]
        
        return Polynomial(result)
    
    def __rsub__(self, other: Union['Polynomial', float]) -> 'Polynomial':
        """Right subtraction."""
        if isinstance(other, (int, float)):
            other = Polynomial([other])
        return other.__sub__(self)
    
    def __mul__(self, other: Union['Polynomial', float]) -> 'Polynomial':
        """Multiply two polynomials or multiply a polynomial by a constant."""
        if isinstance(other, (int, float)):
            result = [c * other for c in self.coefficients]
            return Polynomial(result)
        
        if not isinstance(other, Polynomial):
            raise TypeError("Can only multiply Polynomial or number")
        
        # Result degree is sum of degrees
        result_len = len(self.coefficients) + len(other.coefficients) - 1
        result = [0.0] * result_len
        
        for i, a in enumerate(self.coefficients):
            for j, b in enumerate(other.coefficients):
                result[i + j] += a * b
        
        return Polynomial(result)
    
    def __rmul__(self, other: Union['Polynomial', float]) -> 'Polynomial':
        """Right multiplication."""
        return self.__mul__(other)
    
    def __truediv__(self, other: Union[float, 'Polynomial']) -> Union['Polynomial', Tuple['Polynomial', 'Polynomial']]:
        """
        Divide polynomial by a scalar or perform polynomial division.
        
        For scalar division, returns the polynomial with all coefficients divided.
        For polynomial division, returns (quotient, remainder).
        """
        if isinstance(other, (int, float)):
            if abs(other) < 1e-10:
                raise ValueError("Division by zero")
            result = [c / other for c in self.coefficients]
            return Polynomial(result)
        
        if not isinstance(other, Polynomial):
            raise TypeError("Can only divide by Polynomial or number")
        
        return self.divmod(other)
    
    def __pow__(self, n: int) -> 'Polynomial':
        """Raise polynomial to an integer power."""
        if not isinstance(n, int) or n < 0:
            raise ValueError("Power must be a non-negative integer")
        
        if n == 0:
            return Polynomial([1])
        
        result = Polynomial([1])
        base = Polynomial(self.coefficients)
        
        # Fast exponentiation
        while n > 0:
            if n % 2 == 1:
                result = result * base
            base = base * base
            n //= 2
        
        return result
    
    def __call__(self, x: float) -> float:
        """Evaluate the polynomial at a given value using Horner's method."""
        if not self.coefficients:
            return 0.0
        
        # Horner's method: evaluate from highest to lowest degree
        result = self.coefficients[-1]
        for i in range(len(self.coefficients) - 2, -1, -1):
            result = result * x + self.coefficients[i]
        
        return result
    
    def evaluate(self, x: float) -> float:
        """
        Evaluate the polynomial at a given value.
        
        Args:
            x: The value at which to evaluate the polynomial
            
        Returns:
            The value of the polynomial at x
        """
        return self(x)
    
    def derivative(self, n: int = 1) -> 'Polynomial':
        """
        Compute the nth derivative of the polynomial.
        
        Args:
            n: Order of the derivative (default: 1)
            
        Returns:
            The nth derivative as a new Polynomial
        """
        if n < 0:
            raise ValueError("Derivative order must be non-negative")
        
        if n == 0:
            return Polynomial(self.coefficients)
        
        if len(self.coefficients) <= n:
            return Polynomial([0])
        
        result = list(self.coefficients)
        
        for _ in range(n):
            if len(result) <= 1:
                result = [0]
                break
            result = [result[i] * i for i in range(1, len(result))]
        
        return Polynomial(result)
    
    def integrate(self, constant: float = 0.0) -> 'Polynomial':
        """
        Compute the indefinite integral of the polynomial.
        
        Args:
            constant: The constant of integration (default: 0)
            
        Returns:
            The integral as a new Polynomial
        """
        result = [constant]
        for i, coef in enumerate(self.coefficients):
            result.append(coef / (i + 1))
        
        return Polynomial(result)
    
    def definite_integral(self, a: float, b: float) -> float:
        """
        Compute the definite integral from a to b.
        
        Args:
            a: Lower bound
            b: Upper bound
            
        Returns:
            The value of the definite integral
        """
        antiderivative = self.integrate()
        return antiderivative(b) - antiderivative(a)
    
    def divmod(self, other: 'Polynomial') -> Tuple['Polynomial', 'Polynomial']:
        """
        Perform polynomial division, returning quotient and remainder.
        
        Args:
            other: The divisor polynomial
            
        Returns:
            Tuple of (quotient, remainder)
        """
        if not isinstance(other, Polynomial):
            raise TypeError("Divisor must be a Polynomial")
        
        if all(abs(c) < 1e-10 for c in other.coefficients):
            raise ValueError("Division by zero polynomial")
        
        # Make copies
        dividend = list(self.coefficients)
        divisor = list(other.coefficients)
        
        # Normalize divisor
        while len(divisor) > 1 and abs(divisor[-1]) < 1e-10:
            divisor.pop()
        
        if len(dividend) < len(divisor):
            return Polynomial([0]), Polynomial(dividend)
        
        quotient = []
        
        while len(dividend) >= len(divisor):
            # Divide leading terms
            coef = dividend[-1] / divisor[-1]
            quotient.append(coef)
            
            # Subtract divisor * coef from dividend
            for i in range(len(divisor)):
                dividend[len(dividend) - len(divisor) + i] -= coef * divisor[i]
            
            # Remove leading term
            dividend.pop()
        
        quotient.reverse()
        
        return Polynomial(quotient if quotient else [0]), Polynomial(dividend if dividend else [0])
    
    def compose(self, other: 'Polynomial') -> 'Polynomial':
        """
        Compose this polynomial with another: self(other(x)).
        
        Args:
            other: The inner polynomial
            
        Returns:
            The composed polynomial
        """
        if not isinstance(other, Polynomial):
            raise TypeError("Can only compose with another Polynomial")
        
        result = Polynomial([0])
        power = Polynomial([1])  # other^0
        
        for coef in self.coefficients:
            result = result + power * coef
            power = power * other
        
        return result
    
    def gcd(self, other: 'Polynomial') -> 'Polynomial':
        """
        Compute the greatest common divisor using Euclidean algorithm.
        
        Args:
            other: The other polynomial
            
        Returns:
            The GCD polynomial (monic)
        """
        a = Polynomial(self.coefficients)
        b = Polynomial(other.coefficients)
        
        while not all(abs(c) < 1e-10 for c in b.coefficients):
            _, remainder = a.divmod(b)
            a = b
            b = remainder
        
        # Make monic (leading coefficient = 1)
        if abs(a.coefficients[-1]) > 1e-10:
            return a / a.coefficients[-1]
        return a
    
    def roots_linear_quadratic(self) -> List[complex]:
        """
        Find roots for linear and quadratic polynomials analytically.
        
        Returns:
            List of roots (may be complex)
        """
        # Remove leading zeros
        coeffs = self.coefficients.copy()
        while len(coeffs) > 1 and abs(coeffs[-1]) < 1e-10:
            coeffs.pop()
        
        degree = len(coeffs) - 1
        
        if degree == 0:
            return []  # Constant polynomial
        elif degree == 1:
            # Linear: ax + b = 0 => x = -b/a
            return [-coeffs[0] / coeffs[1]]
        elif degree == 2:
            # Quadratic: ax^2 + bx + c = 0
            a, b, c = coeffs[2], coeffs[1], coeffs[0]
            discriminant = b * b - 4 * a * c
            
            if discriminant >= 0:
                sqrt_disc = math.sqrt(discriminant)
                return [
                    (-b + sqrt_disc) / (2 * a),
                    (-b - sqrt_disc) / (2 * a)
                ]
            else:
                sqrt_disc = math.sqrt(-discriminant)
                real_part = -b / (2 * a)
                imag_part = sqrt_disc / (2 * a)
                return [
                    complex(real_part, imag_part),
                    complex(real_part, -imag_part)
                ]
        else:
            raise ValueError("Analytical root finding only supported for degree <= 2")
