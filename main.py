import math
from decimal import Decimal, getcontext
import time
import matplotlib.pyplot as plt


def chudnovsky(n):
    getcontext().prec = n + 15
    C = Decimal(426880) * Decimal(10005).sqrt()
    pi_sum = Decimal(0)

    for k in range(n // 14 + 1):
        num = Decimal((-1) ** k) * math.factorial(6 * k) * (13591409 + 545140134 * k)
        den = math.factorial(3 * k) * math.factorial(k) ** 3 * (640320 ** (3 * k))
        pi_sum += num / den

    pi_val = C / pi_sum

    # Convert pi_val to a string and extract the nth digit
    pi_str = str(pi_val)
    digit = int(pi_str[n])

    return digit


def compute_pi_bbp(n):
    getcontext().prec = n + 2  # Set precision to obtain n decimal places

    pi = Decimal(0)
    k = 0
    while k <= n:
        term1 = Decimal(1) / (16 ** k)
        term2 = Decimal(4) / (8 * k + 1)
        term3 = Decimal(2) / (8 * k + 4)
        term4 = Decimal(1) / (8 * k + 5)
        term5 = Decimal(1) / (8 * k + 6)
        pi += term1 * (term2 - term3 - term4 - term5)
        k += 1

    pi_str = str(pi)
    return pi_str[n]  # Extract the desired decimal places


def spigot(x):
    k, a, b, a1, b1 = 2, 4, 1, 12, 4
    while x > 0:
        p, q, k = k * k, 2 * k + 1, k + 1
        a, b, a1, b1 = a1, b1, p*a + q*a1, p*b + q*b1
        d, d1 = a/b, a1/b1
        while d == d1 and x > 0:
            yield int(d)
            x -= 1
            if x == 0:
                break
            a, a1 = 10*(a % b), 10*(a1 % b1)
            d, d1 = a/b, a1/b1


def get_time(func, n):
    start_time = time.time()
    if func != spigot:
        func(n)
    else:
        list(func(n))
    end_time = time.time()
    return end_time - start_time


chudnovsky_time = []
bbp_time = []
spigot_time = []
n = [x for x in range(2, 10002, 500)]
for i in n:
    chudnovsky_time.append(get_time(chudnovsky, i))
    bbp_time.append(get_time(compute_pi_bbp, i))
    spigot_time.append(get_time(spigot, i))

print(chudnovsky_time)
print(bbp_time)
print(spigot_time)

# Plotting results
plt.figure(figsize=(8, 6))
plt.plot(n, chudnovsky_time, label='Chudnovsky')
plt.plot(n, bbp_time, label='Bailey–Borwein–Plouffe')
plt.plot(n, spigot_time, label='Spigot')
plt.xlabel('Number of digits')
plt.ylabel('Time')
plt.title('Results')
plt.legend()
plt.grid(True)
plt.show()
