import chiller.chiller as chill
import pytest
import warnings
from icecream import ic


def test_initialization():
    c = chill.Chiller()

def test_chiller_set_point():
    c = chill.Chiller()
    c.set_target(20)
    assert c.target == 20

def test_heat_move_capacity():
    c = chill.Chiller()

def test_default_chiller_type():
    c = chill.Chiller()
    assert c.type == "refrigeration"

def test_set_chiller_type():
    c = chill.Chiller()
    c.set_type("tec")
    assert c.type == "tec"

def test_set_tec_performance():
    c = chill.Chiller()
    c.set_type("tec")
    t_amb = 20
    Q = 180
    c.add_performance_data_point(t_amb, t_amb, Q)
    assert c.test_ambients[0] == t_amb
    assert c.Qs[0] == Q

def test_tec_add_second_performance_point():
    c = chill.Chiller()
    c.set_type("tec")
    t_amb = 20
    t_cold = 20
    Q = 180
    c.add_performance_data_point(t_amb, t_cold, Q)
    t_amb = 70
    Q = 0
    c.add_performance_data_point(t_amb, t_cold, Q)
    assert len(c.test_ambients) == 2
    assert len(c.Qs) == 2

def test_tec_remove_heat_1():
    c = chill.Chiller()
    c.set_type("tec")
    t_ambient = 30
    t_contents = 10
    c.add_performance_data_point(t_ambient, t_contents, 0)
    t_ambient = 10
    t_contents = 10
    c.add_performance_data_point(t_ambient, t_contents, 50)
    w = c.get_Q_for_temps(20, 10)
    assert w == 25

def test_tec_remove_heat_2():
    c = chill.Chiller()
    c.set_type("tec")
    t_ambient = 20
    t_contents = 10
    c.add_performance_data_point(20, 0, 0)
    c.add_performance_data_point(0, 0, 100)
    w = c.get_Q_for_temps(t_ambient, t_contents)
    assert abs(w - 50) < .1

def test_tec_remove_heat_beyond_model_bounds():
    c = chill.Chiller()
    c.set_type("tec")
    t_ambient = 21
    t_contents = 0
    c.add_performance_data_point(20, 0, 0)
    c.add_performance_data_point(0, 0, 100)
    with pytest.warns(UserWarning):
        heat_flow = c.get_Q_for_temps(t_ambient, t_contents)
        assert heat_flow == 0

def test_tec_remove_heat_thermostat_off():
    c = chill.Chiller()
    c.set_type("tec")
    t_ambient = 20
    t_contents = 10
    c.add_performance_data_point(20, 0, 0)
    c.add_performance_data_point(0, 0, 100)
    c.set_thermostat(20)
    w = c.get_Q_for_temps(t_ambient, t_contents)
    assert w == 0

def test_set_performance():
    c = chill.Chiller()
    delta_t = 10
    Q = 180
    c.add_performance_data_point(10 + delta_t, 10, Q)
    assert c.test_ambients[0] - c.test_temps[0] == delta_t
    assert c.Qs[0] == Q

def test_add_second_performance_point():
    c = chill.Chiller()
    delta_t = 10
    Q = 180
    c.add_performance_data_point(10, 0, Q)
    delta_t = 50
    Q = 5
    c.add_performance_data_point(50, 0, Q)
    assert len(c.test_ambients) == 2
    assert len(c.Qs) == 2

def test_remove_heat_1():
    c = chill.Chiller()
    t_ambient = 15
    t_contents = 0
    c.add_performance_data_point(20, 0, 0)
    c.add_performance_data_point(10, 0, 50)

    w = c.get_Q_for_temps(t_ambient, t_contents)
    assert abs(w -16.5) < 1

def test_LC200_remove_heat_thermostat_off():
    c = chill.TE_LC200(thermostat_temp = 20)
    t_ambient = 30
    t_contents = 10
    w = c.get_Q_for_temps(t_ambient, t_contents)
    assert w == 0

def test_LC200_remove_heat_thermostat_on():
    c = chill.TE_LC200(thermostat_temp = 20)
    t_ambient = 30
    t_contents = 25
    w = c.get_Q_for_temps(t_ambient, t_contents)
    assert w != 0
