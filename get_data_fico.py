import pandas as pd
import matplotlib.pylab as plt

from responsibly.fairness.metrics import plot_roc_curves
from responsibly.fairness.interventions.threshold import (find_thresholds,
                                                          plot_fpt_tpr,
                                                          plot_roc_curves_thresholds,
                                                          plot_costs,
                                                          plot_thresholds)
from responsibly.dataset import build_FICO_dataset
from scipy.spatial import Delaunay
import numpy as np

def get_fpr_tpr_scores():
    FICO = build_FICO_dataset()
    return FICO['fpr'],FICO['tpr']

def intersecting_x_values(FICO):
    intersection_point = []
    different_set = set()

    score = 0.0
    attributes = ['Asian', 'Black', 'Hispanic', 'White']
    for a in attributes:
        score = 0.0
        while (score <= 101.0):
            if (score in FICO['fpr'][a]):
                element = FICO['fpr'][a][score]
            else:
                score = score + 0.5
                continue
            if (element in different_set):
                intersection_point.append(element)
            else:
                different_set.add(element)

            score = score + 0.5

    print(intersection_point)

def get_fpr_for_threshold(threshold):
    start_threshold = 0.0
    end_threshold = 101.0

if __name__ == '__main__':
    FICO = build_FICO_dataset()
    print(FICO.keys())
    #help(build_FICO_dataset)

    plot_roc_curves(FICO['rocs'],FICO['aucs'],figsize=(7,5))
    #plt.xlim(0,0.3)
    #plt.ylim(0.4,1)
    #plt.show()

    print(FICO['fpr']['Asian'][101.0])

    #polygons = [Delaunay(list(zip(fprs, tprs)))
                #for group, (fprs, tprs, _) in FICO['rocs'].items()]

    #print(polygons)

    #getting the common x values from FICO['fpr'] let's see how much you get?

    intersecting_x_values(FICO)








