def comp(x, y):
    if x < y:
        return 1
    elif x > y:
        return -1
    else:
        return 0
nums = [3, 2, 8 ,0 , 1]
nums.sort(comp)
print(nums)
