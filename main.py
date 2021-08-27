from pathlib import Path
from datetime import datetime
import os

from demand_elec import demand_elec
from link import link_generator
from timeseries import timeseries
from regions import region_dir
from installations import installation_dir
from base_files import conv_multiconv_storage_transmission_primaries
from domestic_limit import domestic_limit
from load_data import *
from global_co2 import *


SCENARIO_ID = 58

if __name__ == '__main__':
    
    if not os.path.exists('db'):
        os.makedirs('db')

    dump_region_db(SCENARIO_ID)
    regions_data = load_region_db(SCENARIO_ID)
    
    dump_concrete_db(SCENARIO_ID)
    concrete_data = load_concrete_db(SCENARIO_ID)    

    if not Path('ID'+str(SCENARIO_ID)).is_dir():
        cwd = 'ID'+str(SCENARIO_ID)
        Path(cwd).mkdir(parents= True)
    else:
        cwd = 'ID'+str(SCENARIO_ID)+'_'+datetime.now().strftime('%Y-%m-%d_%H-%M')
        Path(cwd).mkdir(parents= True)
    
    conv_multiconv_storage_transmission_primaries(regions_data, SCENARIO_ID, cwd)
    
    installation_dir(regions_data, SCENARIO_ID, cwd)
    
    timeseries(regions_data, cwd)
    
    demand_elec(regions_data, cwd)
    
    link_generator(SCENARIO_ID, cwd)

    domestic_limit(regions_data, cwd)

    region_dir(regions_data, cwd)            

    create_global_co2(concrete_data, cwd)
    create_global(regions_data, cwd)