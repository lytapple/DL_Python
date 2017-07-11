a = [1,2,3,4]
print(a)
a.append(5)
print(a)
def f(x):
    return x
print([f(x) for x in a])
def add100(x):
    return x+100
list1 = [11,22,33]
print(map(add100,list1))
print([add100(i) for i in list1])
def abc(a,b,c):
    return a*10000 + b*100 + c
list2 = [44,55,66]
list3 = [77,88,99]
print([map(abc,list3,list2,list1)])
result = []

for a in list1:
    for b in list2:
        for c in list3:
            result.append(abc(a,b,c))
print result