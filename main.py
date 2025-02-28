import numpy as np
from functools import reduce

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
              "\t3)различные строки могут быть разделены переносом строки, но это не обязательно(можно ввести строку длины n^2+n\n"
              "\t4)в файле должно быть ровно n^2 коэффициентов\n"
              "\t5)посторонних символов в файле быть не должно\n")
    try:
        f = open(x)
        lines = f.readlines()
        st = ''.join(lines)
        st = st.replace("\n", '')
        list1 = list(map(float, st.split(" ")))
        if (len(list1) != n ** 2 + n): raise Exception("incorrect number of args")
        arr = [list1[i * (n + 1):(i + 1) * (n + 1)] for i in range(n)]
        return arr
    except Exception as e:
        print(e)
        return 0


def read_matrix_from_terminal(n):
    matrix = [[0] * (n + 1) for _ in range(n)]
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
                    matrix[i][j] = x
                    fl = 1
                except Exception as e:
                    print(e)
    return matrix


def weak_get_determinant(matrix, n):
    if n == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    return sum([(-1)**j*matrix[0][j] * weak_get_determinant([row[:j] + row[j + 1:] for row in matrix[1:]], n - 1) for j in range(n)])
def strong_get_determinant(triang_matrix):
    return reduce(lambda x,y: x*y, [triang_matrix[i][i] for i in range(len(triang_matrix))])


def print_matrix(matrix):
    print('[', end='')
    for row in range(len(matrix)):
        if row != len(matrix) - 1:
            print(matrix[row], ',', sep='')
        else:
            print(matrix[row], '].', sep='')


#надо еще сделать чтобы дет на -1 умножался
def find_not_null_row(matrix, row):
    for i in range(row, len(matrix)):
        if matrix[i][row] != 0:
            print(matrix[i], i, row)
            return [matrix[k] for k in range(row)] + [matrix[i]] + [matrix[k] for k in range(row, n) if k!=i]
    return 0



def triang_matrix(matrix):
    for i in range(len(matrix)):
        matrix = find_not_null_row(matrix, i)
        if matrix==0: return 0
        a_i = matrix[i][i]
        x_i = [matrix[i][x]/a_i for x in range(i+1, n+1)]
        for j in range(i+1, n):
            a_j = matrix[j][i]
            matrix[j][i] = 0

            for k in range(i+1, n+1):
                matrix[j][k] = matrix[j][k] - x_i[k-i-1]*a_j
       # print_matrix(matrix)
    return matrix

# variables
n = 0
input_type = -1
matrix = 0

# value_read

# while n == 0:
#    n = get_n()
# while input_type == -1:
#    input_type = get_input_name()
n = 100
input_type = 0
if (input_type == 0):
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
matrix = triang_matrix(matrix)
if matrix==0:
    print("детерминант равен нулю, матрица не является определенной, вычисления закончены")
    exit(0)
print_matrix(matrix)
print(strong_get_determinant(matrix))




#numpy
print("детерминант рассчитанный с помощью сторонних библиотек:", )
# main_part
