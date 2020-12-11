from item_55_use_queue_to_coordinate_work import ClosableQueue, StoppableWorker
from item_56_recognize_concurrency import Grid, ALIVE, EMPTY


def simulate_pool(pool, grid):
    next_grid = Grid(grid.height, grid.width)

    futures = []
    for y in range(grid.height):
        for x in range(grid.width):
            args = (y, x, grid.get, next_grid.set)
            future = pool.submit(step_cell, *args)  # Fan out
            futures.append(future)

    for future in futures:
        future.result()                             # Fan in

    return next_grid


def count_neighbors(y, x, get):
    n_ = get(y - 1, x + 0)  # North
    ne = get(y - 1, x + 1)  # Northeast
    e_ = get(y + 0, x + 1)  # East
    se = get(y + 1, x + 1)  # Southeast
    s_ = get(y + 1, x + 0)  # South
    sw = get(y + 1, x - 1)  # Southwest
    w_ = get(y + 0, x - 1)  # West
    nw = get(y - 1, x - 1)  # Northwest
    neighbor_states = [n_, ne, e_, se, s_, sw, w_, nw]
    count = 0
    for state in neighbor_states:
        if state == ALIVE:
            count += 1
    return count


def game_logic(state, neighbors):
    if state == ALIVE:
        if neighbors < 2:
            return EMPTY     # Die: Too few
        elif neighbors > 3:
            return EMPTY     # Die: Too many
    else:
        if neighbors == 3:
            return ALIVE     # Regenerate
    return state


def step_cell(y, x, get, set):
    state = get(y, x)
    neighbors = count_neighbors(y, x, get)
    next_state = game_logic(state, neighbors)
    set(y, x, next_state)


def step_cell_thread(item):
    y, x, get, set = item
    out = None
    try:
        step_cell(y, x, get, set)
    except Exception as e:
        out = e
    return y, x, out


class SimulationError(Exception):
    pass


def simulate_pipeline(grid, in_queue, out_queue):
    next_grid = Grid(grid.height, grid.width)
    for y in range(grid.height):
        for x in range(grid.width):
            in_queue.put((y, x, grid.get, next_grid.set))  # Fan out

    in_queue.join()  # wait to process all items and put to out queue
    out_queue.close()  # close out queue since we need to iterate over it

    for item in out_queue:                          # Fan in
        y, x, e = item
        if isinstance(item, Exception):
            raise SimulationError(y, x) from e
    return next_grid


in_queue = ClosableQueue()
out_queue = ClosableQueue()
# Start the threads upfront
threads = []
for _ in range(20):
    thread = StoppableWorker(
        step_cell_thread, in_queue, out_queue)
    thread.start()
    threads.append(thread)

grid = Grid(5, 9)
grid.set(0, 3, ALIVE)
grid.set(1, 4, ALIVE)
grid.set(2, 2, ALIVE)
grid.set(2, 3, ALIVE)
grid.set(2, 4, ALIVE)

columns = []
for i in range(5):
    columns.append(str(grid))
    grid = simulate_pipeline(grid, in_queue, out_queue)

for thread in threads:
    in_queue.close()
for thread in threads:
    thread.join()
