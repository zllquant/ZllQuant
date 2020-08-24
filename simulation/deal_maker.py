from threading import Thread
import time as timer
from queue import Queue
from datetime import datetime, timedelta


class DealMaker:
    def __init__(self):
        self.tick_queue = Queue()
        self.tick_receiver = TickReceiver(self.tick_queue)
        self.feedback_queue = Queue()
        self.feedback_processor = FeedBackProcessor(self.feedback_queue)

    def start(self):
        pass

    def receive_order(self):
        pass

    def receive_tick(self):
        pass

    def deal(self):
        pass


class TickReceiver(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        delta = timedelta(seconds=3)
        time = datetime.strptime('09:30:00', '%H:%M:%S')
        while 1:
            path = ''
            time += delta
            timer.sleep(1)


class OrderReceiver(Thread):
    def __init__(self):
        Thread.__init__(self)


class FeedBackProcessor(Thread):
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
