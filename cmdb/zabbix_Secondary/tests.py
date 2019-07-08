from django.test import TestCase

# Create your tests here.
# aaa = {'a':10, "b":34, "c":11}
# # print({v: k for k, v in aaa.items()})
# # print(for i in sorted({v: k for k, v in aaa.items()}))
# # a={v: k for k, v in aaa.items()}
# # l=[]
# # for i in sorted(a):
# #     l.append((a[i],i))
# # print(l)
# # print(aaa.items())
# # def key(item):
# #     return item[1]
# print(sorted(aaa.items(),key=lambda item:item[1]))
#
# # print(sorted(aaa.items()))
#
# # def key(items):
# #     []
# #     for item in items:
# #         return item[1]
#
# aaa = {'a':10, "b":34, "c":11}

a = ['a,1', "b,3,22", "c,3,4"]
b = ["a,2", "b,1", "d,2"]
d = {i[0]: i for i in a}
for i in b:
    if i[0] in d:
        d[i[0]] = d.get(i[0]) + i[1:]
    else:
        d.setdefault(i[0], i)
print([i for i in d.values()])




# def so(aaa):
#     li = []
#     for item in aaa.items():
#         li.append(key(item))
#     li.sort()
#     return li

# print(so(aaa))
