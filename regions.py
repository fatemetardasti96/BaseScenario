from pathlib import Path
import logging
logging.basicConfig(format='%(levelname)s:%(asctime)s:%(message)s', level=logging.INFO)

from build_in_functions import iterate_mapping
from misc import seperator_to_csv
from detail_block import region_dir_block
      
    
    
def region_dir(data, cwd):
    logging.info("Create regions directory")
    grouped_year = iterate_mapping(data, "unique(timeseries[*].timeindex_start)")
    regions = iterate_mapping(data, "unique(timeseries[*].region)")
        
    for region in regions:
        for year in grouped_year:
            grouped = iterate_mapping(data,"group_by(sort_by(scalars[? region == '{}' && year == `{}`], &join('_',[technology, technology_type, input_energy_vector])),\
            &join('_',[technology, technology_type, input_energy_vector]))".format(region, year.split("-")[0]))

            region_csv = []
            
            timeseries = iterate_mapping(data, "timeseries[? parameter_name == 'demand' && timeindex_start == '{}' && region == '{}'].series".format(year, region))
            trade_series = iterate_mapping(data, "timeseries[? parameter_name=='trade volume' && technology_type=='trade export' && region == '{}' && timeindex_start == '{}'].series".format(region, year))

            outputs_primary_energy = iterate_mapping(data, "timeseries[? parameter_name == 'capacity factor' && region == '{}' && timeindex_start == '{}'].\
                {{energy: input_energy_vector, tech_type: technology_type}}".format(region, year))
            trade_primary_energy = iterate_mapping(data, "timeseries[? parameter_name == 'trade volume' && region == '{}' && technology_type=='trade import' \
                && timeindex_start == '{}']".format(region, year))
            outputs_converter = []
            for elem in grouped:
                technology, technology_type, inp_energy = elem.split('_')                                        
                try:
                    installed_capacity = iterate_mapping(data, "scalars[? year==`{}` && input_energy_vector=='{}' && technology == '{}' && technology_type == '{}'\
                    && parameter_name == 'installed capacity' && region=='{}'].value".format(year.split('-')[0], inp_energy, technology, technology_type, region))[0]
                    outputs_converter.append({'energy': inp_energy, 'tech': technology, 'tech_type': technology_type, 'installation': installed_capacity})
                except:
                    try:
                        iterate_mapping(data, "scalars[? year==`{}` && input_energy_vector=='{}' && technology == '{}' && technology_type == '{}'\
                        && parameter_name == 'expansion limit' && region=='{}'].value".format(year.split('-')[0], inp_energy, technology, technology_type, region))[0]
                        installed_capacity = 0
                        outputs_converter.append({'energy': inp_energy, 'tech': technology, 'tech_type': technology_type, 'installation': installed_capacity})
                    except:
                        continue
            e2p_ratio = iterate_mapping(data, "scalars[? parameter_name == 'E2P ratio' && region == '{}' && year == `{}` && technology == 'storage'].\
                {{tech_type: technology_type, E2P: value}}".format(region, year.split("-")[0]))            

            region_dir_block(region, year, timeseries, trade_series, outputs_primary_energy, trade_primary_energy, outputs_converter, e2p_ratio, data, region_csv, cwd)
            dirname = cwd + '/' + year.split("-")[0] + '/regions/'
            Path(dirname).mkdir(exist_ok=True, parents=True)
            seperator_to_csv(region_csv, year.split("-")[0]+'/regions/'+region+'.csv', cwd)