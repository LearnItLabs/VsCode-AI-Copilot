# Polynomial Math Library

A comprehensive Python library for polynomial operations including arithmetic, calculus, and various utility functions.

## Features

- **Polynomial Representation**: Store polynomials with coefficients in ascending order of powers
- **Arithmetic Operations**: Addition, subtraction, multiplication, division
- **Calculus Operations**: Derivatives, integration (definite and indefinite)
- **Evaluation**: Efficient polynomial evaluation using Horner's method
- **Advanced Operations**: Composition, GCD, polynomial division with quotient and remainder
- **Root Finding**: Analytical solutions for linear and quadratic polynomials
- **Clean API**: Pythonic interface with operator overloading

## Installation

Simply copy `polynomial.py` to your project directory.

## Quick Start

```python
from polynomial import Polynomial

# Create polynomials: 1 + 2x + 3x²
p1 = Polynomial([1, 2, 3])

# Create: 4 - x + 2x² + x³
p2 = Polynomial([4, -1, 2, 1])

# Arithmetic
result = p1 + p2
result = p1 * p2
result = p1 ** 3

# Evaluate
value = p1(2)  # Evaluate at x=2

# Calculus
derivative = p1.derivative()
integral = p1.integrate()
area = p1.definite_integral(0, 5)

# Roots (for linear/quadratic)
roots = p1.roots_linear_quadratic()
```

## API Reference

### Creating Polynomials

```python
# Coefficients in ascending order: [a₀, a₁, a₂, ...] = a₀ + a₁x + a₂x² + ...
p = Polynomial([1, 2, 3])  # 1 + 2x + 3x²
```

### Arithmetic Operations

```python
p1 + p2      # Addition
p1 - p2      # Subtraction
p1 * p2      # Multiplication
p1 / 2       # Scalar division
p1 ** 3      # Power
p1 + 5       # Add constant
```

### Polynomial Division

```python
quotient, remainder = p1.divmod(p2)
```

### Evaluation

```python
value = p(x)           # Evaluate at x using Horner's method
value = p.evaluate(x)  # Alternative method
```

### Calculus

```python
# Derivatives
p_prime = p.derivative()      # First derivative
p_double_prime = p.derivative(2)  # Second derivative

# Integration
integral = p.integrate()               # Indefinite integral
integral = p.integrate(constant=5)     # With constant of integration
area = p.definite_integral(a, b)      # Definite integral from a to b
```

### Advanced Operations

```python
# Composition: f(g(x))
result = f.compose(g)

# Greatest Common Divisor
gcd_poly = p1.gcd(p2)

# Find roots (analytical, degree ≤ 2)
roots = p.roots_linear_quadratic()
```

### Properties

```python
p.degree          # Degree of polynomial
p.coefficients    # List of coefficients
str(p)           # String representation
```

## Examples

Run the examples file to see comprehensive demonstrations:

```bash
python polynomial_examples.py
```

### Example: Projectile Motion

```python
# Height: h(t) = -4.9t² + 20t + 2
height = Polynomial([2, 20, -4.9])

# Evaluate at different times
h_at_0 = height(0)  # Initial height
h_at_2 = height(2)  # Height at t=2

# Velocity (derivative)
velocity = height.derivative()
v_at_0 = velocity(0)  # Initial velocity

# Acceleration (second derivative)
acceleration = velocity.derivative()
```

### Example: Finding Roots

```python
# Quadratic: x² + x - 6 = (x+3)(x-2)
quad = Polynomial([-6, 1, 1])
roots = quad.roots_linear_quadratic()  # [-3.0, 2.0]

# Complex roots: x² + 5
quad2 = Polynomial([5, 0, 1])
roots2 = quad2.roots_linear_quadratic()  # [±√5·i]
```

## Implementation Details

- Uses Horner's method for efficient polynomial evaluation
- Handles numerical precision with epsilon-based comparisons (1e-10)
- Removes trailing zero coefficients automatically
- Supports both real and complex roots for quadratics
- Implements Euclidean algorithm for polynomial GCD

## License

Free to use for any purpose.
