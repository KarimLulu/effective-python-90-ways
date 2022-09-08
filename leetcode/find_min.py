def findMin(nums) -> int:
    l, r = -1, len(nums)
    while r - l > 1:
        m = (l + r) // 2
        if nums[m] >= nums[0]:
            l = m
        else:
            r = m
    ans = nums[r] if r < len(nums) else nums[l]
    return min(ans, nums[0])

n = [1,2,1]
print(findMin(n))
