import requests
import os
import json


def dump_region_db(SCENARIO_ID):
    if not os.path.isfile('db/db_regions_id_{}.json'.format(SCENARIO_ID)):
        db_name = 'https://modex.rl-institut.de/scenario/id/{}?source=modex&mapping=regions'.format(SCENARIO_ID)
        r = requests.get(db_name)
        with open('db/db_regions_id_{}.json'.format(SCENARIO_ID), 'w') as f:
            json.dump(r.json(), f)


def load_region_db(SCENARIO_ID):
    with open('db/db_regions_id_{}.json'.format(SCENARIO_ID), 'r') as f:
        data =  json.load(f)
    return data


def dump_concrete_db(SCENARIO_ID):
    if not os.path.isfile('db/db_concrete_id_{}.json'.format(SCENARIO_ID)):
        db_name = 'https://modex.rl-institut.de/scenario/id/{}?source=modex&mapping=concrete'.format(SCENARIO_ID)
        r = requests.get(db_name)
        with open('db/db_concrete_id_{}.json'.format(SCENARIO_ID), 'w') as f:
            json.dump(r.json(), f)


def load_concrete_db(SCENARIO_ID):
    with open('db/db_concrete_id_{}.json'.format(SCENARIO_ID), 'r') as f:
        data =  json.load(f)
    return data


def dump_transmission_db(SCENARIO_ID):
    if not os.path.isfile('db/db_transmission_id_{}.json'.format(SCENARIO_ID)):
        db_name = 'https://modex.rl-institut.de/scenario/id/{}?source=modex&mapping={{%20"base_mapping":%20"concrete",%20"mapping":%20{{%20"scalars_transmission":%20"oed_scalars[?technology==%27transmission%27]"%20}}%20}}'.format(SCENARIO_ID)
        r = requests.get(db_name)
        with open('db/db_transmission_id_{}.json'.format(SCENARIO_ID), 'w') as f:
            json.dump(r.json(), f)

def load_transmission_db(SCENARIO_ID):
    with open('db/db_transmission_id_{}.json'.format(SCENARIO_ID), 'r') as f:
        data =  json.load(f)
    return data