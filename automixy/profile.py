__all__ = ['profile']
import time
from functools import wraps

def profile(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.call_count += 1
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        wrapper.total_time += (end_time - start_time)
        return result

    def print_stats():
        print(f"{func.__name__} was called {wrapper.call_count} times. Total time: {wrapper.total_time:.4f} seconds")

    wrapper.call_count = 0
    wrapper.total_time = 0.0
    wrapper.print_stats = print_stats
    return wrapper