# BaseScenario

To install packages:
pip install -r requirements.txt

To run the program:
python main.py

scenario id can be passed to SCENARIO_ID to run the corresponding ID. Currently it's 43. 

files description:

1. base_files.py: create Converter.csv, Multiconverter.csv, Storage.csv, TranmissionConverter.csv, PrimaryEnergy.csv
2. config_files.py: create ProgramSetting.dat and start_genesys.sh
3. demand_elec.py: create demand_elec.csv for each region in TimeSeries directory
4. detail_block.py: corresponding values are gathered from other files and sent to detail_block.py to create each csv file. for example lifetime, cost and OaM_rate
value are gathered from base_file.py and then sent to detail_block.py to create a csv block.
5. domestic_limit.py: create local limits PrimaryEnergyLimited_BB_biogas.csv in TimeSeries directory.
6. global_co2.py: create TimeSeries/LookupTable_globalCO2.csv and global.csv files.
7. installation.py: create installation_lists directory and InstallationListResult.csv and InstallationList.csv
8. links.py: create Links.csv
9. load_data.py: dump and load data from modex.rl-institut.de into local so that further processing is faster
10. main.py: Starting point to run the program and create files and folders. They are independant.
11. misc.py: miscellanious functions 
12. regions.py: create regions directory
13. timeseries.py: create TimeSeries directory
14. type_def.py: definition of Technology, InputEnergy, TechnologyType, Code and so on
