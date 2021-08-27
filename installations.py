from pathlib import Path
import logging
logging.basicConfig(format='%(levelname)s:%(asctime)s:%(message)s', level=logging.INFO)

from build_in_functions import iterate_mapping
from type_def import Technology, TechnologyType, CodeGenerator, TechnologyType, Code, InputEnergy
from misc import CodeBook, seperator_to_csv
from detail_block import installation_list_block
from load_data import load_concrete_db
    
    
    
def installation_dir(data, SCENARIO_ID, cwd):    
    for year in (2030, 2050):
        dirname = cwd + '/' + str(year) + '/installation_lists/'
        Path(dirname).mkdir(exist_ok=True, parents=True)
        grouped = iterate_mapping(data,"group_by(sort_by(scalars[? year == `{}` && parameter_name == 'expansion limit'], &join('_',[region, technology, technology_type, input_energy_vector])),\
            &join('_',[region, technology, technology_type, input_energy_vector]))".format(year))
        installation_lists = []
        installation_csv = {}
        for elem in grouped:
            region, technology, technology_type, inp_energy = elem.split('_')                        
            try:
                installed_capacity = iterate_mapping(data, "scalars[? year==`{}` && input_energy_vector=='{}' && technology == '{}' && technology_type == '{}'\
                && parameter_name == 'installed capacity' && region=='{}'].value".format(year, inp_energy, technology, technology_type, region))[0]
            except:
                installed_capacity = 0
            
            if (CodeGenerator(technology, technology_type, inp_energy).to_str() in CodeBook):                        
                installation_list_code = CodeBook[CodeGenerator(technology, technology_type, inp_energy).to_str()]
                if installation_list_code not in installation_lists:
                    installation_lists.append(installation_list_code)
                    installation_csv[installation_list_code] = []
                #add these extra values for converter
                if technology == Technology.STORAGE:
                    if technology_type == TechnologyType.BATTERY:
                        code_name = Code.BAT1POWER
                    # elif technology_type == TechnologyType.HYDROGEN_GAS:
                        # code_name = Code.CCH2_TURBINE
                    # elif technology_type == TechnologyType.HYDROGEN_FUELCELL:
                        # code_name = Code.FUEL_CELL
                    elif technology_type == TechnologyType.PUMPED:
                        code_name = Code.PH_TURBINE
                    if code_name not in installation_lists:
                        installation_lists.append(code_name)                        
                        installation_csv[code_name] = []    
                        # if technology_type == TechnologyType.HYDROGEN_GAS:
                            # installation_lists.append(Code.H2_ELECTROLYSER)
                            # installation_csv[Code.H2_ELECTROLYSER] = []
                        # if technology_type == TechnologyType.HYDROGEN_FUELCELL:
                            # installation_lists.append(Code.H2_ELECTROLYSER_FC)
                            # installation_csv[Code.H2_ELECTROLYSER_FC] = []                                    

                region_code_installation_value = iterate_mapping(grouped, "\"{}\"[? region == '{}'].value".format(elem, region))[0]
                name = region + '.' + installation_list_code

                if installed_capacity < region_code_installation_value:
                    if technology == Technology.STORAGE:
                        # for storage : E = p * ratio
                        e2p_ratio = iterate_mapping(data, "scalars[? parameter_name == 'E2P ratio' && region == '{}' && year == `{}` && \
                        technology == 'storage' && technology_type == '{}'].value".format(region, year, technology_type))[0]            

                        installation_list_block(name, installed_capacity*e2p_ratio/1000.0, region_code_installation_value*e2p_ratio/1000.0, installation_csv[installation_list_code], year)
                        # for converter
                        converter_name = region + '.' + code_name
                        installation_list_block(converter_name, installed_capacity/1000.0, region_code_installation_value/1000.0, installation_csv[code_name], year)
                        # if technology_type == TechnologyType.HYDROGEN_GAS:
                            # installation_list_block(region + '.' + Code.H2_ELECTROLYSER, installed_capacity/1000.0, region_code_installation_value/1000.0, installation_csv[Code.H2_ELECTROLYSER], year)
                        # elif technology_type == TechnologyType.HYDROGEN_FUELCELL:
                            # installation_list_block(region + '.' + Code.H2_ELECTROLYSER_FC, installed_capacity/1000.0, region_code_installation_value/1000.0, installation_csv[Code.H2_ELECTROLYSER_FC], year)
                    else:
                        installation_list_block(name, installed_capacity/1000.0, region_code_installation_value/1000.0, installation_csv[installation_list_code], year)

        
        installation_lists.append('hvac')
        installation_csv['hvac'] = []
        data_trans = load_concrete_db(SCENARIO_ID)    
        transmission_data = iterate_mapping(data_trans,"oed_scalars[? year == `{}` && parameter_name == 'expansion limit' && technology == 'transmission' && (technology_type=='hvac' || technology_type=='DC')]".format(year))
        for elem in transmission_data:
            regions = elem['region']
            expansion_value = elem['value']
            name = '{0}_{1}.hvac_{0}_{1}'.format(regions[0], regions[1])
            try:
                installed_capacity = iterate_mapping(data_trans,"oed_scalars[? year == `{}` && parameter_name == 'installed capacity' &&\
                technology == 'transmission' && region == {}].value".format(year, regions))[0]
            except:
                installed_capacity = 0
            
            if installed_capacity < expansion_value:                
                installation_list_block(name, installed_capacity/1000.0, expansion_value/1000.0, installation_csv['hvac'], year)

        
        """
        Handle photovoltaics
        """
        
        unique_regions = iterate_mapping(data,"unique(timeseries[? timeindex_start== `{}`].region)".format('2016-01-01T00:00:00'))
        for region in unique_regions:
            technology = Technology.PHOTOVOLTAICS
            technology_type = TechnologyType.ROOFTOP
            inp_energy = InputEnergy.SOLAR
            try:
                installed_capacity_rooftop = iterate_mapping(data, "scalars[? year==`{}` && technology == '{}' && technology_type == '{}' && input_energy_vector=='{}'\
                && parameter_name == 'installed capacity' && region=='{}'].value".format(year, technology, technology_type, inp_energy, region))[0]
            except:
                installed_capacity_rooftop = 0

            technology_type = TechnologyType.UTILITY
            try:
                installed_capacity_utility = iterate_mapping(data, "scalars[? year==`{}` && technology == '{}' && technology_type == '{}' && input_energy_vector=='{}'\
                && parameter_name == 'installed capacity' && region=='{}'].value".format(year, technology, technology_type, inp_energy, region))[0]
            except:
                installed_capacity_utility = 0

            technology_type = TechnologyType.UNKNOWN

            try:
                expansion_limit = iterate_mapping(data, "scalars[? year==`{}` && technology == '{}' && technology_type == '{}' && input_energy_vector=='{}'\
                && parameter_name == 'expansion limit' && region=='{}'].value".format(year, technology, technology_type, inp_energy, region))[0]
            except:
                continue
            
            expansion_limit_rooftop, expansion_limit_utility = expansion_limit/2, expansion_limit/2

            installation_list_code_rooftop = Code.PV1
            installation_list_code_utility = Code.PV2
            
            name_pv1 = region + '.' + installation_list_code_rooftop
            name_pv2 = region + '.' + installation_list_code_utility
            
            if installation_list_code_rooftop not in installation_lists:
                installation_lists.append(installation_list_code_rooftop)
                installation_csv[installation_list_code_rooftop] = []

            if installation_list_code_utility not in installation_lists:
                installation_lists.append(installation_list_code_utility)
                installation_csv[installation_list_code_utility] = []

            installation_list_block(name_pv1, installed_capacity_rooftop/1000.0, expansion_limit_rooftop/1000.0, installation_csv[installation_list_code_rooftop], year)
            installation_list_block(name_pv2, installed_capacity_utility/1000.0, expansion_limit_utility/1000.0, installation_csv[installation_list_code_utility], year)
            
        
        
        
        
        
        
        
        installationList_csv = [['#comment','MOUNTING-CODE.TECH-CODE;DATA-TYPE;DATA(may contain placeholders varxy)', '(if applicable) next lines:','#varxy', 'INIT-POINT', 'lBOUND', 'uBOUND']]
        for code in installation_lists:
            if installation_csv[code]:
                installation_list_path = '/installation_lists/InstallationList_{}.csv'.format(code)
                seperator_to_csv(installation_csv[code], str(year)+installation_list_path, cwd)
                installationList_csv.append(['/include(.{})'.format(installation_list_path)])

        seperator_to_csv(installationList_csv, str(year)+'/InstallationList.csv', cwd)