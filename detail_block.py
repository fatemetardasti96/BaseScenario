from pathlib import Path
import numpy as np

from type_def import Converter, MultiConverter, Storage, TechnologyType, CodeGenerator, Code, InputEnergy, OutputEnergy
from misc import CodeBook, seperator_to_csv, ConverterStorageCodeBook, StorageCodeBook
from build_in_functions import iterate_mapping
from load_data import dump_transmission_db, load_transmission_db

def converter_detail_block(code, input_energy, out_energy, is_bidirectional, year, efficiency, total_cost, lifetime, OaM_rate, converter_list):
    name = code
    comment = "this is a comment"
    if input_energy != InputEnergy.ELECTRIC_ENERGY:
        input_energy = input_energy.upper()
    converter_list.append(["#code",code,"#name",name,"#input",input_energy,"#output",*(i for i in out_energy),"#bidirectional",is_bidirectional,"#comment",comment])
    #efficiency row
    type_ = "DVP_linear"
    
    start_date = str(year) + "-01-01_00:00"
    converter_list.append(["efficiency_new","#type",type_,"#data",start_date,efficiency])
    
    converter_list.append(["cost","#type",type_,"#data",start_date,total_cost])
    
    converter_list.append(["lifetime","#type",type_,"#data",start_date,lifetime])
    
    converter_list.append(["OaM_rate","#type",type_,"#data",start_date,OaM_rate])
    #last_row
    converter_list.append(["#endblock"])


def converter_block(technology, technology_type, input_energy, out_energy, year, efficiency, lifetime, total_cost, OaM_rate, e2p_ratio, converter_list):
    if technology_type in (TechnologyType.BATTERY, TechnologyType.PUMPED):
        is_bidirectional = str(True).lower()
    else:
        is_bidirectional = str(False).lower()

    if technology_type == TechnologyType.HYDROGEN_GAS:
        code = Code.H2_ELECTROLYSER
        inp_energy = InputEnergy.ELECTRIC_ENERGY
        out_energy = [OutputEnergy.H2]
        efficiency = 1
        total_cost = total_cost*(e2p_ratio[0]/(e2p_ratio[0]+1))/2
        converter_detail_block(code, inp_energy, out_energy, is_bidirectional, year, efficiency, total_cost, lifetime, OaM_rate, converter_list)

    if technology_type == TechnologyType.HYDROGEN_FUELCELL:
        code = Code.H2_ELECTROLYSER_FC
        inp_energy = InputEnergy.ELECTRIC_ENERGY
        out_energy = [OutputEnergy.H2_FC]
        efficiency = 1
        total_cost = total_cost*(e2p_ratio[0]/(e2p_ratio[0]+1))/2
        converter_detail_block(code, inp_energy, out_energy, is_bidirectional, year, efficiency, total_cost, lifetime, OaM_rate, converter_list)

    code = CodeBook[CodeGenerator(technology, technology_type, input_energy).to_str()]
    if technology_type in ConverterStorageCodeBook.keys():
        code = ConverterStorageCodeBook[technology_type].code
        input_energy = ConverterStorageCodeBook[technology_type].input_energy
        out_energy = [ConverterStorageCodeBook[technology_type].output_energy]
        efficiency = 1
    
    if technology_type == TechnologyType.BATTERY:
        total_cost = total_cost*(e2p_ratio[0]/(e2p_ratio[0]+1))
    elif technology_type == TechnologyType.PUMPED:
        total_cost = total_cost*(e2p_ratio[0]/(e2p_ratio[0]+1))



    if code == Code.WIND_OFF:
        input_energy = InputEnergy.WIND_OFF
    elif code == Code.WIND_ONS:
        input_energy = InputEnergy.WIND_ONS
    elif code == Code.TRANSMISSION_IMPORT:
        input_energy = InputEnergy.TRADE_IMPORT

    input_energy = input_energy.replace(" ","_")
    input_energy = InputEnergy.ELECTRIC_ENERGY if input_energy == InputEnergy.ELECTRICITY else input_energy

    converter_detail_block(code, input_energy, out_energy, is_bidirectional, year, efficiency, total_cost, lifetime, OaM_rate, converter_list)
    


def storage_detail_block(technology_type, year, efficiency, lifetime, total_cost, OaM_rate, e2p_ratio, storage_list):
    code = StorageCodeBook[technology_type].code
    input_energy = StorageCodeBook[technology_type].input_energy
    out_energy = StorageCodeBook[technology_type].output_energy
    name = code
    storage_list.append(["#code",code,"#name",name,"#input",input_energy,"#output", out_energy])
    #efficiency row
    type_ = "DVP_linear"
    start_date = str(year) + "-01-01_00:00"
    storage_list.append(["efficiency_new","#type",type_,"#data",start_date,efficiency])

    if technology_type == TechnologyType.BATTERY:
        total_cost = total_cost/(e2p_ratio+1)
    elif technology_type == TechnologyType.HYDROGEN_FUELCELL:
        total_cost = total_cost/(e2p_ratio+1)
    elif technology_type == TechnologyType.HYDROGEN_GAS:
        total_cost = total_cost/(e2p_ratio+1)
    elif technology_type == TechnologyType.PUMPED:
        total_cost = total_cost/(e2p_ratio+1)
    
    storage_list.append(["cost","#type",type_,"#data",start_date,total_cost])
    
    storage_list.append(["lifetime","#type",type_,"#data",start_date,lifetime])
    
    storage_list.append(["OaM_rate","#type",type_,"#data",start_date,OaM_rate])
    #last_row
    storage_list.append(["#endblock"])


def multiconverter_detail_block(technology, technology_type, input_energy, out_energy, year, emission_factor, efficiency, lifetime, total_cost, OaM_rate, multiconverter_list):
    code = CodeBook[CodeGenerator(technology, technology_type, input_energy).to_str()]
    name = code
    input_energy = input_energy.replace(" ","_")
    input_energy = InputEnergy.ELECTRIC_ENERGY if input_energy == InputEnergy.ELECTRICITY else input_energy.upper()
    multiconverter_list.append(["#code",code,"#name",name,"#input",input_energy])
    #output_energy row
    if ('co2' or 'CO2') not in out_energy:
        out_energy.append('CO2')

    multiconverter_list.append(["#output",*(i for i in out_energy)])
    #conversion row
    if emission_factor == 0:
        emission_factor = 1e-9
    else:
        emission_factor = 1000*emission_factor

    multiconverter_list.append(["#conversion",str(-1),emission_factor])
    #efficiency row
    type_ = "DVP_linear"
    
    start_date = str(year) + "-01-01_00:00"
    multiconverter_list.append(["efficiency_new","#type",type_,"#data",start_date,efficiency])
    
    multiconverter_list.append(["cost","#type",type_,"#data",start_date,total_cost])
    
    multiconverter_list.append(["lifetime","#type",type_,"#data",start_date,lifetime])
    
    multiconverter_list.append(["OaM_rate","#type",type_,"#data",start_date,OaM_rate])
    #last_row
    multiconverter_list.append(["#endblock"])


def transmission_detail_block(region_A, region_B, technology, technology_type, input_energy, out_energy, year, efficiency, lifetime, total_cost, OaM_rate, transmission_list):
    code  = 'hvac' + '_' + region_A + '_' + region_B
    name = str(technology_type) + '_' + 'Elec'
    is_bidirectional = str(True).lower()
    input_energy = InputEnergy.ELECTRIC_ENERGY if input_energy == InputEnergy.ELECTRICITY else input_energy.upper()
    transmission_list.append(["#code",code,"#name",name,"#input",input_energy,"#output",*(i for i in out_energy),"#bidirectional",is_bidirectional])
    #efficiency row
    type_ = "DVP_linear"
    
    start_date = str(year) + "-01-01_00:00"
    transmission_list.append(["efficiency_new","#type",type_,"#data",start_date,efficiency])
    
    transmission_list.append(["cost","#type",type_,"#data",start_date,total_cost])
    
    transmission_list.append(["lifetime","#type",type_,"#data",start_date,lifetime])
    
    transmission_list.append(["OaM_rate","#type",type_,"#data",start_date,OaM_rate])

    transmission_list.append(["length_dep_loss","#type",type_,"#data",start_date,str(0)])
    transmission_list.append(["length_dep_cost","#type",type_,"#data",start_date,str(0)])
    #last_row
    transmission_list.append(["#endblock"])


def transmission_detail(technology, technology_type, inp_energy, out_energy, year, efficiency, lifetime, cost_per_len, OaM_rate, transmission_list, SCENARIO_ID):
    dump_transmission_db(SCENARIO_ID)
    data = load_transmission_db(SCENARIO_ID)
    links = iterate_mapping(data,"scalars_transmission[? year == `{}` && parameter_name == 'installed capacity' && technology_type=='{}'].region".format(year, technology_type))
    for link in links:
        if len(link) == 2:
            try:
                length = iterate_mapping(data,"scalars_transmission[? year == `{}` && parameter_name == 'distance' && technology_type=='{}' && region==['{}','{}']].value".format(year, technology_type, link[0], link[1]))[0]
            except:
                length = 300
            total_cost = length*1000 * cost_per_len
            transmission_detail_block(link[0], link[1], technology, technology_type, inp_energy, out_energy, year, efficiency, lifetime, total_cost, OaM_rate, transmission_list)


def primary_energy_block(energy, year, base, value, energy_list):
    if energy != InputEnergy.ELECTRIC_ENERGY:
        energy = energy.upper()
    energy_list.append(['#code', energy, '#name', energy])
    table = 'TBD_lookupTable'
    energy_list.append(['cost_table', '#type', table])
    type_ = 'DVP_const'
    start_date = str(year) + "-01-01_00:00"
    energy_list.append(['base', '#type', type_,'#data', start_date, base])
    energy_list.append(['value', '#type', type_,'#data', start_date, value])
    energy_list.append(['#endtable'])
    energy_list.append(['#endblock'])


def link_detail_block(link, year, length, installation, link_list):
    region_A = link[0]
    region_B = link[1]
    code = ("_").join([region_A, region_B])
    link_list.append(["#code",code,"#region_A",region_A,"#region_B",region_B])
    #length row
    type_ = "DVP_const"
    start_date = str(year) + "-01-01_00:00"
    link_list.append(["length","#type",type_,"#data",start_date,length])
    # converter_code row
    converter_code = 'hvac_' + code
    link_list.append(["#converter","#code",converter_code])
    #installation row
    link_list.append(["installation","#type",type_,"#data",start_date,installation])
    
    link_list.append(["#endblock"])


    
def timeseries_detail_block(year, region, input_energy, timeseries, cwd):
    csv_list = []
    csv_list.append(["#comment","===============generation time series============================================"])
    base_type = "DVP_const"
    base = 1000000
    year = year.replace('T','_')[:-3]
    csv_list.append(["base", "#type", base_type, "#data", year, base])
    value_type = "TS_repeat_const"
    csv_list.append(["value", "#type", value_type, "#interval", "1h", "#start", year, "#data", *(t for t in timeseries)])
    csv_list.append(["#endtable"])

    filename = year.split("-")[0] + '/TimeSeries/' + region + '/' + region + '_' + input_energy.replace(" ","_").upper() + '.csv'
    seperator_to_csv(csv_list, filename, cwd)


def primary_energy_minus_one_detail_block(year, cwd):
    csv_list = []
    csv_list.append(["#comment","unlimited -1 primary ressource"])
    base_type = "DVP_const"
    base = 1E15
    date = str(year) + "-01-01_00:00"
    csv_list.append(["base", "#type", base_type, "#data", date, base])
    value_type = "DVP_linear"
    value = -1
    csv_list.append(["value", "#type", value_type, "#data", date, value])
    csv_list.append(["#endtable"])

    filename = str(year) + '/TimeSeries/PrimaryEnergyUnlimited_minusOne.csv'
    seperator_to_csv(csv_list, filename, cwd)


def installation_list_result(year, cwd):
    csv_list = []
    csv_list.append(["#comment","MOUNTING-CODE.TECH-CODE;DATA-TYPE;DATA(may contain placeholders varxy);(if applicable) next lines:;#varxy;INIT-POINT;lBOUND;uBOUND;"])
    csv_list.append(["#empty"])
    filename = str(year) + '/InstallationListResult.csv'
    seperator_to_csv(csv_list, filename, cwd)


    
def region_detail_block(region, year, demand_per_a, region_csv):
    region_csv.append(["#code", region, "#name", region])
    type_dyn = "TS_repeat_const"
    start_date = year.replace('T','_')[:-3]
    
    source_path = "./TimeSeries/" + region + "/demand_elec.csv"
    region_csv.append(["demand_electric_dyn", "#type", type_dyn, "#interval", "1h", "#start", start_date, "#data_source_path", source_path])
    type_a = "DVP_linear"
    region_csv.append(["demand_electric_per_a", "#type", type_a, "#data", start_date, demand_per_a])



def region_primary_energy_block(region, input_energy, region_csv):
    region_csv.append(["#primary_energy", "#code", input_energy.replace(' ','_').upper()])
    lookUpTable = "TBD_lookupTable"
    energy = input_energy.replace(" ","_").upper()
    source_path = "./TimeSeries/" + region + "/" + region + "_" + energy + ".csv"
    region_csv.append(["potential", "#type", lookUpTable, "#data_source_path", source_path])



def determine_primary_source_path(year, region, input_energy, cwd):
    year = year.split('-')[0]
    domestic_limit_path = '{}/{}/TimeSeries/PrimaryEnergyLimited_{}_{}.csv'.format(cwd, year, region, input_energy)
    if Path(domestic_limit_path).exists():
        return './TimeSeries/PrimaryEnergyLimited_{}_{}.csv'.format(region, input_energy)
    else:
        return './TimeSeries/PrimaryEnergyUnlimited_minusOne.csv'


def region_primary_energy_block_minusone(year, region, input_energy, region_csv, cwd):
    region_csv.append(["#primary_energy", "#code", input_energy.replace(' ','_').upper()])
    lookUpTable = "TBD_lookupTable"
    source_path = determine_primary_source_path(year, region, input_energy, cwd)    
    region_csv.append(["potential", "#type", lookUpTable, "#data_source_path", source_path])


def region_converter_block(region, code, installation, start_date, end_date, region_csv):
    region_csv.append(["#converter", "#code", code])
    converter_type = "DVP_const"
    region_csv.append(["installation", "#type", converter_type, "#data", start_date, installation, end_date, 0])


def region_multiconverter_block(region, code, installation, start_date, end_date, region_csv):
    region_csv.append(["#multi-converter", "#code", code])
    converter_type = "DVP_const"
    region_csv.append(["installation", "#type", converter_type, "#data", start_date, installation, end_date, 0])


def region_storage_block(region, code, installation, start_date, end_date, region_csv):
    region_csv.append(["#storage", "#code", code])
    converter_type = "DVP_const"
    region_csv.append(["installation", "#type", converter_type, "#data", start_date, installation, end_date, 0])

TRADE_DEMAND = {}
TRADE_DEMAND[2016]=[]
TRADE_DEMAND[2030]=[]
TRADE_DEMAND[2050]=[]
TIME_DEMAND={}
TIME_DEMAND[2016]=[]
TIME_DEMAND[2030]=[]
TIME_DEMAND[2050]=[]

def region_dir_block(region, year, timeseries, trade_series, outputs_primary_energy, trade_primary_energy, outputs_converter, e2p_ratio, data, region_csv, cwd):    
    dirname = year.split("-")[0]+'/regions/'
    Path(dirname).mkdir(exist_ok=True, parents=True)

    demand_per_a = find_demand(trade_series, timeseries, year)

    region_detail_block(region, year, demand_per_a, region_csv)
    
    input_energies = set([output['energy'] for output in outputs_primary_energy if output['energy']])
    for input_energy in input_energies:
        if input_energy != InputEnergy.AIR:
            region_primary_energy_block(region, input_energy, region_csv)
    
    for output in outputs_primary_energy:
        input_energy = output['energy']
        if input_energy == InputEnergy.AIR:
            tech_type = output['tech_type']
            if tech_type == TechnologyType.ONSHORE:
                input_energy = InputEnergy.WIND_ONS
            elif tech_type == TechnologyType.OFFSHORE:
                input_energy = InputEnergy.WIND_OFF
            
            region_primary_energy_block(region, input_energy, region_csv)
    
    if len(trade_primary_energy):
        region_primary_energy_block(region, 'trade import', region_csv)

    outputs_converter_set = set([output['energy'] for output in outputs_converter])
    for input_energy in outputs_converter_set:
        if input_energy not in (output['energy'] for output in outputs_primary_energy) and input_energy not in ('unknown', 'electricity'):
            region_primary_energy_block_minusone(year, region, input_energy, region_csv, cwd)

    for output in outputs_converter:
        input_energy = output['energy']
        tech = output['tech']
        if tech in [mconverter.value for mconverter in MultiConverter]:
            region_primary_energy_block_minusone(year, region, "CO2", region_csv, cwd)
            break


    for output in outputs_converter:
        input_energy = output['energy']
        tech = output['tech']
        tech_type = output['tech_type']
        installation = output['installation']/1000.0
        year = year.split("-")[0]
        start_date = str(year) + "-01-01_00:00"
        end_date = str(int(year)+1) + "-01-01 00:00:00"
        if CodeGenerator(tech, tech_type, input_energy).to_str() in CodeBook:
            code = CodeBook[CodeGenerator(tech, tech_type, input_energy).to_str()]
        else:
            continue
        
        if (tech in [converter.value for converter in Converter] or tech_type=='trade import'):
            region_converter_block(region, code, installation, start_date, end_date, region_csv)

        if tech_type == TechnologyType.HYDROGEN_GAS:
            code = Code.H2_ELECTROLYSER
            region_converter_block(region, code, installation, start_date, end_date, region_csv)

        if tech_type == TechnologyType.HYDROGEN_FUELCELL:
            code = Code.H2_ELECTROLYSER_FC
            region_converter_block(region, code, installation, start_date, end_date, region_csv)


        if tech_type in ConverterStorageCodeBook.keys():
            code = ConverterStorageCodeBook[tech_type].code
            region_converter_block(region, code, installation, start_date, end_date, region_csv)
    

        
    for output in outputs_converter:
        input_energy = output['energy']
        tech = output['tech']
        tech_type = output['tech_type']
        installation = output['installation']/1000.0
        year = year.split("-")[0]
        start_date = str(year) + "-01-01_00:00"
        end_date = str(int(year)+1) + "-01-01_00:00"
        if CodeGenerator(tech, tech_type, input_energy).to_str() in CodeBook:
            code = CodeBook[CodeGenerator(tech, tech_type, input_energy).to_str()]
        else:
            continue

        code = CodeBook[CodeGenerator(tech, tech_type, input_energy).to_str()]

        if tech in [mconverter.value for mconverter in MultiConverter]:
            region_multiconverter_block(region, code, installation, start_date, end_date, region_csv)
                
    for output in outputs_converter:
        input_energy = output['energy']
        tech = output['tech']
        tech_type = output['tech_type']
        installation = output['installation']
        year = year.split("-")[0]
        start_date = str(year) + "-01-01_00:00"
        end_date = str(int(year)+1) + "-01-01_00:00"
        if CodeGenerator(tech, tech_type, input_energy).to_str() in CodeBook:
            code = CodeBook[CodeGenerator(tech, tech_type, input_energy).to_str()]
        else:
            continue
        code = CodeBook[CodeGenerator(tech, tech_type, input_energy).to_str()]
        if tech in [storage.value for storage in Storage]:
            try:
                ratio = [e2p['E2P'] for e2p in e2p_ratio if e2p['tech_type'] == tech_type][0]
            except:
                ratio = 1
            storage_installation = installation * ratio
            region_storage_block(region, code, storage_installation, start_date, end_date, region_csv)

    region_csv.append(["#endblock"])


def find_demand(trade_series, timeseries, year):
    try:
        demand_per_a_trade = sum(trade_series[0])/1000.0
    except:
        demand_per_a_trade = 0
    try:        
        demand_per_a_time = sum(timeseries[0])/1000.0
    except:
        demand_per_a_time = 0

    try:
        year = int(year.split("-")[0])
    except:
        year = int(year)

    TRADE_DEMAND[year].append(demand_per_a_trade)
    TIME_DEMAND[year].append(demand_per_a_time)
    demand_per_a = demand_per_a_time + demand_per_a_trade
    return demand_per_a


def installation_list_block(name, installed_capacity, region_code_installation_value, installation_csv, year):
    start_date = "{}-01-01_00:00".format(year)
    end_date = "{}-01-01_00:00".format(year+1)
    installation_csv.append([name, "#type", "DVP_linear", "#data", start_date, "var0", end_date, 0,''])
    # installation_csv.append(["#var0", installed_capacity, installed_capacity, region_code_installation_value,''])
    installation_csv.append(["#var0", 0, 0, region_code_installation_value,''])
