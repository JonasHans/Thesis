import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def analyzeBRON(bron):
    total = 0
    filled = 0
    percentages = []

    for feature in bron:
        # Get lengths
        featureLen = len(bron[feature])
        filledLen = len(bron[bron[feature].notnull()])

        # Add to counters
        total += featureLen
        filled += filledLen

        percentages.append((filledLen/featureLen)*100)

    # Create bar plot of all features
    y_pos = np.arange(len(list(bron)))
    plt.barh(y_pos, percentages, align='center', alpha=0.5)
    plt.yticks(y_pos, list(bron))
    plt.yticks(fontsize=5)
    plt.savefig('../results/bronFeatureInfo.png')

    # Create bar plot of non null features
    nnPercentages = []
    nnLabels = []
    for i in range(0,len(percentages)):
        if percentages[i] != 0.0:
            nnPercentages.append(percentages[i])
            nnLabels.append(list(bron)[i])
    y_pos = np.arange(len(list(nnLabels)))
    plt.clf()
    plt.barh(y_pos, nnPercentages, align='center', alpha=0.5)
    plt.yticks(y_pos, nnLabels)
    plt.yticks(fontsize=6)
    plt.savefig('../results/bronFilledFeatureInfo.png')

    print('Number of features: ',len(list(bron)))
    print('Total number of fields: ',total)
    print('Total filled in: ',filled)
    print('Percentage: ', (filled/total)*100)

def main():
    # Read in the BRON ongevallen.txt
    # TODO: Define dtypes
    bron = pd.read_csv('../data/BRON2017/gegevens/Ongevallengegevens/ongevallen.txt', sep=',', index_col='VKL_NUMMER', low_memory=False)
    analyzeBRON(bron)

if __name__== "__main__":
    main()
