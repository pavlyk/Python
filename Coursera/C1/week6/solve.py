'''
На предыдущей неделе вы разработали клиентское сетевое приложение — клиента для сервера метрик, который умеет отправлять и получать всевозможные метрики. Пришло время финального задания — нужно реализовать серверную часть самостоятельно.
Как обычно вам необходимо разработать программу в одном файле-модуле, который вы загрузите на проверку обычным способом. Сервер должен соответствовать протоколу, который был описан в задании к предыдущей неделе. Он должен уметь принимать от клиентов команды put и get, разбирать их, и формировать ответ согласно протоколу. По запросу put требуется сохранять метрики в структурах данных в памяти процесса. По запросу get сервер обязан отдавать данные в правильной последовательности.
На верхнем уровне вашего модуля должна быть объявлена функция run_server(host, port) — она принимает адрес и порт, на которых должен быть запущен сервер.
Для проверки правильности решения мы воспользуемся своей реализацией клиента и будем отправлять на ваш сервер put и get запросы, ожидая в ответ правильные данные от сервера (согласно объявленному протоколу). Все запросы будут выполняться с таймаутом — сервер должен отвечать за приемлемое время.
Сервер должен быть готов к неправильным командам со стороны клиента и отдавать клиенту ошибку в формате, оговоренном в протоколе. В таком случае работа сервера не должна завершаться аварийно.
На последней неделе мы с вами разбирали пример tcp-сервера на asyncio:
import asyncio
class ClientServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport
    def data_received(self, data):
        resp = process_data(data.decode())
        self.transport.write(resp.encode())
loop = asyncio.get_event_loop()
coro = loop.create_server(
    ClientServerProtocol,
    '127.0.0.1', 8181
)
server = loop.run_until_complete(coro)
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()
Данный код создает tcp-соединение для адрса 127.0.0.1:8181 и слушает все входящие запросы. При подключении клиента будет создан новый экземпляр класса ClientServerProtocol, а при поступлении новых данных вызовется метод этого объекта - data_received. Внутри asyncio.Protocol спрятана вся магия обработки запросов через корутины, остается реализовать протокол взаимодействия между клиентом и сервером.
Этот код может использоваться как основа для реализации сервера. Это не обязательное требование. Для реализации задачи вы можете использовать любые вызовы из стандартной библиотеки Python 3. Сервер должен обрабатывать запросы от нескольких клиентов одновременно.
В процессе разработки сервера для тестирования работоспособности вы можете использовать клиент, написанный на предыдущей неделе.
Давайте еще раз посмотрим на текстовый протокол в действии при использовании утилиты telnet:
$: telnet 127.0.0.1 8888
Trying 127.0.0.1...
Connected to localhost.
Escape character is '^]'.
> get test_key
< ok
< 
> got test_key
< error
< wrong command
< 
> put test_key 12.0 1503319740
< ok
< 
> put test_key 13.0 1503319739
< ok
< 
> get test_key 
< ok
< test_key 13.0 1503319739
< test_key 12.0 1503319740
< 
> put another_key 10 1503319739
< ok
< 
> get *
< ok
< test_key 13.0 1503319739
< test_key 12.0 1503319740
< another_key 10.0 1503319739
< 
'''

import asyncio
from collections import defaultdict
from copy import deepcopy


class StorageDriverError(ValueError):
    pass


class Storage:
    """Класс для хранения метрик в памяти процесса"""

    def __init__(self):
        self._data = defaultdict(dict)

    def put(self, key, value, timestamp):
        self._data[key][timestamp] = value

    def get(self, key):

        if key == '*':
            return deepcopy(self._data)

        if key in self._data:
            return {key: deepcopy(self._data.get(key))}

        return {}


class StorageDriver:
    """Класс, предосталяющий интерфейс для работы с хранилищем данных"""

    def __init__(self, storage):
        self.storage = storage

    def __call__(self, data):

        method, *params = data.split()

        if method == "put":
            key, value, timestamp = params
            value, timestamp = float(value), int(timestamp)
            self.storage.put(key, value, timestamp)
            return {}
        elif method == "get":
            key = params.pop()
            if params:
                raise StorageDriverError
            return self.storage.get(key)
        else:
            raise StorageDriverError


class MetricsStorageServerProtocol(asyncio.Protocol):
    """Класс для реализации сервера при помощи asyncio"""

    # Обратите внимание на то, что storage является атрибутом класса, что предоставляет
    # доступ к хранилищу данных для всех экземпляров класса MetricsStorageServerProtocol
    # через обращение к атрибуту self.storage.
    storage = Storage()
    # настройки сообщений сервера
    sep = '\n'
    error_message = "wrong command"
    code_err = 'error'
    code_ok = 'ok'

    def __init__(self):
        super().__init__()
        self.driver = StorageDriver(self.storage)
        self._buffer = b''

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        """Метод data_received вызывается при получении данных в сокете"""

        self._buffer += data

        try:
            request = self._buffer.decode()
            # ждем данных, если команда не завершена символом \n
            if not request.endswith(self.sep):
                return

            self._buffer, message = b'', ''
            raw_data = self.driver(request.rstrip(self.sep))

            for key, values in raw_data.items():
                message += self.sep.join(f'{key} {value} {timestamp}' \
                                         for timestamp, value in sorted(values.items()))
                message += self.sep

            code = self.code_ok
        except (ValueError, UnicodeDecodeError, IndexError):
            message = self.error_message + self.sep
            code = self.code_err

        response = f'{code}{self.sep}{message}{self.sep}'
        # отправляем ответ
        self.transport.write(response.encode())


def run_server(host, port):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(MetricsStorageServerProtocol, host, port)
    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


if __name__ == "__main__":
    run_server("127.0.0.1", 8888)