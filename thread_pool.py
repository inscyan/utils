import time
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED, FIRST_COMPLETED


# 参数times用来模拟网络请求的时间
def get_html(times):
    time.sleep(times)
    print("get page {}s finished".format(times))

    return times


executor = ThreadPoolExecutor(max_workers=2)
urls = [3, 2, 4]  # 并不是真的url
all_task = [executor.submit(get_html, url) for url in urls]
wait(all_task, return_when=ALL_COMPLETED)

all_task_list = [item.result() for item in all_task]
print()
print(all_task_list)  # [3, 2, 4] all_task_list顺序与submit顺序一致

print()
print('main thread')
