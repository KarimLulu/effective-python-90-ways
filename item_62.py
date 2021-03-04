import asyncio
import tempfile
import time
import threading


class NoNewData(Exception):
    pass


async def async_tell(handle):
    return handle.tell()


async def async_seek(handle, *args):
    return handle.seek(*args)


async def async_read(handle):
    return handle.readline()


async def async_readline(handle):
    offset = await async_tell(handle)
    await async_seek(handle, 0, 2)
    length = await async_tell(handle)
    if length == offset:
        raise NoNewData
    await async_seek(handle, 0)
    return await async_read(handle)


def readline(handle):
    offset = handle.tell()
    handle.seek(0, 2)
    length = handle.tell()

    if length == offset:
        raise NoNewData

    handle.seek(offset, 0)
    return handle.readline()


def tail_file(handle, interval, write_func):
    while not handle.closed:
        try:
            line = readline(handle)
        except NoNewData:
            time.sleep(interval)
        except ValueError as err:
            print(err)
        else:
            write_func(line)


def run_threads(handles, interval, size):
    with tempfile.TemporaryFile() as output:
        lock = threading.Lock()

        def write(data):
            with lock:
                output.write(data)

        threads = []
        for handle in handles:
            args = (handle, interval, write)
            thread = threading.Thread(target=tail_file, args=args)
            thread.start()
            threads.append(thread)

        for handle in handles:
            handle.close()

        for thread in threads:
            thread.join()
        print(f"Expected: {size}, got: {output.tell()}")


def get_handles(n_files):
    handles = [tempfile.TemporaryFile() for _ in range(n_files)]
    size = 0
    for handle in handles:
        handle.write(b"Hello world\n")
        size += handle.tell()
        handle.seek(0)
    return handles, size


n_files = 2
interval = 0.1
handles, size = get_handles(n_files)
run_threads(handles, interval, size)


async def tail_file_async(output, handle, interval, write_func):
    loop = asyncio.get_event_loop()
    while not handle.closed:
        try:
            line = await loop.run_in_executor(None, readline, handle)
        except NoNewData:
            await asyncio.sleep(interval)
        except ValueError:
            pass
        else:
            await write_func(output, line)


async def write_async(output, text):
    output.write(text)


async def run_tasks_mixed(handles, interval, size):
    with tempfile.TemporaryFile() as output:
        tasks = []
        for handle in handles:
            coro = tail_file_async(output, handle, interval, write_async)
            task = asyncio.create_task(coro)
            tasks.append(task)

        await asyncio.sleep(0.5)

        for handle in handles:
            handle.close()

        await asyncio.gather(*tasks)
        print(f"Expected: {size}, got: {output.tell()}")


handles, size = get_handles(n_files)
asyncio.run(run_tasks_mixed(handles, interval, size))
