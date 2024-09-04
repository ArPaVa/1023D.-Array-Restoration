from math import log2

def sparse_table(arr):
    n = len(arr)
    min_st = [[0] * (int(log2(n)) + 1) for _ in range(n)]
    for i in range(n):
        min_st[i][0] = i
    
    j = 1
    pot = (1 << j) # (2 ** j)
    while pot <= n:
        i = 0
        while i + pot - 1 < n:
            # If arr[lookup[i][j-1]] <= arr[lookup[i+2^(j-1)][j-1]]
            #     lookup[i][j] = lookup[i][j-1]
            # Else 
            #     lookup[i][j] = lookup[i+2^(j-1)][j-1]
            if arr[min_st[i][j-1]] <= arr[min_st[i + (1 << (j-1)) ][j-1]]:
                min_st[i][j] = min_st[i][j-1]
            else:
                min_st[i][j] = min_st[i + (1 << (j-1)) ][j-1]
                
            i += 1
        j += 1
        pot = (1 << j)
    return min_st

def rmq(arr, st, l, r):
    j = int(log2(r - l + 1))
    if arr[st[l][j]] <= arr[st[r - (1 << j) + 1][j]]:
        return arr[st[l][j]]
    return arr[st[r - (1 << j) + 1][j]]
    
    
first_line = input()
n, q = first_line.split() # 1 <= n, q <= 2 * 10^5
n = int(n)
q = int(q)
line = input()
line = line.split()
def arr_resto(line):
    result_str = ""
    query_count = [[] for i in range(q+1)]
    arr = []
    are_zeros = False
    max_total = 0
    for i in range(len(line)):
        arr.append(int(line[i]))
        query_count[arr[i]].append(i)
        max_total = max(max_total, arr[i])
        if arr[i] == 0: 
            are_zeros = True        

    if max_total < q and max_total > 0 and are_zeros:
        arr[query_count[0][0]] = q   
         
    if max_total == 0:
        result_str = f"{q} " * (n-1)
        result_str += f"{q}"
        print("YES")
        print(result_str)
        return
    if not are_zeros and max_total < q:
        print("NO")
        return
    
    if are_zeros:
        for i in range(n):
            if arr[i] == 0:
                for j in range(i+1,n):
                    if arr[j] == 0:
                        continue
                    else:
                        arr[i] = arr[j]
                        break
                    
                if arr[i] == 0:
                    arr[i] = arr[i-1]
                
    min_st = sparse_table(arr)
    
    for i in range(q, 0, -1):
        if len(query_count[i]) > 1:
            first = query_count[i][0]
            last = query_count[i][len(query_count[i]) - 1]
            if first == last:
                continue
            min_ = rmq(arr, min_st, first, last)
            if min_ != i:
                print("NO")
                return
            
    for i in range(n-1):
        result_str += f"{arr[i]} "
    result_str += f"{arr[n-1]}"
    print("YES")
    print(result_str)           
            
        

arr_resto(line)

""" 100 100
19 67 31 66 29 23 62 17 63 93 71 87 82 62 38 49 77 35 61 36 32 18 93 7 31 73 17 3 15 82 80 19 26 87 38 57 30 86 31 8 21 22 93 52 41 3 92 29 45 18 93 18 80 9 5 52 9 65 85 79 33 50 5 11 49 14 64 86 81 5 58 32 24 92 39 86 97 37 55 80 35 93 14 97 55 97 96 3 6 91 85 61 13 26 93 61 42 74 77 73
"""
# rmq usage
# arr = [7, 2, 3, 0, 5, 10, 3, 12, 18]
# arr = [1, 0, 2, 3]
# min_st, max_st = sparse_table(arr)
# print(rmq(arr, min_st, 0, 4), rmq(arr, max_st, 0, 4, False))
# print('max', rmq(arr, max_st, 0, 4))  
# print('max', rmq(arr, max_st, 1, 4))
# print('max', rmq(arr, max_st, 4, 7))
# print('max', rmq(arr, max_st, 7, 8))
# print('min', rmq(arr, min_st, 0, 4))  
# print('min', rmq(arr, min_st, 1, 4))
# print('min', rmq(arr, min_st, 4, 7))
# print('min', rmq(arr, min_st, 7, 8))
