import numpy as np

Path = 'diagonal.rle'
#Path = 'Pattern_ex.txt'

def make_number(a):
    num = 0
    l = len(a)
    for i in range(l):
        num += a[i] * 10**(l-i-1)
    return num
        
def count_digits(string):
    dig = []
    c = 0
    for s in string:
        if s.isdigit():
            c += 1
            dig.append(int(s))
            continue
        else:
            return make_number(dig), c
    
def sym_change(a):
    change = a
    if a == 'b':
        change = 0
    elif a == 'o':
        change = 1
    return change


with open(Path, 'r') as f:
    data = f.read()
#print(data)
def load_and_transform(Path):  
    with open(Path, 'r') as f:
        data = []
        for line in f:
            if line[0] != '#' and line[0] != 'x':
                index = -1
                for i in range(len(line)-1):
                    if i >= index:
                        index = - 1
                        if line[i].isdigit():
                            num, step = count_digits(line[i:])
                            index = i + step
                            data.extend([sym_change(line[index])] * (num - 1))
                        elif line[i] == '$':
                            data.append(line[i])
                        elif line[i] == 'b':
                            data.append(0)
                        elif line[i] == 'o':
                            data.append(1)
                        '''elif line[i] == '!':
                            print('!')
                        else:
                            print('That:', line[i])''' 
    data_list = []
    line_list = []
    for d in data:
        if d != '$':
            line_list.append(d)
        elif d == '$':
            data_list.append(line_list)
            line_list = []
    data_list.append(line_list)
     
    lens = [len(l) for l in data_list]
    maxlen = max(lens)
    data_np = np.zeros((len(data_list), maxlen), int)
    mask = np.arange(maxlen) < np.array(lens)[:,None]
    data_np[mask] = np.concatenate(data_list)
    return data_np


                            