import asyncio, traceback, time
from typing import Tuple
from functools import wraps, partial
from copy import copy
from .warning import deprecated


class TaskItem:
    def __init__(self, index, func, args, kwargs, retry=None) -> None:
        self.index = index
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.retry = retry


def async_wrap(func):
    if asyncio.iscoroutinefunction(func):
        return func
    @wraps(func)
    async def run(*args, loop=None, executor=None, **kwargs):
        if loop is None:
            loop = asyncio.get_event_loop()
        pfunc = partial(func, *args, **kwargs)
        return await loop.run_in_executor(executor, pfunc)
    return run 


class CoroutinePool:
    def __init__(self, n_workers=10, retry=0) -> None:
        self.n_workers = n_workers
        self.wait_list = []
        self.ret_list_when_timeout = None
        self.retry = retry
        self.failed = {}


    def _get_task_result(self, task)->Tuple[bool, str]:
        try:
            return True, task.result()
        except asyncio.CancelledError:
            return False, traceback.format_exc()
        except:
            pass
        try:
            return False, task.exception()
        except:
            return False, traceback.format_exc()


    @deprecated()
    def add_task(self, func, *args, **kwargs):
        task_item = TaskItem(len(self.wait_list), func, args, kwargs)
        self.wait_list.append(task_item)


    def add_task2(self, func, retry=0, *args, **kwargs):
        task_item = TaskItem(len(self.wait_list), func, args, kwargs, retry)
        self.wait_list.append(task_item)


    def create_task(self, task_item:TaskItem):
        func, args, kwargs = task_item.func, task_item.args, task_item.kwargs
        func = async_wrap(func)
        task = asyncio.create_task(func(*args, **kwargs))
        return task
    

    async def run(self, wait_list, delay=0, timeout=100):
        start_time = time.time()
        ret_list = [None]*len(wait_list)
        runner = []
        
        for _ in range(1000000000):
            if (time.time()-start_time)>timeout:
                self.ret_list_when_timeout = ret_list
                raise ValueError(f'Fail to finish task in {timeout}s')

            # create task
            if len(runner)<self.n_workers and wait_list:
                print('create task')
                task_item:TaskItem = wait_list.pop()
                task = self.create_task(task_item)
                runner.append((task_item.index, task, task_item))
            else:
                print('check task')
                # check tasks
                for i, (idx, task, item) in enumerate(runner):
                    if not task.done():
                        continue
                    succeed, result = self._get_task_result(task)
                    if succeed:
                        print('succeed', result)
                        ret_list[idx] = result
                        runner[i] = None
                        if idx in self.failed: del self.failed[idx]
                    elif idx not in self.failed and item.retry>0:
                        print('failed1', result)
                        assert idx==item.index
                        self.failed[idx] = 1
                        task = self.create_task(item)
                        runner[i] = (item.index, task, item)
                    elif idx in self.failed and self.failed[idx]<item.retry:
                        print('failed2', result)
                        self.failed[idx] += 1
                        task = self.create_task(item)
                        runner[i] = (item.index, task, item)
                    else:
                        print('failed3', result)
                        ret_list[idx] = result
                        runner[i] = None
                        if idx in self.failed: del self.failed[idx]
                runner = [r for r in runner if r is not None]

                #exit
                if not runner and not wait_list:
                    print(runner, wait_list)
                    print('break')
                    break
                await asyncio.sleep(delay)
        return ret_list


    def execute(self, delay=0, timeout=100, n_workers=None):
        if n_workers is not None:
            self.n_workers = n_workers
        wait_list = copy(self.wait_list)

        event_loop = asyncio.get_event_loop()
        ret_list = event_loop.run_until_complete(self.run(wait_list, delay, timeout))
        print('finish')
        # ret_list = asyncio.run(run())
        self.wait_list = []
        return ret_list
    

    async def gather(self, delay=0, timeout=100, n_workers=None):
        if n_workers is not None:
            self.n_workers = n_workers
        wait_list = copy(self.wait_list)
        return await self.run(wait_list, delay, timeout)