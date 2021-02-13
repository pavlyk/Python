import asyncio
from collections import defaultdict


def run_server(host, port):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(
        ClientServerProtocol,
        host, port)

    server = loop.run_until_complete(coro)

    try:
        loop.run_forever() # запускаем бесконечный цикл
        # в первою очередь прослушиваются новые входящие подключения
        # потом прослушиваются данные с каждого уже подключенного сокета
        # и далее по кругу
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


class ClientServerProtocol(asyncio.Protocol):
    storage = defaultdict(list)

    def __init__(self):
        super().__init__()

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        resp = self.process_data(data.decode())
        self.transport.write(resp.encode())

    def process_data(self, data):
        data_splitted = data.split()
        if len(data_splitted) < 2:
            return 'error\nwrong command\n\n'
        command = data_splitted[0]
        ret = ''
        if command not in ('get', 'put'):
            ret = 'error\nwrong command\n\n'
        else:
            ret = 'ok\n'

        if command == 'get':
            if len(data_splitted) == 2:
                key = data_splitted[1]
                ret += self.get(key)
            else:
                return 'error\nwrong command\n\n'
        elif command == 'put':
            metric = data_splitted[1:]
            if len(metric) == 3:
                if not isfloat(metric[1]) or not isfloat(metric[2]):
                    return 'error\nwrong command\n\n' 
                self.put(metric)
                ret += '\n'
            else:
                return 'error\nwrong command\n\n'

        return ret

    def get(self, key):
        ret = ''
        if key == '*':
            # отправляем всё
            retl = ''
            newdict = {}
            for i in ClientServerProtocol.storage:
                for v in ClientServerProtocol.storage[i]:
                    newdict[(i, v[1])] = v[0]
            retl = ''
            for i in newdict:
                retl += '{} {} {}\n'.format(i[0], newdict[i], i[1])
            ret = retl + '\n'
        else:
            # отпраляем уникальное значение на одно время
            allvalue = [[key, v1, v2] for (v1, v2) in ClientServerProtocol.storage[key]]
            newdict = {}
            for i in allvalue:
                newdict[(key, i[2])] = i[1]
            retl = ''
            for i in newdict:
                retl += '{} {} {}\n'.format(key, newdict[i], i[1])
            ret = retl + '\n'
        return ret

    def put(self, metric):
        k, v1, v2 = metric
        ClientServerProtocol.storage[k].append((float(v1), int(v2)))
        print(ClientServerProtocol.storage)


def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


# run_server('127.0.0.1', 8888)