
import numpy as np

def life(cell_field):
    #t1 = t.time()
    # Подсчет соседей для каждой клетки кроме граничных
    N = (cell_field[0:-2,0:-2] + cell_field[0:-2,1:-1] + cell_field[0:-2,2:] + cell_field[1:-1,0:-2] + 
        cell_field[1:-1,2:] + cell_field[2: ,0:-2] + cell_field[2: ,1:-1] + cell_field[2: ,2:])
    # Применение правил
    birth = np.logical_and(N == 3, np.logical_not(cell_field[1:-1,1:-1]))
    survive = np.logical_and(np.logical_or(N == 2, N == 3), cell_field[1:-1,1:-1])
    cell_field[1:-1,1:-1] = np.logical_or(birth, survive)
    #print('Новое поколение', t.time() - t1)
    return cell_field

if __name__ == "__main__":
    print("This module is not for direct call!")