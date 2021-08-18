import numpy as np

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
    elif a == 0:
        change = 'b'
    elif a == 1:
        change = 'o'
    return change

def add_num(a):
    if a > 1:
        return str(a)
    else:
        return ''

def load_and_transform(path):  
    with open(path, 'r') as f:
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
    data_list = [[0]]
    line_list = [0]
    for d in data:
        if d != '$':
            line_list.append(d)
        elif d == '$':
            line_list.append(0)
            data_list.append(line_list)
            line_list = [0]
    line_list.append(0)
    data_list.append(line_list)
    data_list.append([0])
     
    lens = [len(l) for l in data_list]
    maxlen = max(lens)
    data_np = np.zeros((len(data_list), maxlen), int)
    mask = np.arange(maxlen) < np.array(lens)[:,None]
    data_np[mask] = np.concatenate(data_list)
    return data_np

def rle_encoder(field):
    data_str = ''
    step = 70
    line_len = np.size(field[0])
    count_1 = 0
    t = 0
    for line in field:
        if t != 0:
            if np.all(line == 0):
                count_1 += 1
                continue
            data_str = data_str + add_num(count_1) + '$'
            count_1 = 1
        n1 = line[0]
        num = 1
        for i in range(1, line_len):
            if t > 5 and (len(data_str) % step > step - 5 or len(data_str) % step < 5):
                data_str = data_str + '\n'
            if line[i] == n1:
                num += 1
            elif line[i] != n1:
                data_str = data_str + add_num(num) + sym_change(n1)
                num = 1
                n1 = line[i]
            if i == line_len - 1:
                data_str = data_str + add_num(num) + sym_change(n1)
        t += 1
    return data_str
