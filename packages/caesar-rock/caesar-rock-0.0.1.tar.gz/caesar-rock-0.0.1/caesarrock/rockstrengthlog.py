import pandas as pd
import matplotlib.pyplot as plt
import sympy as sym
import math
from enum import Enum
import numpy as np

class Data(Enum):
    POROSITY = 'porosity'
    DELTA_TC = 'delta_tc'

class Lit(Enum):
    CLAYSTONE = 'claystone'
    LIMESTONE = 'limestone'
    MARL = 'marl'
    SANDSTONE = 'sandstone'
    SILTSTONE = 'siltstone'

class Grad_poro(Enum):
    EATON = 'eaton'
    ZAMORA = 'zamora'

class RockStrengthLog:
    def __init__(self, df, variable, grad_poro_method, shale_list=None, shale_equation=None, limestone_list=None, limestone_equation=None, \
                 sandstone_list=None, sandstone_equation=None, seabed=None, unconsolidated_density=None, pre_data_rock_density=None, data_depth=None):
        self.df = df
        self.variable = variable
        self.grad_poro_method = grad_poro_method
        self.shale_list = [item.value if isinstance(item, Enum) else item for item in shale_list]
        self.limestone_list = [item.value if isinstance(item, Enum) else item for item in limestone_list]
        self.sandstone_list = [item.value if isinstance(item, Enum) else item for item in sandstone_list]
        self.shale_equation = shale_equation
        self.limestone_equation = limestone_equation
        self.sandstone_equation = sandstone_equation
        self.seabed_depth = seabed
        self.unconsolidated_density = unconsolidated_density
        self.pre_data_rock_density = pre_data_rock_density
        self.data_depth = data_depth
        self.rows_obj = []

        if grad_poro_method == Grad_poro.EATON:
            self.calcule_sigma_ov()
            self.calcule_gov()
            self.calcule_coeff()

        for i, lithology in df.iloc[:, 1].iteritems():

            main_lit = lithology.split('-')[0].lower()

            if main_lit in self.shale_list:
                equation = shale_equation

            elif main_lit in self.limestone_list:
                equation = limestone_equation

            elif main_lit in self.sandstone_list:
                equation = sandstone_equation

            else:
                print('The lithology is not included in any type.')

            porosity = df.iloc[i, 5] if self.variable == Data.POROSITY else None
            gov = df['Gov'].iloc[i] if self.grad_poro_method == Grad_poro.EATON else None
            coeff = self.coeff if self.grad_poro_method == Grad_poro.EATON else None

            row_obj = RockCompressiveStrength(depth = df.iloc[i, 0],  
                                              ecd = df.iloc[i, 2], 
                                              bulk_density = df.iloc[i, 3],
                                              delta_tc = df.iloc[i, 4],
                                              porosity = porosity,
                                              equation = equation,
                                              variable = self.variable,
                                              grad_poro_method = self.grad_poro_method,
                                              gov = gov,
                                              coeff = coeff)
            
            self.rows_obj.append(row_obj)
        
        self.get_df_result()

    def calcule_sigma_ov(self):
        sigma_ov_init = 1.02 * self.seabed_depth + self.unconsolidated_density * 50 + self.pre_data_rock_density * (self.data_depth - (self.seabed_depth + 50))
    
        aux = 0
        for j in range(1, len(self.df)):
            aux = aux + self.df.iloc[j-1, 3] * (self.df.iloc[j, 0] - self.df.iloc[j-1, 0])

        self.sigma_ov = 1.422 * (sigma_ov_init + aux)

    def calcule_gov(self):
        self.df['Gov'] = self.df.apply(lambda row: self.sigma_ov / (0.1704 * row.iloc[0]), axis=1) # lb/gal
    
    def calcule_coeff(self):
        self.coeff = np.polyfit(self.df.iloc[:, 0], self.df.iloc[:, 4], 1)
        
    def get_df_result(self):
        list_calc = []

        for obj in self.rows_obj:
            dict_obj = {}
            dict_obj['Friction angle - deg'] = obj.angle
            dict_obj['UCS - MPa'] = obj.ucs
            dict_obj['CCS - MPa'] = obj.ccs

            list_calc.append(dict_obj)

        df_calc = pd.DataFrame(list_calc)

        self.df_result = pd.concat([self.df, df_calc], axis=1)
        self.df_result = self.df_result.drop('Gov', axis=1)
 
    def plot(self):

        plt.figure(figsize=(5, 12))
        plt.plot(self.df_result['CCS - MPa'], self.df_result.iloc[:, 0], label='CCS')
        plt.ylim(max(self.df_result.iloc[:, 0]), min(self.df_result.iloc[:, 0]))
        plt.legend()
        plt.grid(True)
        plt.show()
    
class RockCompressiveStrength:
    def __init__(self, depth, ecd, bulk_density, delta_tc, porosity, equation, variable, grad_poro_method, gov, coeff):
        self.depth = depth
        self.ecd = ecd
        self.bulk_density = bulk_density
        self.delta_tc = delta_tc
        self.porosity = porosity
        self.equation = equation
        self.variable = variable
        self.grad_poro_method = grad_poro_method
        self.gov = gov
        self.coeff = coeff

        self.calcule_pp()
        self.calcule_dp()
        self.calcule_ucs()
        self.calcule_friction_angle()
        self.calcule_ccs()  
    
    def calcule_pp(self):
        if self.grad_poro_method == Grad_poro.EATON:
            y = self.coeff[0] * self.depth + self.coeff[1]
            self.pp = self.gov - (self.gov - 8.5) * (y / self.delta_tc) ** 1.2

    def calcule_dp(self):
        self.dp = (self.ecd - self.pp) * self.depth * 119.8 * 9.81 * 10 ** (-6)
    
    def calcule_ucs(self):
        self.ucs = self.equation(self.delta_tc) if self.variable == Data.DELTA_TC else self.equation(self.porosity)
    
    def calcule_friction_angle(self):
        phi = sym.Symbol('phi')
        tau = -0.41713 + 0.28907 * self.ucs - 0.00051878 * (self.ucs ** 2)
        eq = (self.ucs / tau) - (2 * sym.cos(phi)) / (1 - sym.sin(phi))
        self.angle = math.degrees(sym.solve(eq, phi)[0])    
    
    def calcule_ccs(self):
        self.ccs = self.ucs + self.dp + 2 * self.dp * \
            math.sin(math.radians(self.angle)) / (1 - math.sin(math.radians(self.angle)))