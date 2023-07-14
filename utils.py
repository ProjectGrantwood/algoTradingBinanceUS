import time
import pandas_ta as ta
import numpy as np

def num_out(str_or_iterable):
    object_type = type(str_or_iterable)
    
    if object_type == list:
        new_list = list(str_or_iterable)
        for i in range(len(new_list)):
            new_list[i] = num_out(new_list[i])
        return new_list
    if object_type == dict:
        new_dict = dict(str_or_iterable)
        for k in new_dict:
            new_dict[k] = num_out(new_dict[k])
        return new_dict
    if object_type == range:
        return num_out(list(str_or_iterable))
    if object_type == str:
        if is_float(str_or_iterable):
            return float(str_or_iterable)
    else:
        return str_or_iterable

def is_float(element):
    try:
        if type(element) == str:
            float(element)
            return True
    except (ValueError, TypeError):
        return False

def get_time():
    return int(time.time() * 1000)

def to_precision(val, precision):
    precision_power = 10**precision
    return round(val * precision_power) / precision_power

def transpose(matrix, key_filter = None):
    transposed = []
    for i in range(len(matrix[0])):
        transposed_row = []
        for row in matrix:
            to_append = None
            if key_filter != None:
                to_append = row[i][key_filter]
            else:
                to_append = row[i]
            transposed_row.append(to_append)
        transposed.append(transposed_row)
    return transposed

def get_angle(price_series, sample_length):
        data = ta.verify_series(price_series)
        angles = data.rolling(sample_length, min_periods = sample_length).apply(np.arctan)
        return angles
    
def get_slope(series, length):
    data = ta.verify_series(ta.mom(series, length))
    slopes = data.rolling(length, min_periods = length)

def get_highest(data_series, length):
    data = ta.verify_series(data_series, length)
    data = data.rolling(length, min_periods=length)
    maximums = data.max()
    return maximums

def get_lowest(data_series, length):
    data = ta.verify_series(data_series, length)
    data = data.rolling(length, min_periods=length)
    minimums = data.min()
    return minimums