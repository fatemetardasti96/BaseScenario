from build_in_functions import iterate_mapping

from misc import seperator_to_csv
from detail_block import find_demand


def limit_block(region, inp, year, value):
    limit_csv = []
    limit_csv.append(['#comment', 'limited primary energy for {}'.format(inp)])
    start_date = '{}-01-01_00:00'.format(year)
    end_date = '{}-01-01_00:00'.format(year+1)
    base = 1E10
    #convert PJ to GW
    value = 1000*value/3.6
    limit_csv.append(['base', '#type', 'DVP_const', '#data', start_date, base, end_date, 0])
    limit_csv.append(['value', '#type', 'DVP_const', '#data', start_date, value, end_date, 0])
    limit_csv.append(['#endtable'])
    return limit_csv


def find_total_demand(regions_data, year):
    total_demand = 0
    all_region_list = iterate_mapping(regions_data, "timeseries[? timeindex_start=='{}-01-01T00:00:00'].region".format(year))
    for region in all_region_list:
        timeseries = iterate_mapping(regions_data, "timeseries[? parameter_name == 'demand' && timeindex_start == '{}-01-01T00:00:00' && region == '{}'].series".format(year, region))
        trade_series = iterate_mapping(regions_data, "timeseries[? parameter_name=='trade volume' && technology_type=='trade export' && region == '{}' && timeindex_start == '{}-01-01T00:00:00'].series".format(region, year))
        total_demand += find_demand(trade_series, timeseries, year)    
    return total_demand


def find_demand_factor(regions_data, region, year):
    timeseries = iterate_mapping(regions_data, "timeseries[? parameter_name == 'demand' && timeindex_start == '{}-01-01T00:00:00' && region == '{}'].series".format(year, region))
    trade_series = iterate_mapping(regions_data, "timeseries[? parameter_name=='trade volume' && technology_type=='trade export' && region == '{}' && timeindex_start == '{}-01-01T00:00:00'].series".format(region, year))
    demand =  find_demand(trade_series, timeseries, year)
    demand_denum = find_total_demand(regions_data, year)
    if demand == 0:
        return 'do not include this region'
    return demand/demand_denum


def handle_DE_domestic_limit(regions_data, domestic_limit, region, year):
    factor = find_demand_factor(regions_data, region, year)
    if factor == 'do not include this region':
        return 'do not include this region'
    return factor*domestic_limit


def domestic_limit(data, cwd):
    domestic_limits = iterate_mapping(data, "scalars[? parameter_name=='natural domestic limit'].{region:region, input:input_energy_vector, year:year, value:value}")
    for limit in domestic_limits:
        if limit['region'] == 'DE':
            all_region_list = iterate_mapping(data, "timeseries[? timeindex_start=='{}-01-01T00:00:00'].region".format(limit['year']))
            for domestic_region in all_region_list:
                domestic_limit_region_value = handle_DE_domestic_limit(data, limit["value"], domestic_region, limit['year'])
                if domestic_limit_region_value == 'do not include this region':
                    continue
                limit_list = limit_block(domestic_region, limit['input'], int(limit['year']), domestic_limit_region_value)
                limit_filename = '{}/TimeSeries/PrimaryEnergyLimited_{}_{}.csv'.format(limit['year'], domestic_region, limit['input'])
                seperator_to_csv(limit_list, limit_filename, cwd)
        else:
            limit_csv = limit_block(limit['region'], limit['input'], int(limit['year']), limit['value'])
            limit_filename = '{}/TimeSeries/PrimaryEnergyLimited_{}_{}.csv'.format(limit['year'], limit['region'], limit['input'])
            seperator_to_csv(limit_csv, limit_filename, cwd)

