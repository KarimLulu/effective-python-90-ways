def majorityElement(nums) -> int:
    count = 0
    maj = None
    for n in nums:
        print(n, maj, count)
        if count == 0:
            maj = n
        if maj == n:
            count += 1
        else:
            count -= 1
    return maj

nums = [3, 3, 4]
print(majorityElement(nums))


