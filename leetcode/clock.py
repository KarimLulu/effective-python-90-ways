def angleClock(hour: int, minutes: int) -> float:
    h = hour + minutes / 60
    a1 = 360 * h / 12
    a2 = minutes * 360 / 60
    print(a1, a2)
    return min(abs(a1 - a2), 360 - abs(a1 - a2))


print(angleClock(12, 30))
