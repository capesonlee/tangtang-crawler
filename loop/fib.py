def fib_write(n):
    a,b=0,1
    while b<n:
        print(b,end=",")
        a,b=b,a+b
    print()
def for_range(n,s):
    l = range(0,n,s)
    for k in l:
        print(k,end=",")
    print()

