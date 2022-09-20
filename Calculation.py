from math import sqrt, pi, cos, exp

#import math

Gravitation_Param = 398_600_000_000_000
RADIUS_EARTH = 6371

class Calculations:
    '''
    Класс хранящий расчетные параметры и производящий расчет
    '''
    def __init__(self):
        self.Fly_Time = 0
        self.Start_Orbit_Height = 0
        self.orbit_radius_start = 0

        self.SC_mass_start = 0 # стартовая масса заправленного КА

        self.gas_mass = 0 # Масса рабочего тела
        self.gas_flow_speed = 0  # Скорость истечения рабочего тела

        self.engine_power = 0 # Мощность энергоустановки
        self.engine_thrust = 0 # тяга ДУ

        self.Construct_Mass = 0
        self.Realitive_Construct_Mass = 0



    def set_engines_power(self, val: float) -> None:
        self.engine_power = val

    def set_Engines_Thrust(self, val: float) -> None:
        self.engine_thrust = val

    def set_Fly_Time(self, val):
        self.Fly_Time = val * 86400

    def set_Start_Orbit_Height(self, val):
        self.Start_Orbit_Height = val

    def set_orbit_inclination_start(self, val):
        self.orbit_inclination_start = val * pi / 180

    def set_Finally_Orbit_Height(self, val):
        self.Finally_Orbit_Height = val

    def set_Finally_Orbit_Inclination(self, val):
        self.orbit_inclination_finally = val * pi / 180

    def set_Start_SC_Mass(self, val):
        self.SC_mass_start = val

    def set_Realitive_Construct_Mass(self, val):
        self.Realitive_Construct_Mass = val

    def set_SSS_Realitive_Mass(self, val):
        self.SSS_Realitive_Mass = val

    def set_Gas_Flow_Speed(self, val):
        self.gas_flow_speed = val

    def set_Engine_Specific_Mass(self, val):
        self.Engine_Specific_Mass = val

    def set_Electro_Specific_Mass(self, val):
        self.Electro_Specific_Mass = val

    def set_efficency(self, val):
        self.EFFICIENCY = val * 0.01

    # def db_calc(self):
    #     self.database.db_read()
    #     self.orbit_radius_start = (RADIUS_EARTH + self.Start_Orbit_Height) * 1000
    #     self.orbit_radius_finally = (RADIUS_EARTH + self.Finally_Orbit_Height) * 1000
    #     self.speed_initial = math.sqrt(self.Gravitation_Param / self.orbit_radius_start)
    #     self.speed_delta = self.speed_initial * math.sqrt(
    #         1 - 2 * math.sqrt(self.orbit_radius_start / self.orbit_radius_finally) *
    #         math.cos((math.pi / 2) * (self.orbit_inclination_finally - self.orbit_inclination_start)) +
    #         (self.orbit_radius_start / self.orbit_radius_finally)
    #     )
    #     self.gas_mass = self.SC_mass_start * (
    #             1 - math.exp((-self.speed_delta) / self.gas_flow_speed)
    #     )
    #
    #     self.Construct_Mass = self.Realitive_Construct_Mass * self.SC_mass_start
    #     self.Engines_Mass = self.Engine_Specific_Mass * self.engine_thrust
    #     self.Electro_Mass = self.Electro_Specific_Mass * self.engine_power
    #     self.SSS_Mass = self.SSS_Realitive_Mass * self.gas_mass
    #     self.Payload_Mass = (self.SC_mass_start
    #                          - self.gas_mass
    #                          - self.Construct_Mass
    #                          - self.SSS_Mass
    #                          - self.Engines_Mass
    #                          - self.Electro_Mass)
    #     foo = self.gas_mass / (3 * math.pi)
    #     self.Tank_Radius = 100 * round(pow(foo, 1 / 3))
    #     self.Tank_CTR = round(self.Tank_Radius * 1.5)
    #     self.Body_lenght = round(500 * pow(self.Construct_Mass, 1 / 3))
    #     self.SP_Square = 0.5 * self.engine_power / (1.3 * 0.29 * 0.866)
    #     self.Payload_R = round(math.sqrt(self.Payload_Mass / (0.02 * 1.5 * math.pi)))
    #     self.EnginesCount = round(self.engine_thrust)

    # def optimize_calc(self):
    #     pl_mass=0
    #     for i in range(18):
    #         database.index = i+1
    #         self.db_calc()
    #         if self.Payload_Mass > pl_mass:
    #             pl_mass = self.Payload_Mass
    #             bestindex = database.index
    #     database.index = bestindex
    #     self.db_calc()

    def theor_calc(self):
        self.orbit_radius_start = (RADIUS_EARTH + self.Start_Orbit_Height) * 1000
        self.orbit_radius_finally = (RADIUS_EARTH + self.Finally_Orbit_Height) * 1000
        self.speed_initial = sqrt(Gravitation_Param / self.orbit_radius_start)
        self.speed_delta = self.speed_initial * sqrt(
            1 - 2 * sqrt(self.orbit_radius_start / self.orbit_radius_finally) *
            cos((pi / 2) * (self.orbit_inclination_finally - self.orbit_inclination_start)) +
            (self.orbit_radius_start / self.orbit_radius_finally)
        )
        self.gas_mass = self.SC_mass_start * (
                1 - exp(-self.speed_delta / self.gas_flow_speed)
        )
        self.engine_thrust = (self.gas_flow_speed * self.gas_mass) / self.Fly_Time
        self.engine_power = (self.engine_thrust * self.gas_flow_speed) / (2 * self.EFFICIENCY)
        self.Construct_Mass = self.Realitive_Construct_Mass * self.SC_mass_start
        self.Engines_Mass = self.Engine_Specific_Mass * self.engine_thrust
        self.Electro_Mass = self.Electro_Specific_Mass * self.engine_power
        self.SSS_Mass = self.SSS_Realitive_Mass * self.gas_mass
        self.Payload_Mass = (self.SC_mass_start
                             - self.gas_mass
                             - self.Construct_Mass
                             - self.SSS_Mass
                             - self.Engines_Mass
                             - self.Electro_Mass)
        foo = self.gas_mass / (3 * pi)
        self.Tank_Radius = 100 * round(pow(foo, 1 / 3))
        self.Tank_CTR = round(self.Tank_Radius * 1.5)
        self.Body_lenght = round(500 * pow(self.Construct_Mass, 1 / 3))
        self.SP_Square = 0.5 * self.engine_power / (1.3 * 0.29 * 0.866)
        self.Payload_R = round(sqrt(self.Payload_Mass / (0.02 * 1.5 * pi)))
        self.EnginesCount = round(self.engine_thrust)

    def calc_master(self, mode):
        if mode == 1:
            self.theor_calc()
        elif mode == 2:
            pass  # self.db_calc()
        elif mode == 3:
            pass  # self.optimize_calc()

        self.EFFICIENCY = round(self.EFFICIENCY*100)
        self.speed_initial = round(self.speed_initial, 3)
        self.gas_flow_speed = round(self.gas_flow_speed, 3)
        self.Electro_Mass = round(self.Electro_Mass, 3)
        self.Payload_Mass = round(self.Payload_Mass, 3)
        self.SSS_Mass = round(self.SSS_Mass, 3)
        self.Engines_Mass = round(self.Engines_Mass, 3)
        self.Construct_Mass = round(self.Construct_Mass, 3)
        self.engine_power = round(self.engine_power)
        self.gas_mass = round(self.gas_mass)
        self.engine_thrust = round(1000 * self.engine_thrust / 9.81, 3)
        self.speed_delta = round(self.speed_delta)
