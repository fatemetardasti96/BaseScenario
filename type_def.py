from dataclasses import dataclass
from enum import Enum
from typing import Optional

@dataclass
class Technology:
    PHOTOVOLTAICS = 'photovoltaics'
    GENERATOR = 'generator'
    TRANSMISSION = 'transmission'
    WIND_TURBINE = 'wind turbine'
    STORAGE = 'storage'
    CHP = 'chp'
    HYDRO_TURBINE = 'hydro turbine'
    GEOTHERMAL = 'geothermal'
    NUCLEAR = 'nuclear'
    UNKNOWN = 'unknown'
    ELECTROLYSER = 'electrolyser'
    


@dataclass    
class InputEnergy:
    SOLAR = 'solar radiation'
    LIGNITE = 'lignite'
    HARDCOAL = 'hard coal'
    NATURALGAS = 'natural gas'
    BIOGAS = 'biogas'
    BIOMASS = 'biomass'
    HEAVYOIL = 'heavy oil'
    # UNKNOWN = 'unknown'
    LIGHTOIL = 'light oil'
    URANIUM = 'uranium'
    ELECTRICITY = 'electricity'
    AIR = 'air'
    WASTE = 'waste'
    WATER = 'water'
    HEAT = 'heat'
    ELECTRIC_ENERGY = 'electric_energy'
    H2 = 'H2'
    H2_FC = 'H2_FC'
    WIND_ONS = 'WIND_ONS'
    WIND_OFF = 'WIND_OFF'
    TRADE_IMPORT = 'TRADE_IMPORT'
    HYDROGEN = 'hydrogen'


def is_renewable(energy):
    RENEWABLE = [InputEnergy.SOLAR, InputEnergy.AIR, InputEnergy.WATER, InputEnergy.WIND_OFF, InputEnergy.WIND_ONS, InputEnergy.TRADE_IMPORT]
    if energy in RENEWABLE:
        return True
    return False

    

@dataclass
class OutputEnergy:
    ELECTRICITY = 'electricity'
    CO2 = 'co2'
    ELECTRIC_ENERGY = 'electric_energy'
    BATTERY_ENERGY = 'Battery_Energy'
    H2 = 'H2'
    H2_FC = 'H2_FC'
    HYDRO_ENERGY = 'hydro_energy'
    HYDROGEN = 'hydrogen'


@dataclass
class TechnologyType:
    UTILITY = 'utility'
    ROOFTOP = 'rooftop'
    UNKNOWN = 'unknown'
    HVAC = 'hvac'
    OFFSHORE = 'offshore'
    ONSHORE =  'onshore'
    BATTERY =  'battery'
    PUMPED = 'pumped'
    STEAM = 'steam'
    RUN_OF_RIVER =  'run-of-river'
    GAS =  'gas'
    COMBINED = 'combined cycle'
    COMBUSTION_ENGINE = 'combustion engine'
    HYDROGEN_FUELCELL = 'hydrogen fuelcell'
    HYDROGEN_GAS = 'hydrogen gas'
    TRADE_IMPORT = 'trade import'
    SALT_CAVERN = 'salt cavern'
    ALKALINE = 'alkaline'


@dataclass
class CodeGenerator:
    technology: str 
    input_energy: str
    technology_type: Optional[str] = None


    def to_str(self):
        if not self.technology_type is None:
            return self.technology + '_' + self.input_energy + '_' + self.technology_type
        else:
            return self.technology + '_' + self.input_energy




@dataclass
class Code:
    WIND_ONS = 'WIND_ONS'
    WIND_OFF = 'WIND_OFF'
    PV1 = 'PV1'
    PV2 = 'PV2'
    ROR = 'ROR'
    OIL_TURBINE = 'OIL_TURBINE'
    GASN_TURBINE = 'GASN_TURBINE'
    GASN_TURBINE_CHP = 'GASN_TURBINE_CHP'
    CH4_OCTURBINE = 'CH4_OCTURBINE'
    CH4_TURBINE = 'CH4_TURBINE'
    NUCLEAR_TURBINE = 'NUCLEAR_TURBINE'
    NUCLEAR_TURBINE_GEN = 'NUCLEAR_TURBINE_GEN'
    LIGNITE_OCTURBINE = 'LIGNITE_OCTURBINE'
    LIGNITE_CHP = 'LIGNITE_CHP'
    HARDCOAL_OCTURBINE = 'HARDCOAL_OCTURBINE'
    HARDCOAL_OCTURBINE_CHP = 'HARDCOAL_OCTURBINE_CHP'
    BIOMASS_TURBINE = 'BIOMASS_TURBINE'
    BIOMASS_TURBINE_CHP = 'BIOMASS_TURBINE_CHP'
    BIO_CH4_TURBINE = 'BIO_CH4_TURBINE'
    BIO_CH4_TURBINE_CHP = 'BIO_CH4_TURBINE_CHP'
    BATPOWER = 'BATPOWER'
    BIOMASS_FURNANCE = 'BIOMASS_FURNANCE'
    BIOMASS_FURNANCE_CHP = 'BIOMASS_FURNANCE_CHP'
    GEO = 'GEO'
    LIGHT_OIL = 'LIGHT_OIL'
    LIGHT_OIL_CHP = 'LIGHT_OIL_CHP'
    HEAVY_OIL = 'HEAVY_OIL'
    PH_TURBINE = 'PH_TURBINE'
    PH_TURBINE_PUMP = 'PH_TURBINE_PUMP'
    GAS_TURBINE = 'GAS_TURBINE'
    GAS_TURBINE_CHP = 'GAS_TURBINE_CHP'
    CH4_CCTURBINE = 'CH4_CCTURBINE'
    CH4_CCTURBINE_CHP = 'CH4_CCTURBINE_CHP'
    H2_ELECTROLYSER = 'H2_ELECTROLYSER'
    # H2_ELECTROLYSER_FC = 'H2_ELECTROLYSER_FC'
    GAS_H2 = 'GAS_H2'
    H2 = 'H2'
    # H2_FC = 'H2_FC'
    H2_storage_GASTURBINE = 'H2_storage_gasturbine'
    # H2_storage_FUEL = 'H2_storage_fuel_cell'
    # FUEL_CELL = 'FUEL_CELL'
    BAT1POWER = 'BAT1POWER'
    Battery_Energy_storage = 'Battery_Energy_storage'
    PH_storage = 'PH_storage'
    CCH2_TURBINE = 'CCH2_TURBINE'
    TRANSMISSION_IMPORT = 'TRANSMISSION_IMPORT'




@dataclass
class Cost:
    VARIABLE_COST = 'variable costs'
    FIXED_COST = 'fixed costs'
    CAPITAL_COST = 'capital costs'
    FUEL_COST = 'fuel costs'

@dataclass
class Unit:
    hour_based = "€/MWh"
    yearly_based = "€/MW/a"
    normal = "€/MW"


class Converter(Enum):
    PHOTOVOLTAICS = 'photovoltaics'
    WIND_TURBINE = 'wind turbine'
    HYDRO_TURBINE = 'hydro turbine'    
    ELECTROLYSER = 'electrolyser'
    

class ConverterStorageTech(Enum):
    BATTERY = TechnologyType.BATTERY
    PUMPED = TechnologyType.PUMPED
    # HYDROGEN_GAS = TechnologyType.HYDROGEN_GAS
    # FUEL_CELL = TechnologyType.HYDROGEN_FUELCELL

class MultiConverter(Enum):
    GENERATOR = 'generator'
    CHP = 'chp'
    GEOTHERMAL = 'geothermal'
    NUCLEAR = 'nuclear'


class Storage(Enum):
    STORAGE = 'storage'


class Transmission(Enum):
    TRANSMISSION = 'transmission'



class InputPrimaryEnergy(Enum):
    SOLAR = 'solar radiation'
    LIGNITE = 'lignite'
    HARDCOAL = 'hard coal'
    NATURALGAS = 'natural gas'
    BIOGAS = 'biogas'
    BIOMASS = 'biomass'
    HEAVYOIL = 'heavy oil'
    LIGHTOIL = 'light oil'
    URANIUM = 'uranium'
    WIND = 'wind'
    # WIND_OSH = 'wind_osh'
    WASTE = 'waste'
    WATER = 'water'
    HEAT = 'heat'
    CO2 = 'CO2'
    WIND_OFF = 'WIND_OFF'
    WIND_ONS = 'WIND_ONS'
    TRADE_IMPORT = 'TRADE_IMPORT'


@dataclass
class StorageEnergy:
    BATTERY_ENERGY = 'Battery_Energy'
    H2 = 'H2'
    H2_FC = 'H2_FC'
    HYDRO_ENERGY = 'hydro_energy'
    HYDROGEN = 'hydrogen'


@dataclass
class ConverterStorageData:
    code: 'str'
    input_energy: 'str'
    output_energy: 'str'

