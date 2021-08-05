class Box:
    def __init__(self):
        self.length = 1
        self.width = 1
        self.height = 1
        self.side = self.length*self.height
        self.front = self.width*self.height
        self.top = self.length*self.width
        self.surface_area = 2*(self.side + self.front+self.top)

        self.misc_inflow = 0 # W/K

        self.k = 1 # W/m*K
        self.ins_thickness = 1 # m
        self.conductance = 1 #W/C
        self.calculate_conductance()

    def set_insulation_k(self,new_k):
        self.k = new_k
        self.calculate_conductance()

    def calculate_conductance(self):
        insulation_conductance = self.k*self.surface_area/self.ins_thickness # W/K
        self.conductance = insulation_conductance + self.misc_inflow

    def set_insulation_thick(self, new_t):
        self.ins_thickness = new_t
        self.calculate_conductance()

    def set_length(self, l):
        self.length = l
        self.calculate_surface_area()
        self.calculate_conductance()

    def set_width(self, w):
        self.width = w
        self.calculate_surface_area()
        self.calculate_conductance()

    def set_height(self, h):
        self.height = h
        self.calculate_surface_area()
        self.calculate_conductance()

    def calculate_surface_area(self):
        self.side = self.length*self.height
        self.front = self.width*self.height
        self.top = self.length*self.width
        self.surface_area = 2*(self.side + self.front+self.top)

    def set_misc_conductance(self, c):
        self.misc_inflow = c
        self.calculate_conductance()

    def get_conductance_kW_per_C(self):
        return self.conductance/1000

    def get_conductance_W_per_C(self):
        return self.conductance
