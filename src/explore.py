import matplotlib.pyplot as plt
import seaborn as sns

def make_coast_graph(ex_df):
    plt.figure(figsize=(14,8))
    sns.scatterplot(x='longitude', y='latitude', hue='fips', size='taxvaluedollarcnt', data=ex_df)
    plt.xticks(ticks=[])
    plt.yticks(ticks=[])
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.legend()
    plt.show()
    
def make_histogram(df):
    df.hist(figsize=(20, 20), bins = 8, log = False)
    plt.suptitle('Histograms of the Data')
    plt.tight_layout
    
def make_heatmap(df):
    corr = df.corr()

    plt.figure(figsize=(20,12))
    ax = sns.heatmap(
        corr,
        #annot = True, <--- Don't run this, it's a nightmare
        vmin=-1, vmax=1, center=0,
        cmap=sns.diverging_palette(20, 220, n=200),
        square=True)
    
    ax.set_xticklabels(
        ax.get_xticklabels(),
        rotation=45,
        horizontalalignment='right');