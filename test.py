def enroll(a,b,c=1,d=2):
    print(a,b,c,d)
enroll(10,1)
enroll(1,5)
enroll(1,2,3)
enroll(1,4,d=6)

def calc(numbers):
    sum = 0
    for n in numbers:
        sum = sum + n * n
    return sum
d = calc([3])
print([1,2,3][1:2])
from matplotlib import pyplot as plt
plt.plot([1,2,3] , [1,2,3], '-o')