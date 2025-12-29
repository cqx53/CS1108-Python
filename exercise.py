import time
"""
众所周知time.time()会回传一个很奇怪（而且很大）的浮点数，代表从1970年到现在过了多久，
但这串浮点数不是很informative，所以我们用time.localtime()函数他就会帮我们换算time.time()的
那个浮点数具体是几年几月几分等等，再加上1970/1/1就是现在的时间。最后，把结果储存在time.struct_time
这个类里面。
调用time.strftime是把一个time.struct_time喂进去，会根据你的f'string'去类里提取元素，
比如你写到'%Y'就会把time.struct_time（算出来）的年捞出来
"""
#print(time.strftime(f'%Y-%m-%d %H:%M:%S', time.localtime()))
a = time.localtime()
time.sleep(61)
print(time.strftime(f'%Y-%m-%d %H:%M:%S', a))