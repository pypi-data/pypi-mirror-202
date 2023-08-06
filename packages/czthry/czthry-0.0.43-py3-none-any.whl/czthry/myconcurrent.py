import concurrent.futures


class ConcurrentFuture(object):
    def __init__(self, action, data_list, max_workers=3, each=None, finish=None, all_together=False):
        '''
        :param action: 每个线程执行的函数
        :param data_list: 数据列表
        :param max_workers: 最大线程数
        :param each: 每个线程执行完毕后的回调函数
        :param finish: 所有线程执行完毕后的回调函数
        :param all_together: 是否等待所有线程执行完毕后再返回结果
        '''
        self.action = action
        self.data_list = data_list
        self.max_workers = max_workers
        self.total = len(data_list)
        self.future_to_data = {}
        self.each = each
        self.finish = finish
        self.all_together = all_together

    def start(self):
        ''' 开始执行 '''
        total = len(self.data_list)
        # 创建线程池
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            for i in range(total):
                data = self.data_list[i]
                future = executor.submit(self.action, i, data, total) # 提交任务
                self.future_to_data[future] = i

        # 获取每个任务的结果
        for future in self.future_to_data:
            i = self.future_to_data[future]
            result = future.result()
            if self.each and callable(self.each):
                self.each(result, index=i, total=total)
        if self.finish and callable(self.finish):
            self.finish()
    pass



def test():
    from czthry import alog
    import time
    logger = alog.Logger()
    def perform_operation(index, data, total):
        result = data * 2
        time.sleep(1)
        logger.d(index+1, '/', total)
        return result

    print('start')
    a = list(range(10))
    c = ConcurrentFuture(perform_operation, a)
    c.start()
    print('done')


if __name__ == '__main__':
    test()
    pass

