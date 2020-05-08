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