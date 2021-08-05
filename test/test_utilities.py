from chiller import utilities as utils
from icecream import ic

def test_moving_average_single_entry_list():
    test_list = [1]
    assert utils.moving_average(test_list)[0] == 1

def test_moving_average_single_value_list():
    test_list = [1, 1, 1, 1, 1]
    assert utils.moving_average(test_list)[-1] == 1

def test_moving_average_length_averages_list():
    test_list = [0, 0, 0, 0, 1, 1, 1, 1]
    avgs = utils.moving_average(test_list)
    assert len(avgs) == len(test_list)

def test_moving_average_start_end_values():
    test_list = [0, 0, 0, 0, 1, 1, 1, 1]
    avgs = utils.moving_average(test_list)
    assert avgs[0] == 0
    assert avgs[-1] == 1

def test_moving_average_small_window():
    test_list = [0, 0, 0, 0, 1, 1, 1, 1]
    avgs = utils.moving_average(test_list)
    assert avgs[0] == 0
    assert avgs[-1] == 1

def test_moving_average_small_window_2():
    test_list = [0, 1, 2, 3, 4, 5, 6, 7]
    avgs = utils.moving_average(test_list)
    assert avgs[0] == 0.5
    assert avgs[-1] == 6.5

def test_moving_average_even_number_window():
    test_list = [0, 2, 4, 6, 8, 10, 12, 14]
    avgs = utils.moving_average(test_list, window=4)
    assert avgs[0] == 1
    assert avgs[-1] == 12

def test_moving_average_window_larger_than_list():
    test_list = [1, 2, 3, 4, 5]
    avgs = utils.moving_average(test_list, window=8)
    assert avgs[0] == 3

def test_linear_interpolate_1():
    x_target = 0.5
    x_low = 0
    x_high = 1
    y_low = 0
    y_high = 1
    y = utils.linear_interpolate(x_target, x_low, x_high, y_low, y_high)
    assert y == 0.5

def test_linear_interpolate_2():
    x_target = 0.75
    x_low = 0
    x_high = 1
    y_low = 2
    y_high = 4
    y = utils.linear_interpolate(x_target, x_low, x_high, y_low, y_high)
    assert y == 3.5
