
import numpy as np, scipy.stats

from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import KNeighborsClassifier, RadiusNeighborsClassifier
#from plot_and_util import plot_points

train_file = 'dist-alt-hdg.train200.csv'
train_time_and_flt = np.genfromtxt(train_file, delimiter=',', usecols=(0,1), dtype='str')
train_labels = np.genfromtxt(train_file, delimiter=',', usecols=(5), dtype='str')
train_rawdata = np.genfromtxt(train_file, delimiter=',', usecols=(2,3,4))
print("Training Label Freq")
print(scipy.stats.itemfreq(train_labels))

test_file = 'dist-alt-hdg.to20181229.csv'
test_time_and_flt = np.genfromtxt(test_file, delimiter=',', usecols=(0,1), dtype='str')
test_rawdata = np.genfromtxt(test_file, delimiter=',', usecols=(2,3,4))

# scale to all data
mm_scaler = MinMaxScaler()
all_rawdata = np.vstack((train_rawdata, test_rawdata))
print(np.shape(train_rawdata), np.shape(test_rawdata), np.shape(all_rawdata))
mm_scaler.fit(all_rawdata)

# train the radius neighbors
train_data = mm_scaler.transform(train_rawdata)
neigh = KNeighborsClassifier(n_neighbors = 5, weights = 'distance')
#neigh = RadiusNeighborsClassifier(radius=10000., outlier_label="Other")
neigh.fit(train_data, train_labels) 

# predict based on test
test_data = mm_scaler.transform(test_rawdata)
pred = neigh.predict(test_rawdata)
print("Test Freq")
print(scipy.stats.itemfreq(pred))

plot_points(test_rawdata[:, 0],
            test_rawdata[:, 1],
            test_rawdata[:, 2],
            title = 'Radius Nearest Neighbors',
            color_type='explicit', c_pred=pred, colormap = None,
            #colormap=cmap(norm(lof_outlier.negative_outlier_factor_)),
            xlabel='distance', ylabel='altitude', zlabel='heading', file = 'plots/k-nn.grid.png')
