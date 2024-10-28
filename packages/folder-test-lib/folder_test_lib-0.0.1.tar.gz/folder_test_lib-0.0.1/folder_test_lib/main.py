def fibonachi(n:int)->int:
    if n<1:
        return 1
    return fibonachi(n-1)+fibonachi(n-2)

if __name__=='__main__':

    print(fibonachi(4))