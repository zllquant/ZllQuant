from threading import Thread
import time as timer
from queue import Queue
from datetime import datetime, timedelta
import json


class DealMaker(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.tick_queue = Queue()
        self.tick_receiver = TickReceiver(self.tick_queue)

        self.feedback_queue = Queue()
        self.feedback_processor = FeedBackProcessor(self.feedback_queue)

        self.order_queue = Queue()
        self.order_receiver = OrderReceiver(self.order_queue)

        print('启动行情接收...')
        self.tick_receiver.start()
        print('启动反馈处理...')
        self.feedback_processor.start()
        print('启动委托接收...')
        self.order_receiver.start()

    def run(self):
        while 1:
            try:
                tick = self.tick_queue.get_nowait()
                self.on_receive_tick(tick)
            except:
                print("No tick")

            try:
                order = self.order_queue.get_nowait()
                self.on_receive_order(order)
            except:
                print("No order")
            timer.sleep(1)

    def on_receive_order(self, order):
        print(order)

    def on_receive_tick(self, tick):
        print(tick)

    def deal(self):
        pass


class TickReceiver(Thread):
    """Tick数据接收"""

    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        delta = timedelta(seconds=3)
        time = datetime.strptime('09:30:00', '%H:%M:%S')
        path = r'E:\学习资料\量化投资\ZllQuant\simulation\tick_data'
        while 1:
            with open(path, encoding='utf8') as file:
                for line in file:
                    line = line.replace('\n', '').replace('\'', '"')
                    tick = json.loads(line)
                    # tick.update({
                    #     'datetime': time.strftime('%H:%M:%S')
                    # })
                    self.queue.put_nowait(tick)
                    time += delta
            timer.sleep(1)


class OrderReceiver(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue


class FeedBackProcessor(Thread):
    """处理模拟盘的反馈"""

    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while 1:
            try:
                feedback = self.queue.get(timeout=1)
                if feedback is not None:
                    print(feedback)
            except:
                pass

            timer.sleep(1)


if __name__ == '__main__':
    deal_maker = DealMaker()
    deal_maker.start()
