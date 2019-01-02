
import numpy as np

from sklearn.ensemble import IsolationForest
from sklearn.neighbors import KNeighborsClassifier, RadiusNeighborsClassifier
from plot_and_util import plot_points

train_file = 'dist-alt-hdg.train200.csv'
train_time_and_flt = np.genfromtxt(train_file, delimiter=',', usecols=(0,1), dtype='str')
train_labels = np.genfromtxt(train_file, delimiter=',', usecols=(5), dtype='str')
train_rawdata = np.genfromtxt(train_file, delimiter=',', usecols=(2,3,4))

test_file = 'dist-alt-hdg.to20181229.csv'
test_time_and_flt = np.genfromtxt(input_file, delimiter=',', usecols=(0,1), dtype='str')
test_rawdata = np.genfromtxt(input_file, delimiter=',', usecols=(2,3,4))

# scale to all data
mm_scaler = preprocessing.MinMaxScaler()
all_rawdata = np.vstack((train_rawdata, test_rawdata))
print(np.shape(train_rawdata), np.shape(test_rawdata), np.shape(all_rawdata))
mm_scaler.fit(all_rawdata)

# train the radius neighbors
train_data = mm_scaler.transform(train_rawdata)
rnn = RadiusNeighborsClassifier(radius=0.1)
rnn.fit(train_data, train_labels) 

# predict based on test
test_data = mm_scaler.transform(test_rawdata)
pred = rnn.predict(test_rawdata)

np.savetxt('non-outliers.csv', non_outlier_out[non_outlier_out[:, 0].argsort()], fmt='%s', delimiter=',')

plot_points(test_rawdata[:, 0],
            test_rawdata[:, 1],
            test_rawdata[:, 2],
            title = 'Radius Nearest Neighbors',
            color_type='explicit', c_pred=pred, colormap = None,
            #colormap=cmap(norm(lof_outlier.negative_outlier_factor_)),
            xlabel='distance', ylabel='altitude', zlabel='heading', file = 'plots/rad-nn.grid.png')

all_outlier_pred = both_outlier_pred + dbscan2_pred + 1
all_outlier_truth = all_outlier_pred == 0
train_just_outliers = train_data[all_outlier_truth]
rescale_just_outliers = mm_scaler.inverse_transform(train_just_outliers)
time_and_flt_just_outliers = time_and_flt[all_outlier_truth]

plot_points(rescale_just_outliers[:, 0],
            rescale_just_outliers[:, 1],
            rescale_just_outliers[:, 2],
            title = 'all outliers',
            color_type='explicit', c_pred=np.ones((len(rescale_just_outliers,1))), colormap = None,
            #colormap=cmap(norm(lof_outlier.negative_outlier_factor_)),
            xlabel='distance', ylabel='altitude', zlabel='heading', file = 'plots/just-outliers-class.grid.png')
