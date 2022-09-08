def smallestDistancePair(nums, k) -> int:
    nums = sorted(nums)
    n = len(nums)
    l, r = 0, max(nums) - min(nums)
    while r > l:
        m = (l + r) // 2  # possible answer
        less = 0
        for i, num in enumerate(nums):
            a, b = -1, n
            while b - a > 1:
                y = (a + b) // 2
                if nums[k] - num <= m:
                    a = y
                else:
                    b = y
            # a is an index
            if a > -1:  # all elements excluding the current
                less += a - i
        print(less, m)
        if less < k:
            l = m + 1
        else:
            r = m
    return r

x = [1,3,1]
k = 1
print(smallestDistancePair(x, k))
