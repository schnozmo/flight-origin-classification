
import numpy as np

from plot_and_util import plot_points

input_file = 'dist-alt-hdg.train200.csv'

time_and_flt = np.genfromtxt(input_file, delimiter=',', usecols=(0,1), dtype='str')
labels = np.genfromtxt(input_file, delimiter=',', usecols=(5), dtype='str')
rawdata = np.genfromtxt(input_file, delimiter=',', usecols=(2,3,4))

uvals, colors = np.unique(labels, return_inverse=True)

print(uvals)

plot_points(rawdata[:, 0], rawdata[:, 1], rawdata[:, 2],
            title = 'Labeled Airports',
            color_type='explicit', c_pred=colors, colormap = None,
            #colormap=cmap(norm(lof_outlier.negative_outlier_factor_)),
            xlabel='distance', ylabel='altitude', zlabel='heading', file = 'plots/labelled.grid.png')


