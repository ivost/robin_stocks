import logging
import os
import threading
import time
import robin_stocks as rs
from work.dto import Point

EXPIRATION = 86400  # sec in a day (max)
ETH = "ETH"
BTC = "BTC"


def sensitive(m):
    if len(m) < 2:
        return "."
    l: int = 3 if len(m) > 7 else 1
    return m[:l] + "..." + m[-l:]


def make_point(dct):
    p = Point(dct['begins_at'],
              float(dct['low_price']),
              float(dct['open_price']),
              float(dct['close_price']),
              float(dct['high_price']),
              float(dct['volume'])
              )
    return p


class MyRobin:
    def __init__(self):
        user = os.environ.get("robinhood_username")
        passwd = os.environ.get("robinhood_password")
        log.debug(f"login {user}/{sensitive(passwd)}")
        rs.login(user, passwd, expiresIn=EXPIRATION)

    def eth_hist(self):
        # result is list of data points
        # 5minute, 10minute, 'hour', 'day', 'week'
        interval = '15second'
        interval = '5minute'
        # 'begins_at,open_price,close_price'
        result = rs.crypto.get_crypto_historicals(ETH, interval=interval, span='hour')
        return [make_point(p) for p in result]

        # 240 / 12 pts
        #log.debug(f"{len(ld)}")
        #[print(p) for p in ld]
        # {'begins_at': '2021-02-05T16:35:00Z', 'open_price': '1752.225000', 'close_price': '1733.560000',
        #  'high_price': '1753.045000', 'low_price': '1718.862457', 'volume': 0, 'session': 'reg', 'interpolated': False,
        #  'symbol': 'ETHUSD'}
        #
        # {'begins_at': '2021-02-05T16:40:00Z', 'open_price': '1733.560000', 'close_price': '1732.135000',
        #  'high_price': '1740.965000', 'low_price': '1719.720441', 'volume': 0, 'session': 'reg', 'interpolated': False,
        #  'symbol': 'ETHUSD'}
        #[print(p) for p in ld]
        #### todo: optimization to reduce API calls / volume
        ### cache ids and skip repeated get_crypto_info
        # id = get_crypto_info(symbol[0], info='id')
        # url = urls.crypto_historical(id)

class Counter:
    def __init__(self, interval_sec):
        self.next_time = time.time()
        self.counter = 0
        self.done = False
        self.interval = interval_sec
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

    # logging.basicConfig(level=logging.DEBUG, filename='/tmp/temp.log', filemode='w')

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


def test_timer():
    minutes = 24 * 60
    log.debug(f"{minutes} min/day")
    a = Counter(interval_sec=5)
    time.sleep(10)
    a.stop()


def test_robin():
    r = MyRobin()
    h = r.eth_hist()
    for p in h:
        log.debug(f"{p.dt}  low: {p.low}, open: {p.open}, close: {p.close}, high: {p.high}, delta: {p.close-p.open:.2f}")


if __name__ == "__main__":
    init_log()
    test_robin()
