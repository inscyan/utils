import time
import random
import multiprocessing


def worker(num):
    time.sleep(random.random())

    return num


if __name__ == '__main__':
    cores = multiprocessing.cpu_count() - 2
    pool = multiprocessing.Pool(processes=cores)

    pool_list = []
    for i in range(10):
        pool_list.append(pool.apply_async(worker, args=(i,)))
    pool.close()
    pool.join()

    print([item.get() for item in pool_list])
