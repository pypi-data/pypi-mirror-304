def square_num(num):
    return num ** 2

def cube_num(num):
    return num ** 3

def fact_series(num):
    if num == 0:
        return 1
    else:
        return num * fact_series(num-1)

def is_even_num(num):
    return num % 2 == 0

def is_odd_num(num):
    return num % 2 != 0

def fibonacci_series(n):
    sequence = [0, 1]
    while len(sequence) < n:
        sequence.append(sequence[-1] + sequence[-2])
    return sequence[:n]

def sum_digits(num):
    return sum(int(digit) for digit in str(num))

def reverse_string(s):
    return s[::-1]

def gcdofnum(a, b):
    while b:
        a, b = b, a % b
    return a

def lcmofnum(a, b):
    return abs(a*b)

def convert_to_binary(num):
    return bin(num)[2:]

def convert_to_hex(num):
    return hex(num)[2:]

def convert_to_octal(num):
    return oct(num)[2:]

def count_vowels(s):
    return sum(1 for char in s.lower() if char in 'aeiou')

def find_max_num(lst):
    return max(lst)

def find_min_num(lst):
    return min(lst)

def square_root(num):
    return num ** 0.5

def powerofnum(base, exp):
    return base ** exp

def num_abs_value(num):
    return abs(num)

def is_prime_num(num):
    if num <= 1:
        return False
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True

def sum_list(lst):
    return sum(lst)

def product_list(lst):
    result = 1
    for num in lst:
        result *= num
    return result

def find_mean(lst):
    return sum(lst) / len(lst)

def find_median(lst):
    sorted_list = sorted(lst)
    n = len(sorted_list)
    mid = n // 2
    return (sorted_list[mid] + sorted_list[~mid]) / 2

def find_mode(lst):
    return max(set(lst), key=lst.count)

def linear_search(lst, target):
    for index, value in enumerate(lst):
        if value == target:
            return index
    return -1

def binary_search(lst, target):
    left, right = 0, len(lst) - 1
    while left <= right:
        mid = (left + right) // 2
        if lst[mid] == target:
            return mid
        elif lst[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

def bubble_sort(lst):
    n = len(lst)
    for i in range(n):
        for j in range(0, n-i-1):
            if lst[j] > lst[j+1]:
                lst[j], lst[j+1] = lst[j+1], lst[j]
    return lst

def add_num(num1, num2):
    return num1+num2

def subtract_num(num1, num2):
    return num1-num2

def multiply_num(num1, num2):
    return num1*num2

def divide_num(num1, num2):
    return num1/num2

def modulus_num(num1, num2):
    return num1%num2

def for_loop(num1):
    result = []
    for i in range(num1):
        result.append(i)
    return result

def multiplication_table(num1):
    for i in range(1,11):
        print(f"{num1} X {i} = {num1 * i}")