from typing import List
import sys
import jmespath
import csv
import json
import urllib.request
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

from build_in_functions import iterate_mapping, load_custom_mapping
from type_def import Technology, TechnologyType, InputEnergy, OutputEnergy, Energy, Code, Cost
from scalar_class import Scalar


# Technology.STORAGE(converter), Technology.GENERATOR(multiconverter), Technology.TRANSMISSION(converter) ---> converter or multiconverter?
def is_converter(technology):
    converter_list = [Technology.PHOTOVOLTAICS, Technology.HYDRO_TURBINE, Technology.WIND_TURBINE]
    if technology in converter_list:
        return True
    else:
        return False


def is_multiconverter(technology):
    multiconverter_list = [Technology.CHP, Technology.NUCLEAR, Technology.STEAM, Technology.GENERATOR, Technology.GEOTHERMAL]
    if technology in multiconverter_list:
        return True
    else:
        return False



def converter_csv_writer(technologies):
    converter_list = []
    multiconverter_list = []
    #comment row
    converter_list.append(["#comment","===============converter-technologies============================================"])
    multiconverter_list.append(["#comment","===============multiconverter-technologies============================================"])
    for technology in technologies:
        if not technology == (Technology.UNKNOWN or Technology.TRANSMISSION or Technology.STORAGE):
            # print(technology)
            query_inp = "unique(oed_scalars[? technology == '" + technology + "'].input_energy_vector)"
            inp_energies = iterate_mapping(data, query_inp)
            for inp_energy in inp_energies:
                query_out = "unique(oed_scalars[? technology == '" + technology + "' && input_energy_vector == '" + inp_energy + "'].output_energy_vector)"
                out_energy = iterate_mapping(data, query_out)
                query_technology_type = "unique(oed_scalars[? technology == '" + technology + "' && input_energy_vector == '" + inp_energy + "'].technology_type)"
                technology_types = iterate_mapping(data, query_technology_type)
                for technology_type in technology_types:
                    if is_converter(technology):
                        print("converter: "+ technology)
                        converter_multiconverter_detail_block(technology, technology_type, inp_energy, out_energy, converter_list)

                    elif is_multiconverter(technology):        
                        print("multiconverter: "+ technology)
                        converter_multiconverter_detail_block(technology, technology_type, inp_energy, out_energy, multiconverter_list)
                
                    else:
                        print(technology)
                        continue
                
    seperator_to_csv(converter_list, 'converter.csv')
    seperator_to_csv(multiconverter_list, 'multiconverter.csv')
    

    
def foo(x,y):
    return x,y
def converter_multiconverter_detail_block(technology, technology_type, input_energy, out_energy, converter_detail_csv):
    #first row
    converter_detail_csv.append(["#blockwise"])
    scalar = Scalar(input_energy, out_energy, technology, technology_type)
    #code row
    code = scalar.code_generator()
    name = code
    is_bidirectional = str(scalar.is_bidirectional())
    comment = "#this is a comment"

    converter_detail_csv.append(["#code",code,"#name",name,"#input",input_energy,"#output",*(i for i in out_energy),"#bidirectional",is_bidirectional,"#comment",comment])
    #efficiency row
    type_ = "DVP_linear"
    # efficiency = scalar.efficiency()
    query_efficiency = "unique(oed_scalars[? technology == '" + technology + "' && input_energy_vector == '" + input_energy + "' && technology_type == '" + technology_type + "'&& parameter_name == 'output ratio'].value)"
    try:
        efficiency = iterate_mapping(data, query_efficiency)[0]
    except:
        efficiency = 1

    query_year = "unique(oed_scalars[? technology == '" + technology + "' && input_energy_vector == '" + input_energy + "'].year)"
    year = iterate_mapping(data, query_year)
    start_date = str(year[0]) + "-01-01_00:00"
    converter_detail_csv.append(["efficiency_new","#type",type_,"#data",start_date,efficiency])
    #cost row
    query_capital_cost = "unique(oed_scalars[? technology == '" + technology + "' && input_energy_vector == '" + input_energy + "' && technology_type == '" + technology_type + "'&& parameter_name == '" + Cost.CAPITAL_COST + "'].value)"
    try:
        capital_cost = iterate_mapping(data, query_capital_cost)[0]
    except:
        capital_cost = 0

    query_variable_cost = "unique(oed_scalars[? technology == '" + technology + "' && input_energy_vector == '" + input_energy + "' && technology_type == '" + technology_type + "'&& parameter_name == '" + Cost.VARIABLE_COST + "'].value)"
    try:
        variable_cost = iterate_mapping(data, query_variable_cost)[0]
    except:
        variable_cost = 0

    try:
        query_fixed_cost = "unique(oed_scalars[? technology == '" + technology + "' && input_energy_vector == '" + input_energy + "' && technology_type == '" + technology_type + "'&& parameter_name == '" + Cost.FIXED_COST + "'].value)"
        fixed_cost = iterate_mapping(data, query_fixed_cost)[0]
    except:
        fixed_cost = 0

    try:
        query_fuel_cost = "unique(oed_scalars[? technology == '" + technology + "' && input_energy_vector == '" + input_energy + "' && technology_type == '" + technology_type + "'&& parameter_name == '" + Cost.FUEL_COST + "'].value)"
        fuel_cost = iterate_mapping(data, query_fuel_cost)[0]
    except:
        fuel_cost = 0

    ##TODO ---> what is factor? over all hours?
    factor = 1
    cost = capital_cost + fixed_cost + variable_cost*factor + fuel_cost
    cost = capital_cost
    converter_detail_csv.append(["cost","#type",type_,"#data",start_date,cost])
    #lifetime row
    query_lifetime = "unique(oed_scalars[? technology == '" + technology + "' && input_energy_vector == '" + input_energy + "' && technology_type == '" + technology_type + "'&& parameter_name == 'lifetime'].value)"
    try:
        lifetime = iterate_mapping(data, query_lifetime)[0]
    except:
        lifetime = ''
    converter_detail_csv.append(["lifetime","#type",type_,"#data",start_date,lifetime])
    #OaM_rate row
    query_num = "unique(oed_scalars[? technology == '" + technology + "' && input_energy_vector == '" + input_energy + "' && technology_type == '" + technology_type + "' && unit == '€/MW/a'].value)"
    num = iterate_mapping(data, query_num)
    query_denum = "unique(oed_scalars[? technology == '" + technology + "' && input_energy_vector == '" + input_energy + "' && technology_type == '" + technology_type + "' && unit == '€/MW'].value)"
    try:
        denum = iterate_mapping(data, query_denum)[0]
        OaM_rate = float(num[0])/float(denum)
    except:
        OaM_rate = 0
    converter_detail_csv.append(["OaM_rate","#type",type_,"#data",start_date,OaM_rate])
    #last_row
    converter_detail_csv.append(["endblock"])



def seperator_to_csv(seperator_list: List, filename):
    with open(filename,"w") as f:
        wr = csv.writer(f)
        for row in seperator_list:
            wr.writerow(row)


if __name__ == '__main__':
    #request database from url
    db_name = 'https://modex.rl-institut.de/scenario/id/6?source=modex&mapping=concrete'
    request = urllib.request.urlopen(db_name)
    data = json.load(request)

    #download the database into data.json file
    data = load_custom_mapping('data')

    unique_technologies = iterate_mapping(data,"unique(oed_scalars[*].technology)")
    converter_csv_writer(unique_technologies)
        