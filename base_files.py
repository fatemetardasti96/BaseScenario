from pathlib import Path
import logging
logging.basicConfig(format='%(levelname)s:%(asctime)s:%(message)s', level=logging.INFO)

from build_in_functions import iterate_mapping
from type_def import Converter, MultiConverter, Storage, Transmission, Technology, TechnologyType, CodeGenerator, is_renewable, InputPrimaryEnergy,\
InputEnergy, TechnologyType, OutputEnergy, ConverterStorageTech
from misc import CodeBook, seperator_to_csv
from detail_block import converter_block, multiconverter_detail_block, storage_detail_block, transmission_detail, primary_energy_block
from config_files import create_config_files   

SCENARIO_ID = 38


def conv_multiconv_storage_transmission_primaries(data, SCENARIO_ID, cwd):
    
    years = iterate_mapping(data, "unique(scalars[*].year)")
    for year in years:                            

        grouped = iterate_mapping(data,"group_by(sort_by(scalars[? year == `{}`], &join('_',[technology, technology_type, input_energy_vector])), &join('_',[technology, technology_type, input_energy_vector]))".format(year))

        Path(cwd+'/'+str(year)).mkdir(parents=True, exist_ok=True)
        try:
            interest_rate = iterate_mapping(data, "unique(scalars[? parameter_name == 'WACC' && year == `{}`].value)".format(year))[0]
        except:
            interest_rate = 1
        
        logging.info("Create config files")
        create_config_files(year, interest_rate, cwd)
        
        converter_list = []
        multiconverter_list = []
        storage_list = []
        transmission_list = []
        primary_energy_list = []
        #comment row
        converter_list.append(["#comment","===============converter-technologies============================================"])
        converter_list.append(["#blockwise"])

        multiconverter_list.append(["#comment","===============multiconverter-technologies============================================"])
        multiconverter_list.append(["#blockwise"])

        storage_list.append(["#comment","===============storage-technologies============================================"])
        storage_list.append(["#blockwise"])

        transmission_list.append(["#comment","===============Transmission Converters============================================"])
        transmission_list.append(["#blockwise"])

        primary_energy_list.append(['#comment','===============Primary Energy============================================'])
        primary_energy_list.append(['#blockwise'])

        for elem in grouped.keys():
            technology, technology_type, inp_energy = elem.split('_')                        
            if (CodeGenerator(technology, technology_type, inp_energy).to_str() in CodeBook or technology == Technology.TRANSMISSION):
                out_energy = iterate_mapping(grouped,"unique(\"{}\"[? year == `{}`].output_energy_vector)".format(elem, year))
                out_energy = [OutputEnergy.ELECTRIC_ENERGY if i == OutputEnergy.ELECTRICITY else i for i in out_energy]
                try:
                    efficiency =  iterate_mapping(grouped,"unique(\"{}\"[? parameter_name == 'output ratio' && year == `{}`].value)".format(elem, year))[0]
                except:
                    efficiency = 1
                try:
                    lifetime =  iterate_mapping(grouped,"unique(\"{}\"[? parameter_name == 'lifetime' && year == `{}`].value)".format(elem, year))[0]
                except:
                    lifetime = 0
                try:
                    ANF = (((1+interest_rate)**(lifetime))*interest_rate)/(((1+interest_rate)**(lifetime))-1)
                    total_cost = iterate_mapping(grouped,"unique(\"{}\"[? parameter_name == 'capital costs' && year == `{}`].value)".format(elem, year))[0]*(ANF+1)
                except:
                    total_cost = 0
                try:
                    fixed_costs = iterate_mapping(grouped,"unique(\"{}\"[? parameter_name == 'fixed costs' && year == `{}`].value)".format(elem, year))[0]
                    investment_cost = iterate_mapping(grouped,"unique(\"{}\"[? parameter_name == 'capital costs' && year == `{}`].value)".format(elem, year))[0]
                    ANF = (((1+interest_rate)**(lifetime))*interest_rate)/(((1+interest_rate)**(lifetime))-1)
                    OaM_rate = float(fixed_costs)/float(investment_cost * ANF)
                except:
                    OaM_rate = 0
                if (technology in [c.value for c in Converter] or technology_type in [t.value for t in ConverterStorageTech] or technology_type==TechnologyType.TRADE_IMPORT):            
                    logging.info('Converter technology')
                    e2p_ratio = iterate_mapping(grouped, "unique(\"{}\"[? parameter_name == 'E2P ratio' && year == `{}`].value)".format(elem, year))
                    converter_block(technology, technology_type, inp_energy, out_energy, year, efficiency, lifetime, total_cost, OaM_rate, e2p_ratio, converter_list)
                if technology in [m.value for m in MultiConverter]:
                    logging.info('MultiConverter technology')
                    try:
                        emission_factor = iterate_mapping(grouped,"unique(\"{}\"[? parameter_name == 'emission factor' && year == `{}`].value)".format(elem, year))[0]
                    except:
                        emission_factor = 0
                    multiconverter_detail_block(technology, technology_type, inp_energy, out_energy, year, emission_factor, efficiency, lifetime, total_cost, OaM_rate, multiconverter_list)
                if technology in [s.value for s in Storage]:
                    logging.info('Storage technology')
                    e2p_ratio = iterate_mapping(grouped, "unique(\"{}\"[? parameter_name == 'E2P ratio' && year == `{}`].value)".format(elem, year))[0]
                    storage_detail_block(technology_type, year, efficiency, lifetime, total_cost, OaM_rate, e2p_ratio, storage_list)
                if (technology in [t.value for t in Transmission] and technology_type in ('hvac', 'DC')):
                    logging.info('Transmission technology')
                    transmission_detail(technology, technology_type, inp_energy, out_energy, year, efficiency, lifetime, total_cost, OaM_rate, transmission_list, SCENARIO_ID)                

            else:
                logging.info(elem)

        energies = iterate_mapping(data, "unique(scalars[? year == `{}`].input_energy_vector)".format(year))
        energies.append('CO2')
        energies.append(InputEnergy.TRADE_IMPORT)
        for energy in energies:
            if energy == InputEnergy.AIR:
                tech_type_list = iterate_mapping(data, "unique(scalars[? year == `{}` && input_energy_vector == 'air'].technology_type)".format(year))
                for tech_type in tech_type_list:
                    if tech_type == TechnologyType.OFFSHORE:
                        energies.append(InputEnergy.WIND_OFF)
                    elif tech_type == TechnologyType.ONSHORE:
                        energies.append(InputEnergy.WIND_ONS)
        
        for energy in energies:
            if energy in [e.value for e in InputPrimaryEnergy]:
                logging.info("Input Primary Energy")
                if is_renewable(energy):
                    base = 1
                    value = 0
                else:
                    base = 1E10
                    if energy == 'CO2':
                        value = iterate_mapping(data, "scalars[? year == `{}` && parameter_name == 'emission costs'].value".format(year))[0]
                    else:
                        try:
                            value =  iterate_mapping(data, "scalars[? input_energy_vector == '{}' && year == `{}` && parameter_name == 'fuel costs'].value".format(energy, year))[0]*1000.0
                        except:
                            value = 0.001
                        if value == 0:
                            value = 0.001
                energy = energy.replace(" ","_")
                
                primary_energy_block(energy, year, base, value, primary_energy_list)
            
        
        seperator_to_csv(converter_list, str(year)+'/Converter.csv', cwd)
        seperator_to_csv(multiconverter_list, str(year)+'/MultiConverter.csv', cwd)
        seperator_to_csv(storage_list, str(year)+'/Storage.csv', cwd)
        seperator_to_csv(transmission_list, str(year)+'/TransmissionConverter.csv', cwd)       
        seperator_to_csv(primary_energy_list, str(year)+'/PrimaryEnergy.csv', cwd)

        region_list = []
        region_list.append(['#blockwise'])
        unique_regions = iterate_mapping(data,"map(&join(``,['/include(./regions/',@,'.csv)']),unique(timeseries[? timeindex_start== `{}`].region[]))".format(str(year)+'-01-01T00:00:00'))
        for region in unique_regions:
            region_list.append([region])

        seperator_to_csv(region_list, str(year)+'/Region.csv', cwd)
