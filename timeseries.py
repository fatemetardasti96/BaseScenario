from pathlib import Path
import logging
logging.basicConfig(format='%(levelname)s:%(asctime)s:%(message)s', level=logging.INFO)

from build_in_functions import iterate_mapping
from type_def import TechnologyType, InputEnergy
from detail_block import timeseries_detail_block

        

def timeseries(data, cwd):    
    logging.info("Time Series")
    regions = iterate_mapping(data, "unique(timeseries[*].region)")
    grouped_year = iterate_mapping(data, "unique(timeseries[*].timeindex_start)")
    for region in regions:
        for year in grouped_year:
            dirname = cwd + '/' + year.split("-")[0] + '/TimeSeries/' + region
            Path(dirname).mkdir(exist_ok=True, parents=True)
            outputs = iterate_mapping(data, "timeseries[? (parameter_name == 'capacity factor' || parameter_name == 'trade volume') && timeindex_start == '{}' && region == '{}'].{{energy: input_energy_vector, series: series, tech_type: technology_type}}".format(year, region))
            for output in outputs:
                input_energy = output['energy']
                timeseries = output['series']
                tech_type = output['tech_type']
                if tech_type == 'trade export':
                    continue
                if (input_energy == InputEnergy.AIR and tech_type == TechnologyType.ONSHORE):
                    input_energy = InputEnergy.WIND_ONS
                elif (input_energy == InputEnergy.AIR and tech_type == TechnologyType.OFFSHORE):
                    input_energy = InputEnergy.WIND_OFF
                elif tech_type == TechnologyType.TRADE_IMPORT:
                    input_energy = 'TRADE_IMPORT'                        
                timeseries_detail_block(year, region, input_energy, timeseries, cwd)
