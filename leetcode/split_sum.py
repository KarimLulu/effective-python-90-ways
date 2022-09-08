def splitArray(nums, m) -> int:
    l, r = max(nums)-1, sum(nums)
    ans = float("inf")
    while r - l > 1:
        mid = (r + l) // 2
        # mid is our approximate answer
        cnt, s = 1, 0
        for el in nums:
            if el + s > mid:
                cnt += 1
                s = el
            else:
                s += el
        if cnt <= m:
            r = mid
        else:
            l = mid
    return r

x = [1,4,4]
y = 3
print(splitArray(x, y))
