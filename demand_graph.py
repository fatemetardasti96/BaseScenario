import csv
from decimal import Decimal
import matplotlib.pyplot as plt
from pathlib import Path


def indices(list, filter=lambda x: bool(x)):
    return [1 for i,x in enumerate(list) if filter(x)]


for x in Path('./2030/TimeSeries').iterdir():
    if x.is_dir():
        with open('{}/demand_elec.csv'.format(x)) as f:
            reader = csv.reader(f, delimiter=';')
            for row in reader:
                demand = [Decimal(val) for val in row]

        negative_demand = [v if v<0 else 0 for v in demand]
        if sum(negative_demand) == 0:
            print('no negative demand in {}'.format(x.name))
        else:
            negative_time_indices = indices(demand, filter=lambda x: x<0)
            nb_time_points = sum(negative_time_indices)
            plt.plot(demand)
            plt.title('negative demand in {} with {} negative time points'.format(x.name, nb_time_points))
            plt.savefig('negative_demand_plot/2030/{}.png'.format(x.name))
            plt.show()
