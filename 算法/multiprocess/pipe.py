from multiprocessing import Process,Queue
import time
import random
def xiaofei(q):
    while 1:
        x = q.get()#取出队列中的内容
        time.sleep(random.randrange(0, 11, 2))
        if x:#判断取出的额内容是不是空,不是空打印
            print("处理"+x)
        else:#取出的内容是空,直接退出循环
            break
def shengchan(q):
    for i in range(10):
        p = 'data'+ str(i)
        time.sleep(random.randrange(0, 11, 2))
        q.put(p)
        print(p)
    q.put(None)#当所有产品都被生产完之后给队列传一个空,用于取出时判断
    
if __name__ == '__main__':
    q = Queue()#实例化队列,并且设置队列最大长度为6
    s = Process(target=shengchan , args=(q,))#开启生产者进程
    s.start()
    x = Process(target=xiaofei , args=(q,))#开启消费者进程
    x.start()
