import cooler.insulation as ins
import pytest

#@pytest.fixture
#def simple_chart(chart):
#    data = [1,2,3,2]
#    chart.read_data(data)
#    return chart

def test_basic_box_surface_area():
    expected =  6
    assert ins.Box().surface_area == expected

def test_basic_box_insulation():
    expected =  6
    assert ins.Box().conductance == expected

def test_update_box_k_val():
    expected =  3
    box = ins.Box()
    box.set_insulation_k(0.5)
    assert box.conductance == expected

def test_update_box_insulation_thickness():
    expected = 12
    box = ins.Box()
    box.set_insulation_thick(0.5)
    assert box.conductance == expected

def test_update_length():
    expected = 10
    box = ins.Box()
    box.set_length(2)
    assert box.conductance == expected

def test_update_width():
    expected = 10
    box = ins.Box()
    box.set_width(2)
    assert box.conductance == expected

def test_update_height():
    expected = 10
    box = ins.Box()
    box.set_height(2)
    assert box.conductance == expected

def test_updated_misc_heat_flow():
    expected = 8
    box = ins.Box()
    box.set_misc_conductance(2)
    assert box.conductance == expected
