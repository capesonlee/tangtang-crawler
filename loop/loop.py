from time import sleep,ctime
import threading
import  fib

loops =[3,2,4]


def loop(i,secs):

    print("start loop ",i," at:",ctime())
    sleep(secs)
    print("stop loop ",i," at:",ctime())

def main():
    print("start time ",ctime())
    for i in range(len(loops)):
        loop(i,loops[i])
    print("stop time ",ctime())

def thread_main():
    print("start time ",ctime())
    threads =[]

    nloops = range(len(loops))
    for i in nloops:
        t = threading.Thread(target=loop,args=(i,loops[i]))
        threads.append(t)
    for i in nloops:
        threads[i].start()

    for i in nloops:
        threads[i].join()

    # sleep(12)
    print("all done at: ",ctime())

if __name__=="__main__":
    #main()
    #thread_main()
    fib.fib_write(2999)
    fib.for_range(12,2)
