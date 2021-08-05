class Contents:
    def __init__(self):
        self.specific_heat = 1 # kJ/kg*K
        self.mass = 1 # kg
        self.latent_heat = 1 # kJ/kg
        self.temp = 20
        self.transition_temp = 0
        self.liquid_fraction = 1

    def set_mass(self, m):
        self.mass = m
        self.calculate_thermal_mass()
        self.calculate_heat_of_fusion()

    def set_specific_heat(self, s):
        self.specific_heat = s
        self.calculate_thermal_mass()

    def calculate_thermal_mass(self):
        self.thermal_mass = self.specific_heat*self.mass # kJ/K

    def set_latent_heat(self, l):
        self.latent_heat = l
        self.calculate_heat_of_fusion()

    def calculate_heat_of_fusion(self):
        self.heat_of_fusion = self.mass*self.latent_heat

    def set_temp(self, t):
        self.temp = t
        if t < self.transition_temp:
            self.liquid_fraction = 0
        elif t > self.transition_temp:
            self.liquid_fraction = 1

    def set_transition_temp(self, t):
        self.transition_temp = t

    def set_liquid_fraction(self, f):
        self.liquid_fraction = f

    def change_energy(self, e):
        "e is energy moved in (+) or out (-) of the contents, in kJ"
        # Fully liquid
        if self.liquid_fraction == 1 and self.temp > self.transition_temp:
            if self.crosses_thawed_thresh(e):
                remaining_energy = e - self.relative_energy_to_liquid()
                self.temp = self.transition_temp
                self.change_energy(remaining_energy)
            else:
                self.temp = self.temp + e / (self.specific_heat * self.mass)

        # Liquid-freezing boundary
        elif self.liquid_fraction == 1 and self.temp == self.transition_temp:
            if e > 0:
                self.temp = self.temp + e / (self.specific_heat * self.mass)
            else:
                if self.crosses_frozen_thresh(e):
                    remaining_energy = e - self.relative_energy_to_liquid()
                    self.set_liquid_fraction(0)
                    self.change_energy(remaining_energy)
                else:
                    self.liquid_fraction = 1 - abs(e/self.latent_heat)

        # During Freezing
        elif 0 < self.liquid_fraction < 1:
            if self.temp != self.transition_temp:
                raise ValueError('Inconsistant content state. Temperature incorrect for phase state.')
            if self.crosses_thawed_thresh(e):
                remaining_energy = e - self.relative_energy_to_liquid()
                self.temp = self.transition_temp
                self.liquid_fraction = 1
                self.change_energy(remaining_energy)
            elif self.crosses_frozen_thresh(e):
                # subtract energy to get to thresh and recures
                remaining_energy = e - self.relative_energy_to_solid()
                self.temp = self.transition_temp
                self.liquid_fraction = 0
                self.change_energy(remaining_energy)
            else:
                # change liquid fraction and return
                self.liquid_fraction += e / self.heat_of_fusion

        # At freezing-solid threshhold
        elif self.liquid_fraction == 0 and self.temp == self.transition_temp:
            if e < 0:
                self.temp = self.temp + e / (self.specific_heat * self.mass)
            else:
                if self.crosses_thawed_thresh(e):
                    remaining_energy = e - self.relative_energy_to_liquid()
                    self.set_liquid_fraction(1)
                    self.change_energy(remaining_energy)
                else:
                    self.liquid_fraction = e/self.latent_heat

        # Below frozen temp
        elif self.liquid_fraction == 0 and self.temp < self.transition_temp:
            if self.crosses_frozen_thresh(e):
                remaining_energy = e - self.relative_energy_to_solid()
                self.temp = self.transition_temp
                self.change_energy(remaining_energy)
            else:
                self.temp = self.temp + e / (self.specific_heat * self.mass)

    def crosses_thawed_thresh(self, e):
        if self.liquid_fraction == 1:
            return e < self.relative_energy_to_liquid()
        else:
            return e > self.relative_energy_to_liquid()

    def crosses_frozen_thresh(self, e):
        if self.liquid_fraction == 0:
            return e > self.relative_energy_to_solid()
        else:
            return e < self.relative_energy_to_solid()

    def relative_energy_to_liquid(self):
        energy = 0
        delta_T = (self.temp - self.transition_temp)
        if self.liquid_fraction == 1:
            energy = -delta_T * self.specific_heat * self.mass
        elif self.liquid_fraction == 0:
            energy =  -delta_T * self.specific_heat * self.mass + self.heat_of_fusion
        else:
            energy =  (1-self.liquid_fraction) * self.heat_of_fusion
        return energy

    def relative_energy_to_solid(self):
        if self.liquid_fraction == 0:
            return -(self.temp - self.transition_temp) * self.specific_heat * self.mass
        elif self.liquid_fraction == 1:
            return -(self.temp - self.transition_temp) * self.specific_heat * self.mass - self.heat_of_fusion
        else:
            return -self.liquid_fraction * self.heat_of_fusion

class Water(Contents):
    def __init__(self, mass=1, temp=20, liquid_fraction=1):
        specific_heat = 4.187 # kJ/kg*K
        latent_heat = 334 # kJ/kg
        transition_temp = 0
        super().__init__()

        self.set_mass(mass)
        self.set_temp(temp)
        self.set_specific_heat(specific_heat)
        self.set_latent_heat(latent_heat)
        self.set_transition_temp(transition_temp)
# integrity check: if temp != transition_temp liquid_fraction must equal 0 or 1

# Define items separately, combine all by rule of mixtures before starting simulation. Does not work for differing melting temperatures.
