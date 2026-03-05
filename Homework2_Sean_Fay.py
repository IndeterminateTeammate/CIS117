# Homework 2
# Author: Sean
# Date: 2024-02-12

print("Hello, my name is Sean")

my_id = 1030779

print(f"Padded integer: {my_id:08d}")
print(f"Two decimals: {my_id:.2f}")
print(f"In Binary: {my_id:b}")
print(f"As hexadecimal: {my_id:#x}")

num_digits = len(str(my_id))
first = my_id // (10 ** (num_digits - 1))
last = my_id % 10

print(f"First digit: {first}")
print(f"Last digit: {last}")
print(f"Sum of first and last digits: {first + last}")