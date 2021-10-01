import cooler.insulation as ins
import pytest

#@pytest.fixture
#def simple_chart(chart):
#    data = [1,2,3,2]
#    chart.read_data(data)
#    return chart

def test_basic_box_surface_area():
    expected =  6
    assert ins.Box_Uniform_Insulation(1, 1, 1, 1, 1).surface_area == expected

def test_basic_box_insulation():
    expected =  6
    assert ins.Box_Uniform_Insulation(1, 1, 1, 1, 1).conductance == expected

def test_update_box_k_val():
    expected =  3
    box = ins.Box_Uniform_Insulation(1, 1, 1, 1, 0.5)
    assert box.conductance == expected

def test_update_box_insulation_thickness():
    expected = 12
    box = ins.Box_Uniform_Insulation(1, 1, 1, 0.5, 1)
    assert box.conductance == expected

def test_update_length():
    expected = 10
    box = ins.Box_Uniform_Insulation(2, 1, 1, 1, 1)
    assert box.conductance == expected

def test_update_width():
    expected = 10
    box = ins.Box_Uniform_Insulation(1, 2, 1, 1, 1)
    assert box.conductance == expected

def test_update_height():
    expected = 10
    box = ins.Box_Uniform_Insulation(1, 1, 2, 1, 1)
    assert box.conductance == expected

def test_updated_misc_heat_flow():
    expected = 8
    box = ins.Box_Uniform_Insulation(1, 1, 1, 1, 1, misc_inflow = 2)
    assert box.conductance == expected

def test_wall_conductance():
    expected = 0.5
    wall = ins.Wall(2, 1, length=1, width=1)
    assert wall.surface_area == 1 # m^2
    assert wall.conductance == expected

def test_insulator_from_walls():
    expected = 3
    wall = ins.Wall(2, 1, length=1, width=1)
    walls = [wall]*6
    box = ins.Box_From_Walls(walls)
    assert box.surface_area == 6 # m^2
    assert box.conductance == expected
