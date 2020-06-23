import os
import math
from sys import argv
import multiprocessing as mp
import time
import timeit


def start(number : int):
    with mp.Pool(processes=2) as my_pool:
        proc = my_pool.starmap(Resheto,
                             iterable=[
                                       [number , 1],
                                       [number , 0]                                       
                                      ],
                             )
        my_pool.close()


def read()->list:
    with open('1st.txt','r',encoding='utf-8') as f1:
        first_read = f1.read()
        list_1 = first_read.split("\n")
    with open('2nd.txt','r',encoding='utf-8') as f2:
            first_read = f2.read()
            list_2 = first_read.split("\n")
    lens=len(list_1)        
    list_12=[False]*lens
    for i in range(0,lens):
        if list_1[i]=="False":
            a=False
        else: 
            a=True
        if list_2[i]=="False":
            b=False
        else: 
            b=True
        list_12[i]=(a+b)%2
    list_3=[False]*len(list_12)
    for id,x in enumerate(list_12):
        if x==1:
            if id%5==0:
                pass
            else:
                list_3[id]=id
    for x in range(5, int(math.sqrt(len(list_12)))):
        if list_3[x]:
            for y in range(x ** 2, number  + 1, x ** 2):
                list_3[y] = False
    return list_3


def Resheto(number : int, x: int):
    if x == 1:
        path = "1st.txt"
        status = "1 the process is over"
        i=1
    elif x == 0:
        path = "2nd.txt"
        status = "2 the process is over"
        i=2
    m_list = [False] * (number +1)
    t=time.time()
    t=int(t)
    for x in range(i, int(math.sqrt(number )) + 1, 2):
        for y in range(1, int(math.sqrt(number )) + 1):
            n = 4 * x ** 2 + y ** 2
            if n <= number  and (n % 12 == 1 or n % 12 == 5):
                m_list[n] = not m_list[n]
            n = 3 * x ** 2 + y ** 2
            if n <= number  and n % 12 == 7:
                m_list[n] = not m_list[n]
            n = 3 * x ** 2 - y ** 2
            if x > y and n <= number  and n % 12 == 11:
                m_list[n] = not m_list[n]
            if int(time.time())-t>3:
                print(x)
                t=time.time()
                t=int(t)
    with open(path, "w", encoding='utf-7') as file_atk:
        for x in m_list:
            string = str(x) + '\n'
            file_atk.write(string)
    print(status)


if __name__ == '__main__':
    try:
        if int(argv[1]) > 0:
            pass
        elif int(argv[1]) < 0:
            raise Exception
        elif int(argv[1]) == 0:
            raise Exception
        else:
            raise Exception
        number  = int(argv[1])
        a = timeit.default_timer()
        start(number )
        time_list = read()
        while len(time_list)>number :
            time_list.pop()
        res=list()
        for index,elem in enumerate(time_list):
            if elem is not False:
                res.append(elem)
        res.sort()
        with open("result.txt", "w", encoding='utf-8') as file:
            file.write("2\n3\n5\n")
            for p in res:
                string = ""+str(p)+"\n"
                file.write(string)
        print("Time to work:", timeit.default_timer()-a)
    except Exception:
        print("Invalid input")
    except BaseException:
        print("Completing the work...")
    except FileNotFoundError:
        pass