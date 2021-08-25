import shutil


def create_config_files(year, interest_rate, cwd):
    src = r'./start_genesys.sh'
    dst = cwd + '/' + str(year) + '/start_genesys.sh'
    shutil.copy(src, dst, follow_symlinks=True)

    g = open(cwd + '/' + str(year)+'/ProgramSettings.dat','w')
    with open('./ProgramSettings.dat', 'r') as f:
        for line in f.readlines():
            if line.strip() == 'simulation_start=':
                line = line.strip() + str(year)+'-01-01_00:00\n'
            elif line.strip() == 'simulation_end=':
                line = line.strip() + str(int(year)+1)+'-01-01_00:00\n'
            elif line.strip() == 'interest_rate=':
                line = line.strip() + str(interest_rate) + '\n'

            g.writelines(line)
    
    g.close()


