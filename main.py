import copy

import numpy as np
from functools import reduce


class IncorrectArgs(Exception):
    pass

# functions
def get_n():
    n = input("введите размерность матрицы(натуральное число < 21)\n")
    try:
        n = int(n)
        if n > 20 or n < 1: raise Exception
        return n
    except:
        return 0


def get_input_name():
    x = input("введите способ задания элементов - 1 - вручную, 0 - через файл\n")
    try:
        x = int(x)
        if x != 0 and x != 1: raise Exception
        return x
    except:
        return -1


def read_matrix_from_file(n):
    x = input("введите название файла. ВАЖНО! в файле данные должны хранится в следующем виде:\n"
              "\t1)коэффициенты разделены ровно одним пробелом\n"
              "\t2)десятичные дроби записаны через точку\n"
              "\t3)различные строки могут быть разделены переносом строки, но это не обязательно(можно ввести строку длины n^2+n)\n"
              "\t4)в файле должно быть ровно n^2+n коэффициентов\n"
              "\t5)посторонних символов в файле быть не должно\n")

    try:
        f = open(x)
        lines = f.readlines()
        st = ''.join(lines)
        st = st.replace("\n", ' ').replace("  ", ' ')
        list1 = list(map(float, st.split(" ")))
        if (len(list1) != n ** 2 + n): raise IncorrectArgs("incorrect number of args")
        arr = [list1[i * (n + 1):(i + 1) * (n + 1)] for i in range(n)]
        return arr


    except FileNotFoundError:
        print("файл с данным именем не найден")

    except ValueError:
        print("в файле обнаружены посторонние символы (возможно тройной пробел)")

    except IncorrectArgs:
        print("некорректное количество коэффициентов в файле")
    return 0

def read_matrix_from_terminal(n):
    arr = [[0] * (n + 1) for _ in range(n)]
    print("начинайте вводить элементы. ВАЖНО! \n"
          "\t1)десятичные дроби записаны через точку\n"
          "\t2)не вводите некорректные символы")
    for i in range(n):
        for j in range(n + 1):
            fl = 0
            while not fl:
                x = input(f"введите элемент на позиции {i + 1}, {j + 1}\n")
                try:
                    x = float(x)
                    arr[i][j] = x
                    fl = 1
                except Exception:
                    print("вводите конкретные числа!")
    return arr


def print_matrix(arr):
    print('[', end='')
    for row in range(len(arr)):
        if row != len(arr) - 1:
            print(list(map(lambda x: round(x, 2), arr[row])), ',', sep='')
        else:
            print(list(map(lambda x: round(x, 2), arr[row])), '].', sep='')




def weak_get_determinant(matrix, n):
    if n == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    return sum([(-1)**j*matrix[0][j] * weak_get_determinant([row[:j] + row[j + 1:] for row in matrix[1:]], n - 1) for j in range(n)])

def strong_get_determinant(triang_matrix):
    return reduce(lambda x,y: x*y, [triang_matrix[i][i] for i in range(len(triang_matrix))])


def find_not_null_row(arr, row):
    global det_mult
    for i in range(row, len(arr)):
        if arr[i][row] != 0:
            det_mult *= (-1)**(row-i)
            return [arr[k] for k in range(row)] + [arr[i]] + [arr[k] for k in range(row, n) if k!=i]
    return 0


def triangulate_matrix(arr):
    for i in range(len(arr)):
        arr = find_not_null_row(arr, i)
        if arr==0: return 0
        a_i = arr[i][i]
        x_i = [arr[i][x]/a_i for x in range(i+1, n+1)]
        for j in range(i+1, n):
            a_j = arr[j][i]
            arr[j][i] = 0

            for k in range(i+1, n+1):
                arr[j][k] = arr[j][k] - x_i[k-i-1]*a_j
       # print_matrix(matrix)
    return arr


def get_x_vector(tr_matrix):
    answer = [0]*n
    for j in range(n-1, -1, -1):
        answer[j] = tr_matrix[j][n]/tr_matrix[j][j]
        for i in range(j):
            tr_matrix[i][n] -= tr_matrix[i][j]*answer[j]
            tr_matrix[i][j] = 0
    return answer

# variables

matrix = 0
det_mult = 1


# value_read
n = get_n()
while n == 0:
  print("Введите корректное n!")
  n = get_n()


input_type = get_input_name()
while input_type == -1:
    print("Следуйте инструкциям по вводу!")
    input_type = get_input_name()

if input_type == 0:
    while matrix == 0:
        matrix = read_matrix_from_file(n)
    print('ваша матрица:')
    print_matrix(matrix)
else:
    matrix = read_matrix_from_terminal(n)
    print('ваша матрица:')
    print_matrix(matrix)

#det = get_determinant(matrix, n)
#print("рассчитанный детерминант:", det)
#if(det==0):
#    print("детерминант равен нулю, матрица не является определенной, вычисления закончены")
# else:

#прямой ход
matrix_for_np_solving = copy.deepcopy(matrix)
triang_matrix = triangulate_matrix(matrix)

if triang_matrix==0:
    print("ранг матрицы меньше n, матрица не является определенной, вычисления закончены")
    exit(0)
print("Триангулированная матрица: ")
print_matrix(triang_matrix)
print("рассчитанный детерминант:", round(strong_get_determinant(triang_matrix)*det_mult, 2))

#обратный ход
answers =  get_x_vector(triang_matrix)
#print("Рассчитанный вектор неизвестных([x_1, x_2, ...]:", list(map(lambda x: round(x, 3), answers)))
print("Рассчитанный вектор неизвестных([x_1, x_2, ...]:", answers)
print("Рассчитанный вектор невязок([r_1, r_2, ...]", [sum([matrix_for_np_solving[j][i]*answers[i] for i in range(n)]) - matrix_for_np_solving[j][n] for j in range(n)])


#numpy
print("детерминант рассчитанный с помощью сторонних библиотек:",  round(np.linalg.det(np.array(matrix_for_np_solving)[:, :len(matrix_for_np_solving)]), 2))
print("решение СЛАУ расситанное с помощью сторонних библиотек:", np.linalg.solve(np.array(matrix_for_np_solving)[:, :n], np.array(matrix_for_np_solving)[:, n]))
# main_part
