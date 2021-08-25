from build_in_functions import iterate_mapping
from misc import seperator_to_csv


def create_global(regions_data, cwd):
    years = iterate_mapping(regions_data, "unique(scalars[*].year)")
    for year in years:
        global_csv = []
        global_csv.append(["#blockwise", ""])
        global_csv.append(["#code", "CO2", "#name", "global_CO2"])
        global_csv.append(["#primary_energy", "#code", "CO2"])
        global_csv.append(["potential", "#type", "TBD_lookupTable", "#data_source_path", "./TimeSeries/LookupTable_globalCO2.csv"])
        global_csv.append(["#endblock"])
        seperator_to_csv(global_csv, str(year) + '/global.csv', cwd)


def create_global_co2(concrete_data, cwd):
    global_csv = []
    global_csv.append(["#comment", "unlimited -1 primary resource"])
    emission_limit = iterate_mapping(concrete_data, "oed_scalars[? parameter_name == 'emission limit'].{value: value, year: year}")
    for elem in emission_limit:
        year = elem["year"]
        val = elem["value"]
        filename = "{}/TimeSeries/LookupTable_globalCO2.csv".format(year)
        global_csv.append(["base", "#type", "DVP_linear", "#data", "{}-01-01_00:00".format(year), 1E10])
        global_csv.append(["value", "#type", "DVP_linear", "#data", "{}-01-01_00:00".format(year), val])
        global_csv.append(["#endtable"])
        seperator_to_csv(global_csv, filename, cwd)
