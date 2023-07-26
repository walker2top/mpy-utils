import time


def wait_until(result, timeout_second, interval_second=1):
    while timeout_second > 0:
        if result:
            break
        time.sleep(interval_second)
        timeout_second = timeout_second - interval_second
    else:
        raise RuntimeError('function timeout')
