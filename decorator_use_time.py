import time
import functools


def time_used(unit='s'):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            time_start = time.time()

            # 执行函数
            func_result = func(*args, **kw)

            usetime = time.time() - time_start
            if unit == 'm':
                usetime = usetime / 60
            elif unit == 'h':
                usetime = usetime / 3600
            print('`%s` func time used: %.2f%s' % (func.__name__, usetime, unit))
            return func_result

        return wrapper

    return decorator


@time_used(unit='m')
def func_test(num, loop=1e7):
    for _ in range(int(loop)):
        pass

    return num


if __name__ == '__main__':
    print(func_test(666, loop=1e8))
    print(func_test.__name__)
