"""
基于ESP32编写的定时器工具类，默认总共4个定时器。
"""

from machine import Timer
import sys

__seats = [Timer(timer_id) for timer_id in range(0, 4)]
__periodic_jobs = []
__one_shot_jobs = []


def __one_shot_handler(func):
    """这个方法用于装饰 one shot timer 的callback, 在定时器执行完回调函数之后释放该 timer, 使该 timer 回到可用列表中"""

    def inner(t):

        try:
            result = func()
        except Exception as e:
            sys.print_exception(e)
            raise e
        finally:
            # 无论回调是否成功, 释放定时器
            t.deinit()
            __seats.append(t)  # 放回可用席位

            # 从注册列表移除
            for job_index in range(len(__one_shot_jobs)):
                if __one_shot_jobs[job_index].get("timer") == t:
                    __one_shot_jobs.pop(job_index)
                    break

        return result

    return inner


class Jobs:

    def add_periodic_job(self, period, callback):
        """添加一个周期性任务。无空闲计时器时抛出IndexError"""
        if not __seats:
            raise IndexError('无空闲可用计时器!')
        timer = __seats.pop(0)
        try:
            timer.init(period=period, mode=Timer.PERIODIC, callback=callback)
            __periodic_jobs.append({"timer": timer, "callback": callback})
        except Exception as e:
            sys.print_exception(e)
            timer.deinit()
            __seats.append(timer)
            for i in range(__periodic_jobs):
                if __periodic_jobs[i].get("timer", None) == timer:
                    __periodic_jobs.pop(i)
                    break

    def add_one_shot_job(self, period, callback):
        """添加一个一次性任务。无空闲计时器时抛出IndexError"""
        if not __seats:
            raise IndexError('无空闲可用计时器!')
        timer = __seats.pop(0)
        try:
            timer.init(period=period, mode=Timer.ONE_SHOT, callback=__one_shot_handler(callback))
            __one_shot_jobs.append({"timer": timer, "callback": callback})
        except Exception as e:
            sys.print_exception(e)
            timer.deinit()
            __seats.append(timer)
            for i in range(__one_shot_jobs):
                if __one_shot_jobs[i].get("timer", None) == timer:
                    __one_shot_jobs.pop(i)
                    break

    def get_registered_periodic_jobs(self, ):
        """获取当前已注册的周期性任务的列表，任务结构为{ "timer": timer, "callback": callback }"""
        return __periodic_jobs

    def get_registered_one_shot_jobs(self, ):
        """获取当前已注册且尚未过期的一次性任务的列表，任务结构为{ "timer": timer, "callback": callback }"""
        return __one_shot_jobs

    def get_registered_jobs(self, ):
        """获取当前所有激活状态的任务"""
        return __periodic_jobs + __one_shot_jobs

    def get_available_seat_amount(self, ):
        """获取当前可用定时器数量"""
        return len(__seats)

    def has_empty_seat(self, ):
        """判断是否有可用计时器"""
        return len(__seats) > 0

    def unregister_job_on_timer(self, timer):
        """取消指定定时器的任务"""

        for i in range(__periodic_jobs):
            if __periodic_jobs[i].get("timer", None) == timer:
                __periodic_jobs.pop(i)
                timer.deinit()
                break
        for i in range(__one_shot_jobs):
            if __one_shot_jobs[i].get("timer", None) == timer:
                __one_shot_jobs.pop(i)
                timer.deinit()
                break
        if timer not in __seats:
            __seats.append(timer)

    def clear_jobs(self, ):
        __seats = [Timer(timer_id) for timer_id in range(0, 4)]
        __periodic_jobs = []
        __one_shot_jobs = []
        for timer in __seats:
            timer.deinit()


jobs = Jobs()

