# Численное интегрирование. Оптимизация

import math
import timeit
from concurrent.futures import as_completed
from concurrent.futures import ProcessPoolExecutor
from functools import partial

def func(x): 
    return float(math.cos(x) + math.sin(x))

def integrate(f, a, b, *, n_iter = 10000):
    h = (b - a) / n_iter
    i = a + h
    sum = 0
    while i <= b-h:
        sum += f(i)
        i += h
    sum += (f(b) + f(a)) / 2
    sum *= h
    return float(sum)

def integrate_async(f, a, b, n_jobs, *, n_iter=10000): 
    executor = ProcessPoolExecutor(max_workers = n_jobs)
    spawn = partial(executor.submit, integrate, f, n_iter = n_iter // n_jobs) 
    step = (b - a) / n_jobs
    fs = [spawn(a + i * step, a + (i + 1) * step) for i in range(n_jobs)] 
    return sum(f.result() for f in as_completed(fs)) 

if __name__ == "__main__":
    print("Result for lab 3: ", integrate(func, -10, 10))
    print("Time: ", timeit.timeit('integrate(func, -10, 10)', globals = globals(), number = 100), "\n")

    print("2 flows: ", integrate_async(func, -10, 10, 2))
    print("Time: " ,timeit.timeit('integrate_async(func, -10, 10, 2)', globals = globals(), number = 100), "\n")

    print("4 flows: ", integrate_async(func, -10, 10, 4))
    print("Time: " ,timeit.timeit('integrate_async(func, -10, 10, 4)', globals = globals(), number = 100), "\n")

    print("6 flows: ", integrate_async(func, -10, 10, 6))
    print("Time: " ,timeit.timeit('integrate_async(func, -10, 10, 2)', globals = globals(), number = 100), "\n")
