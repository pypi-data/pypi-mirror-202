import time
import datetime
import timeit


def output_runtime(func):
    def wrapper(*args, **kwargs):
        print(f"[{datetime.datetime.now()}] Start to run: '{func.__name__}'")
        ts_start = time.time()
        resp = func(*args, **kwargs)
        ts_end = time.time()
        tp = round(ts_end - ts_start, 3)
        print(f"[{datetime.datetime.now()}] '{func.__name__}' running finished, time used: {tp} seconds\n")
        return resp
    return wrapper


if __name__ == '__main__':

    @output_runtime
    def f1(a, b):
        time.sleep(5)
        c = a + b
        print(c)
        return c

    f1(3, 5)
