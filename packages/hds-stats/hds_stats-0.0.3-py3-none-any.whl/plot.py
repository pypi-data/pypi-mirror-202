# Import libraries for Python Advanced
import numpy as np
import pandas as pd
from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt


# Draw a plot
# plt.plot(0, 0)
# plt.close()

# Set line width
plt.rc(group = 'lines', linewidth = 0.5)


# EDA functions
# outlier properties for box plot
outlier = {
    'marker': 'o', 
    'markersize': 3, 
    'markerfacecolor': 'pink',
    'markeredgecolor': 'red', 
    'markeredgewidth': 0.2
}

def plot_box_group(
    data, 
    x, 
    y, 
    pal = None
):
    avg = data.groupby(x)[y].mean().reset_index()
    sns.boxplot(
        data = data, 
        x = x, 
        y = y, 
        order = avg[x], 
        palette = pal, 
        flierprops = outlier
    )
    sns.scatterplot(
        data = avg, 
        x = avg.index, 
        y = y, 
        color = 'red', 
        s = 30, 
        edgecolor = 'black', 
        linewidth = 0.5
    )
    plt.axhline(
        y = data[y].mean(), 
        color = 'red', 
        linestyle = '--'
    )
    plt.title(label = f'{x} 범주별 {y}의 평균 비교');

def plot_scatter(
    data, 
    x, 
    y, 
    color = '0.3'
):
    sns.scatterplot(
        data = data, 
        x = x, 
        y = y, 
        color = color
    )
    plt.title(label = f'{x}와(과) {y}의 관계');

def plot_regression(
    data, 
    x, 
    y, 
    color = '0.3', 
    size = 15
):
    x_min = data[x].min()
    x_max = data[x].max()
    sns.regplot(
        data = data, 
        x = x, 
        y = y, 
        ci = None, 
        scatter_kws = {'color': color, 'edgecolor': '1', 
                       's': size, 'linewidth': 0.5},
        line_kws = {'color': 'red', 'linewidth': 1.5}
    )
    plt.title(label = f'{x}와(과) {y}의 관계')
    # plt.xlim(x_min * 0.9, x_max * 1.1);

def plot_bar_freq(
    data, 
    y, 
    color = None, 
    pal = None
):
    freq = data[y].value_counts().sort_index().reset_index()
    freq.columns = [y, 'freq']
    sns.barplot(
        data = freq, 
        x = y, 
        y = 'freq', 
        color = color, 
        palette = pal
    )
    for index, row in freq.iterrows():
        plt.text(
            x = index, 
            y = row['freq'] + 5, 
            s = row['freq'], 
            ha = 'center', 
            va = 'bottom', 
            c = 'black'
        )
    plt.title(label = '목표변수의 범주별 빈도수 비교')
    plt.ylim(0, freq['freq'].max() * 1.1);

def plot_bar_dodge_freq(
    data, 
    x, 
    y, 
    pal = None
):
    grp = data.groupby(by = [x, y]).count().iloc[:, 0]
    sns.countplot(
        data = data, 
        x = x, 
        hue = y, 
        order = grp.index.levels[0], 
        hue_order = grp.index.levels[1], 
        palette = pal
    )    
    for i, v in enumerate(grp):
        if i % 2 == 0:
            i = i/2 - 0.2
        else:
            i = (i-1)/2 + 0.2
        plt.text(
            x = i, 
            y = v, 
            s = v, 
            ha = 'center', 
            va = 'bottom'
        )
    plt.title(label = f'{x}의 범주별 {y}의 빈도수 비교')
    plt.legend(loc = 'best');

def plot_bar_stack_freq(
    data, 
    x, 
    y, 
    kind = 'bar', 
    pal = None
):
    p = data[y].unique().size
    pv = pd.pivot_table(
        data = data, 
        index = x, 
        columns = y, 
        aggfunc = 'count'
    )
    pv = pv.iloc[:, 0:p].sort_index()
    pv.columns = pv.columns.droplevel(level = 0)
    pv.columns.name = None
    pv = pv.reset_index()
    
    cols = pv.columns[1:]
    cumsum = pv[cols].cumsum(axis = 1)
    
    if type(pal) == list:
        pal = sns.set_palette(sns.color_palette(pal))
    
    pv.plot(
        x = x, 
        kind = kind, 
        stacked = True, 
        rot = 0, 
        title = f'{x}의 범주별 {y}의 빈도수 비교', 
        legend = 'reverse', 
        colormap = pal
    )
    
    plt.legend(loc = 'best')
    
    if kind == 'bar':
        for col in cols:
            for i, (v1, v2) in enumerate(zip(cumsum[col], pv[col])):
                plt.text(
                    x = i, 
                    y = v1 - v2/2, 
                    s = v2, 
                    ha = 'center', 
                    va = 'center', 
                    c = 'black'
                );
    elif kind == 'barh':
        for col in cols:
            for i, (v1, v2) in enumerate(zip(cumsum[col], pv[col])):
                plt.text(
                    x = v1 - v2/2, 
                    y = i, 
                    s = v2, 
                    ha = 'center', 
                    va = 'center', 
                    c = 'black'
                );

def plot_bar_stack_prop(
    data, 
    x, 
    y, 
    kind = 'bar', 
    pal = None
):
    p = data[y].unique().size
    pv = pd.pivot_table(
        data = data, 
        index = x, 
        columns = y, 
        aggfunc = 'count'
    )
    pv = pv.iloc[:, 0:p].sort_index()
    pv.columns = pv.columns.droplevel(level = 0)
    pv.columns.name = None
    pv = pv.reset_index()
    
    cols = pv.columns[1:]
    rowsum = pv[cols].apply(func = sum, axis = 1)
    pv[cols] = pv[cols].div(rowsum, 0) * 100
    cumsum = pv[cols].cumsum(axis = 1)
    
    if type(pal) == list:
        pal = sns.set_palette(sns.color_palette(pal))
        
    pv.plot(
        x = x, 
        kind = kind, 
        stacked = True, 
        rot = 0, 
        title = f'{x}의 범주별 {y}의 상대도수 비교', 
        legend = 'reverse', 
        colormap = pal, 
        mark_right = True
    )
    
    plt.legend(loc = 'best')
    
    if kind == 'bar':
        for col in cols:
            for i, (v1, v2) in enumerate(zip(cumsum[col], pv[col])):
                v3 = f'{np.round(v2, 1)}%'
                plt.text(
                    x = i, 
                    y = v1 - v2/2, 
                    s = v3, 
                    ha = 'center', 
                    va = 'center', 
                    c = 'black'
                );
    elif kind == 'barh':
        for col in cols:
            for i, (v1, v2) in enumerate(zip(cumsum[col], pv[col])):
                v3 = f'{np.round(v2, 1)}%'
                plt.text(
                    x = v1 - v2/2, 
                    y = i, 
                    s = v3, 
                    ha = 'center', 
                    va = 'center', 
                    c = 'black'
                );


## End of Document
