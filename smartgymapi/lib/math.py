from math import pow


def normalize(value, min_value, max_value):
    return (value - min_value) / (max_value - min_value)


def triangle_number(number):
    return (pow(number, 2) + number) / 2
