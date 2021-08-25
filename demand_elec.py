import logging
logging.basicConfig(format='%(levelname)s:%(asctime)s:%(message)s', level=logging.INFO)

from build_in_functions import iterate_mapping
from misc import seperator_to_csv
from detail_block import primary_energy_minus_one_detail_block, installation_list_result


def timeseries_length(year):
    year = int(year)
    if (year%4) == 0:
        if year%100 == 0:
            if year%400 == 0:
                return 24*366
            else:
                return 24*365
        else:
            return 24*366
    else:
        return 24*365



def demand_elec(data, cwd):
    #Add demand_elec.csv in TimeSeries
    logging.info("demand_elec")
    regions = iterate_mapping(data, "unique(timeseries[*].region)")
    timeindex_years = iterate_mapping(data, "unique(timeseries[*].timeindex_start)")
    for timeindex_year in timeindex_years:
        year = timeindex_year.split('-')[0]
        for region in regions:            
            
            try:            
                timeseries_list = iterate_mapping(data, "timeseries[? parameter_name == 'demand' && region == '{}' && timeindex_start == '{}'].series".format(region, timeindex_year))[0]
            except:
                timeseries_len = timeseries_length(year)
                timeseries_list = [0 for i in range(timeseries_len)]
            try:
                tradeseries_list = iterate_mapping(data, "timeseries[? parameter_name=='trade volume' && technology_type=='trade export' && region == '{}' && timeindex_start == '{}'].series".format(region, timeindex_year))[0]
            except:
                timeseries_len = timeseries_length(year)
                tradeseries_list = [0 for i in range(timeseries_len)]

            time_and_trade_list = [a + b for a, b in zip(timeseries_list, tradeseries_list)]
            abs_time_and_trade_list = [abs(t) for t in time_and_trade_list]
            if sum(abs_time_and_trade_list):
                nfactor = sum(abs_time_and_trade_list)
                time_and_trade_list = [t/nfactor for t in time_and_trade_list]
            
            filename = str(year) + '/TimeSeries/' + region + '/demand_elec.csv'
            seperator_to_csv([time_and_trade_list], filename, cwd)
            
        logging.info("primary_energy_minus_one")
        primary_energy_minus_one_detail_block(year, cwd)
        installation_list_result(year, cwd)