
import numpy as np, scipy.stats

from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import KNeighborsClassifier, RadiusNeighborsClassifier
from plot_and_util import plot_points

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
print(train_data)
#neigh = KNeighborsClassifier(n_neighbors = 5, weights = 'distance')
neigh = RadiusNeighborsClassifier(radius=.08, outlier_label="Other")
neigh.fit(train_data, train_labels) 

# predict based on test
test_data = mm_scaler.transform(test_rawdata)
print(test_data)
pred = neigh.predict(test_data)
print("Test Freq")
print(scipy.stats.itemfreq(pred))

# plot test values
uvals, colors = np.unique(pred, return_inverse=True)
plot_points(test_rawdata[:, 0],
            test_rawdata[:, 1],
            test_rawdata[:, 2],
            title = 'Radius Nearest Neighbors',
            color_type='explicit', c_pred=colors, colormap = None,
            #colormap=cmap(norm(lof_outlier.negative_outlier_factor_)),
            xlabel='distance', ylabel='altitude', zlabel='heading', file = 'plots/rad-nn.grid.png')

print(uvals)

# output sample of points
labels_out = np.ones((1, 6))
for label in uvals:
    label_rawdata = test_rawdata[pred == label]
    label_time_and_flt = test_time_and_flt[pred == label]
    label_labels = pred[pred == label, None]
    label_combined = np.hstack((label_time_and_flt, label_rawdata, label_labels))
    labels_out = np.vstack((labels_out, label_combined))

np.savetxt('sample_labels.csv', labels_out, delimiter = ',', fmt = '%s')
