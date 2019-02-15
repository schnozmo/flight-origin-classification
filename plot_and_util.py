
import numpy as np, matplotlib.pyplot as plt, matplotlib.colors

def plot_points(x, y, z, title, xlabel, ylabel, zlabel, c_pred, colormap, color_type = 'explicit', file = ''):
    colors = np.array(['#377eb8', '#ff7f00', '#4daf4a', '#f781bf', '#a65628', '#984ea3',
                       '#999999', '#e41a1c', '#dede00', '#101010', '#202020', '#303030',
                       '#404040', '#505050', '#606060', '#707070', '#808080', '#909090',
                       '#A0A0A0', '#B0B0B0', '#D0D0D0', '#E0E0E0', '#F0F0F0'])



    plt.figure(1, figsize=(10, 10))
    plt.title(title)

    plt.subplot(221)
    if color_type == 'explicit':
        plt.scatter(x, y, color = colors[c_pred], alpha = 0.5)
    else:
        plt.scatter(x, y, color = colormap)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)

    plt.subplot(222)
    if color_type == 'explicit':
        plt.scatter(z, y, color = colors[c_pred], alpha = 0.5)
    else:
        plt.scatter(z, y, color = colormap)
    plt.xlabel(zlabel)
    plt.ylabel(ylabel)
    plt.grid(True)

    plt.subplot(223)
    if color_type == 'explicit':
        plt.scatter(x, z, color = colors[c_pred], alpha = 0.5)
    else:
        plt.scatter(x, z, color = colormap)
    plt.xlabel(xlabel)
    plt.ylabel(zlabel)
    plt.grid(True)

    plt.tight_layout()

    if file != '':
        plt.savefig(file)
    else:
        plt.show()

    plt.close()

# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 11:09:57 2019

@author: jb3435
"""

import numpy as np, matplotlib.pyplot as plt, matplotlib.colors

def plot_points(x, y, z, title, xlabel, ylabel, zlabel, c_pred, colormap, color_type = 'explicit', file = ''):
    colors = np.array(['#377eb8', '#ff7f00', '#4daf4a', '#f781bf', '#a65628', '#984ea3',
                       '#999999', '#e41a1c', '#dede00', '#101010', '#202020', '#303030',
                       '#404040', '#505050', '#606060', '#707070', '#808080', '#909090',
                       '#A0A0A0', '#B0B0B0', '#D0D0D0', '#E0E0E0', '#F0F0F0'])



    plt.figure(1, figsize=(10, 10))
    plt.title(title)

    plt.subplot(221)
    if color_type == 'explicit':
        plt.scatter(x, y, color = colors[c_pred], alpha = 0.5)
    else:
        plt.scatter(x, y, color = colormap)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)

    plt.subplot(222)
    if color_type == 'explicit':
        plt.scatter(z, y, color = colors[c_pred], alpha = 0.5)
    else:
        plt.scatter(z, y, color = colormap)
    plt.xlabel(zlabel)
    plt.ylabel(ylabel)
    plt.grid(True)

    plt.subplot(223)
    if color_type == 'explicit':
        plt.scatter(x, z, color = colors[c_pred], alpha = 0.5)
    else:
        plt.scatter(x, z, color = colormap)
    plt.xlabel(xlabel)
    plt.ylabel(zlabel)
    plt.grid(True)

    plt.tight_layout()

    if file != '':
        plt.savefig(file)
    else:
        plt.show()

    plt.close()

def plot_points_flight_5d(dist, alt, hdg, spd, title,
                   c_pred, colormap, color_type = 'explicit', file = ''):
    colors = np.array(['#377eb8', '#ff7f00', '#4daf4a', '#f781bf', '#a65628', '#984ea3',
                       '#999999', '#e41a1c', '#dede00', '#101010', '#202020', '#303030',
                       '#404040', '#505050', '#606060', '#707070', '#808080', '#909090',
                       '#A0A0A0', '#B0B0B0', '#D0D0D0', '#E0E0E0', '#F0F0F0'])


    plt.figure(1, figsize=(10, 10))
    plt.title(title)

    plt.subplot(321)
    if color_type == 'explicit':
        plt.scatter(hdg, alt, color = colors[c_pred], alpha = 0.5)
    else:
        plt.scatter(hdg, alt, color = colormap)
    plt.xlabel('Heading')
    plt.ylabel('Altitude')
    plt.grid(True)

    plt.subplot(322)
    if color_type == 'explicit':
        plt.scatter(spd, alt, color = colors[c_pred], alpha = 0.5)
    else:
        plt.scatter(spd, alt, color = colormap)
    plt.xlabel('Speed')
    plt.ylabel('Altitude')
    plt.grid(True)

    plt.subplot(323)
    if color_type == 'explicit':
        plt.scatter(hdg, dist, color = colors[c_pred], alpha = 0.5)
    else:
        plt.scatter(hdg, dist, color = colormap)
    plt.xlabel('Heading')
    plt.ylabel('Distance')
    plt.grid(True)


    plt.subplot(324)
    if color_type == 'explicit':
        plt.scatter(spd, dist, color = colors[c_pred], alpha = 0.5)
    else:
        plt.scatter(spd, dist, color = colormap)
    plt.xlabel('Speed')
    plt.ylabel('Distance')
    plt.grid(True)

    plt.subplot(325)
    if color_type == 'explicit':
        plt.scatter(hdg, spd, color = colors[c_pred], alpha = 0.5)
    else:
        plt.scatter(hdg, spd, color = colormap)
    plt.xlabel('Heading')
    plt.ylabel('Speed')
    plt.grid(True)

    plt.subplot(326)
    if color_type == 'explicit':
        plt.scatter(dist, alt, color = colors[c_pred], alpha = 0.5)
    else:
        plt.scatter(dist, alt, color = colormap)
    plt.xlabel('Distance')
    plt.ylabel('Altitude')
    plt.grid(True)

    plt.tight_layout()

    if file != '':
        plt.savefig(file)
    else:
        plt.show()

    plt.close()
