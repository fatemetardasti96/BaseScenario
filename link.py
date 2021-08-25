import logging
logging.basicConfig(format='%(levelname)s:%(asctime)s:%(message)s', level=logging.INFO)

from build_in_functions import iterate_mapping
from misc import seperator_to_csv
from detail_block import link_detail_block
from load_data import dump_transmission_db, load_transmission_db

def link_generator(SCENARIO_ID, cwd):
    logging.info("Link Parametrisation")
    dump_transmission_db(SCENARIO_ID)
    data = load_transmission_db(SCENARIO_ID)
    years = iterate_mapping(data, "unique(scalars_transmission[*].year)")    
    for year in years:
        links = iterate_mapping(data,"scalars_transmission[? year == `{}` && parameter_name == 'installed capacity' && (technology_type=='hvac' || technology_type=='DC')].region".format(year))
        link_list = []
        link_list.append(["#comment","===============LINK Parameterisation============================================"])
        link_list.append(["#blockwise"])
        for link in links:            
            print('{}'.format(str(link)))
            if len(link) == 2:
                try:
                    length = iterate_mapping(data, "scalars_transmission[? region == {} && parameter_name == 'distance' && year == `{}`].value".format(str(link), year))[0]
                except:
                    print(year, link, 'this link does not have length')
                    length = 300
                    
                installation = iterate_mapping(data, "scalars_transmission[? region == {} && parameter_name == 'installed capacity' && year == `{}`].value".format(str(link), year))[0]/1000.0

                link_detail_block(link, year, length, installation, link_list)        
                
        seperator_to_csv(link_list, str(year) + '/Link.csv', cwd)