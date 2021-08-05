from icecream import ic
import warnings
from cooler import utilities as utils

class Chiller:
    def __init__(self):
        self.target = 0
        self.type = "refrigeration"
        # Data sheet values for calibration
        self.test_ambients = []
        self.test_temps = []
        self.Qs = []
        self.model = carnot_model
        # performance model fit constants
        self.c1 = -1
        self.c2 = 1
        self.t_target = -10

    def set_target(self, t):
        self.target = t

    def add_performance_data_point(self, t_ambient, t_cold, Q):
        self.test_ambients.append(t_ambient)
        self.test_temps.append(t_cold)
        self.Qs.append(Q)
        self.fit_model()

    def set_type(self, type):
        self.type = type
        if self.type == "tec":
            self.model = linear_model
        else:
            self.model = carnot_model

    def get_Q_for_temps(self, t_amb, t_contents):
        q = self.model(t_amb, t_contents, self.c1, self.c2)
        # check for heat pump being overwhelmed
        if q < 0:
            warnings.warn(UserWarning("Large temperature difference detected. Model indicates reverse heat flow through heat pump. Returning 0."))
            q = 0
        if t_contents < self.t_target:
            q = 0
        return q

    def get_Q_kW_for_temps(self, t_amb, t_contents):
        return self.get_Q_for_temps(t_amb, t_contents)/1000

    def fit_model(self):
        starting = [self.c1, self.c2]
        error_func = self.init_calibration_model()
        error, constants = utils.minimize(error_func, starting)
        self.c1 = constants[0]
        self.c2 = constants[1]

    def init_calibration_model(self):
        def model_error(params):
            a = params[0]
            b = params[1]
            error = 0
            for th, tc, q_experimental in zip(self.test_ambients, self.test_temps, self.Qs):
                q_expected = self.model(th, tc, a, b)
                error += (q_expected - q_experimental) ** 2
            return error
        return model_error

    def set_thermostat(self, t):
        self.t_target = t

class TE_LC200(Chiller):
    def __init__(self, thermostat_temp = 20):
        super().__init__()
        self.set_type("tec")
        self.add_performance_data_point(45,0 , 53.8)
        self.add_performance_data_point(0, 0, 250)
        self.set_thermostat(thermostat_temp)

def carnot_model(t_h, t_c, c1, c2):
    t_c = t_c + 273.15
    t_h = t_h + 273.15
    cop_carnot = t_c/(t_h-t_c)
    q = cop_carnot * c1 + c2
    return q

def linear_model(t_h, t_c, c1, c2):
    dt = t_h - t_c
    q = c1 * dt + c2
    return q
