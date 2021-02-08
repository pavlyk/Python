import socket
import time
from collections import defaultdict


class Client:
    def __init__(self, ip, port, timeout=15):
        self.ip = ip
        self.port = port
        self.timeout = timeout
        self.buffer_size = 1024

    def put(self, metric, value, timestamp=None):
        if not timestamp:
            timestamp = str(int(time.time()))
        else:
            timestamp = str(timestamp)
        timestamp += '\n'
        value = str(value)
        message = ' '.join(['put', metric, value, timestamp])
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self.ip, self.port))
            sock.settimeout(self.timeout)
            sock.send(message.encode())  # кодируем в байт строку
            data = sock.recv(self.buffer_size).decode()  # декодируем из байтов

        if data == 'error\nwrong command\n\n':
            raise ClientError()

    def get(self, metric):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self.ip, self.port))
            sock.settimeout(self.timeout)
            key = 'get {}\n'.format(metric)
            sock.send(key.encode())
            data = sock.recv(self.buffer_size).decode()

        if data == 'ok\n\n':  # данных нет
            return {}
        if data[:3] != 'ok\n' or data == 'error\nwrong command\n\n':
            raise ClientError()

        # lstrip Возвращает копию указанной строки, слева которой убраны указанные символы.
        temp_metric_items = data.lstrip('ok\n').rstrip('\n\n')

        # split из строки разбивает на словарь
        metric_items = []
        for i in temp_metric_items.split('\n'):
            if len(i.split()) == 3:
                metric_items.append(i.split())
            else:
                raise ClientError()
        # metric_items = [x.split() if len(x.split()) > 1 for x in metric_items.split('\n')]
        if len(metric_items) == 0:
            raise ClientError()

        # defaultdict при обращении по несуществующему ключу
        # вызвает переданную дефолтную функцию
        metric_dict = defaultdict(list)
        for key, metric, timestamp in metric_items:
            if not isfloat(metric) or not isfloat(timestamp):
                raise ClientError()
            metric_dict[key].append((int(timestamp), float(metric)))

        for i in metric_dict.items():
            metric_dict[i[0]] = sorted(i[1], key=lambda item: item[0])
        # metric_dict = {k: v for k, v in sorted(metric_dict.items(), key=lambda item: item[1][0])}

        return metric_dict


def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


class ClientError(Exception):
    pass
