
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn import preprocessing
from sklearn.neighbors import LocalOutlierFactor
from sklearn.ensemble import IsolationForest

from plot_and_util import plot_points

input_file = 'dist-alt-hdg.to20181229.csv'

time_and_flt = np.genfromtxt(input_file, delimiter=',', usecols=(0,1), dtype='str')
rawdata = np.genfromtxt(input_file, delimiter=',', usecols=(2,3,4))
mm_scaler = preprocessing.MinMaxScaler()
alldata = mm_scaler.fit_transform(rawdata)
alldata_len = len(alldata)

train_pct = 1.
train_len = int(train_pct * alldata_len)
train_idx = np.full(alldata_len, False)
train_idx[np.random.choice(np.arange(alldata_len), size = train_len, replace = False)] = True

train_data = alldata[train_idx, ]
rescale_train_data = mm_scaler.inverse_transform(train_data)
test_data = alldata[~train_idx, ]

lof_outlier = LocalOutlierFactor(n_neighbors=8)
lof_pred = lof_outlier.fit_predict(train_data)
lof_outlier_truth = lof_pred == -1

iso_outlier = IsolationForest(n_estimators=100, max_features=2)
iso_pred = iso_outlier.fit_predict(train_data)
iso_pred = iso_pred + 1
iso_outlier_truth = iso_pred == 0

# Combine outlier data
both_outlier_pred = iso_pred + lof_pred + 1
no_outlier_truth = both_outlier_pred == np.max(both_outlier_pred)

train_no_outliers = train_data[no_outlier_truth]
rescale_no_outliers = mm_scaler.inverse_transform(train_no_outliers)
time_and_flt_no_outliers = time_and_flt[no_outlier_truth]

dbscan2_pred = DBSCAN(eps=0.08).fit_predict(train_no_outliers)
dbscan2_no_outlier_truth = dbscan2_pred != -1

print(np.shape(dbscan2_pred), np.shape(time_and_flt_no_outliers), np.shape(rescale_no_outliers))

non_outlier_out = np.hstack((dbscan2_pred[dbscan2_no_outlier_truth, None],
                          time_and_flt_no_outliers[dbscan2_no_outlier_truth],
                          rescale_no_outliers[dbscan2_no_outlier_truth]))

np.savetxt('non-outliers.csv', non_outlier_out[non_outlier_out[:, 0].argsort()], fmt='%s', delimiter=',')

plot_points(rescale_no_outliers[:, 0],
            rescale_no_outliers[:, 1],
            rescale_no_outliers[:, 2],
            title = 'DBSCAN no outliers',
            color_type='explicit', c_pred=dbscan2_pred, colormap = None,
            #colormap=cmap(norm(lof_outlier.negative_outlier_factor_)),
            xlabel='distance', ylabel='altitude', zlabel='heading', file = 'plots/dbscan2-class.grid.png')

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
