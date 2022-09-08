def intersect(nums1 , nums2):
    nums1 = sorted(nums1)
    nums2 = sorted(nums2)
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1
    res = []
    j = 0
    for i in range(len(nums1)):

        l, r = j-1, len(nums2)
        while r - l > 1:
            m = (l + r) // 2
            if nums2[m] < nums1[i]:
                l = m
            else:
                r = m
        if r == len(nums2):
            break
        j = r
        if nums1[i] == nums2[j]:
            res.append(nums1[i])
            j += 1
    return res

x = [1,3,8,9,3]
y = [1,0]
print(intersect(x, y))
