# mypackage/decorators.py

import time

def timeit_one(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Время выполнения {func.__name__}: {end_time - start_time:.4f} секунд")
        return result
    return wrapper

@timeit_one
def slow_sum(a, b, delay):
    time.sleep(delay)
    return a + b

if __name__ == "__main__":
    slow_sum(2, 2, delay=1)
