import logging
import threading
import time
from logging import debug, info


class Counter:
    def __init__(self, interval_sec):
        #global log
        self.next_time = time.time()
        self.counter = 0
        self.done = False
        self.interval = interval_sec
        #self.log = log
        log.debug("counter start")
        self.run()

    def run(self):
        if self.done:
            return
        self.next_time += self.interval
        self.counter += 1
        log.debug(f"counter: {self.counter}")
        # arn timer
        threading.Timer(self.next_time - time.time(), self.run).start()

    def stop(self):
        self.done = True
        log.debug("counter stop")


def init_log():
    global log
    # create logger
    log = logging.getLogger('robin')
    log.setLevel(logging.DEBUG)

    # create console handler and set level to debug
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)

    # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    console.setFormatter(formatter)

    log.addHandler(console)
    # log.debug('debug message')
    # log.info('info message')
    # log.warning('warn message')
    # log.error('error message')
    # log.critical('critical message')


if __name__ == "__main__":
    init_log()
    # logging.basicConfig(level=logging.DEBUG, filename='/tmp/temp.log', filemode='w')
    minutes = 24 * 60
    log.debug(f"{minutes} min/day")

    a = Counter(interval_sec=5)

    time.sleep(10)

    a.stop()
