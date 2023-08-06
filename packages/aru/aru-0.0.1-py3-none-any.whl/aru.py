import math
import numpy as np
import scipy.special as sp

def add(x, y):
    #Add two numbers
    return x + y

def subtract(x, y):
    #Subtract two numbers
    return x - y

def multiply(x, y):
    #Multiply two numbers
    return x * y

def divide(x, y):
    #Divide two numbers
    if y == 0:
        raise ValueError("Cannot divide by zero")
    return x / y

def square(x):
    #Return the square of a number
    return x ** 2

def cube(x):
    #Return the cube of a number
    return x ** 3

def square_root(x):
    #Return the square root of a number
    if x < 0:
        raise ValueError("Cannot compute square root of a negative number")
    return math.sqrt(x)

def power(x, y):
    #Return x to the power of y
    return math.pow(x, y)

def exponential(x):
    #Return the exponential of a number
    return math.exp(x)

def logarithm(x, base=10):
    #Return the logarithm of a number with a given base
    return math.log(x, base)

def absolute_value(x):
    #Return the absolute value of a number
    return abs(x)

def factorial(x):
    #Return the factorial of a number
    if x < 0:
        raise ValueError("Cannot compute factorial of a negative number")
    if x == 0:
        return 1
    return x * factorial(x - 1)

def sine(angle):
    #Return the sine of an angle in radians
    return math.sin(angle)

def cosine(angle):
    #Return the cosine of an angle in radians
    return math.cos(angle)

def tangent(angle):
    #Return the tangent of an angle in radians
    return math.tan(angle)

def arctangent(x):
    #Return the arctangent of a number
    return math.atan(x)

def hyperbolic_sine(x):
    #Return the hyperbolic sine of a number
    return math.sinh(x)

def hyperbolic_cosine(x):
    #Return the hyperbolic cosine of a number
    return math.cosh(x)

def hyperbolic_tangent(x):
    #Return the hyperbolic tangent of a number
    return math.tanh(x)

def degrees_to_radians(degrees):
    #Convert degrees to radians
    return math.radians(degrees)

def radians_to_degrees(radians):
    #Convert radians to degrees
    return math.degrees(radians)

def euclidean_distance(point1, point2):
    #Calculate the Euclidean distance between two points
    return math.sqrt(sum([(a - b) ** 2 for a, b in zip(point1, point2)]))

def pi():
    #Return the value of pi
    return math.pi

def e():
    #Return the value of e
    return math.e

def quadratic_formula(a, b, c):
    #Solve the quadratic equation ax^2 + bx + c = 0
    discriminant = b**2 - 4*a*c
    if discriminant < 0:
        return None
    elif discriminant == 0:
        return -b / (2*a)
    else:
        root1 = (-b + math.sqrt(discriminant)) / (2*a)
        root2 = (-b - math.sqrt(discriminant)) / (2*a)
        return root1, root2

def midpoint(x1, y1, x2, y2):

    #Calculate the midpoint of a line given two points
    return ((x1 + x2) / 2, (y1 + y2) / 2)

def distance_to_line(point, line):

    #Calculate the distance between a point and a line
    x0, y0 = point
    x1, y1 = line[0]
    x2, y2 = line[1]
    return abs((y2 - y1) * x0 - (x2 - x1) * y0 + x2*y1 - y2*x1) / math.sqrt((y2 - y1)**2 + (x2 - x1)**2)

def discriminant(a, b, c):
    #Calculate the discriminant of a quadratic equation
    return b**2 - 4*a*c

def golden_ratio():
    #Return the golden ratio
    return (1 + math.sqrt(5)) / 2

def logarithm_base_n(x, n):
    #Return the logarithm of a number with base n
    return math.log(x, n)

def natural_logarithm(x):
    #Return the natural logarithm of a number
    return math.log(x)

def inverse_sine(x):
    #Return the inverse sine of a number in radians
    return math.asin(x)

def inverse_cosine(x):
    #Return the inverse cosine of a number in radians
    return math.acos(x)

def inverse_tangent(x):
    #Return the inverse tangent of a number in radians
    return math.atan(x)

def inverse_hyperbolic_sine(x):
  #Return the inverse hyperbolic sine of a number
  return math.asinh(x)

def inverse_hyperbolic_cosine(x):
 #Return the inverse hyperbolic cosine of a number
 return math.acosh(x)

def inverse_hyperbolic_tangent(x):
 #Return the inverse hyperbolic tangent of a number
 return math.atanh(x)

def gamma_function(x):
    #Calculate the Gamma function of x
    return math.gamma(x)

def log_gamma_function(x):
    #Calculate the natural logarithm of the Gamma function of x
    return math.lgamma(x)

def beta_function(x, y):
    #Calculate the Beta function of x and y
    return math.beta(x, y)

def regularized_incomplete_gamma_function(a, x):
    #Calculate the regularized incomplete Gamma function of a and x
    return math.gammainc(a, x)

def inverse_regularized_incomplete_gamma_function(a, p):
    #Calculate the inverse regularized incomplete Gamma function of a and p
    return math.gammaincinv(a, p)

def error_function(x):
    #Calculate the error function of x
    return math.erf(x)

def complementary_error_function(x):
    #Calculate the complementary error function of x
    return math.erfc(x)

def inverse_error_function(x):
    #Calculate the inverse error function of x
    return math.erfinv(x)

def inverse_complementary_error_function(x):
    #Calculate the inverse complementary error function of x
    return math.erfcinv(x)

def chi_squared_distribution_cdf(x, k):
    #Calculate the cumulative distribution function of the chi-squared distribution with k degrees of freedom
    return math.chdtr(k, x)

def chi_squared_distribution_pdf(x, k):
    #Calculate the probability density function of the chi-squared distribution with k degrees of freedom
    return math.chdtrc(k, x)

def beta_distribution_pdf(x, a, b):
    #Calculate the probability density function of the beta distribution with parameters a and b
    return math.beta(a, b) * x**(a-1) * (1-x)**(b-1)

def elliptic_k(m):
    #Calculate the complete elliptic integral of the first kind with parameter m
    return sp.ellipk(m)

def elliptic_e(m):
    #Calculate the complete elliptic integral of the second kind with parameter m
    return sp.ellipe(m)

def elliptic_f(phi, m):
    #Calculate the incomplete elliptic integral of the first kind with parameter m and argument phi
    return sp.ellipf(phi, m)

def elliptic_e_inc(phi, m):
    #Calculate the incomplete elliptic integral of the second kind with parameter m and argument phi
    return sp.ellipeinc(phi, m)

def elliptic_pi(n, phi, m):
    #Calculate the incomplete elliptic integral of the third kind with parameter n, argument phi, and parameter m
    return sp.ellippi(n, phi, m)

def jacobi_theta1(u, q):
    #Calculate the Jacobi theta function of order 1 with argument u and nome q
    return np.exp(np.pi*1j/4) * np.exp(np.pi*1j*u) * np.prod([1 - np.exp(np.pi*1j*2**k*q)*np.exp(2*np.pi*1j*u) for k in range(1, np.inf)])

def jacobi_theta2(u, q):
    #Calculate the Jacobi theta function of order 2 with argument u and nome q
    return np.exp(np.pi*1j/4) * np.prod([1 + np.exp(np.pi*1j*(2*k-1)*q)*np.exp(2*np.pi*1j*u) for k in range(1, np.inf)])

def jacobi_theta3(u, q):
    #Calculate the Jacobi theta function of order 3 with argument u and nome q
    return np.prod([1 + np.exp(np.pi*1j*2*k*q)*np.exp(2*np.pi*1j*u) for k in range(0, np.inf)])

def jacobi_theta4(u, q):
    #Calculate the Jacobi theta function of order 4 with argument u and nome q
    return np.prod([1 - np.exp(np.pi*1j*(2*k+1)*q)*np.exp(2*np.pi*1j*u) for k in range(0, np.inf)])

def bessel_j(n, x):
    #Calculate the Bessel function of the first kind of order n with argument x
    return sp.jv(n, x)

def bessel_y(n, x):
    #Calculate the Bessel function of the second kind of order n with argument x
    return sp.yv(n, x)

def bessel_i(n, x):
    #Calculate the modified Bessel function of the first kind of order n with argument x
    return sp.iv(n, x)

def bessel_k(n, x):
    #Calculate the modified Bessel function of the second kind of order n with argument x
    return sp.kv(n, x)

def hankel1(n, x):
    #Calculate the Hankel function of the first kind of order n with argument x
    return sp.hankel1(n, x)

def hankel2(n, x):
    #Calculate the Hankel function of the second kind of order n with argument x
    return sp.hankel2(n, x)

def spherical_bessel_j(n, x):
    #Calculate the spherical Bessel function of the first kind of order n with argument x
    return sp.spherical_jn(n, x)

def spherical_bessel_y(n, x):
    #Calculate the spherical Bessel function of the second kind of order n with argument x
    return sp.spherical_yn(n, x)

def spherical_hankel1(n, x):
    #Calculate the spherical Hankel function of the first kind of order n with argument x
    return sp.spherical_jn(n, x) + 1j*sp.spherical_yn(n, x)

def spherical_hankel2(n, x):
    #Calculate the spherical Hankel function of the second kind of order n with argument x
    return sp.spherical_jn(n, x) - 1j*sp.spherical_yn(n, x)

def zeta(s):
    #Calculate the Riemann zeta function of s
    if s == 1:
        return math.inf
    elif s < 1:
        return None
    else:
        zeta_sum = 0
        for n in range(1, 1000):
            zeta_sum += 1/n**s
        return zeta_sum

def dirichlet_eta(s):
    #Calculate the Dirichlet eta function of s
    eta_sum = 0
    for n in range(1, 1000):
        eta_sum += (-1)**(n-1) / n**s
    return eta_sum

def alternating_zeta(s):
    #Calculate the alternating zeta function of s
    zeta_sum = 0
    for n in range(1, 1000):
        zeta_sum += (-1)**(n-1) / n**s
    return zeta_sum

def hurwitz_zeta(s, a):
    #Calculate the Hurwitz zeta function of s and a
    zeta_sum = 0
    for n in range(1, 1000):
        zeta_sum += 1/(n+a)**s
    return zeta_sum

def hyp1f1(a, b, z):
    #Calculate the confluent hypergeometric function 1F1(a,b,z)
    hyp_sum = 0
    for n in range(0, 1000):
        hyp_sum += math.gamma(a+n) / (math.gamma(a) * math.gamma(b+n) * math.factorial(n)) * z**n
    return hyp_sum

def hyp2f1(a, b, c, z):
    #Calculate the hypergeometric function 2F1(a,b,c,z)
    hyp_sum = 0
    for n in range(0, 1000):
        hyp_sum += math.gamma(a+n) * math.gamma(b+n) / (math.gamma(a) * math.gamma(b) * math.gamma(c+n) * math.factorial(n)) * z**n
    return hyp_sum

def hyp2f0(a, b, z):
    #Calculate the hypergeometric function 2F0(a,b,z)
    hyp_sum = 0
    for n in range(0, 1000):
        hyp_sum += math.gamma(a+n) * math.gamma(b) / (math.gamma(a) * math.gamma(b+n) * math.factorial(n)) * z**n
    return hyp_sum

def hyp0f1(b, z):
    #Calculate the hypergeometric function 0F1(b,z)
    hyp_sum = 0
    for n in range(0, 1000):
        hyp_sum += 1 / (math.gamma(b+n) * math.factorial(n)) * z**n
    return hyp_sum

def iterated_exponential(x, n):
    #Calculate the iterated exponential function of x, with n iterations
    result = x
    for i in range(1, n+1):
        result = math.exp(result) - 1
    return result