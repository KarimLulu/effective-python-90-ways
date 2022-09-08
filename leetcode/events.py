import heapq


def maxEvents(events) -> int:
    events = sorted(events)
    total_days = max(s[-1] for s in events)
    day, count = 1, 0
    h = []
    i = 0
    while day <= total_days:
        if i < len(events) and not h:
            day = events[i][0]
        # add events to heap that are ongoing
        while i < len(events) and events[i][0] <= day:
            heapq.heappush(h, events[i][1])  # push end date
            i += 1
        # remove events that already ended
        while h and h[0] < day:
            heapq.heappop(h)
        if h:
            # smth in heap - attend it
            heapq.heappop(h)
            count += 1
        day += 1
    return count


events = [[1,2],[1,2],[1,6],[1,2],[1,2]]
print(maxEvents(events))
