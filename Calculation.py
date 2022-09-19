import math


class calculations():
    Gravitation_Param = 398_600_000_000_000

    def set_Engines_Power(self, val):
        self.Engines_Power = val
    def set_Engines_Thrust(self, val):
        self.Engines_Thrust = val
    def set_Fly_Time(self, val):
        self.Fly_Time = val * 86400

    def set_Start_Orbit_Height(self, val):
        self.Start_Orbit_Height = val

    def set_Start_Orbit_Inclination(self, val):
        self.Start_Orbit_Inclination = val * math.pi / 180

    def set_Finally_Orbit_Height(self, val):
        self.Finally_Orbit_Height = val

    def set_Finally_Orbit_Inclination(self, val):
        self.Finally_Orbit_Inclination = val * math.pi / 180

    def set_Start_SC_Mass(self, val):
        self.Start_SC_Mass = val

    def set_Realitive_Construct_Mass(self, val):
        self.Realitive_Construct_Mass = val

    def set_SSS_Realitive_Mass(self, val):
        self.SSS_Realitive_Mass = val

    def set_Gas_Flow_Speed(self, val):
        self.Gas_Flow_Speed = val

    def set_Engine_Specific_Mass(self, val):
        self.Engine_Specific_Mass = val

    def set_Electro_Specific_Mass(self, val):
        self.Electro_Specific_Mass = val

    def set_efficency(self, val):
        self.EFFICIENCY = val * 0.01

    def db_calc(self):
        self.database.db_read()
        self.Start_Orbit_Radius = (6371 + self.Start_Orbit_Height) * 1000
        self.Finnaly_Orbit_Radius = (6371 + self.Finally_Orbit_Height) * 1000
        self.Initial_Speed = math.sqrt(self.Gravitation_Param / self.Start_Orbit_Radius)
        self.Delta_velocity = self.Initial_Speed * math.sqrt(
            1 - 2 * math.sqrt(self.Start_Orbit_Radius / self.Finnaly_Orbit_Radius) *
            math.cos((math.pi / 2) * (self.Finally_Orbit_Inclination - self.Start_Orbit_Inclination)) +
            (self.Start_Orbit_Radius / self.Finnaly_Orbit_Radius)
        )
        self.Gas_Mass = self.Start_SC_Mass * (
                1 - math.exp((-self.Delta_velocity) / self.Gas_Flow_Speed)
        )

        self.Construct_Mass = self.Realitive_Construct_Mass * self.Start_SC_Mass
        self.Engines_Mass = self.Engine_Specific_Mass * self.Engines_Thrust
        self.Electro_Mass = self.Electro_Specific_Mass * self.Engines_Power
        self.SSS_Mass = self.SSS_Realitive_Mass * self.Gas_Mass
        self.Payload_Mass = (self.Start_SC_Mass
                             - self.Gas_Mass
                             - self.Construct_Mass
                             - self.SSS_Mass
                             - self.Engines_Mass
                             - self.Electro_Mass)
        foo = self.Gas_Mass / (3 * math.pi)
        self.Tank_Radius = 100 * round(pow(foo, 1 / 3))
        self.Tank_CTR = round(self.Tank_Radius * 1.5)
        self.Body_lenght = round(500 * pow(self.Construct_Mass, 1 / 3))
        self.SP_Square = 0.5 * self.Engines_Power / (1.3 * 0.29 * 0.866)
        self.Payload_R = round(math.sqrt(self.Payload_Mass / (0.02 * 1.5 * math.pi)))
        self.EnginesCount = round(self.Engines_Thrust)

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
        self.Start_Orbit_Radius = (6371 + self.Start_Orbit_Height) * 1000
        self.Finnaly_Orbit_Radius = (6371 + self.Finally_Orbit_Height) * 1000
        self.Initial_Speed = math.sqrt(self.Gravitation_Param / self.Start_Orbit_Radius)
        self.Delta_velocity = self.Initial_Speed * math.sqrt(
            1 - 2 * math.sqrt(self.Start_Orbit_Radius / self.Finnaly_Orbit_Radius) *
            math.cos((math.pi / 2) * (self.Finally_Orbit_Inclination - self.Start_Orbit_Inclination)) +
            (self.Start_Orbit_Radius / self.Finnaly_Orbit_Radius)
        )
        self.Gas_Mass = self.Start_SC_Mass * (
                1 - math.exp((-self.Delta_velocity) / self.Gas_Flow_Speed)
        )
        self.Engines_Thrust = (self.Gas_Flow_Speed * self.Gas_Mass) / self.Fly_Time
        self.Engines_Power = (self.Engines_Thrust * self.Gas_Flow_Speed) / (2 * self.EFFICIENCY)
        self.Construct_Mass = self.Realitive_Construct_Mass * self.Start_SC_Mass
        self.Engines_Mass = self.Engine_Specific_Mass * self.Engines_Thrust
        self.Electro_Mass = self.Electro_Specific_Mass * self.Engines_Power
        self.SSS_Mass = self.SSS_Realitive_Mass * self.Gas_Mass
        self.Payload_Mass = (self.Start_SC_Mass
                             - self.Gas_Mass
                             - self.Construct_Mass
                             - self.SSS_Mass
                             - self.Engines_Mass
                             - self.Electro_Mass)
        foo = self.Gas_Mass / (3 * math.pi)
        self.Tank_Radius = 100 * round(pow(foo, 1 / 3))
        self.Tank_CTR = round(self.Tank_Radius * 1.5)
        self.Body_lenght = round(500 * pow(self.Construct_Mass, 1 / 3))
        self.SP_Square = 0.5 * self.Engines_Power / (1.3 * 0.29 * 0.866)
        self.Payload_R = round(math.sqrt(self.Payload_Mass / (0.02 * 1.5 * math.pi)))
        self.EnginesCount = round(self.Engines_Thrust)

    def calc_master(self, mode):
        if mode == 1:
            self.theor_calc()
        elif mode == 2:
            self.db_calc()
        elif mode == 3:
            self.optimize_calc()

        self.EFFICIENCY = round(self.EFFICIENCY*100)
        self.Initial_Speed = round(self.Initial_Speed, 3)
        self.Gas_Flow_Speed = round(self.Gas_Flow_Speed, 3)
        self.Electro_Mass = round(self.Electro_Mass, 3)
        self.Payload_Mass = round(self.Payload_Mass, 3)
        self.SSS_Mass = round(self.SSS_Mass, 3)
        self.Engines_Mass = round(self.Engines_Mass, 3)
        self.Construct_Mass = round(self.Construct_Mass, 3)
        self.Engines_Power = round(self.Engines_Power)
        self.Gas_Mass = round(self.Gas_Mass)
        self.Engines_Thrust = round(1000 * self.Engines_Thrust / 9.81, 3)
        self.Delta_velocity = round(self.Delta_velocity)
