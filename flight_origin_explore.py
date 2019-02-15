
import numpy as np, scipy
import matplotlib.colors, matplotlib.pyplot as plt
from sklearn.cluster import KMeans, AffinityPropagation, AgglomerativeClustering, DBSCAN
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

#now, let's run some stuff

dbscan_model = DBSCAN(eps=0.05).fit(train_data)
print("DBSCAN core examples", len(dbscan_model.core_sample_indices_))
dbscan_not_core = np.full(train_len, True)
dbscan_not_core[dbscan_model.core_sample_indices_] = False

dbscan_pred = dbscan_model.fit_predict(train_data)
plot_points(rescale_train_data[:, 0], rescale_train_data[:, 1], rescale_train_data[:, 2],
            title = 'DBSCAN',
            color_type='explicit', c_pred=dbscan_pred, colormap = None,
            #colormap=cmap(norm(lof_outlier.negative_outlier_factor_)),
            xlabel='distance', ylabel='altitude', zlabel='heading', file = 'plots/dbscan.grid.png')

kmeans3_pred = KMeans(n_clusters=3).fit_predict(train_data)
plot_points(rescale_train_data[:, 0], rescale_train_data[:, 1], rescale_train_data[:, 2],
            title = 'KMeans - 3 clusters',
            color_type='explicit', c_pred=kmeans3_pred, colormap = None,
            #colormap=cmap(norm(lof_outlier.negative_outlier_factor_)),
            xlabel='distance', ylabel='altitude', zlabel='heading', file = 'plots/kmeans3.grid.png')

kmeans5_pred = KMeans(n_clusters=5).fit_predict(train_data)
plot_points(rescale_train_data[:, 0], rescale_train_data[:, 1], rescale_train_data[:, 2],
            title = 'KMeans - 5 clusters',
            color_type='explicit', c_pred=kmeans5_pred, colormap = None,
            #colormap=cmap(norm(lof_outlier.negative_outlier_factor_)),
            xlabel='distance', ylabel='altitude', zlabel='heading', file = 'plots/kmeans5.grid.png')

ap_pred = AffinityPropagation(damping=.9, preference=-50).fit_predict(train_data)
plot_points(rescale_train_data[:, 0], rescale_train_data[:, 1], rescale_train_data[:, 2],
            title = 'Affinity Propagation',
            color_type='explicit', c_pred=ap_pred, colormap = None,
            #colormap=cmap(norm(lof_outlier.negative_outlier_factor_)),
            xlabel='distance', ylabel='altitude', zlabel='heading', file = 'plots/affprop.grid.png')

agg_model = AgglomerativeClustering(n_clusters=23, linkage='single')
agg_pred = agg_model.fit_predict(train_data)
plot_points(rescale_train_data[:, 0], rescale_train_data[:, 1], rescale_train_data[:, 2],
            title = 'Agglomerative - Single Linkage',
            color_type='explicit', c_pred=agg_pred, colormap = None,
            #colormap=cmap(norm(lof_outlier.negative_outlier_factor_)),
            xlabel='distance', ylabel='altitude', zlabel='heading', file = 'plots/agglom-single.grid.png')

agg_model = AgglomerativeClustering(n_clusters=23, linkage='ward')
agg_pred = agg_model.fit_predict(train_data)
plot_points(rescale_train_data[:, 0], rescale_train_data[:, 1], rescale_train_data[:, 2],
            title = 'Agglomerative - Single Linkage',
            color_type='explicit', c_pred=agg_pred, colormap = None,
            #colormap=cmap(norm(lof_outlier.negative_outlier_factor_)),
            xlabel='distance', ylabel='altitude', zlabel='heading', file = 'plots/agglom-ward.grid.png')

lof_outlier = LocalOutlierFactor(n_neighbors=8)
lof_pred = lof_outlier.fit_predict(train_data)
lof_outlier_truth = lof_pred == -1
cmap = plt.cm.rainbow
norm = matplotlib.colors.Normalize(vmin=lof_outlier.negative_outlier_factor_.min(),
                                   vmax=lof_outlier.negative_outlier_factor_.max())
plot_points(rescale_train_data[:, 0], rescale_train_data[:, 1], rescale_train_data[:, 2],
            title = 'Local Outliers Factor',
            color_type='explicit', c_pred=lof_pred, colormap = None,
            #colormap=cmap(norm(lof_outlier.negative_outlier_factor_)),
            xlabel='distance', ylabel='altitude', zlabel='heading', file = 'plots/lof-outliers.grid.png')

iso_outlier = IsolationForest(n_estimators=100, max_features=2)
iso_pred = iso_outlier.fit_predict(train_data)
iso_pred = iso_pred + 1
iso_outlier_truth = iso_pred == 0
#non_outliers = iso_pred == 2

plot_points(rescale_train_data[:, 0], rescale_train_data[:, 1], rescale_train_data[:, 2],
            title = 'Iso Forest outliers',
            color_type='explicit', c_pred=iso_pred, colormap = None,
            #colormap=cmap(norm(lof_outlier.negative_outlier_factor_)),
            xlabel='distance', ylabel='altitude', zlabel='heading', file = 'plots/isoforest-outliers.grid.png')


iso_lof_outlier_truth = np.vstack((iso_outlier_truth, lof_outlier_truth)).transpose()
print(iso_lof_outlier_truth)
print("ISO outliers =", len(iso_pred[iso_outlier_truth]))
print("LOF outliers =", len(lof_pred[lof_outlier_truth]))
any_outlier_truth = np.any(iso_lof_outlier_truth, axis = 1)
print("One outlier =", len(iso_lof_outlier_truth[any_outlier_truth]),
      "Both outliers =", len(iso_lof_outlier_truth[np.all(iso_lof_outlier_truth, axis = 1)]))

print(np.shape(iso_lof_outlier_truth[any_outlier_truth]),
      np.shape(rescale_train_data[any_outlier_truth]),
      np.shape(time_and_flt[any_outlier_truth]))

outlier_data = np.hstack((iso_lof_outlier_truth[any_outlier_truth],
                          time_and_flt[any_outlier_truth],
                          rescale_train_data[any_outlier_truth]))

np.savetxt('isoforest-lof.outliers2.csv', np.random.choice(outlier_data[:, 0], 20, replace=False),
           fmt='%s', delimiter=',')


both_outlier_pred = iso_pred + lof_pred + 1
print("Both Pred FQ")
print(scipy.stats.itemfreq(both_outlier_pred))
plot_points(rescale_train_data[:, 0], rescale_train_data[:, 1], rescale_train_data[:, 2],
            title = 'Both Outliers',
            color_type='explicit', c_pred=both_outlier_pred, colormap = None,
            #colormap=cmap(norm(lof_outlier.negative_outlier_factor_)),
            xlabel='distance', ylabel='altitude', zlabel='heading', file = 'plots/both-outliers.grid.png')

no_outlier_truth = both_outlier_pred == np.max(both_outlier_pred)
print(scipy.stats.itemfreq(no_outlier_truth))


train_no_outliers = train_data[no_outlier_truth]
time_and_flt_no_outliers = time_and_flt[no_outlier_truth]

dbscan2_model = DBSCAN(eps=0.08).fit(train_no_outliers)
print("DBSCAN2 core examples", len(dbscan2_model.core_sample_indices_))

dbscan2_pred = dbscan2_model.fit_predict(train_no_outliers)
rescale_no_outliers = mm_scaler.inverse_transform(train_no_outliers)
plot_points(rescale_no_outliers[:, 0], rescale_no_outliers[:, 1], rescale_no_outliers[:, 2],
            title = 'DBSCAN no outliers',
            color_type='explicit', c_pred=dbscan2_pred, colormap = None,
            #colormap=cmap(norm(lof_outlier.negative_outlier_factor_)),
            xlabel='distance', ylabel='altitude', zlabel='heading', file = 'plots/dbscan2.grid.png')
