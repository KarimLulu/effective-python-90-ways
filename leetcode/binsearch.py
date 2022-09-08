def searchRange(nums, target):
    if not nums:
        return [-1, -1]
    bad, good = -1, len(nums)
    while good - bad > 1:
        m = bad + (good - bad) // 2
        if nums[m] > target:
            good = m
        else:
            bad = m

    bad1, good1 = -1, len(nums)
    while good1 - bad1 > 1:
        m = bad1 + (good1 - bad1) // 2
        if nums[m] < target:
            bad1 = m
        else:
            good1 = m
    if bad > len(nums) - 1 or nums[bad] != target or good1 > len(nums) - 1 or nums[good1] != target:
        return [-1, -1]
    return [good1, bad]

print(searchRange([5,7,7,8,8,10], 6))
print(searchRange([5,7,7,8,8,10], 8))
