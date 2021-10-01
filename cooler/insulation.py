class Wall:
    def __init__(self, thickness, k, length=None, width=None,
                surface_area = None):
        self.t = thickness
        self.k = k
        self.length = length
        self.width = width
        self.__surface_area = surface_area

    @property
    def surface_area(self):
        if self.length and self.width:
            return self.length * self.width

    @property
    def conductance(self):
        return self.k*self.surface_area/self.t

class Box_From_Walls:
    def __init__(self, walls, misc_inflow = 0):
        self.walls = walls
        self.misc_inflow = misc_inflow

    @property
    def surface_area(self):
        return sum([w.surface_area for w in self.walls])

    @property
    def conductance(self):
        return sum([w.conductance for w in self.walls]) + self.misc_inflow

class Box_Uniform_Insulation:
    def __init__(self, length, width, height, thickness, k, misc_inflow = 0):
        self.length = length
        self.width = width
        self.height = height
        self.thickness = thickness # m
        self.k = k # W/m*K
        self.side = Wall(self.thickness, self.k, length = self.length, width = self.height)
        self.front = Wall(self.thickness, self.k, length = self.width, width = self.height)
        self.top = Wall(self.thickness, self.k, length = self.length, width = self.width)
        self.walls = [self.side, self.side, self.front, self.front, self.top, self.top]
        self.misc_inflow = misc_inflow # W/K
        self.box = Box_From_Walls(self.walls, self.misc_inflow)

    @property
    def conductance(self):
        return self.box.conductance
    @property
    def surface_area(self):
        return self.box.surface_area

    @property
    def conductance_kW_per_C(self):
        return self.conductance/1000

    @property
    def conductance_W_per_C(self):
        return self.conductance
