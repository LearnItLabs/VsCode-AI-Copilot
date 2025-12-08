"""
Examples demonstrating the Polynomial Math Library functionality.
"""

from polynomial import Polynomial


def main():
    print("=" * 60)
    print("POLYNOMIAL MATH LIBRARY - EXAMPLES")
    print("=" * 60)
    
    # Creating polynomials
    print("\n1. CREATING POLYNOMIALS")
    print("-" * 40)
    p1 = Polynomial([1, 2, 3])  # 1 + 2x + 3x^2
    p2 = Polynomial([4, -1, 2, 1])  # 4 - x + 2x^2 + x^3
    p3 = Polynomial([5, 0, -3])  # 5 - 3x^2
    
    print(f"p1 = {p1}")
    print(f"p2 = {p2}")
    print(f"p3 = {p3}")
    print(f"p1 degree: {p1.degree}")
    print(f"p2 degree: {p2.degree}")
    
    # Arithmetic operations
    print("\n2. ARITHMETIC OPERATIONS")
    print("-" * 40)
    print(f"p1 + p2 = {p1 + p2}")
    print(f"p1 - p2 = {p1 - p2}")
    print(f"p1 * p2 = {p1 * p2}")
    print(f"p1 * 3 = {p1 * 3}")
    print(f"p1 + 5 = {p1 + 5}")
    
    # Polynomial division
    print("\n3. POLYNOMIAL DIVISION")
    print("-" * 40)
    dividend = Polynomial([1, 0, -1])  # x^2 - 1
    divisor = Polynomial([1, -1])  # x - 1
    quotient, remainder = dividend.divmod(divisor)
    print(f"({dividend}) ÷ ({divisor})")
    print(f"Quotient: {quotient}")
    print(f"Remainder: {remainder}")
    
    # Division by scalar
    print(f"\n({p1}) / 2 = {p1 / 2}")
    
    # Power
    print("\n4. POLYNOMIAL POWER")
    print("-" * 40)
    p_simple = Polynomial([1, 1])  # 1 + x
    print(f"({p_simple})^2 = {p_simple ** 2}")
    print(f"({p_simple})^3 = {p_simple ** 3}")
    print(f"({p_simple})^4 = {p_simple ** 4}")
    
    # Evaluation
    print("\n5. POLYNOMIAL EVALUATION")
    print("-" * 40)
    p = Polynomial([1, 2, 3])  # 1 + 2x + 3x^2
    print(f"p(x) = {p}")
    print(f"p(0) = {p(0)}")
    print(f"p(1) = {p(1)}")
    print(f"p(2) = {p(2)}")
    print(f"p(-1) = {p(-1)}")
    
    # Derivatives
    print("\n6. DERIVATIVES")
    print("-" * 40)
    p = Polynomial([1, 2, 3, 4])  # 1 + 2x + 3x^2 + 4x^3
    print(f"f(x) = {p}")
    print(f"f'(x) = {p.derivative()}")
    print(f"f''(x) = {p.derivative(2)}")
    print(f"f'''(x) = {p.derivative(3)}")
    print(f"f''''(x) = {p.derivative(4)}")
    
    # Integration
    print("\n7. INTEGRATION")
    print("-" * 40)
    p = Polynomial([3, 2, 1])  # 3 + 2x + x^2
    print(f"f(x) = {p}")
    integral = p.integrate()
    print(f"∫f(x)dx = {integral}")
    integral_with_c = p.integrate(constant=5)
    print(f"∫f(x)dx + 5 = {integral_with_c}")
    
    # Definite integral
    print(f"\n∫₀² f(x)dx = {p.definite_integral(0, 2):.4f}")
    print(f"∫₁³ f(x)dx = {p.definite_integral(1, 3):.4f}")
    
    # Composition
    print("\n8. POLYNOMIAL COMPOSITION")
    print("-" * 40)
    f = Polynomial([1, 1])  # 1 + x
    g = Polynomial([0, 2])  # 2x
    print(f"f(x) = {f}")
    print(f"g(x) = {g}")
    print(f"f(g(x)) = {f.compose(g)}")
    print(f"g(f(x)) = {g.compose(f)}")
    
    # More complex composition
    h = Polynomial([0, 0, 1])  # x^2
    print(f"\nh(x) = {h}")
    print(f"f(h(x)) = {f.compose(h)}")
    
    # Root finding (linear and quadratic)
    print("\n9. ROOT FINDING (ANALYTICAL)")
    print("-" * 40)
    
    # Linear
    linear = Polynomial([6, -2])  # 6 - 2x
    print(f"Linear: {linear}")
    print(f"Roots: {linear.roots_linear_quadratic()}")
    
    # Quadratic with real roots
    quad1 = Polynomial([-6, 1, 1])  # -6 + x + x^2 = (x+3)(x-2)
    print(f"\nQuadratic (real roots): {quad1}")
    print(f"Roots: {quad1.roots_linear_quadratic()}")
    
    # Quadratic with complex roots
    quad2 = Polynomial([5, 0, 1])  # 5 + x^2
    print(f"\nQuadratic (complex roots): {quad2}")
    roots = quad2.roots_linear_quadratic()
    print(f"Roots: {roots}")
    
    # Perfect square
    quad3 = Polynomial([1, -2, 1])  # 1 - 2x + x^2 = (x-1)^2
    print(f"\nQuadratic (repeated root): {quad3}")
    print(f"Roots: {quad3.roots_linear_quadratic()}")
    
    # GCD
    print("\n10. GREATEST COMMON DIVISOR")
    print("-" * 40)
    p1 = Polynomial([-1, 0, 1])  # x^2 - 1 = (x-1)(x+1)
    p2 = Polynomial([-1, 1])  # x - 1
    print(f"p1 = {p1}")
    print(f"p2 = {p2}")
    print(f"gcd(p1, p2) = {p1.gcd(p2)}")
    
    p3 = Polynomial([-2, -3, 1])  # x^2 - 3x - 2
    p4 = Polynomial([4, -4, 1])  # x^2 - 4x + 4 = (x-2)^2
    print(f"\np3 = {p3}")
    print(f"p4 = {p4}")
    print(f"gcd(p3, p4) = {p3.gcd(p4)}")
    
    # Practical examples
    print("\n11. PRACTICAL EXAMPLES")
    print("-" * 40)
    
    # Projectile motion: h(t) = -4.9t^2 + 20t + 2
    print("Projectile Motion: h(t) = -4.9t² + 20t + 2 (meters)")
    height = Polynomial([2, 20, -4.9])
    print(f"Height at t=0: {height(0):.2f}m")
    print(f"Height at t=1: {height(1):.2f}m")
    print(f"Height at t=2: {height(2):.2f}m")
    
    velocity = height.derivative()
    print(f"\nVelocity: v(t) = {velocity}")
    print(f"Velocity at t=0: {velocity(0):.2f}m/s")
    print(f"Velocity at t=2: {velocity(2):.2f}m/s")
    
    acceleration = velocity.derivative()
    print(f"\nAcceleration: a(t) = {acceleration}")
    print(f"Acceleration (constant): {acceleration(0):.2f}m/s²")
    
    # Area under curve
    print("\n\nArea Under Curve: f(x) = x²")
    parabola = Polynomial([0, 0, 1])
    area = parabola.definite_integral(0, 3)
    print(f"Area from 0 to 3: {area:.2f}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
