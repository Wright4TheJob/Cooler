import cooler.contents as cont
import pytest

def test_initialization():
    contents = cont.Contents()

def test_update_mass():
    contents = cont.Contents()
    contents.set_mass(2)
    assert contents.mass == 2

def test_set_specific_heat():
    contents = cont.Contents()
    contents.set_specific_heat(2)
    assert contents.specific_heat == 2

def test_set_set_latent_heat():
    contents = cont.Contents()
    contents.set_latent_heat(2)
    assert contents.latent_heat == 2

def test_set_temperature():
    contents = cont.Contents()
    contents.set_temp(20)
    assert contents.temp == 20

def test_set_transition_temp():
    contents = cont.Contents()
    contents.set_transition_temp(20)
    assert contents.transition_temp == 20

def test_set_liquid_fraction():
    contents = cont.Contents()
    contents.set_liquid_fraction(0.5)
    assert contents.liquid_fraction == 0.5

def test_same_phase_energy_change():
    specific_heat = 2
    mass = 10
    t0 = 20
    added_energy = 10 #kJ

    c = cont.Contents()
    c.set_temp(t0)
    c.set_specific_heat(specific_heat)
    c.set_mass(mass)
    expected = t0 + added_energy / (specific_heat*mass)
    c.change_energy(added_energy)
    assert c.temp == expected

def test_thaw_point_detection_all_liquid():
    contents = cont.Contents()
    contents.set_temp(1)
    contents.set_liquid_fraction(1)
    assert contents.crosses_thawed_thresh(-20) == True

def test_thaw_point_detection_stay_liquid():
    contents = cont.Contents()
    contents.set_temp(100)
    contents.set_liquid_fraction(1)
    assert contents.crosses_thawed_thresh(-20) == False

def test_thaw_point_detection_from_part_frozen():
    contents = cont.Contents()
    contents.set_temp(0)
    contents.set_transition_temp(0)
    contents.set_liquid_fraction(0.5)
    assert contents.crosses_thawed_thresh(100) == True

def test_thaw_point_detection_from_part_frozen():
    contents = cont.Contents()
    contents.set_temp(0)
    contents.set_transition_temp(0)
    contents.set_liquid_fraction(0.5)
    contents.set_mass(100)
    assert contents.crosses_thawed_thresh(0.1) == False

def test_frozen_point_detection_from_solid():
    contents = cont.Contents()
    contents.set_temp(-10)
    contents.set_transition_temp(0)
    contents.set_liquid_fraction(0)
    assert contents.crosses_frozen_thresh(100) == True

def test_frozen_point_detection_from_solid():
    contents = cont.Contents()
    contents.set_temp(-10)
    contents.set_transition_temp(0)
    contents.set_liquid_fraction(0)
    assert contents.crosses_frozen_thresh(1) == False

def test_frozen_point_detection_from_part_frozen():
    contents = cont.Contents()
    contents.set_temp(0)
    contents.set_transition_temp(0)
    contents.set_liquid_fraction(0.5)
    assert contents.crosses_frozen_thresh(-100) == True

def test_frozen_point_detection_from_part_frozen():
    contents = cont.Contents()
    contents.set_temp(0)
    contents.set_transition_temp(0)
    contents.set_liquid_fraction(0.5)
    contents.set_mass(100)
    assert contents.crosses_frozen_thresh(-0.1) == False

def test_relative_energy_to_liquid():
    contents = cont.Contents()
    contents.set_temp(1)
    contents.set_transition_temp(0)
    contents.set_liquid_fraction(1)
    contents.set_mass(1)
    contents.set_specific_heat(1)
    assert contents.relative_energy_to_liquid() == -1

def test_relative_energy_to_liquid_from_half_frozen():
    contents = cont.Contents()
    contents.set_temp(0)
    contents.set_transition_temp(0)
    contents.set_liquid_fraction(0.5)
    contents.set_mass(1)
    contents.set_specific_heat(1)
    contents.set_latent_heat(1)
    assert contents.relative_energy_to_liquid() == 0.5

def test_relative_energy_to_liquid_from_all_frozen():
    contents = cont.Contents()
    contents.set_temp(-2)
    contents.set_transition_temp(0)
    contents.set_liquid_fraction(0)
    contents.set_mass(1)
    contents.set_specific_heat(1)
    contents.set_latent_heat(1)
    assert contents.relative_energy_to_liquid() == 3

def test_relative_energy_to_solid():
    contents = cont.Contents()
    contents.set_temp(-2)
    contents.set_transition_temp(0)
    contents.set_liquid_fraction(0)
    contents.set_mass(1)
    contents.set_specific_heat(1)
    assert contents.relative_energy_to_solid() == 2

def test_change_energy_across_liquid_thresh():
    contents = cont.Contents()
    contents.set_temp(1)
    contents.set_transition_temp(0)
    contents.set_liquid_fraction(1)
    contents.set_mass(1)
    contents.set_specific_heat(1)
    contents.set_latent_heat(1)
    contents.change_energy(-1.5)
    assert contents.temp == 0
    assert contents.liquid_fraction == 0.5

def test_energy_change_at_liquid_freeze_thresh():
    contents = cont.Contents()
    contents.set_temp(0)
    contents.set_transition_temp(0)
    contents.set_liquid_fraction(1)
    contents.set_mass(1)
    contents.set_specific_heat(1)
    contents.set_latent_heat(1)
    contents.change_energy(-0.5)
    assert contents.temp == 0
    assert contents.liquid_fraction == 0.5

def test_energy_change_during_freeze():
    contents = cont.Contents()
    contents.set_temp(0)
    contents.set_transition_temp(0)
    contents.set_liquid_fraction(0.5)
    contents.set_mass(1)
    contents.set_specific_heat(1)
    contents.set_latent_heat(1)
    contents.change_energy(-0.1)
    assert contents.temp == 0
    assert contents.liquid_fraction == 0.4

def test_full_thaw_from_frozen_threshhold():
    contents = cont.Contents()
    contents.set_temp(0)
    contents.set_transition_temp(0)
    contents.set_liquid_fraction(0)
    contents.set_mass(1)
    contents.set_specific_heat(1)
    contents.set_latent_heat(1)
    contents.change_energy(1.5)
    assert contents.temp == 0.5
    assert contents.liquid_fraction == 1

def test_partial_thaw_from_fully_frozen():
    contents = cont.Contents()
    contents.set_temp(0)
    contents.set_transition_temp(0)
    contents.set_liquid_fraction(0)
    contents.set_mass(1)
    contents.set_specific_heat(1)
    contents.set_latent_heat(1)
    contents.change_energy(0.5)
    assert contents.temp == 0
    assert contents.liquid_fraction == 0.5

def test_partial_thaw_from_fully_frozen():
    contents = cont.Contents()
    contents.set_temp(-1)
    contents.set_transition_temp(0)
    contents.set_liquid_fraction(0)
    contents.set_mass(1)
    contents.set_specific_heat(1)
    contents.set_latent_heat(1)
    contents.change_energy(1.5)
    assert contents.temp == 0
    assert contents.liquid_fraction == 0.5

def test_change_temp_while_frozen():
    contents = cont.Contents()
    contents.set_temp(-1)
    contents.set_transition_temp(0)
    contents.set_liquid_fraction(0)
    contents.set_mass(1)
    contents.set_specific_heat(1)
    contents.set_latent_heat(1)
    contents.change_energy(-1)
    assert contents.temp == -2
    assert contents.liquid_fraction == 0
