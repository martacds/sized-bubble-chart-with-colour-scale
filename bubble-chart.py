import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

#df = pd.read_excel("test-data.xlsx") # read an excel
df = pd.read_csv("repo/test-data.tsv", sep='\t', header=0) # read tsv with header

# Drop rows that have at least one missing element
df = df.dropna()

# convert column for X axis into numbers
df['X'] = df['X'].astype(float)

# colour palette (https://www.practicalpythonfordatascience.com/ap_seaborn_palette)
cmap = sns.color_palette("RdBu_r", as_cmap=True)

# variables for calculations
size_col = df["sizes"] # column with bubble sizes
sizeref=9 # increases the size of the bubbles visually

# create plot
fig, ax = plt.subplots()
scatter = ax.scatter(df['X'], df['Y'], c=df['colour scale'], s=df['sizes']*sizeref, cmap=cmap, edgecolors="black", linewidths=0.5)
plt.title("This is the title of the graph", fontsize=20)
plt.yticks(fontsize=15)

# graph lines
ax.spines[['right', 'top']].set_visible(False) # L-shaped axis
ax.axvline(0, linestyle="--", color="LightGrey") # vertical line at 0

# add lines from vertical 0 to each bubble
y_map = {cat: i for i, cat in enumerate(df['Y'])}
for _, row in df.iterrows():
    desc = row['Y']
    y_val = y_map[desc]
    if row['X'] == 0: # value is zero (draw no line)
        continue
    elif row['X'] > 0: # positive values
        xmin=0
        xmax=row['X']
    elif row['X'] < 0: # negative values
        xmin=row['X']
        xmax=0
    
    plt.plot([xmin,xmax], [y_val, y_val], color="Grey", linewidth=0.5) # create each line as a plot

# legend for heatmap
cax = ax.inset_axes([1.15, 0.35, 0.05, 0.6]) # location of colour bar within image container
clb = plt.colorbar(scatter, cax=cax) # create colour bar
clb.ax.set_title('Colour scale title', fontsize=10)

# legend for sizes (https://matplotlib.org/stable/gallery/lines_bars_and_markers/scatter_with_legend.html)
kw = dict(
    prop="sizes", # sizes / colours
    num=[int(size_col.min()),int(np.median(size_col)),int(size_col.max())], # shows three numbers in legend (minimum, median, maximum)
    func=lambda s: s/sizeref # sizes are adjusted by variable sizeref
)
legend = ax.legend(
    *scatter.legend_elements(**kw), # https://matplotlib.org/stable/api/collections_api.html#matplotlib.collections.PathCollection.legend_elements
    loc="center right", # location of legend
    title="Title for bubble size legend", 
    frameon=False, # frame around legend
    bbox_to_anchor=(1.3, 0.2), # places legend within image container
    labelspacing=3, # spacing between each line
    handletextpad=2 # distance between symbol and text
)

# figure sizing (https://stackoverflow.com/questions/44970010/axes-class-set-explicitly-size-width-height-of-axes-in-given-units)
width=6
height=7
l = ax.figure.subplotpars.left
r = ax.figure.subplotpars.right
t = ax.figure.subplotpars.top
b = ax.figure.subplotpars.bottom
figw = float(width)/(r-l)
figh = float(height)/(t-b)
ax.figure.set_size_inches(figw, figh) # numbers can be changed directly here

plt.savefig(  # saves figure in same folder as the code (https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.savefig.html)
    "plot.png", # name
    format="png", # e.g. 'png', 'pdf', 'svg', etc
    bbox_inches="tight", # sizing Sis tight to the plot
    dpi=100 # quality of the image (dots per inch)
) 