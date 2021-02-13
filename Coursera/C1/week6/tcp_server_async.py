# python3
import asyncio
import sys

counter = 0

async def run_server(host, port):
  server = await asyncio.start_server(serve_client, host, port) # выполняется сразу после запуска скрипта
  await server.serve_forever() # бесконечное ожидание
  print('await server.serve_forever()')

async def serve_client(reader, writer): # сюда попадаем после коннекта от клиента
  global counter
  cid = counter
  counter += 1  # Потоко-безопасно, так все выполняется в одном потоке
  print(f'Client #{cid} connected')

  request = await read_request(reader) # ждем сообщение от приконектившегося клиента
  if request is None:
    print(f'Client #{cid} unexpectedly disconnected')
  else:
    response = await handle_request(request)
    await write_response(writer, response, cid)

async def read_request(reader, delimiter=b'!'):
  request = bytearray()
  while True:
    chunk = await reader.read(4)
    if not chunk:
      # Клиент преждевременно отключился.
      break

    request += chunk
    if delimiter in request:
      return request

  return None

async def handle_request(request):
  await asyncio.sleep(0)
  return request[::-1]

async def write_response(writer, response, cid):
  writer.write(response)
  await writer.drain()
  writer.close()
  print(f'Client #{cid} has been served')


if __name__ == '__main__':
  asyncio.run(run_server('localhost', int(8181)))