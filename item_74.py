import logging
import os
import random
import timeit

random.seed(1234)


def timecode_to_index(video_id, timecode):
    return 1234
    # Returns the byte offset in the video data


def request_chunk(video_id, byte_offset, size):
    return video_data[byte_offset:byte_offset + size]


timecode = "01:09:14:28"
size = 20 * 1024 * 1024
video_id = 0
video_data = 100 * os.urandom(1024 * 1024)
byte_offset = timecode_to_index(video_id, timecode)
chunk = request_chunk(video_id, byte_offset, size)


def run_test():
    chunk = request_chunk(video_id, byte_offset, size)
    # socket.send(chunk)


n = 100
result = timeit.timeit(
    stmt='run_test()',
    globals=globals(),
    number=n) / n
total_data_throughput = size / result / (1024 * 1024 * 1024)
print(f'{result:0.9f} seconds, throughput: {total_data_throughput:.3f} Gb')


data = b'shave and a haircut, two bits'
view = memoryview(data)
chunk = view[12:19]
print(chunk)
print(f'Size: {chunk.nbytes}')
print(f'Data in view: {chunk.tobytes()}')
print(f'Underlying data: {chunk.obj}')

video_view = memoryview(video_data)


def run_test():
    return video_view[byte_offset:byte_offset + size]


result = timeit.timeit(
    stmt='run_test()',
    globals=globals(),
    number=n) / n
total_data_throughput = size / result / (2 ** 30)
print(f'{result:0.9f} seconds, throughput: {total_data_throughput:.3f} Gb')


def recv_into(buffer):
    source_data = video_view[byte_offset:byte_offset + size]
    buffer[:] = source_data


class FakeSocket(object):

    def recv(self, size):
        return video_view[byte_offset:byte_offset+size]

    def recv_into(self, buffer, size):
        source_data = video_view[byte_offset:byte_offset + size]
        buffer[:] = source_data


video_cache = video_data[:]
byte_offset = 1234
size = 1024 * 1024
socket = FakeSocket()

# Try a simple example
chunk = socket.recv(size)  # request some data
video_view = memoryview(video_cache)
before = video_view[:byte_offset]
after = video_view[byte_offset + size:]
new_cache = b''.join([before, chunk, after])


# Example 7
def run_test():
    chunk = socket.recv(size)
    before = video_view[:byte_offset]
    after = video_view[byte_offset + size:]
    _ = b''.join([before, chunk, after])


result = timeit.timeit(
    stmt='run_test()',
    globals=globals(),
    number=n) / n

total_data_throughput = size / result / (2 ** 20)
print(f'{result:0.9f} seconds, throughput: {total_data_throughput:.3f} Mb')


# Work with bytearray
try:
    my_bytes = b"hello"
    my_bytes[0] = b"\x79"
except TypeError:
    logging.exception("Bytes are read-only")
else:
    assert False

my_array = bytearray(b"hello")
my_array[0] = 0x79

my_array = bytearray(b'row, row, row your boat')
my_view = memoryview(my_array)
write_view = my_view[3:13]
write_view[:] = b'-10 bytes-'
print(my_array)


# Let's use bytearray
video_array = bytearray(video_cache)
write_view = memoryview(video_array)
chunk = write_view[byte_offset:byte_offset + size]
socket.recv_into(chunk, size)


def run_test():
    chunk = write_view[byte_offset:byte_offset + size]  # take slice of the data
    socket.recv_into(chunk, size)


result = timeit.timeit(
    stmt='run_test()',
    globals=globals(),
    number=100) / 100

total_data_throughput = size / result / (2 ** 30)
print(f'{result:0.9f} seconds, throughput: {total_data_throughput:.3f} Gb')
