import asyncio
import contextlib
import math
import random


class EOFError(Exception):
    pass


WARMER = 'Warmer'
COLDER = 'Colder'
UNSURE = 'Unsure'
CORRECT = 'Correct'


class UnknownCommandError(Exception):
    pass


class AsyncConnectionBase:
    def __init__(self, reader, writer):
        """

        :type connection: object
        """
        self.reader = reader
        self.writer = writer

    async def send(self, command):
        line = command + '\n'
        data = line.encode()
        self.writer.write(data)
        await self.writer.drain()

    async def receive(self):
        line = await self.reader.readline()
        if not line:
            raise EOFError('Connection closed')
        return line[:-1].decode()


class AsyncSession(AsyncConnectionBase):

    def __init__(self, *args):
        super().__init__(*args)
        self._clear_state(None, None)

    def _clear_state(self, lower, upper):
        self.lower = lower
        self.upper = upper
        self.secret = None
        self.guesses = []

    async def loop(self):
        while command := await self.receive():
            parts = command.split()
            if parts[0] == "PARAMS":
                self.set_params(parts)
            elif parts[0] == "NUMBER":
                await self.send_number()
            elif parts[0] == "REPORT":
                self.receive_report(parts)
            else:
                raise UnknownCommandError(command)

    def set_params(self, parts):
        assert len(parts) == 3
        lower, upper = int(parts[1]), int(parts[2])
        self._clear_state(lower, upper)

    def next_guess(self):
        if self.secret is not None:
            return self.secret

        while True:
            guess = random.randint(self.lower, self.upper)
            if guess not in self.guesses:
                return guess

    async def send_number(self):
        g = self.next_guess()
        self.guesses.append(g)
        await self.send(format(g))

    def receive_report(self, parts):
        assert len(parts) == 2
        decision = parts[1]
        last = self.guesses[-1]
        if decision == CORRECT:
            self.secret = last
        print(f"Server: {last} is {decision}")


class AsyncClient(AsyncConnectionBase):

    def __init__(self, *args):
        super().__init__(*args)
        self._clear_state()

    def _clear_state(self):
        self.secret = None
        self.last_distance = None

    @contextlib.asynccontextmanager
    async def session(self, lower, upper, secret):
        print(f'Guess a number between {lower} and {upper}!'
              f' Shhhhh, it\'s {secret}.')
        self.secret = secret
        await self.send(f'PARAMS {lower} {upper}')
        try:
            yield
        finally:
            self._clear_state()
            await self.send('PARAMS 0 -1')

    async def request_numbers(self, count):
        for _ in range(count):
            await self.send('NUMBER')
            data = await self.receive()
            yield int(data)
            if self.last_distance == 0:
                return

    async def report_outcome(self, number):
        new_distance = math.fabs(number - self.secret)
        decision = UNSURE

        if new_distance == 0:
            decision = CORRECT
        elif self.last_distance is None:
            pass
        elif new_distance < self.last_distance:
            decision = WARMER
        elif new_distance > self.last_distance:
            decision = COLDER

        self.last_distance = new_distance
        await self.send(f'REPORT {decision}')
        return decision


async def handle_async_connection(reader, writer):
    session = AsyncSession(reader, writer)
    try:
        await session.loop()
    except EOFError:
        pass


async def run_async_server(address):
    server = await asyncio.start_server(handle_async_connection, *address)
    print("server started")
    async with server:
        await server.serve_forever()


async def run_async_client(address):
    streams = await asyncio.open_connection(*address)
    client = AsyncClient(*streams)

    async with client.session(1, 50, 3):
        results = [(x, await client.report_outcome(x))
                   async for x in client.request_numbers(3)]

    async with client.session(10, 15, 12):
        async for number in client.request_numbers(5):
            outcome = await client.report_outcome(number)
            results.append((number, outcome))
    _, writer = streams
    writer.close()
    await writer.wait_closed()
    return results


async def main():
    address = ('127.0.0.1', 1234)
    server = run_async_server(address)
    asyncio.create_task(server)
    await asyncio.sleep(1e-2)
    results = await run_async_client(address)
    for x, y in results:
        print(f"Client: {x} is {y}")


if __name__ == '__main__':
    asyncio.run(main())

